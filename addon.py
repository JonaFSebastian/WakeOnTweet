import xbmcaddon, xbmc
import word_resolver
import requests
import re
import os
import sys

#if True enable operation logging
logEnabled = True

#log info to xbmc logging system
def LOG(msg):
    if (logEnabled):
        if isinstance(msg, unicode):
            msg = msg.encode('utf-8')
        xbmc.log('WOT>'+msg)

LOG('Wake On Tweet Addon start processing')

#set default values
twitter_screen_name = 'J_F_Sebastian'
check_interval = 60
pc_mac = '00:11:D8:22:19:1F'
net_broadcast = '255.255.255.255'
net_dest = '255.255.255.255'
net_port = 9
cmd_command = 'WAKEMYPC'

#get setting
settings = xbmcaddon.Addon( id = 'service.xbmc.wakeontweet' )
language  = settings.getLocalizedString

rootDir = settings.getAddonInfo('path')
if rootDir[-1] == ';':rootDir = rootDir[0:-1]
resDir = os.path.join(rootDir, 'resources')
iconDir = os.path.join(resDir, 'icons')
iconWOT = os.path.join(iconDir, 'WOT.png')

try:        
    twitter_name = settings.getSetting("screenName")
    twitter_name = word_resolver.searchstr('@'+twitter_name)    
    check_interval = int(settings.getSetting("checkInterval"))
    
    pc_mac = settings.getSetting("macAddress")
    net_broadcast = settings.getSetting("netBroadcast")
    net_dest = settings.getSetting("netDest")
    net_port = int(settings.getSetting("netPort"))    
    cmd_command = settings.getSetting("tweetText")
    cmd_command = cmd_command.upper()
except:
    pass

#wake pc using xbmc builtint api
def WAKE():
    xbmc.executebuiltin('XBMC.Notification("Wake On Tweet","' + language(60001) + ' ' + pc_mac + '",5000,"' + iconWOT + '")')
    xbmc.executebuiltin('XBMC.WakeOnLan("'+pc_mac+'")')
    return

#check for tweet
def CHECK(t):      
    url = 'http://www.twitter.com/search?f=realtime&q='+twitter_name    
    try:
        LOG(url)         
        link = requests.get(url).text
        mistweet = re.compile('(data-promoted)').findall(link)
        mistweet2 = re.compile('(data-relevance-type)').findall(link)        
        test_tweet = len(mistweet) + len(mistweet2)
        text=re.compile('<p class="js-tweet-text tweet-text".+?>(.+?)</p>').findall(link)
        text=text[test_tweet]
        text = word_resolver.text(text)
        text = text.upper()
        text = unicode(text).encode('utf-8')
        LOG('D0')
        LOG(t)
        LOG('D1')        
        LOG(text)
        LOG('D2')
        LOG(t)
        if not text == t:
            LOG('D3')
            if not t == unicode('').encode('utf-8'):
                LOG('D4')
                if unicode(cmd_command).encode('utf-8') in text:
                    LOG('D5')
                    WAKE()                  
    except:
        LOG(str(sys.exc_info()[0]))
    return text

LOG('twitter account set to '+ twitter_name)
LOG('twitter check interval set to '+ str(check_interval))

xbmc.executebuiltin('XBMC.Notification("Wake On Tweet","' + language(60000) + ' @' + settings.getSetting("screenName") + '",5000,"'+iconWOT+'")')

def WAIT():
    w = 0
    while (w < check_interval and not xbmc.abortRequested):
        xbmc.sleep(1000)
        w = w + 1
    return

text_old = unicode('').encode('utf-8')

while (not xbmc.abortRequested):
    if settings.getSetting("enable_service") == 'true':
        t = CHECK(text_old)
        LOG('D6')
        text_old = t 
        LOG('D7')       
        try:            
            WAIT()
        except:
            xbmc.sleep(1000*60)
    else:
        xbmc.sleep(1000)
    
