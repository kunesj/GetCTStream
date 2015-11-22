#!/usr/bin/python2
# coding: utf-8
# License: GPL 3

import logging
logger = logging.getLogger(__name__)

import requests
import json

class GetCtStream():
    """
    1. get url with streams: stream_url = getChannelStream("ct24");
    2. select stream quality: filtered_stream_url = selectStreamQuality(stream_url);
    3. put url to videoView: filtered_stream_url
    """    

    channels = ['ct1','ct2','ct24','ctsport','ctd','ctart']

    def getPlaylistUrl(self, playlist_type = "channel", playlist_id = "24",
                    requestSource="iVysilani", mediatype='flash', 
                    addCommercials="1", lowQuality=False):
        """
        orignal javascript code:
            getPlaylistUrl([{"type":"channel","id":"24"}], requestSource, 'flash', 1);
            var getPlaylistUrl = function(playlist, requestSource, type, addCommercials) { ... }
        """
        timeout = 4000
        url = "http://www.ceskatelevize.cz/ivysilani/ajax/get-client-playlist"
        
        data = {
            'playlist[0][type]': playlist_type,
            'playlist[0][id]': playlist_id,
            'requestUrl': "/ivysilani/embed/iFramePlayerCT24.php",
            'requestSource': requestSource,
            'addCommercials': addCommercials,
            'type': mediatype
            }
        if lowQuality:
            data['streamQuality'] = 'nizka'
            
        headers={
                'Referer': "http://www.ceskatelevize.cz/ct24#live",
                'Host': 'www.ceskatelevize.cz',
                'x-addr': "127.0.0.1"
                }
        
        logger.info("requests.post(...), getting playlist url...")
        r = requests.post(url, timeout=timeout, data=data, headers=headers)
        
        logger.info("got playlist url, parsing...")
        purl = json.loads(r.text)['url']
        
        logger.info("playlist_url - "+purl)
        return purl

    def getStreamUrl(self, playlist_url=None):
        if playlist_url is None:
            playlist_url = self.getPlaylistUrl()
        
        logger.info("Getting playlist...")
        r = requests.get(playlist_url, timeout=30)
        data = json.loads(unicode(r.text))
        stream_url = data['playlist'][0]['streamUrls']['main']
        
        logger.info("stream_url - "+stream_url)
        return stream_url
        
    def getChannelStream(self, channel):
        """
        channel values:
            ct1, ct2, ct24, ctsport, ctd, ctart
        """
        logger.info("getting stream for channel - "+channel)
        
        # confirmed working playlist ids:
        # 1-6, 24
        playlist_id = ""
        if channel == "ct1":
            # často může mít přestávku (programy co nemůžou dát do iVysílání)
            playlist_id = "1" 
        elif channel == "ct2":
            playlist_id = "2" 
        elif channel == "ctsport":
            # Občas může mít přestávku
            playlist_id = "4" 
        elif channel == "ctd":
            playlist_id = "5"
        elif channel == "ctart":
            playlist_id = "6" #TODO - test jestli nekdy skonci prestavka
        else: # channel == "ct24"
            playlist_id = "24" 
            # playlist_id = "3" also works
        
        playlist_url = self.getPlaylistUrl(
            playlist_type = "channel", playlist_id = playlist_id,
            requestSource="iVysilani", mediatype='flash', addCommercials="1", 
            lowQuality=False
            )
        stream_url = self.getStreamUrl(playlist_url)
        
        return stream_url
    
    def selectStreamQuality(self, stream_url, qualityid=1):
        r = requests.get(stream_url, timeout=30)
        data = unicode(r.text)
        
        # get urls of different quality streams
        urls = []
        for l in data.split("\n"):
            if l.startswith("http"):
                urls.append(l)
        
        # fix qualityid
        logger.info("qualityid to use: "+str(qualityid))
        if qualityid>=len(urls):
            qualityid = len(urls)
        if qualityid<0:
            qualityid = -1
        logger.info("using qualityid: "+str(qualityid))
        
        selected_url = urls[qualityid]
        
        # return first stream url (lowest quality)
        logger.info("filtered_stream_url - "+selected_url)
        return selected_url
