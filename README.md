# selenium-autobrowse

# behaviour
The script will read the configuration file.
With the list of URLs

* Load the URL web page
    
* Click on the Didomi Consent (if found)
    
* Scroll down the page until the end is reached
    
* Find the first Article in the page and get the article url
    
* Load the article web page

* Scroll down the article until the end is reached

# use

USE: <i>python chrome-loop.py config-file.json</i>

Note for linux: install chromedriver with "sudo apt install chromium-chromedriver"

Note for windows: installl chromedriver following https://www.youtube.com/watch?v=dz59GsdvUF8

chromedriver command must be included in the path

# Configuration File

<b>Example of json file</b>

<code>{
    "proxy": "",           <-- IP:PORT, or leave proxy empty for no proxy 
    "loops": 99,           <-- Number of loops the navigation will be performed
    "user-agent": "xxxx"   <-- User agent for the HTTP request header
    "urls": [              <-- List of URLs to navigate
        "https://www.hola.com/",
        "https://www.hola.com/actualidad/",
        "https://www.hola.com/moda/",
        "https://www.hola.com/fashion/",
        "https://www.hola.com/decoracion/"
    ]
}</code>

