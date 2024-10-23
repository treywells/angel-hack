# Tools for Port Scanning
## Nmap
General use: </br></br>
`nmap <IP>`</br>
  - `-T5` : Rapid Scanning
  - `-O`  : Find Operating Systems
  - `-sV` : Find versions
  - `-p`  : Scan only for certain ports

## Masscan
General use: </br></br>
`sudo masscan -e tun0 -p1-65535,U:1-65535 10.129.92.165 --rate=500`
