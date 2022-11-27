from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import numpy as np
from datetime import datetime
import logging as Logger
import socket
import re
import urllib.parse

# Browser Environment Configurations...
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(options=options)

# Logger Configurations...
Logger.basicConfig(filename="./logs/operations.log", filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',level=Logger.INFO)

# Log Formatter...
def Log(url,urlLen,message,error):
    if(error != None):
        Logger.info("URL: %s [%s]::: %s",url,message,error)
        return
    
    if(re.match("http://",url[0:7:1]) and urlLen<len(url)):
        Logger.info("URL: %s [%s]",url[7:(7+urlLen):1],message)
        return

    if(urlLen<len(url)):
        Logger.info("URL: %s [%s]",url[8:(8+urlLen):1],message)
    else:
        Logger.info("URL: %s [%s]",url[0:(8+urlLen):1],message)
    return

# Regular Expression for URL Verification...
UrlRegex = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"

# Load URLs as array from .txt file...
urlList = np.genfromtxt("./urls.txt",dtype='str')
print(urlList)

def screenshotPage(urls):
    for url in urls:
        try:
            urlLength = len(url)

            # Formatting URL as https://{url}
            if(re.match(UrlRegex,url) == None and urlLength>0):
                url = "https://"+url
                
                # Removing "https://" (if URL is already in http format in .txt file)...
                if(re.search("http://",url) != None):
                    url = url[8:len(url):1]
                
                # Verifying URL as: https://{url} or https://{url}...
                if(re.match(UrlRegex,url) == None):
                    raise ValueError
                
            # Retrieve hostname from URL...
            parsed_url = urllib.parse.urlparse(url)
            hostname = parsed_url.netloc

            # Returns Resolved IP Address from Host Names...
            urlIP = socket.gethostbyname(hostname)

            # Page Screenshot Operation...
            if(len(urlIP)>0 and urlLength>0):
                driver.set_page_load_timeout(10) # Session Timeout in Seconds...
                driver.get(url)
                driver.set_window_size(1920,1080) # Window Resolution Configuration...
                driver.get_screenshot_as_file("./screenshots/"+driver.title[0:6]+"-"+datetime.now().strftime("%d%m%YT%H%M%S")+".png")
                Log(url,urlLength,'ACTION SUCCESSFUL',None)

        # Exception Handling for Unresolved URLs...
        except socket.gaierror as error:
            Log(url,urlLength,'ERROR',error)
            pass

        # Exception Handling for Invalid Format URLs...
        except ValueError:
            Log(url,urlLength,'INVALID URL',None)
            pass

        # Exception Handling for Session Timeout...
        except TimeoutException:
            # isrunning = 0
            Log(url,urlLength,'SESSION TIMEOUT',None)
            pass

screenshotPage(urlList)
driver.close()