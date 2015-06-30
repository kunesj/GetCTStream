# coding: utf-8

from get_ct_stream import GetCtStream

import os, sys
import xbmc, xbmcgui, xbmcaddon

def log(msg, level=xbmc.LOGNOTICE):
    msg = "plugin.video.streamct: "+msg
    xbmc.log(msg, level)

root = xbmc.translatePath( xbmcaddon.Addon(id='plugin.video.streamct').getAddonInfo("path") )
background_path = os.path.join(root, 'resources', 'media-overlay.jpg')
log("background path: "+background_path)
 
#get actioncodes from https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/Key.h
ACTION_PREVIOUS_MENU = 10 # Esc
ACTION_NAV_BACK = 92 # Backspace

ALIGN_CENTER = 6

# resolution values
#1080i = 0
#720p = 1
#480p = 2
#480p16x9 = 3
#ntsc = 4
#ntsc16x9 = 5
pal = 6
#pal16x9 = 7
#pal60 = 8
#pal6016x9 = 9
 
class MyClass(xbmcgui.WindowDialog):
    
    def __init__(self):     
        self.background = xbmcgui.ControlImage(75,75,575,250, background_path, aspectRatio=1)   
        self.addControl(self.background)
        
        self.set_controls()
        self.set_navigation()
        
        self.setResolution(pal)
        
    def setResolution(self, skinnedResolution):
        # get current resolution
        currentResolution = self.getResolution()
        offset = 0
        # if current and skinned resolutions differ and skinned resolution is not
        # 1080i or 720p (they have no 4:3) calculate widescreen offset
        if currentResolution != skinnedResolution and skinnedResolution > 1:
            # check if current resolution is 16x9
            if currentResolution == 0 or currentResolution % 2: iCur16x9 = 1
            else: iCur16x9 = 0
            # check if skinned resolution is 16x9
            if skinnedResolution % 2: i16x9 = 1
            else: i16x9 = 0
            # calculate offset
            offset = iCur16x9 - i16x9
        self.setCoordinateResolution(skinnedResolution + offset)

    def set_controls(self):        
        self.button0 = xbmcgui.ControlButton(104, 100, 153, 50, "ČT 1", alignment=ALIGN_CENTER)
        self.addControl(self.button0)
        self.button1 = xbmcgui.ControlButton(286, 100, 153, 50, "ČT 2", alignment=ALIGN_CENTER)
        self.addControl(self.button1)
        self.button2 = xbmcgui.ControlButton(466, 100, 153, 50, "ČT 24", alignment=ALIGN_CENTER)
        self.addControl(self.button2)
        self.button3 = xbmcgui.ControlButton(100, 175, 153, 50, "ČT Sport", alignment=ALIGN_CENTER)
        self.addControl(self.button3)
        self.button4 = xbmcgui.ControlButton(286, 175, 153, 50, "ČT :D", alignment=ALIGN_CENTER)
        self.addControl(self.button4)
        self.button5 = xbmcgui.ControlButton(466, 175, 153, 50, "ČT Art", alignment=ALIGN_CENTER)
        self.addControl(self.button5)
        self.button_close = xbmcgui.ControlButton(286, 250, 153, 50, "Zavřít menu", alignment=ALIGN_CENTER)
        self.addControl(self.button_close)

    def set_navigation(self):
        self.button0.controlDown(self.button3)
        self.button0.controlRight(self.button1)
        
        self.button1.controlDown(self.button4)
        self.button1.controlRight(self.button2)
        self.button1.controlLeft(self.button0)
        
        self.button2.controlDown(self.button5)
        self.button2.controlLeft(self.button1)
        
        self.button3.controlDown(self.button_close)
        self.button3.controlUp(self.button0)
        self.button3.controlRight(self.button4)
        
        self.button4.controlDown(self.button_close)
        self.button4.controlUp(self.button1)
        self.button4.controlRight(self.button5)
        self.button4.controlLeft(self.button3)
        
        self.button5.controlDown(self.button_close)
        self.button5.controlUp(self.button2)
        self.button5.controlLeft(self.button4)
        
        self.button_close.controlUp(self.button4)
        self.button_close.controlLeft(self.button3)
        self.button_close.controlRight(self.button5)
        
        self.setFocus(self.button0)

    def onAction(self, action):
        if action == ACTION_NAV_BACK or action == ACTION_PREVIOUS_MENU:
            self.close()

    def onControl(self, control): 
        if control == self.button_close:
            self.close()
        
        channel = None
        if control == self.button0:
            channel = 'ct1'
        if control == self.button1:
            channel = 'ct2'
        if control == self.button2:
            channel = 'ct24'
        if control == self.button3:
            channel = 'ctsport'
        if control == self.button4:
            channel = 'ctd'
        if control == self.button5:
            channel = 'ctart'
        
        if channel is not None:
            try:
                gcts = GetCtStream()
                chs = gcts.getChannelStream(channel)
                lq_chs = gcts.selectStreamQuality(chs, qualityid=0) # lowest quality
                xbmc.Player().play(lq_chs)
                self.close()
            except Exception, e:
                self.message('Loading stream failed, '+str(e))
            
    def message(self, message):
        dialog = xbmcgui.Dialog()
        dialog.ok("Message", message)

 
mydisplay = MyClass()
mydisplay .doModal()
del mydisplay
