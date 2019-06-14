# RamanSpectrometer-Flasky

RamanSpectrometer-Flasky是拉曼光谱组分识别软件的一部分，提供拉曼光谱识别的服务接口。

## 安装与运行
有两种方式：直接安装和采用docker安装。前者对系统的入侵性大，但比较省时；后者依赖docker，对系统做了隔离，因此不具有入侵性，但相对耗时。

### 直接安装
1. 首先需安装Python 3.7.3，并将Python命令加到环境变量中；
2. 双击`boot.bat`，它将自动配置软件运行环境；
3. 双击`run.bat`，运行软件。

如果运行成功，即可在`run.bat`的控制台中看到程序运行log，此时可尝试在浏览器上访问[光谱请求接口](http://localhost:5000/api/v1/spectra)，确认是否有以下内容返回：
```json
{"spectra": []}
```
有则说明程序正常运行。

### 借助docker安装
需要两个工具：
 - docker
 - docker-compose

关于该工具的安装方法请查阅[官方文档](https://docs.docker.com/install/linux/docker-ce/ubuntu/)。

安装完以上工具后，在命令行中输入：
```bash
docker-compose up
```
即可实现安装和运行软件。注意，该过程需要一段时间。

如果运行成功，将在控制台看到“[2019-06-14 13:56:48 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000”记录。此时可访问`http://<host ip>/api/v1/spectra`验证程序是否正确返回以下内容：
```json
{"spectra": []}
```
