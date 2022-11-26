from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import numpy as np
from datetime import datetime
import logging as Logger
import socket
import re

# Browser Environment Configurations...
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(options=options)

# Logger Configurations...
Logger.basicConfig(filename="./logs/operations.log", filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',level=Logger.INFO)

# Regular Expression for URL Verification...
httpsUrlRegex = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
httpUrlRegex = "^http?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"

# Load URLs as array from .txt file...
urlList = np.genfromtxt("urls.txt",dtype='str')

def screenshotPage(urls):
    for url in urls:
        try:
            # Returns Resolved IP Address from Host Names...
            urlIP = socket.gethostbyname(url)

            # Formatting URL as http://{url}
            if(re.match(httpUrlRegex,url) == None and len(url)>0):
                url = "http://"+url

            # Formatting URL as https://{url}
            elif(re.match(httpsUrlRegex,url) == None and len(url)>0):
                url = "https://"+url

            # Page Screenshot Operation...
            if(len(urlIP)>0 and len(url)>0):
                driver.get(url)
                driver.set_page_load_timeout(10) # Session Timeout in Seconds...
                driver.set_window_size(1920,1080) # Window Resolution Configuration...
                driver.get_screenshot_as_file("./screenshots/"+driver.title[0:6]+"-"+datetime.now().strftime("%d%m%yT%H%M%S")+".png")
                Logger.info("URL: %s [ACTION SUCCESSFUL]",url)

        # Exception Handling for Unresolved/Invalid URLs...
        except socket.gaierror as error:
            Logger.error("URL: %s [ERROR]::: %s",url,error)
            pass

        # Exception Handling for Session Timeout...
        except TimeoutException:
            Logger.error("URL: %s [TIMEOUT]",url)
            pass

screenshotPage(urlList)
driver.close()