# RamanSpectrometer-Flasky

RamanSpectrometer-Flasky是拉曼光谱组分识别软件的一部分，提供拉曼光谱识别的服务接口。

## 安装
>本软件运行需要`Python3.7.3`支持，请确保在运行本程序前已安装`Python3.7.3`。

安装比较简单，直接双击`boot.bat`，它将自动配置环境。

## 运行
在命令行中输入：
```bash
flask run
```
即可看到程序运行log，此时可尝试在浏览器上访问[光谱请求接口](http://localhost:5000/api/v1/spectra)，确认是否有以下内容返回：
```json
{"spectra": []}
```
有则说明程序正常运行。
