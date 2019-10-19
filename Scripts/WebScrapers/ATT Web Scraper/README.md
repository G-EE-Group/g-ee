BEFORE RUNNING THIS PYTHON SCRIPT

- Replace fields config.ini: USERNAME, PASSWORD and ACCOUNTNUMBER with the relevant information.
- You will have to download and specify your Chromedriver physical location on disk (line 14)
- You will have to install several Python frameworks via PIP (All declared at the top of the file)

Assuming everything is configured properly, when this scripts completes it will create three files within the directory that the script was run from:

- att_amount_due.txt
- att_data_used.txt
- att_due_date.txt

Once these files are written to disk, you can use InfluxDB's Import function to put them in the database:

influx -import -path=att_amount_due.txt
influx -import -path=att_data_used.txt
influx -import -path=att_due_date.txt

On Windows systems you will have to convert the file from Windows format to UNIX format using Powershell before importing into InfluxDB:

$original_file ='C:\Users\Cameron\Documents\influxdb-1.7.3-1\att_amount_due.txt
$text = [IO.File]::ReadAllText($original_file) -replace "`r`n", "`n"
[IO.File]::WriteAllText($original_file, $text)

$original_file ='C:\Users\Cameron\Documents\influxdb-1.7.3-1\att_data_used.txt
$text = [IO.File]::ReadAllText($original_file) -replace "`r`n", "`n"
[IO.File]::WriteAllText($original_file, $text)

$original_file ='C:\Users\Cameron\Documents\influxdb-1.7.3-1\att_due_date.txt
$text = [IO.File]::ReadAllText($original_file) -replace "`r`n", "`n"
[IO.File]::WriteAllText($original_file, $text)
