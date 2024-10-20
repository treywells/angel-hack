from pwn import *

def run():
    print("hellow world")

def printMenu():
    print('1. Recon')
    print('2. Next stuff to add later')

def getTargetIP():
    return input("Entering the target ip address: ")

if __name__ == '__main__':
   targetIP = getTargetIP(); 
