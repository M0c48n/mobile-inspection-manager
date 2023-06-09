from django.shortcuts import render
from sampleapp.forms import ImeiForm
import traceback

# import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from twocaptcha import TwoCaptcha
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
import requests
import base64
import time

solver = TwoCaptcha('58479623af5f28791750cc47c264bc01')  # 自分のAPIキーを設定してください
url = 'http://nw-restriction.nttdocomo.co.jp/top.php'
CHROMEDRIVER = '/usr/local/bin/chromedriver'

# Create your views here.
def camera_view(request):
    return render(request, 'sampleapp/camera.html')

def network_limit_check_view(request):
    docomo_result = None
    form = None
    if request.method == 'POST':
        form = ImeiForm(request.POST)
        if form.is_valid():
            imei = form.cleaned_data['imei']
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')


        chrome_service = fs.Service(executable_path=CHROMEDRIVER) 
        driver = webdriver.Chrome(service=chrome_service, options=options)

        try:
            # ページアクセス
            driver.get(url)
            link = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div[3]/a')
            print(f'link:{link}')
            link.click()

            time.sleep(3)

            # img_srcの取得
            img = driver.find_element(By.XPATH, '/html/body/div/form/div/div[2]/dl[2]/dd/div/img')
            print(img)
            img_src = img.get_attribute('src')
            print(img_src)
            # スクリーンショットをPNG形式のバイナリデータとして取得
            png = img.screenshot_as_png

            # バイナリデータをBASE64エンコード
            base64_img = base64.b64encode(png).decode('utf-8')

            # 2Captchaに送信
            result = solver.normal(file=base64_img)
            print(f'result:{result}')

            # 2Captchaから取得した値を入力フィールドに設定
            input_field = driver.find_element(By.XPATH, '/html/body/div/form/div/div[2]/dl[2]/dd/p/input')
            input_field.send_keys(result['code'])

            # imeiを入力
            imei_input_field = driver.find_element(By.XPATH, '/html/body/div/form/div/div[2]/dl[1]/dd/input')
            imei_input_field.send_keys(imei)

            # 確定ボタンを押下
            confirm_button = driver.find_element(By.XPATH, '/html/body/div/form/div/div[2]/input')
            confirm_button.click()

            # テキスト取得
            text_element = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/span[2]')
            print(f'最終結果！:{text_element.text}')
            docomo_result = text_element.text

        except BaseException:
            print(traceback.format_exc())
        driver.quit()
    else:
        form = ImeiForm()

    return render(request, 'sampleapp/network_limit.html', {'form': form, 'result': docomo_result})