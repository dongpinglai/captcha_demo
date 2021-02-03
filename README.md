### Captcha Demo

---

#### 项目说明

---

基于python3的验证码识别demo



####文件结构

---

- captcha_predict.py

  > demo入口文件

- captcha_settings.json

  > 配置文件
  >
  > 字段说明：
  >
  > | 字段             | 类型   | 是否必传 | 默认值 |    备注  |
  > | ---------------- | ------ | -------- | ---- | ---- |
  > | predict_by_paths | bool   | 是   | false | 预测模式。true为指定路径预测，false为随机批量预测 |
  > | captcha_paths    | list   | 否   | [] | 指定要预测的验证码图片路径。当predict_by_paths为true时生效。 |
  > | batch_size       | int    | 否   | 32 | 随机批量预测的大小。当predict_by_paths为false时生效。 |
  > | model_path       | string | 是   | faded_captcha_correct.h5 | TensorFlow 模型的路径 |
  > | predict_data_dir | string | 是 | captcha_test_data | 默认的测试图片目录。 |
  > |                  |        |          |      |      |

- requirements.txt

  > python依赖

- faded_captcha_correct.h5

  > tensorflow模型文件

- captcha_test_data

  > 测试数据（验证码图片）

#### 项目运行

---

```shell
python captcha_predict.py
```



