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
import time

solver = TwoCaptcha('58479623af5f28791750cc47c264bc01')  # 自分のAPIキーを設定してください
url = 'http://nw-restriction.nttdocomo.co.jp/top.php'
CHROMEDRIVER = '/usr/local/bin/chromedriver'

# Create your views here.
def camera_view(request):
    return render(request, 'sampleapp/camera.html')

def network_limit_check_view(request):
    imei = None
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
            link.click

            time.sleep(5)

            # img_srcの取得
            # a = driver.find_element(By.XPATH, '/html/body/div/form/div/div[2]/dl[2]/dt')
            # print(a)
            img = driver.find_element(By.XPATH, '/html/body/div/form/div/div[2]/dl[2]/dd/div/img')
            print(img)
            img_src = img.get_attribute('src')
            print(img_src)

        except BaseException:
            print(traceback.format_exc())
        driver.quit()
    else:
        form = ImeiForm()

    return render(request, 'sampleapp/network_limit.html', {'form': form, 'imei': imei})