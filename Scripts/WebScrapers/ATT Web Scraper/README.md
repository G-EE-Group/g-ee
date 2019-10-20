## Overview

This script will log into the AT&T website and scrape three metrics:  

Amount Due  
Date Due  
Data Usage 

And them deposit these metrics into InfluxDB via the InfluxDB API.

This script applies to AT&T home internet users only.

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

In cases where InfluxDB does not require authentication, mark `Authenticate with infulx?` as `false` leave `InfluxDB Username` and `InfluxDB Password` alone.

NOTE: Leave spaces and line breaks formatted EXACTLY how you see them in config.ini. If these elements are changed this script will not parse the configuration file correctly.

## The Chromdriver is required for this script to runn corrently

[Chromedriver](https://chromedriver.chromium.org/downloads)

## Enable output of InfluxDB import files

Uncomment lines 132 through 146 to enable this script to output InfluxDB import files. Once this is done, when the script fires it will write three files to the directory from which the script was run:

att_amount_due.txt  
att_data_used.txt
att_due_date.txt


