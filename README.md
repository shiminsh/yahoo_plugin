yahoo_plugin
============

It is a plugin which shows notification of unread yahoo mails.

Configuring This Package
------------------------

Clone this repository using this command:-
    
    git clone https://github.com/shiminsh/yahoo_plugin

Now, get into the directory `yahoo_plugin` using this command:-
    
    cd yahoo_plugin

And run this command:-
    
    sudo pip install -r requirements.txt

Add email and password of your yahoo account in a file named as `.yahoonotif.ini` in the format given below:-

    [SectionOne]
    email = TestUser
    password = ********

And save the file named as `.yahoonotif.ini` in your home folder.

Then Run the mail.py file with python or add the execution of file in startup.

