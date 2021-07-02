# aws
1.
```bash
git clone https://github.com/sally0427/fb.git -b linux_aws

pipenv shell 

pip install requirements.txt

# 下載google-chrome
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


python main.py
```
