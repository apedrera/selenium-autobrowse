from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import sys
import json

# USE: python chrome-loop.py config-file.json

# Read config file (filename=fist argument)
try:
    config_file_name = sys.argv[1]
except:
    print ("ERROR. Expected config file as first argument")
    print ("Example: python %s config-file.json" % sys.argv[0])
    quit()

# Read json configuration file
with open(config_file_name) as config_file:
  config_raw = config_file.read()
config = json.loads(config_raw)

pages_to_browse = config["urls"]
PROXY = config["proxy"]
nloops = config["loops"]
userAgent = config["user-agent"]

driver_path = "chromedriver"            # chromedriver must be in the path of the OS env variables
delay = 0.01                            # delay between scroll downs. Default: 0.1
brow_increase = 2                       # rows every scroll down. Default: 10
seconds_after_section = 1               # delay after section page (in seconds). Default: 5
zoom = 1.5                              # browser zoom. Default: 1.5
window_width = int(360*zoom)            # window width. Default: 360
window_height = int(800*zoom)           # window heigth. Default: 800

# --------------------------------------------------------------------------
# -------------------- end configuration -----------------------------------
# --------------------------------------------------------------------------

service = Service(executable_path=driver_path)      
mobile_emulation = {
   "deviceMetrics": { "width": window_width, "height": window_height, "pixelRatio": 3.0 },
   "userAgent": userAgent }

chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--proxy-server=%s' % PROXY)

browser = webdriver.Chrome(service=service, options = chrome_options)
browser.set_window_size(window_width,window_height)

# FUNC browse_func ----------------------------------------------------------------
def browse_func(page):
    try:
        browser.get(page)
    except:
        print ("ERROR:", page, " (unable to retrieve page)")
        time.sleep(10)  # Waiting 10 seconds after retrieving error.
        exit
    
    browser.execute_script("document.body.style.zoom = '"+ str(zoom) +"'")

    # Click on cookies consent
    try:
        browser.execute_script("document.getElementById('didomi-notice-agree-button').click();")
    except:
        print ("Warning:", page, " (unable to click didomi agree button, or button not present)")
            
    time.sleep(seconds_after_section)

    brow = 0
    totalHeight = browser.execute_script("return document.body.scrollHeight")
    while (brow < totalHeight):
        browser.execute_script("window.scrollTo(0,"+str(brow)+")")
        time.sleep(delay)
        brow+=brow_increase

    try:
        link2 = browser.execute_script("return document.getElementsByTagName('article')[0].getElementsByTagName('a').item(0).href")
        print ("Page:", link2)
        browser.get(link2)
    except:
        print ("Page:", page, " (article not found)")
        exit

    browser.execute_script("document.body.style.zoom = '"+str(zoom)+"'")

    brow = 0
    totalHeight = browser.execute_script("return document.body.scrollHeight")
    while (brow < totalHeight):
        browser.execute_script("window.scrollTo(0,"+str(brow)+")")
        time.sleep(delay)
        brow+=brow_increase
    
# END FUNC browse_func ----------------------------------------------------------------

l = 1
print("Stating Automatic Browsing. Proxy: (%s)" % PROXY)
while (l <= nloops):
    print("Loop: ",l," of ",nloops)
    for page in pages_to_browse:
        print("Page:", page)
        browse_func(page)
    l+=1

browser.close()
