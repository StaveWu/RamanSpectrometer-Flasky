# RamanSpectrometer-Flasky

RamanSpectrometer-Flasky是拉曼光谱组分识别软件的一部分，提供拉曼光谱识别的服务接口。

## 安装与运行
根据需求可安装在本地或服务器上。

### 本地安装（仅针对Windows）
1. 在migrations文件夹中创建versions文件夹；
2. 安装Python 3.7.3，并将Python命令加到环境变量中；
3. 双击`boot.bat`，它将自动配置软件运行环境；
4. 双击`run.bat`，运行软件。

如果运行成功，即可在`run.bat`的控制台中看到程序运行log，此时可尝试在浏览器上访问[本地光谱请求接口](http://localhost:5000/api/v1/spectra)，确认是否有以下内容返回：
```json
{"spectra": []}
```
有则说明程序正常运行。

### 服务器安装
1. 在migrations文件夹中创建versions文件夹。

2. 在根目录下创建.env文件，输入以下字段并保存：
```
FLASK_APP=flasky
FLASK_ENV=production
FLASK_CONFIG=production
DATABASE_URL=mysql+pymysql://flasky:<database-password>@dbserver/flasky
```

3. 在根目录下创建.env-mysql文件，输入以下字段并保存：
```
MYSQL_RANDOM_ROOT_PASSWORD=yes
MYSQL_DATABASE=flasky
MYSQL_USER=flasky
MYSQL_PASSWORD=<database-password>
```

4. 安装两个工具：
     - docker
     - docker-compose

> 关于该工具的安装方法请查阅[官方文档](https://docs.docker.com/install/)。

5. 在命令行中输入以下命令来安装和运行软件，注意该过程需要一段时间：
```bash
docker-compose up
```

如果运行成功，将在控制台看到log`[2019-06-14 13:56:48 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000`。此时可通过浏览器访问服务器光谱请求接口`http://<host ip>/api/v1/spectra`验证程序是否正确返回以下内容：
```json
{"spectra": []}
```
有则说明程序正常运行。
