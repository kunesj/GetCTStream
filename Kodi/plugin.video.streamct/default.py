# coding: utf-8

from get_ct_stream import GetCtStream

import xbmc

if __name__ == '__main__':
    print "Starting GET-CT-STREAM script"
    cts = GetCtStream()
    fs = cts.selectStreamQuality(cts.getChannelStream("ct24"))
    
    xbmc.Player().play(fs)
    
