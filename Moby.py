#!/usr/bin/python3
#test
"""=============================== IMPORT STATEMENTS ========================================="""
import email
import imaplib
import base64
import getpass
import sys
import time
import threading
import itertools
                        #NEW IMPORT TOOL#
import os
"""=======================================VARIABLES =========================================="""
whale_art= '''
                           ****     ****          **
                          /**/**   **/**         /**       **   **
                          /**//** ** /**  ****** /**      //** **
                          /** //***  /** **////**/******   //***
                          /**  //*   /**/**   /**/**///**   /**
                          /**   /    /**/**   /**/**  /**   **
                          /**        /**//****** /******   **
                          //         //  //////  /////    //
                                     ','. '. ; : ,','
                                       '..'.,',..'
                                          ';.'  ,'
                                           ;;
                                           ;'
                            :._   _.------------.___
                    __      :__:-'                  '--.
             __   ,' .'    .'             ______________'.
           /__ '.-  _\___.'          0  .' .'  .'  _.-_.'
              '._                     .-': .' _.' _.'_.'
                 '----'._____________.'_'._:_:_.-'--'
       ########################################################################
                                    Welcome to Moby!
                                Phishing Email Scanner
                                Created by SimpleSecure
                                    Version 1.0
       ########################################################################
'''
imap_username = ""
imap_password = ""
imap_server = "imap.gmail.com"
imap_port = 993
status = ""
messages = ""
status = ""
imap_client = ""
# UN simplesecure01@gmail.com
# PW ivxinlxmaoekyvoj
"""================================== HELPER FUNCTINS ========================================"""
                       #NEW#
            #path to comprehensive word list
with open('/etc/moby/text.log', "r") as f:
    wordlist = [line.strip() for line in f.readlines()]
# with open('text.log', "r") as f:
#     wordlist = [line.strip() for line in f.readlines()]
#wordlist=['prince','test','deez', 'nigerian']
# Opening function that prints our "Welcome"
def greeting():
    print(whale_art)
# This function establishes an IMAP connection
def imap_connect(imap_server, imap_port):
    # If a variable is defined in a function (and you wish to use it outside of that function)
    # use the "global" statement to allow the variable to be recognized globaly
    global imap_username, imap_password, messages, status, imap_client
     # We establish a count for our login attempts
    tries = 0
    # We start to connect to our gmail server by providing our login credentials.
    # The user has three atempts to login, otherwise they exit the program
    while tries < 3:
        imap_username = input("Enter your GMail: ").lower()
        if not imap_username.endswith("@gmail.com"):
            print("invalid email address. Please enter a Gmail address.")
            tries += 1
            continue
        imap_password = getpass.getpass("Password: ")
        try:
            # Set up the IMAP client
            # This creates an IMAP object with an SSL connection by calling the variables
            # for the email server and the SSL port
            imap_client = imaplib.IMAP4_SSL(imap_server, imap_port)
            # Now we log in to the account by calling our variables for the credentials
            # This email server is not as friendly with 3rd party applications
            # accesing their servers. So first we had to first enable two-factor
            # authentication on the email accountinorder for script to connect to the
            # server. We then were able to generate a special key, specific
            # to this account. This key is what we use as the passowrd, and it allows us
            # to bybass the two-factor auth for this account
            imap_client.login(imap_username, imap_password)
            # If the credentials are valid exit the "while" loop and move to the next
            # part of the code
            break
        # If credentials are invalid, display error message and add 1 to the count
        except imaplib.IMAP4.error:
            print("Invalid username or password. Please try again.")
            tries += 1
    # If the count reaches 3, display error message and exit the script
    if tries == 3:
        print("you have exceeded the maximum number of login attempts.")
        sys.exit()
    # This allows us to select from the various mailboxes in this account. In this case we are
    # interested in the "INBOX" mailbox
    imap_client.select("INBOX")
    search_option = input("Search all messages or unseen messages? (Type 'ALL' or 'UNSEEN'): ").upper()
    while search_option not in ["ALL", "UNSEEN"]:
        search_option = input("Invalid input. Please type 'ALL' or 'UNSEEN': ").upper()
     # Search for email messages matching the specified criteria
    # When the search function is used in conjuction with IMAP it parses
    # through the emails in the specified mailbox. The first argument "None"
    # specifies the search CRITERIA, which in this csae is none so all
    # messages should be searched. The second argument, "ALL" specifies the
    # search QUERY, which should return all messages is the mailbox
    # The results will be added to the variables "status" and "messages"
    status, messages = imap_client.search(None, search_option)
    done = False
    #here is the animation
    def animate():
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            sys.stdout.write('\rloading ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\rScan Complete!     \n')
    t = threading.Thread(target=animate)
    t.start()
    #long process here
    time.sleep(8)
    done = True
