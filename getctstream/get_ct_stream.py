#!/usr/bin/env python3
# encoding: utf-8
# License: GPL 3

import logging
logger = logging.getLogger(__name__)

import sys

import requests
import json

class GetCtStream():
    """
    1. get url with streams: stream_url = getChannelStream("ct24");
    2. select stream quality: filtered_stream_url = selectStreamQuality(stream_url);
    3. put url to videoView: filtered_stream_url
    """

    channels = ['ct1','ct2','ct24','ctsport','ctd','ctart']

    def getPlaylistUrl(self, playlist_id = "24", addCommercials=None):
        """
        Important javascript code is in getPlaylistUrl() function.
            - info located inline and in ajax-playlist-o2v2.js
            - has more optional parameters than are implemented

        ---WORKING PACKET FORMAT---
        POST https://www.ceskatelevize.cz/ivysilani/ajax/get-client-playlist/

        Headers:
            Host: www.ceskatelevize.cz
            User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0
            Accept: */*
            Accept-Language: cs,en-US;q=0.7,en;q=0.3
            Accept-Encoding: gzip, deflate, br
            Referer: https://www.ceskatelevize.cz/ivysilani/embed/iFramePlayer.php?skinID=3&videoID=CT24&tpl=live&multimedia=1&width=100%25&hash=abcfaa44d0a903e6abe4117b318184a8de30653b
            Content-Type: application/x-www-form-urlencoded; charset=UTF-8
            x-addr: 127.0.0.1
            X-Requested-With: XMLHttpRequest
            Content-Length: 145
            DNT: 1
            Connection: keep-alive

        Body:
            playlist%5B0%5D%5Btype%5D=channel&playlist%5B0%5D%5Bid%5D=24&requestUrl=%2Fivysilani%2Fembed%2FiFramePlayer.php&requestSource=iVysilani&type=html
        """
        data = {
            "playlist[0][type]": "channel",
            "playlist[0][id]": playlist_id,
            "requestUrl": "/ivysilani/embed/iFramePlayer.php",
            "requestSource": "iVysilani",
            "type": "html",
        }
        if addCommercials is not None:
            data["addCommercials"] = addCommercials
        logger.debug(data)

        headers={
            "Host": "www.ceskatelevize.cz",
            "Referer": "https://www.ceskatelevize.cz/ivysilani/embed/iFramePlayer.php",
            "x-addr": "127.0.0.1", # only this is definitely required
            }
        logger.debug(headers)

        logger.info("requests.post(...), getting playlist url...")
        r = requests.post(
            "https://www.ceskatelevize.cz/ivysilani/ajax/get-client-playlist/",
            timeout=4000, data=data, headers=headers
            )

        logger.info("got playlist url, parsing...")
        purl = json.loads(r.text)['url']

        if purl.lower().strip() == "error":
            logger.error("Failed to get playlist url!!!")
            sys.exit(1)

        logger.info("playlist_url - "+purl)
        return purl

    def getStreamUrl(self, playlist_url=None):
        if playlist_url is None:
            playlist_url = self.getPlaylistUrl()

        logger.info("Getting playlist...")
        r = requests.get(playlist_url, timeout=30)
        data = json.loads(r.text)
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

        playlist_url = self.getPlaylistUrl(playlist_id = playlist_id)
        stream_url = self.getStreamUrl(playlist_url)

        return stream_url

    def selectStreamQuality(self, stream_url, qualityid=1):
        r = requests.get(stream_url, timeout=30)
        data = r.text

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
