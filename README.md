# IOT Project: 智慧遠端開關機電腦手臂

智慧遠端開關機電腦手臂為將樹梅派連上馬達，控制馬達轉動，馬達再和機械手臂接上，接著控制馬達能夠轉動大概 90 到 120 度左右，且固定架設在電腦主機上並連上電源及網路線，尖頭則以軟式尖頭，避免刮傷電腦，為了要準確判斷並且通知使用者，利用攝像頭及影像辨識電腦電源是否開關機，最後以 LineBot 進行控制。

## 作品影片
[![Youtube影片連結](https://github.com/thomashuang2017/NCU_IOT_project/blob/master/image/front.PNG)](https://www.youtube.com/watch?v=wZTWNNkhrE8&t=2s)

## Necessary
1. Raspberry pi
2. 鏡頭
3. 伺服馬達 MG996R
4. 機械手臂
5. Intel Neural Compute stick 2

## Step1: 安裝 flask 及 ngrok
flask 為很好用的 python 輕量化框架，它可以做為你溝通 LineBot 及控制所有邏輯的 server，可以先安裝此套件:
```shell
pip install flask
```
*建議你可以先參考此[範例](https://projects.raspberrypi.org/en/projects/python-web-server-with-flask)先架設在你的 localhost*

因為 LineBot 需要用加密的 https 網址，而此 project 的範例是在本機端架設 server，因此我們會用 ngrok 來為網址加密 :
```shell
Dowload ngrok: https://ngrok.com/
```
設置 ngrok port 和你的 flask port 一樣，預設為 5000:
```shell
./ngrok http 5000
```
**建議你可以先示範先執行 ngrok 再執行 flask 後，看網址是否有變 https**

## Step2: 串接 LineBot
1. 先上官方網站 [Message API](https://developers.line.biz/zh-hant/services/messaging-api/) 創立帳號
2. Create channel and Message API
3. 參考此[LineBot 官方範例 github](https://github.com/line/line-bot-sdk-python)
4. 更改Channel secret 及 Channel access token
5. 更改 Webhook URL 欄位，改成剛剛 ngrok 給的 https 網址，並在後面加上 /callback(ex: https://xxxxxxxx.ngrok.io/callback)

**建議你可以先執行 LineBot 官方範例並且能跟你的 Line 回應溝通**

## Step3: 影像辨識模型
我們需要用到影像辨識來判斷電腦有無開關機，此 project 拍攝了各5張不同角度開機及關機照片當成訓練集，並且用簡單的 CNN + pooling 模型訓練，除了不同角度外也可以用Data augmentation 旋轉平移照片增加模型準確度，我們用 keras 訓練模型後轉成 opencv 可以用的格式，準確度在驗證上的分數高達99.99%，以下為模型資訊，你可以先看此 project 範例照片及訓練過程，然後使用你自己拍的照片去訓練你自己的模型:
```shell
# 模型
model/boost_cls_model.pb

# 訓練資料 
training_data/Boost/
training_data/Not_Boost/

# 訓練程式
training_model.ipynb

# 模型串接flask
Image_boot_cls.py
```


## Step4: 機械手臂製作
此 project 用 [meARM](https://m.ruten.com.tw/goods/show.php?g=21928057912376&fbclid=IwAR2dA_oOykf56BuWX7ER6rZLLNIGhjvFxnxaJcyj9RfDjTxjq0tZaL-17es)中的機械手臂當作材料，
因為原本 meARM 附上的 sg90 馬達扭力不夠，因此改用一顆MG996R的馬達控制手臂，
在此附上meARM[教學影片](http://www.youtube.com/watch?v=xlwTzrsWs48)及[組裝圖教學](https://active.clewm.net/Dsz5aQ?qururl)，控制角度程式為
```shell
Servo.py
```

## Step5: 確認網路
你可以將:
```shell
ping.py
```
這支程式的 hostname 改成你要遠端的ip，這樣才能確認網路狀態是否可以遠端
**如果你要遠端的電腦是windows，請先把防火牆中的ICMP打開，才能ping的到，[參考資料](https://benson82208.pixnet.net/blog/post/43829710-%E8%A7%A3%E6%B1%BAping%E4%B8%8D%E5%88%B0windows-10-%E6%96%B9%E6%B3%95)**

## Step6: 手臂動起來 !!
完成了上述5步驟後，開始讓手臂動起來吧!! 
伺服馬達的棕、紅、橘分別接在GPIO Board上的 9,4,12號，手臂會從垂直0度順時針旋轉100度，
接著執行以下程式:
```shell
python main.py
```
如果失敗了，有幾點是可能需要debug的點:
1. main.py 的 flask port 及 ngrok port 是否一致 
2. Channel secret, Channel access token 及 Webhook URL 是否輸入正確
3. 機械手臂如果不動，有可能是電壓不夠，可以用麵包板再接額外電池連接

























