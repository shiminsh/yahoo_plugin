import os
import sys
import dbus
import urllib
import urllib2
import cookielib
import ConfigParser
from bs4 import BeautifulSoup


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
time              = 5000   # Use seconds x 1000


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

def checkConnection():
    try:
        urllib2.urlopen("http://www.google.com").close()
    except urllib2.URLError:
        return False
    else:
        return True


class yahoo:
    def __init__(self, Email, Passsword):
	self.login(Email, Password)

    def login(self, Email, Password):
        form_data = {'login':Email, 'passwd':Password}
        form_data = urllib.urlencode(form_data)
        jar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
        resp = opener.open(LoginUrl, form_data)
        resp = opener.open(ExportUrl)
        page = resp.read()
        self.parsing(page)

    def parsing(self, page):
        soup = BeautifulSoup(page)
        number = soup.em.b.string
        number = str(number)
        number = number.split(')')[0].lstrip('(')
        number = int(number)
        self.show_popup(number)

    def show_popup(self, number):
        icon = os.path.join(sys.path[0], 'logo.jpg')
        text = "You have %d unread mail" % number
        bus = dbus.SessionBus()
        notif = bus.get_object(item, path)
        notify = dbus.Interface(notif, interface)
        notify.Notify(app_name, id_num_to_replace, icon, title, text, actions_list, hint, time)

if __name__ == '__main__':
    while True:
        isConnected = checkConnection()
        if(isConnected == False):
            print "No internet connection"
        else:
            print "You are connected to the internet"
            config_path = os.path.join(sys.path[0], 'config.ini')
            Config = ConfigParser.ConfigParser()
            Config.read(config_path)
            Email = ConfigSectionMap("SectionOne")['email']
            Password = ConfigSectionMap("SectionOne")['password']
            d = yahoo(Email, Password)


