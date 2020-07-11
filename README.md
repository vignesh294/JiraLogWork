Tool to quickly log work across multiple jira issues in one command.


Setup (Use Python 3.6+):

`pip install jira`

[others if needed]


`config.json` setup:

`set_verify` - Boolean - Required - Use SSL verification while connecting to the jira server (recommended to avoid Man-in-the-Middle attacks)

`cert_path` - String - Required if set_verify is true - Path of the ready to use certificate for SSL verification while connecting to the jira server

`server` - String - Required - jira server host

`username` - String - Required - Login username

`password` - String - Required - Login password [As of now this tool requires account password to be stored as a plain text in config.json, please modify the script to suit your security needs]

`default_work_start_time` - String - Required - Time of the day in HH:MM:SS format to use for the start time field of the worklog if not specified in a request


Running:

`python logwork.py A1,B1,C1,D1 A2,B2,C2,D2, A3,B3,C3,D3, ...`

Example: `python3 logwork.py JRA-1645,4h,Analysis,2020-07-07T14:00:00 jra-6969,7h,,2020-07-07 jra-9696,6h,,`


`A`s - Required - Issue Id to log work for - Example: `JIR-6996`

`B`s - Required - Amount of work to log - Example: `6h`

`C`s - Optional - Description of the worklog. Description can only be SINGLE WORD to avoid complexities with having to deal with taking input from command line. Leave it blank to not have any description on the worklog - Example: `Testing`

`D`s - Optional - Date & time to use for the `started` field of the worklog in YYYY-MM-DDTHH:MM:SS format. Leave the field blank to use the server's current date & time to be used for the field. Supply only the date in the format YYYY-MM-DD to log the work with the time mentioned configured as `default_work_start_time` - Example: `2020-07-07T14:00:00`
