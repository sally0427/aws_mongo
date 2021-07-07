# aws
1.
```bash
git clone https://github.com/sally0427/fb.git -b linux_aws

pipenv shell 

pip install -r requirements.txt

# 下載google-chrome(github已經有安裝檔，若git clone下來的，可直接跳下一步)
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# 安裝google-chrome
sudo dpkg -i google-chrome-stable_current_amd64.deb

# 如果報錯
sudo apt-get install -f

# 確認google-chrome版本
# 各版本對應地址： https://blog.csdn.net/suancai1993/article/details/79742852
google-chrome --version

# 確認chromedriver版本(資料夾內附 91.0.4472.101 版)
chromeDriver

#若版本不合去下載合適版本

#若chromedriver not found，給權限
chmod +x chromedriver

# 安裝aws CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# 設定aws(輸入 Access KeyID, Secret access key, region name: ap-southeast-1)
aws configure


# 執行程式
python main.py

```
