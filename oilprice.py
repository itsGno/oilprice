from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

while True:
    if time.strftime("%H",time.localtime()) == '13':
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        # opt = webdriver.ChromeOptions("D:\Downloads\chromedriver.exe")
        # opt = webdriver.Chrome(ChromeDriverManager().install())
        # opt.('headless') #hidden mode of chrome driver

        # driver = webdriver.Chrome(options=opt) #create driver

        url = 'http://www.pttor.com/oilprice-capital.aspx'

        driver.get(url) #open web
        time.sleep(3) #waiting 3 seconds

        page_html = driver.page_source
        driver.close()
        data = soup(page_html,'html.parser') #scan data
        table = data.findAll('table',{'id':'tbData'})
        table = table[0].findAll('tbody')
        rows = table[0].findAll('tr')
        todayprice = rows[0].findAll('td')
        #print(todayprice)

        oiltitle = ['วันที่',
                    'Diesel Premium',
                    'Diesel',
                    'DieselB10',
                    'DieselB20',
                    'Benzene',
                    'Gasohol95',
                    'Gasohol91',
                    'GasoholE20',
                    'GasoholE85',
                    'NGV']
        oilprice = []


        for ol in todayprice:
            oilprice.append(ol.text)


        result = {}

        for t,o in zip(oiltitle,oilprice):
            result[t] = o

        print(result)

        from songline import Sendline

        token = 'yGl16EdhlgZflBpsZbtPTcn3En9uk33ZeRNvotlChWi'

        messenger = Sendline(token)
        count = 1 
        for res,value in result.items():
            if count == 1:
                messenger.sendtext('ราคาน้ำมัน '+res +value)
                count+=1
            else:
                messenger.sendtext('ราคา '+res+' วันนี้: ' + value+ ' บาท')
        response = messenger.sticker(12,1)
        print(response)
        time.sleep(4000)

