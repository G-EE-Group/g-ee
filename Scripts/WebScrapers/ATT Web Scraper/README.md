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

In cases where InfluxDB does not require authentication, mark "Authenticate with infulx?" as <false> leave "InfluxDB Username" and "InfluxDB Password" alone.

NOTE: Please leave spaces and line breaks formatted EXACTLY how you see them in config.ini. If these elements are not exactly how you received them when they were downloaded, this script will not parse the configuration correctly.

I think you should use an
`<addr>` element here instead


