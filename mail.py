#!/usr/bin/env python

import os
import sys
import time
import dbus
import urllib
import urllib2
import cookielib
import subprocess
import ConfigParser
from bs4 import BeautifulSoup
from os.path import expanduser


LoginUrl="https://login.yahoo.com/config/login?"
ExportUrl="https://in-mg61.mail.yahoo.com/neo/b/launch?"


item              = "org.freedesktop.Notifications"
path              = "/org/freedesktop/Notifications"
interface         = "org.freedesktop.Notifications"
app_name          = "Yahoo Plugin"
id_num_to_replace = 0
title             = "Yahoo Mail"
actions_list      = ''
hint              = ''
bus = dbus.SessionBus()
notif = bus.get_object(item, path)
notify = dbus.Interface(notif, interface)


def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def internet_on():
    return subprocess.call(['/bin/ping', '-c1', 'google.com'])

def update():
    home = expanduser("~")
    homefile = os.path.join(home, '.yahoonotif.ini')
    if os.path.exists(homefile):
        updateconfig = ConfigParser.RawConfigParser()
        updateconfig.read(homefile)
        email = updateconfig.get(updateconfig.sections()[0], updateconfig.options(updateconfig.sections()[0])[0])
        password = updateconfig.get(updateconfig.sections()[0], updateconfig.options(updateconfig.sections()[0])[1])
        changeconfig = ConfigParser.RawConfigParser()
        conpath = sys.path[0]
        configpath = os.path.join(conpath, 'config.ini')
        changeconfig.read(configpath)
        changeconfig.sections()
        changeconfig.set('SectionOne', 'email', email)
        changeconfig.set('SectionOne', 'password', password)
        with open(configpath, 'wb') as configfile:
            changeconfig.write(configfile)
    else:
        return


class yahoo:
    def __init__(self, Email, Passsword, previousnumber):
	self.login(Email, Password, previousnumber)

    def login(self, Email, Password, previousnumber):
        form_data = {'login':Email, 'passwd':Password}
        form_data = urllib.urlencode(form_data)
        jar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
        resp = opener.open(LoginUrl, form_data)
        resp = opener.open(ExportUrl)
        page = resp.read()
        self.parsing(page, previousnumber)

    def parsing(self, page, previousnumber):
        soup = BeautifulSoup(page)
        number = soup.em.b.string
        number = str(number)
        number = number.split(')')[0].lstrip('(')
        number = int(number)
        self.show_popup(number, previousnumber)

    def show_popup(self, number, previousnumber):
        time = 5000   # Use seconds x 1000
        icon = os.path.join(sys.path[0], 'logo.jpg')
        unreadmessages = "You have %d unread mail" % number
        self.sendmessage(unreadmessages, number, previousnumber)

    def sendmessage(self, message, number, previousnumber):
        diff = int(number) - int(previousnumber)
        if int(diff) == 0:
            self.dontshowpopup(message, number, previousnumber)
        else:
            self.showpopup(number, message)

    def dontshowpopup(self, message, number, previousnumber):
        self.value = number

    def showpopup(self, number, message):
        nomessage = "No unread mails"
        if number == 0:
            text = nomessage
            time = 5000
            icon = os.path.join(sys.path[0], 'logo.jpg')
            notify.Notify(app_name, id_num_to_replace, icon, title, text, actions_list, hint, time)
            self.updateconfig(number)
        else:
            text = message
            time = 5000
            icon = os.path.join(sys.path[0], 'logo.jpg')
            notify.Notify(app_name, id_num_to_replace, icon, title, text, actions_list, hint, time)
            self.updateconfig(number)

    def updateconfig(self, number):
        self.cwd = sys.path[0]
        self.basefile = os.path.join(self.cwd, 'config.ini')
        self.editconfig = ConfigParser.RawConfigParser()
        self.editconfig.read(self.basefile)
        self.editconfig.set('SectionOne', 'previousnumber', number)
        with open(self.basefile, 'wb') as configfile:
            self.editconfig.write(configfile)
        return

if __name__ == '__main__':
    update()
    while True:
        if internet_on() == 0:
            config_path = os.path.join(sys.path[0], 'config.ini')
            Config = ConfigParser.ConfigParser()
            Config.read(config_path)
            Email = ConfigSectionMap("SectionOne")['email']
            Password = ConfigSectionMap("SectionOne")['password']
            previousnumber = ConfigSectionMap("SectionOne")['previousnumber']
            d = yahoo(Email, Password, previousnumber)
            time.sleep(300)
        else:
            time.sleep(30)


	
