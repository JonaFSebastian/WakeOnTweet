# Kodi (XBMC) WakeOnTweet
WakeonTweet is a service python script for Kodi (XBMC) checking periodically a Twitter account for specific text in Tweet, and when found send over LAN a WOL packet to a MAC address to wake device supporting WakeOnLan packet. 
Has been designed to run on Raspberry Pi running Kodi (XBMC) Helix version. with small changes can be fitted to run on any Kodi (XBMC) device.
Since it uses builtin function wakeonlan and requests library only the version implementing them could run this script.
