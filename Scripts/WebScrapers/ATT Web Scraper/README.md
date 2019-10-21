## Overview

This script will log into the AT&T website and scrape three metrics:  

- Amount Due  
- Date Due  
- Data Usage 

And then deposit these metrics into InfluxDB via the InfluxDB API.

This script applies to AT&T home internet users. It may work under business AT&T accounts but I haven't tested it.

## Open config.ini to edit configuration:

AT&T Username = USERNAME  
AT&T Password = PASSWORD  
AT&T Account Number = ATTACCTNUMBER  
InfluxDB Host IP Address: INFLUXDBHOSTIP  
InfluxDB Host Port: 8086  
Database Name: telegraf  
Authenticate With Influx?: true  
InfluxDB Username: USERNAME  
InfluxDB Password: PASSWORD  
Chromedriver location: C:\chromedriver.exe  
Run Chromedriver is headless mode?: true  

NOTE: Leave spaces and line breaks formatted EXACTLY how you see them in config.ini. If these elements are changed this script will not parse the configuration file correctly.  

## Python library installation

You can use the requirements.txt to import the necessary Python libraries, or you can use Pip to install the libraries manually:  

pip install selenium  
pip install bs4  
pip install html5lib  
pip install time  
pip install requests  
pip install influxdb  

## Chromedriver is required for this script to run correctly

You will need to download Chromedrive and copy it to the root of your C:\ drive. You can change the location of Chromedriver within the config file under the option "Chromedriver location".

[Download Chromedriver from the Chromium Project](https://chromedriver.chromium.org/downloads)

## Enable output of InfluxDB import files

Uncomment lines 132 through 146 to enable this script to output InfluxDB import files. When the script fires it will now write three files to the directory from which the script was run:

att_amount_due.txt  
att_data_used.txt  
att_due_date.txt  
  
These import files can be used to deposit metrics into InfluxDB via command line.

## Logging  

Current log output to scraper.log is at level "INFO". To change this setting, go into the script and on lines 18 and 19 adjust the following (Depending on what logging level you need):  

Line 18: `level=logging.INFO`  
To:  
Line 18: `level=logging.DEBUG`, or `level=logging.WARNING`, or `level=logging.ERROR`, or `level=logging.FATAL`  

And change:  

Line 19: `LOGGER.setLevel(logging.WARNING)`  
To:  
`LOGGER.setLevel(logging.DEBUG)` or, `LOGGER.setLevel(logging.INFO)` or, `LOGGER.setLevel(logging.ERROR)`, or `LOGGER.setLevel(logging.FATAL)`  

## Planned features

- Add option in Config.ini to change debug logging level to Debug, Info, Warn, Error or Fatal
- Add option to turn on/off e-mail metrics to e-mail address
- Add option to turn on/off send metrics to InfluxDB API
- Add option to turn on/off output metrics to InfluxDB text import files


