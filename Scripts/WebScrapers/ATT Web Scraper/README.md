## Overview

This script will log into the AT&T website and scrape three metrics:  

Amount Due  
Date Due  
Data Usage 

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

In cases where InfluxDB does not require authentication, mark `Authenticate with influx?` as `false` leave `InfluxDB Username` and `InfluxDB Password` alone.

NOTE: Leave spaces and line breaks formatted EXACTLY how you see them in config.ini. If these elements are changed this script will not parse the configuration file correctly.

## The Chromdriver is required for this script to run correctly

You will need to download the Chromedrive and copy it to the root of your C:\ drive. You can change the location of the Chromedriver within the script at line 13.

[Download the Chromedriver](https://chromedriver.chromium.org/downloads)

## Disable Chromedriver

By default this script runs the Chromedriver in headless mode, meaning you will NOT see Chrome pop up when the script is run. If you want to see the Chromedriver visually run on your screen while it's pulling metrics, comment out line 12 of the script by putting a hashtag and a space before the line:

From this:  
`options.add_argument('--headless')`  
To this:  
`# options.add_argument('--headless')`  


## Enable output of InfluxDB import files

Uncomment lines 132 through 146 to enable this script to output InfluxDB import files. Once this is done, when the script fires it will write three files to the directory from which the script was run:

att_amount_due.txt  
att_data_used.txt
att_due_date.txt


