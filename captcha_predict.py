#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

try:
    import tensorflow as tf
    from PIL import Image
    import pathlib
except ImportError:
    import subprocess
    pip_args = ['python', '-m', 'pip', 'install', '-r', 'requirements.txt']
    print('install python dependencies .....')
    subprocess.check_call(pip_args)
    print('python dependencies installed ....')
    import tensorflow as tf
    from PIL import Image
    import pathlib

import random
import numpy as np

class CaptchaPredictor(object):
    def __init__(self, model_path='faded_captcha_correct.h5', predict_data_dir='captcha_test_data'):
        self._model_path = model_path
        self._predict_data_dir = pathlib.Path(predict_data_dir)
        self._img_height = 100
        self._img_width = 120
                
    @property
    def model(self):
        return tf.keras.models.load_model(self._model_path)
    
    def parse_filepath(self, captcha_path):
        try:
            filename =  captcha_path.name
            label, _ = filename.split("_")
            return label
        except Exception as e:
            raise Exception('error to parse %s. %s' % (captcha_path, e))

    @property 
    def all_captcha_paths(self):
        all_captcha_paths = self._predict_data_dir.glob('*.png')
        return all_captcha_paths
    
    def batch_captcha_paths(self, batch_size):
        all_captcha_paths = self.all_captcha_paths
        batch_captcha_paths = random.sample(list(all_captcha_paths), batch_size)
        return batch_captcha_paths

    def predict_on_batch_size(self, batch_size):
        batch_captcha_paths = self.batch_captcha_paths(batch_size)
        self.predict_on_batch(batch_captcha_paths)

    def predict_on_batch(self, batch_captcha_paths):
        imgs = map(Image.open, batch_captcha_paths)
        imgs = map(lambda img: img.resize((self._img_width, self._img_height)), imgs)
        imgs = map(lambda img: np.array(img)/255.0, imgs)
        imgs = np.array(list(imgs))
        model = self.model
        predictions = model.predict_on_batch(imgs)
        self.show_result(batch_captcha_paths, predictions)
  
    def predict_one(self, captcha_path):
        self.predict_on_batch([captcha_path])     
        
    def show_result(self, batch_captcha_paths, predictions):
        labels = map(self.parse_filepath, batch_captcha_paths)
        labels = list(labels)
        print()
        print('results:\n')
        for index, prediction in enumerate(predictions):
            prediction = ''.join(map(str, tf.argmax(prediction, axis=-1).numpy()))
            print('\tlabel is {}, prediction is {}. captcha file path is {}'.format(labels[index], prediction, batch_captcha_paths[index]))


if __name__ == '__main__':
    import argparse
    import json
    with open('captcha_settings.json') as f:
        settings = json.load(f)
    predict_by_paths= settings['predict_by_paths']
    model_path = settings['model_path']
    predict_data_dir = settings['predict_data_dir']
    captcha_predictor = CaptchaPredictor(model_path, predict_data_dir)
    if predict_by_paths:
        captcha_paths = settings['captcha_paths']
        captcha_paths = list(map(pathlib.Path, captcha_paths))
        captcha_predictor.predict_on_batch(captcha_paths)
    else:
        batch_size = settings['batch_size']
        captcha_predictor.predict_on_batch_size(batch_size)