# Since our email outputs to base64 this function brings it back to English
def decode_base64(encoded_string):
    decoded_bytes = base64.b64decode(encoded_string)
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string
                                #NEW#
#create a new directory called emails in the current directory if it doesnt exist
if not os.path.exists("emails"):
    os.mkdir("emails")
                            #NEW#
#create a new variable to append results into a spam.txt and you can see this
#towards the end of the def get_message() function
email_content = []
def get_message():
    global status, imap_client
                         #NEW#
 # create a new variable to sense if there were any unread messages#
    messages_processed = False
    # Start our "For" loop to Process each email message as needed.
    # The vriable "messages" was given a value of all the message ID's in a list following
    # the code above. In order to use this information, we first need to split the list at the [0]
    # index.
    for message_id in messages[0].split():
        # .fetch() function allows us to get the messages based on the message ID's, found in the
        # msg_data variable. We also need to describe the format of the data. In this case, becasue
        # we are looking at messages, it would be RFC822
        status, msg_data = imap_client.fetch(message_id, "(RFC822)")
        # Now that we have fetched our messages, we need to begin to transfer the data into human
        # readable format. To do this we use our module "email" which we imported from above and
        # use the "message_from_byters" function to transfer the data from bytes to encoded data
        email_message = email.message_from_bytes(msg_data[0][1])
        decoded_strings = []
        # We loop through each emal with ".walk()" that creates a directory tree of all the messages
        for part in email_message.walk():
            # If the content of the "part"/message is pain text...
            if part.get_content_type() == "text/plain":
                # Then check if the encoding type is base64. If it is, we get the encoded payload and
                # decode the payload making it plain text. We then add the decoded message to our
                # list above "decoded_strings"
                if part.get('Content-Transfer-Encoding') == 'base64':
                    encoded_string = part.get_payload()
                    decoded_string = decode_base64(encoded_string)
                    # If the content is not encoded with base64, then we apend the readable content
                    # to our list "decoded_strings"
                else:
                        decoded_string = part.get_payload()
                        decoded_strings.append(decoded_string.lower())
            # This is where we look to see if our email message(s) contain any keywords that are in our
            # flagged list of "phishing-words"
            if any(word.lower() in ' '.join(decoded_strings) for word in wordlist):
            # If an email does contain a keyword, the "Sender", "Subject Line", "Date" and content
            # are displayed on screen for the user to easily identify and delete
                print("\rFrom:", email_message["From"])
                print("Subject:", email_message["Subject"])
                print("Date:", email_message["Date"])
                print("___________\n")
                for decoded_string in decoded_strings:
                    print(decoded_string)
                    print("============================================================================================ \n")
                #Catagorizes each email being appended after being decoded
                email_content.append(f"From: {email_message['From']}\nSubject: {email_message['Subject']}\nDate: {email_message['Date']}\n")
                for decoded_string in decoded_strings:
                    email_content.append(decoded_string)
                    email_content.append("==============================================================================\n")
                    messages_processed = True
    if not messages_processed:
        print("No unread messages.")
    if email_content:
        if not os.path.exists("emails"):
            os.makedirs("emails")
        if not os.path.exists(os.path.join("emails", "spam.txt")):
            with open(os.path.join("emails", "spam.txt"), 'w') as f:
                f.write("\n\n".join(email_content))
        else:
            with open(os.path.join("emails", "spam.txt"), 'a') as f:
                f.write("\n\n".join(email_content))
"""==================================== MAIN FUNCTION ======================================"""
def main():
    greeting()
    imap_connect(imap_server, imap_port)
    # print("Scan Complete!")
    get_message()
main()







