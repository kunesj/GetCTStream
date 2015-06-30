#!/usr/bin/python2
# coding: utf-8
# License: GPL 3

import logging
logger = logging.getLogger(__name__)

import argparse
import subprocess

from get_ct_stream import GetCtStream

def ChannelName(v):
    """
    ChannelName DataType
    Použité pro kontrolu povolených hodnot prametru --kanal
    """
    channels = GetCtStream.channels
    if v not in channels:
        raise argparse.ArgumentTypeError("Povolené názvy kanálu jsou pouze "+",".join(channels))
    else:
        return v

def main():
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
        '--qualityid',
        type=int,
        default=1,
        help='Použije stream qualitou zadaneho cisla. Default je 1 = druhá nejnizsi kvalita')
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
        '--playerpath',
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
    stream_url_quality = gcts.selectStreamQuality(stream_url, qualityid=args.qualityid)
    
    if not args.disableprint:
        print "Kanal: "+args.kanal
        print "Stream url: "+stream_url
        print "Selected stream quality url: "+stream_url_quality
    
    if args.playerpath is not None:
        subprocess.call([args.playerpath, stream_url_quality])
    elif args.mpv:
        subprocess.call(["mpv", stream_url_quality])
    elif args.mplayer:
        subprocess.call(["mplayer", stream_url_quality])
    elif args.vlc:
        subprocess.call(["vlc", stream_url_quality])
        
if __name__ == '__main__':
    main()
