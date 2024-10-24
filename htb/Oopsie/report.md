# Hack the Box - Oopsie
## Overview
This is a Linux box that is running a web server on port 80. There is also SSH avaiable and open

## Recon
On the webserver, initial uses of gobuster for directory and subdomain enumeration don't really reveal much, except for the fact that there is a file called /uploads. However, the website suggests that there is a login page somewhere but we can't find any buttons or links to it. 

### Burp Suite
Using the Burp proxy to run the website, we can see a whole website map and that will reveal where the login page actually is and so now we can access the log in page. </br></br>

XSS and SQL injections appear to be off the table but we do see an upload file button that means we could upload any sort of file to the server. However, this action is locked to admins. Luckily, we can intercept traffic with Burp and in doing so, we can see what cookies they are sending and we notice that the cookie is just: `name` and `id`. </br></br>

Doing a little more recon on the website, we can see that the `Accounts` page has a url that we can change and changing the `id` parameter to `1` allows us to see the `user id` for the admin. </br></br>

Now, we can go back to the uploads page and before forwarding the request to the server, we can change the cookie to give up access to uploading files.

## Exploitation
For ParrotOS, in /usr/share/webshells/ we can find a lot of files for reverse shells on a web server. Those are perfect for this. Go ahead and grab one of the php reverse shell files and upload it to the server. Now, how can we run that file? Well, we can navigate to the file in the /uploads folder on the website. So hitting that file on the website will give us a reverse shell once we have a netcat listening port open. 

## Recon
Now time for more recon becuase now we have a non-sudo user on the server. While looking around the victim, we do see a suspicious file called `db.php` that I don't recall seeing during website recon. Opening it up will reveal a sql connection command with a user and a password. Well, that should allow us to see the mysql database on this victim but that database isn't too interesting. I wonder if that user and password are valid on the server??? (btw...they are). </br></br>

Now we can do some recon on this user's profile, one approach is to use linPEAS. Now, the problem is getting that script onto the server. We could do it the same way we got the reverse shell script on it. But we are going to realize that this user can't execute the script cause they don't have that privilege. </br></br>

So instead, let's see what groups this user is a part of. We can see they are a part of the bugtracker group and running `find -group bugtracker` will reveal what they have access to. And soemthing that we see is an executable in /usr/bin called bugTracker. </br></br>

Another thing that is interesting is that this script is actually running as root, we can see this by running `ll bugTracker` and in the permissions, we can see an `s` which means Set User ID and it sets it to root. Now, we could go ahead and run this file but I want to actually go look at the file to see what it does so I will download it to my attacking computer and decompile it ghidra. </br></br>

## Exploitation
Importing into ghidra and analyzing the functions shows a main function that ask the user for a number and then executes the command `cat /root/reports/<INPUT>` with it...with no input checking. That means if we run bugTracker on the victim, we could print out anything we want with a directory traversal attack. Now, the root flag is at `/root/root.txt` and we would be done. 

## Privilege Escalation
Technically, the last Exploitation section was also privilege escalation but oh well. Now, we are technically donw with the lab but you could do much more. The thing about the exploit above is that it can do more than just print stuff out. For example, this bash command is perfectly legal: `cat /root/reports/1;ls /root`. Using that same logic, we can actually get a reverse shell and now we have access to root and can execute anything we want.

## Presistence
Now, we could leave backdoors in the system if we wanted to. I personally haven't done much of this but here are some things that I did. One thing is to add a new user, I called it "service" to try to hide a little. You can set the password and then it added it to the sudo group so it pretty gave me a root account that I could ssh to. Another thing you could do is add your ssh public key to the authorized keys on a user and now you can always log in. 