# 安装类库
本机使用python版本：
```
Python 3.10.4
```
## 安装Django 4.2.3
确保您已经安装了Python 3.8或更高版本（Django 4.x系列要求Python 3.8+）。如果您不确定当前的Python版本，可以通过以下命令检查：
```
python --version
```
确认Python版本符合要求后，使用pip（Python的包管理器）来安装Django 4.2.3：
```
pip install Django==4.2.3
```
这条命令会从Python官方包索引（PyPI）下载并安装指定版本的Django。如果过程中出现任何权限问题，您可能需要使用pip install --user（针对用户级安装）或以管理员身份运行命令（如在Windows上使用cmd时以管理员身份打开命令提示符，或在Unix-like系统中使用sudo前缀）。

## 安装TensorFlow CPU版本 2.16.1
确保您已经安装了兼容的Python版本和必要的系统依赖。对于TensorFlow CPU版本，主要需要确保已安装NumPy等依赖库。接下来，使用pip安装TensorFlow 2.16.1的CPU版本：
```
pip install tensorflow-cpu==2.16.1
```
这条命令将下载并安装TensorFlow 2.16.1的CPU优化版本，适用于没有GPU的系统或不需要GPU加速的情况。如果您的环境中已经安装了其他版本的TensorFlow，这条命令会将其替换为指定版本。

# 运行指令
```
py manage.py runserver [需要自行指定端口号]
```