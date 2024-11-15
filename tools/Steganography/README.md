# Steganography

## Steghide

Built into Linux and will provide encryption and decryption. <br><br>
To embed data: `steghide embed -cf <file to store> -ef <file to hide>` <br><br>
To extract data: `steghide extract -sf <file>`<br><br>

## stegseek

Stegseek is a brute forcing program for steganography. It can use a wordlist to brute force the password used for the encryption.<br><br>

To brute force: `stegseek <file> <wordlist>` <br><br>

### Vulnerability

CVE 2021-27211: Steghide's range for their RNG is not big enough and can be brute forced with `stegseek --seed <file>` to see if there is any data in a file. If the data in the file is unecrypted, it will show the data aswell.

### Installation
Take the debian file from this folder and run `sudo apt install ./<file.deb>` to install stegseek. You can grab the latest release from this link: `https://github.com/RickdeJager/stegseek/releases`