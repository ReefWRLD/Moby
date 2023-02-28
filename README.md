MOBY
A Python script that connects to your Gmail account and searches for email messages matching the specified criteria. This script can be used to scan for phishing emails in your inbox.

Prerequisites
This code requires Python 3 and the following packages:

email
imaplib
base64
getpass
sys
time
threading
itertools
os
Installation
To run this code, first download the script onto your local machine. You will then need to download our comprehensive list of keywords that Moby uses and save the file to the /etc/Moby directory. Then, navigate to the directory where the script is saved using the command line. Finally, enter the command python3 <filename>.py to run the script.
to call Moby by it's name instead of running python3 <filename> you can alternativley save the program to the /usr/bin/ directory and create a PERMANENT alias for Moby. 

Usage
To use this script, follow the on-screen prompts to enter your Gmail account credentials and search criteria. The script will then search your inbox for email messages matching the specified criteria.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Author
This code was written by SimpleSecure.

Acknowledgments
This script was inspired by the need to scan for phishing emails in Gmail inboxes.
