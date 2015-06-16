#!/usr/bin/python2
# coding: utf-8
# License: GPL 2.0

import logging
logger = logging.getLogger(__name__)

import argparse
import sys
import os
import subprocess

import requests
from requests import Session
from BeautifulSoup import BeautifulSoup
import json

def ChannelName(v):
    """
    ChannelName DataType
    Použité pro kontrolu povolených hodnot prametru --kanal
    """
    channels = ['ct1','ct2','ct24']
    if v not in channels:
        raise argparse.ArgumentTypeError("Povolené názvy kanálu jsou pouze "+",".join(channels))
    else:
        return v

class GetCtStream():
    """
    1. get url with streams: stream_url = getChannelStream("ct24");
    2. select stream quality: filtered_stream_url = selectStreamQuality(stream_url);
    3. put url to videoView: filtered_stream_url
    """    
    url_ct1 = "" # TODO 
    url_ct2 = "" # TODO 
    url_ct24 = "http://www.ceskatelevize.cz/ct24/zive-vysilani/"
    
    def getFlashPlayerUrl(self, url=None):
        if url is None:
            url = self.url_ct24 # Default to CT24 settings
                    
        logger.info("requests.get('"+url+"') ...")
        r = requests.get(url, timeout=30)
        html = unicode(r.text)
        soup = BeautifulSoup(html)
        flashplayer_url = "http://www.ceskatelevize.cz"+soup.body.find('div', 
            attrs={'id':'programmePlayer'}).find('iframe').get('src')
        
        logger.info("flashplayer_url - "+flashplayer_url)
        return flashplayer_url

    def getPlaylistUrl(self, playlist_type = "channel", playlist_id = "24",
                    requestSource="iVysilani", mediatype='flash', 
                    addCommercials="1", lowQuality=False, 
                    flashplayer_url=None):
        """
        orignal javascript code:
            getPlaylistUrl([{"type":"channel","id":"24"}], requestSource, 'flash', 1);
            var getPlaylistUrl = function(playlist, requestSource, type, addCommercials) { ... }
        """
        if flashplayer_url is None:
            flashplayer_url = self.getFlashPlayerUrl()    
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
                'Referer': flashplayer_url,
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
            ct1, ct2, ct24
        """
        logger.info("getting stream for channel - "+channel)
        
        url = ""
        playlist_id = ""
        
        if channel == "ct1":
            url = self.url_ct1
            playlist_id = "1" # TODO check this
        elif channel == "ct2":
            url = self.url_ct2
            playlist_id = "2" # TODO check this
        else: # channel == "ct24"
            url = self.url_ct24
            playlist_id = "24"
        
        flashplayer_url = self.getFlashPlayerUrl(url)
        playlist_url = self.getPlaylistUrl(
            playlist_type = "channel", playlist_id = playlist_id,
            requestSource="iVysilani", mediatype='flash', addCommercials="1", 
            lowQuality=False, flashplayer_url=flashplayer_url
            )
        stream_url = self.getStreamUrl(playlist_url)
        
        return stream_url
    
    def selectStreamQuality(self, stream_url):
        r = requests.get(stream_url, timeout=30)
        data = unicode(r.text)
        
        # get urls of different quality streams
        urls = []
        for l in data.split("\n"):
            if l.startswith("http"):
                urls.append(l)
                
        # return first stream url (lowest quality)
        logger.info("filtered_stream_url - "+urls[0])
        return urls[0]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='GetCTStream'
    )
    parser.add_argument(
        '-k', '--kanal',
        type=ChannelName,
        default='ct24',
        help='Vyber pro který kanál získat stream (default: ct24)')
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Debug debug level')
    parser.add_argument(
        '-i', '--info',
        action='store_true',
        help='Info debug level')
    parser.add_argument(
        '--disableprint',
        action='store_true',
        help='Zamezí vypisování získaných streamů')
    parser.add_argument(
        '--mpv',
        action='store_true',
        help='Otevři stream v přehrávači mpv')
    parser.add_argument(
        '--mplayer',
        action='store_true',
        help='Otevři stream v přehrávači mplayer')
    parser.add_argument(
        '--vlc',
        action='store_true',
        help='Otevři stream v přehrávači vlc')
    parser.add_argument(
        '--customplayer',
        default=None,
        help='Otevři stream ve zvoleném přehrávači.')
    args = parser.parse_args()
    
    logging.basicConfig()
    logger = logging.getLogger()
    
    logger.setLevel(logging.WARNING)  
    if args.debug:
        logger.setLevel(logging.DEBUG)
    elif args.info:
        logger.setLevel(logging.INFO)

    gcts = GetCtStream()
    stream_url = gcts.getChannelStream(args.kanal)
    lq_stream_url = gcts.selectStreamQuality(stream_url)
    
    if not args.disableprint:
        print "Kanal: "+args.kanal
        print "Stream url: "+stream_url
        print "Selected stream quality url: "+lq_stream_url
    
    if args.customplayer is not None:
        subprocess.call([args.customplayer, lq_stream_url])
    elif args.mpv:
        subprocess.call(["mpv", lq_stream_url])
    elif args.mplayer:
        subprocess.call(["mplayer", lq_stream_url])
    elif args.vlc:
        subprocess.call(["vlc", lq_stream_url])
