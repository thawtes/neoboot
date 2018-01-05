#!/usr/bin/python
# -*- coding: utf-8 -*-  
                               
from __init__ import _
from Plugins.Extensions.NeoBoot.files import Harddisk                                                                                                                                                     
from Plugins.Extensions.NeoBoot.files.stbbranding import getKernelVersionString, getKernelImageVersion, getCPUtype, getCPUSoC,  getImageNeoBoot, getBoxVuModel, getBoxHostName, getTunerModel
from enigma import getDesktop
from enigma import eTimer
from Screens.Screen import Screen                                                                                                                                               
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Screens.Standby import TryQuitMainloop
from Components.About import about
from Components.Sources.List import List
from Components.Button import Button
from Components.ActionMap import ActionMap, NumberActionMap
from Components.GUIComponent import *
from Components.MenuList import MenuList
from Components.Input import Input
from Components.Label import Label
from Components.ProgressBar import ProgressBar
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap, MultiPixmap
from Components.config import *
from Components.ConfigList import ConfigListScreen
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, pathExists, createDir, resolveFilename, SCOPE_PLUGINS
from os import system, listdir, mkdir, chdir, getcwd, rename as os_rename, remove as os_remove, popen
from os.path import dirname, isdir, isdir as os_isdir
import os
import time
# Copyright (c) , gutosie  license
# 
# Redystrybucja wersji programu i dokonywania modyfikacji JEST DOZWOLONE, pod warunkiem zachowania niniejszej informacji o prawach autorskich. 
# Autor NIE ponosi JAKIEJKOLWIEK odpowiedzialności za skutki użtkowania tego programu oraz za wykorzystanie zawartych tu informacji.
# Modyfikacje przeprowadzasz na wlasne ryzyko!!!
# O wszelkich zmianach prosze poinformowac na  http://all-forum.cba.pl   w temacie pod nazwa  	 -#[NEOBOOT]#-

# This text/program is free document/software. Redistribution and use in
# source and binary forms, with or without modification, ARE PERMITTED provided
# save this copyright notice. This document/program is distributed WITHOUT any
# warranty, use at YOUR own risk.

PLUGINVERSION = '6.00 '
UPDATEVERSION = '6.46'
         
class MyUpgrade(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = '<screen position="center,center" size="1280,570" title="Tools Neoboot">\n\t\t\t<ePixmap position="594,226" zPosition="-2" size="623,313" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrix.png" /> <widget source="list" render="Listbox" position="33,127" size="1229,82" scrollbarMode="showOnDemand">\n\t\t\t\t<convert type="TemplatedMultiContent">\n                \t\t{"template": [\n                    \t\t\tMultiContentEntryText(pos = (90, 1), size = (920, 66), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n                    \t\t\tMultiContentEntryPixmapAlphaTest(pos = (8, 4), size = (66, 66), png = 1),\n                    \t\t\t],\n                    \t\t\t"fonts": [gFont("Regular", 40)],\n                    \t\t\t"itemHeight": 66\n                \t\t}\n            \t\t</convert>\n\t\t</widget>\n    <eLabel text="NeoBoot wykry\xc5\x82 nowsz\xc4\x85 wersj\xc4\x99. " font="Regular; 40" position="27,40" size="1042,70" halign="center" foregroundColor="red" backgroundColor="black" transparent="1" />\n\t\t <eLabel text="EXIT - Zrezygnuj" font="Regular; 40" position="27,441" size="389,80" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />\n\t\t        </screen>'
    else:
        skin = '<screen position="center,center" size="1127,569" title="Tools NeoBoot">\n\t\t\t<ePixmap position="492,223" zPosition="-2" size="589,298" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrix.png" /> <widget source="list" render="Listbox" position="18,122" size="1085,82" scrollbarMode="showOnDemand">\n\t\t\t\t<convert type="TemplatedMultiContent">\n                \t\t{"template": [\n                    \t\t\tMultiContentEntryText(pos = (90, 1), size = (920, 66), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n                    \t\t\tMultiContentEntryPixmapAlphaTest(pos = (8, 4), size = (66, 66), png = 1),\n                    \t\t\t],\n                    \t\t\t"fonts": [gFont("Regular", 40)],\n                    \t\t\t"itemHeight": 66\n                \t\t}\n            \t\t</convert>\n\t\t</widget>\n    <eLabel text="NeoBoot wykry\xc5\x82 nowsz\xc4\x85 wersj\xc4\x99 wtyczki. " font="Regular; 40" position="27,40" size="1042,70" halign="center" foregroundColor="red" backgroundColor="black" transparent="1" />\n\t\t <eLabel text="EXIT - Zrezygnuj" font="Regular; 40" position="27,441" size="389,80" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />\n\t\t        </screen>'
    __module__ = __name__

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.wybierz()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.changever})

    def changever(self):
        ImageChoose = self.session.open(NeoBootImageChoose)
        if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location'):
            out = open('/media/neoboot/ImageBoot/.version', 'w')
            out.write(PLUGINVERSION)
            out.close()
            self.close()
        else:
            self.close(self.session.open(MessageBox, _('No file location NeoBot, do re-install the plugin.'), MessageBox.TYPE_INFO, 10))
        self.close()
        return ImageChoose

    def wybierz(self):
        self.list = []
        mypath = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot'
        if not fileExists(mypath + 'icons'):
            mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/ok.png'
        png = LoadPixmap(mypixmap)
        res = (_('Update neoboot in all images ?'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0 and self.session.open(MyUpgrade2):
            pass
        self.close()


class MyUpgrade2(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = '<screen position="center,center" size="900,450" title="NeoBoot">\n\t\t<widget name="lab1" position="23,42" size="850,350" font="Regular;35" halign="center" valign="center" transparent="1" />\n</screen>'
    else:
        skin = '<screen position="center,center" size="400,200" title="NeoBoot">\n\t\t<widget name="lab1" position="10,10" size="380,180" font="Regular;24" halign="center" valign="center" transparent="1"/>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label(_('NeoBoot: Upgrading in progress\nPlease wait...'))
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.updateInfo)
        self.onShow.append(self.startShow)

    def startShow(self):
        self.activityTimer.start(10)

    def updateInfo(self):
        self.activityTimer.stop()
        f2 = open('/media/neoboot/ImageBoot/.neonextboot', 'r')
        mypath2 = f2.readline().strip()
        f2.close()
        if fileExists('/.multinfo'):
            self.myClose(_('Sorry, NeoBoot can installed or upgraded only when booted from Flash.'))
            self.close()
        elif mypath2 != 'Flash':
            self.myClose(_('Sorry, NeoBoot can installed or upgraded only when booted from Flash.'))
            self.close()
        else:
            for fn in listdir('/media/neoboot/ImageBoot'):
                dirfile = '/media/neoboot/ImageBoot/' + fn
                if isdir(dirfile):
                    target = dirfile + '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot'
                    cmd = 'rm -r ' + target + ' > /dev/null 2>&1'
                    system(cmd)
                    cmd = 'cp -r /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot ' + target
                    system(cmd)
          
            out = open('/media/neoboot/ImageBoot/.version', 'w')
            out.write(PLUGINVERSION)
            out.close()
            self.myClose(_('NeoBoot successfully updated. You can restart the plugin now.\nHave fun !!!'))


    def myClose(self, message):
        ImageChoose = self.session.open(NeoBootImageChoose)
        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        self.close(ImageChoose)


class MyHelp(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = '<screen position="center,center" size="1920,1080" borderWidth="0" borderColor="transpBlack" flags="wfNoBorder">\n\n\n<eLabel text="INFORMACJE NeoBoot" font="Regular; 35" position="71,20" size="1777,112" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />\n<widget name="lab1" position="69,134" size="1780,913" font="Regular;35"    />\n</screen>'
    else:
        skin = '<screen position="center,center" size="1280,720" title="NeoBoot - Informacje">\n<widget name="lab1" position="18,19" size="1249,615" font="Regular;20" backgroundColor="black" transparent="1" />\n</screen>'
    __module__ = __name__

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = ScrollLabel('')
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'DirectionActions'], {'back': self.close,
         'ok': self.close,
         'up': self['lab1'].pageUp,
         'left': self['lab1'].pageUp,
         'down': self['lab1'].pageDown,
         'right': self['lab1'].pageDown})
        self['lab1'].hide()
        self.updatetext()

    def updatetext(self):
        message = _('NeoBoot Ver. ' + PLUGINVERSION + '  Enigma2\n\nDuring the entire installation process does not restart the receiver !!!\n\n')
        message += _('NeoBoot Ver. updates ' + UPDATEVERSION + '  \n\n')
        message = _('For proper operation NeoBota type device is required USB stick or HDD, formatted on your system files Linux ext3 or ext4..\n\n')
        message += _('1. If you do not have a media formatted with the ext3 or ext4 is open to the Device Manager <Initialize>, select the drive and format it.\n\n')
        message += _('2. Go to the device manager and install correctly hdd and usb ...\n\n')
        message += _('3. Install NeoBota on the selected device.\n\n')
        message += _('4. Install the needed packages...\n\n')
        message += _('5. For proper installation XenoBota receiver must be connected to the Internet.\n\n')
        message += _('6. In the event of a problem with the installation cancel and  inform the author of the plug of a problem.\n\n')
        message += _('Have fun !!!')
        self['lab1'].show()
        self['lab1'].setText(message)


class Opis(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = '<screen position="center,center" size="1920,1080" flags="wfNoBorder">   <ePixmap position="0,0" zPosition="-1" size="1920,1080" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/frame_base-fs8.png"  />  <widget source="session.VideoPicture" render="Pig" position=" 1253,134" size="556,313" zPosition="3" backgroundColor="#ff000000"/>    <eLabel text="INFORMACJE NeoBoot" position="340,50"  size="500,55" font="Regular;40" halign="left" foregroundColor="#58bcff" backgroundColor="black" transparent="1"/>  <widget name="key_red" position="30,950" size="430,50" zPosition="1" font="Regular; 30" halign="center" backgroundColor="red" transparent="1" foregroundColor="white" />          <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/scroll.png" position="1144,160" size="26,685" zPosition="5" alphatest="blend"/>   <ePixmap position="1350,750" zPosition="1" size="400,241" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrixhd.png" />   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/red25.png" position="100,1000" size="230,36" alphatest="blend" />    \n<widget name="lab1" position="100,160" size="1070,680" font="Regular; 30"  backgroundColor="black" transparent="1" />\n</screen>'                  		 		   		
    else:
        skin = '<screen position="center,center" size="1280,720" title="NeoBoot - Informacje">\n<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/1frame_base-fs8.png"  position="0,0" zPosition="-1" size="1280,720" />\n<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/red25.png" position="50,680" size="230,36" alphatest="blend"  />\n<widget name="key_red" position="35,630" zPosition="1" size="270,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" />\n<widget name="lab1" position="50,100" size="730,450" font="Regular;20" backgroundColor="black"  />  <widget source="session.VideoPicture" render="Pig" position=" 836,89" size="370,208" zPosition="3" backgroundColor="#ff000000" />    <widget source="Title" render="Label"  position="200,25" size="800,30" font="Regular;28" halign="left" foregroundColor="#58bcff" backgroundColor="transpBlack" transparent="1"/> <ePixmap position="920,520" zPosition="1" size="228,130" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/1matrix.png" />   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/scroll.png" position="754,100" size="26,455" zPosition="5" alphatest="blend"/> backgroundColor="black" transparent="1" \n</screen>'
    __module__ = __name__

    def __init__(self, session):
        Screen.__init__(self, session)
        self['key_red'] = Label(_('Remove NeoBoot of STB'))
        self['lab1'] = ScrollLabel('')
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'DirectionActions'], {'back': self.close,
         'red': self.delete,
         'ok': self.close,
         'up': self['lab1'].pageUp,
         'left': self['lab1'].pageUp,
         'down': self['lab1'].pageDown,
         'right': self['lab1'].pageDown})
        self['lab1'].hide()
        self.updatetext()

    def updatetext(self):
        message = _('NeoBoot Ver. ' + PLUGINVERSION + '\n\n')
        message += _('NeoBoot Ver. updates ' + UPDATEVERSION + '\n\n')
        message += _('1. Requirements: For proper operation of the device NeoBota are required USB stick or HDD.\n\n')
        message += _('2. NeoBot is fully automated\n\n')
        message += _('3. To install a new image in MultiBocie should be sent by FTP software file compressed in ZIP or NIF to the folder: \n/media/neoboot/ImagesUpload and remote control plugin NeoBoot use the green button <Installation>\n\n')
        message += _('4. For proper installation and operation of additional image multiboot, use only the image intended for your receiver. !!!\n\n')
        message += _('5. By installing the multiboot images of a different type than for your model STB DOING THIS AT YOUR OWN RISK !!!\n\n')
        message += _('6. The installed to multiboot images, it is not indicated update to a newer version.\n\n')
        message += _('The authors plug NeoBot not liable for damage a receiver, NeoBoota incorrect use or installation of unauthorized additions or images.!!!\n\n')
        message += _('Have fun !!!')
        message += _('\nCompletely uninstall NeoBota: \nIf you think NeoBot not you need it, you can uninstall it.\nTo uninstall now press the red button on the remote control.\n\n')
        self['lab1'].show()
        self['lab1'].setText(message)

    def delete(self):
        message = _('Are you sure you want to completely remove NeoBoota of your image?\n\nIf you choose so all directories NeoBoota will be removed.\nA restore the original image settings Flash.')
        ybox = self.session.openWithCallback(self.mbdelete, MessageBox, message, MessageBox.TYPE_YESNO)
        ybox.setTitle(_('Removed successfully.'))

    def mbdelete(self, answer):
        if answer is True:
            cmd = "echo -e '\n\n%s '" % _('Recovering setting....\n')
            cmd1 = 'rm -R /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot; rm -R /media/neoboot/ImageBoot/.Flash; rm -R /media/neoboot/ImageBoot/.neonextboot; rm -R /media/neoboot/ImageBoot/.version'
            cmd2 = 'rm -R /sbin/neoinit*'
            cmd3 = 'ln -sfn /sbin/init.sysvinit /sbin/init'     
            cmd4 = 'cp -rf /etc/fstab.org /etc/fstab; rm /etc/fstab.org '
            cmd5 = 'cp -rf /etc/init.d/volatile-media.sh.org /etc/init.d/volatile-media.sh; rm /etc/init.d/volatile-media.sh.org '
            cmd6 = 'opkg install volatile-media; sleep 2; killall -9 enigma2'  
            self.session.open(Console, _('NeoBot was removed !!! \nThe changes will be visible only after complete restart of the receiver.'), [cmd,
             cmd1,
             cmd2,
             cmd3,
             cmd4,
             cmd5,
             cmd6])
            self.close()

class Montowanie(Screen):
    skin = '\n\t<screen position="center,center" size="590,330" title="Devices Panel">\n\t\t<widget source="list" render="Listbox" position="10,16" size="570,300" scrollbarMode="showOnDemand" >\n\t\t\t<convert type="TemplatedMultiContent">\n                \t\t{"template": [\n                    \t\t\tMultiContentEntryText(pos = (50, 1), size = (520, 36), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n                    \t\t\tMultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (36, 36), png = 1),\n                    \t\t\t],\n                    \t\t\t"fonts": [gFont("Regular", 22)],\n                    \t\t\t"itemHeight": 36\n                \t\t}\n            \t\t</convert>\n\t\t</widget>\n        </screen>'
    __module__ = __name__

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/ok.png'
        png = LoadPixmap(mypixmap)
        res = (_('Start the device manager ?'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            if fileExists('/usr/lib/enigma2/python/Plugins/SystemPlugins/DeviceManager*/devicemanager.cfg'):
                system('rm -f /usr/lib/enigma2/python/Plugins/SystemPlugins/DeviceManager*/devicemanager.cfg')
            if fileExists('/etc/devicemanager.cfg'):
                system(' rm -f /etc/devicemanager.cfg')
            cmd = '/media/neoboot/ImageBoot/Backup_NeoBoot.sh '
            from Plugins.Extensions.NeoBoot.files.devices import ManagerDevice
            self.session.open(ManagerDevice)
        else:
            self.session.open(MessageBox, _('The operation has been canceled or meoboot is not running in stb VuPlus'), MessageBox.TYPE_INFO, 7)

class NeoBootInstallation(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = '<screen position="410,138" size="1200,850" title="NeoBoot">\n <widget name="label3" position="10,632" size="1178,114" zPosition="1" halign="center" font="Regular;35" backgroundColor="black" transparent="1" foregroundColor="blue" />\n <ePixmap position="643,282" zPosition="-2" size="531,331" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrix.png" />  <eLabel position="15,76" size="1177,2" backgroundColor="blue" foregroundColor="blue" name="linia" /><eLabel position="10,622" size="1168,3" backgroundColor="blue" foregroundColor="blue" name="linia" /><eLabel position="14,752" size="1168,3" backgroundColor="blue" foregroundColor="blue" name="linia" /><eLabel position="15,276" size="1183,2" backgroundColor="blue" foregroundColor="blue" name="linia" /><widget name="label1" position="14,4" size="1180,62" zPosition="1" halign="center" font="Regular;35" backgroundColor="black" transparent="1" foregroundColor="red" />\n  <widget name="label2" position="15,82" size="1178,190" zPosition="1" halign="center" font="Regular;35" backgroundColor="black" transparent="1" foregroundColor="blue" />\n  <widget name="config" position="15,285" size="641,329" font="Regular; 32" itemHeight="42" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/selektor.png" scrollbarMode="showOnDemand" />\n  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" position="48,812" size="140,28" alphatest="on" />\n  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/greencor.png" position="311,816" size="185,28" alphatest="on" />\n  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/yellowcor.png" position="614,815" size="150,28" alphatest="on" />  \n  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/bluecor.png" position="958,817" size="140,26" alphatest="on" />\n  <widget name="key_red" position="19,760" zPosition="1" size="221,47" font="Regular; 35" halign="center" valign="center" backgroundColor="red" transparent="1" foregroundColor="red" />\n  <widget name="key_green" position="289,761" zPosition="1" size="227,47" font="Regular; 35" halign="center" valign="center" backgroundColor="green" transparent="1" foregroundColor="green" />\n  <widget name="key_yellow" position="583,760" zPosition="1" size="224,51" font="Regular; 35" halign="center" valign="center" backgroundColor="yellow" transparent="1" foregroundColor="yellow" />  \n  <widget name="key_blue" position="856,761" zPosition="1" size="326,52" font="Regular; 35" halign="center" valign="center" backgroundColor="blue" transparent="1" foregroundColor="blue" />\n</screen>'
    else:
        skin = '<screen position="center, center" size="835, 500" title="NeoBoot">         <ePixmap position="0,0" zPosition="-1" size="835,500" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/frame835x500.png"  />   <widget name="label1" position="10,15" size="840,30" zPosition="1" halign="center" font="Regular;25" foregroundColor="red" backgroundColor="black" transparent="1" />\n  <widget name="label2" position="7,100" size="840,296" zPosition="1" halign="center" font="Regular;20" backgroundColor="black" foregroundColor="#58ccff" transparent="1"/>   <widget name="config" position="220,200" size="440,207" backgroundColor="black" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/selektor1.png" scrollbarMode="showOnDemand"  />  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" position="48,406" size="140,40" alphatest="on"    />\n  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/greencor.png" position="246,406" size="140,40" alphatest="on" />\n  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/yellowcor.png" position="474,406" size="150,40" alphatest="on" />  \n  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/bluecor.png" position="675,406" size="140,40" alphatest="on" />\n  <widget name="key_red" position="48,406" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" />\n  <widget name="key_green" position="248,406" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="green" transparent="1" />\n  <widget name="key_yellow" position="474,406" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="yellow" transparent="1" />  \n  <widget name="key_blue" position="672,415" zPosition="1" size="145,45" font="Regular;20" halign="center" valign="center" backgroundColor="blue" transparent="1" />\n  <widget name="label3" position="20,339" size="816,61" zPosition="1" halign="center" font="Regular;24" backgroundColor="black" transparent="1" foregroundColor="#58ccff" /></screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['config'] = MenuList(self.list)
        self['key_red'] = Label(_('Instruction'))
        self['key_green'] = Label(_('Installation'))
        self['key_yellow'] = Label(_('Info disc'))
        self['key_blue'] = Label(_('Device Manager'))
        self['label1'] = Label(_('Welcome to NeoBoot %s Plugin installation.') % PLUGINVERSION)
        self['label3'] = Label(_('WARNING !!! First, mount the device.'))
        self['label2'] = Label(_('Here is the list of mounted devices in Your STB\nPlease choose a device where You would like to install NeoBoot'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'DirectionActions'], {'red': self.Instrukcja,                  
         'green': self.install,
         'yellow': self.datadrive,
         'blue': self.devices, 
         'back': self.close})             
        self.updateList()
                
    def Instrukcja(self):
        self.session.open(MyHelp)

    def datadrive(self):
        try:
            message = "echo -e '\n"
            message += _('NeoBot checks the connected media.\nWAIT ...\n\nDISCS:')
            message += "'"
            cmd = '/sbin/blkid'
            system(cmd)
            print '[MULTI-BOOT]: ', cmd
            self.session.open(Console, _('    NeoBot - Available media:'), [message, cmd])
        except:
            pass

    def updateList(self):
        mycf, myusb, myusb2, myusb3, mysd, myhdd = ('', '', '', '', '', '')
        myoptions = []
        if fileExists('/proc/mounts'):
            fileExists('/proc/mounts')
            f = open('/proc/mounts', 'r')
            for line in f.readlines():
                if line.find('/media/cf') != -1:
                    mycf = '/media/cf/'
                    continue
                if line.find('/media/usb') != -1:
                    myusb = '/media/usb/'
                    continue
                if line.find('/media/usb2') != -1:
                    myusb2 = '/media/usb2/'
                    continue
                if line.find('/media/usb3') != -1:
                    myusb3 = '/media/usb3/'
                    continue
                if line.find('/media/card') != -1:
                    mysd = '/media/card/'
                    continue
                if line.find('/media/ntfs') != -1:
                    mysd = '/media/ntfs/'
                    continue
                if line.find('/hdd') != -1:             
                    myhdd = '/media/hdd/'
                    continue

            f.close()
        else:
            self['label2'].setText(_('Sorry it seems that there are not Linux formatted devices mounted on your STB. To install NeoBoot you need a Linux formatted part1 device. Click on the blue button to open Devices Panel'))
            fileExists('/proc/mounts')
        if mycf:
            self.list.append(mycf)
        else:
            mycf
        if myusb:
            self.list.append(myusb)
        else:
            myusb
        if myusb2:
            self.list.append(myusb2)
        else:
            myusb2
        if myusb3:
            self.list.append(myusb3)
        else:
            myusb3
        if mysd:
            mysd
            self.list.append(mysd)
        else:
            mysd
        if myhdd:
            myhdd
            self.list.append(myhdd)
        else:
            myhdd
        self['config'].setList(self.list)

    def checkReadWriteDir(self, configele):
        from Plugins.Extensions.NeoBoot.files import Harddisk
        import os.path
        import Plugins.Extensions.NeoBoot.files.Harddisk
        supported_filesystems = frozenset(('ext4', 'ext3', 'ext2', 'ntfs', 'nfs', ))
        candidates = []
        mounts = Harddisk.getProcMounts()
        for partition in Harddisk.harddiskmanager.getMountedPartitions(False, mounts):
            if partition.filesystem(mounts) in supported_filesystems:
                candidates.append((partition.description, partition.mountpoint))

        if candidates:
            locations = []
            for validdevice in candidates:
                locations.append(validdevice[1])

            if Harddisk.findMountPoint(os.path.realpath(configele)) + '/' in locations or Harddisk.findMountPoint(os.path.realpath(configele)) in locations:
                if fileExists(configele, 'w'):
                    return True
                else:
                    dir = configele
                    self.session.open(MessageBox, _('The directory %s is not writable.\nMake sure you select a writable directory instead.') % dir, type=MessageBox.TYPE_ERROR)
                    return False
            else:
                dir = configele
                self.session.open(MessageBox, _('The directory %s is not a EXT2, EXT3, EXT4 or NFS partition.\nMake sure you select a valid partition type.') % dir, type=MessageBox.TYPE_ERROR)
                return False
        else:
            dir = configele
            self.session.open(MessageBox, _('The directory %s is not a EXT2, EXT3, EXT4 or NFS partition.\nMake sure you select a valid partition type.') % dir, type=MessageBox.TYPE_ERROR)
            return False

    def devices(self):
        check = False
        if check == False:
            message = _('After selecting OK start Mounting Manager, option Mount - green\n')
            message += _('Do you want to run the manager to mount the drives correctly ?\n')
            ybox = self.session.openWithCallback(self.device2, MessageBox, message, MessageBox.TYPE_YESNO)
            ybox.setTitle(_('Device Manager'))

    def device2(self, yesno):
        if yesno:
            if fileExists('/usr/lib/enigma2/python/Plugins/SystemPlugins/DeviceManager*/devicemanager.cfg'):
                system('rm -f /usr/lib/enigma2/python/Plugins/SystemPlugins/DeviceManager*/devicemanager.cfg')
            if fileExists('/etc/devicemanager.cfg'):
                system(' rm -f /etc/devicemanager.cfg; touch /etc/devicemanager.cfg ')
            from Plugins.Extensions.NeoBoot.files.devices import ManagerDevice
            self.session.open(ManagerDevice)
        else:
            self.close()

    def install(self):
        if not os.path.isfile('/etc/fstab.org'):
            self.session.open(MessageBox, _('NeoBot - First use the Device Manager and mount the drives correctly !!!'), MessageBox.TYPE_INFO, 7)
            self.close()
        else:
            self.first_installation()

    def first_installation(self):
        check = False
        if fileExists('/proc/mounts'):
            fileExists('/proc/mounts')
            f = open('/proc/mounts', 'r')
            for line in f.readlines():
                if line.find('/media/cf') != -1:
                    check = True
                    continue
                if line.find('/media/usb') != -1:
                    check = True
                    continue
                if line.find('/media/usb2') != -1:
                    check = True
                    continue
                if line.find('/media/usb3') != -1:
                    check = True
                    continue
                if line.find('/media/card') != -1:
                    check = True
                    continue
                if line.find('/media/ntfs') != -1:
                    check = True
                    continue
                if line.find('/hdd') != -1:
                    check = True
                    continue

            f.close()
        else:
            fileExists('/proc/mounts')
        if check == False:
            self.session.open(MessageBox, _('Sorry, there is not any connected devices in your STB.\nPlease connect HDD or USB to install NeoBoot!'), MessageBox.TYPE_INFO)
        else:
            if not fileExists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/fstab'):
                self.session.open(MessageBox, _('Device Manager encountered an error, disk drives not installed correctly !!!'), MessageBox.TYPE_INFO)
                self.close()
            fileExists('/boot/dummy')
            self.mysel = self['config'].getCurrent()
            if self.checkReadWriteDir(self.mysel):
                message = _('Do You really want to install NeoBoot in:\n ') + self.mysel + '?'
                ybox = self.session.openWithCallback(self.install2, MessageBox, message, MessageBox.TYPE_YESNO)
                ybox.setTitle(_('Install Confirmation'))
            else:
                self.close()

    def install2(self, yesno):
        if yesno:
            system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; chmod 0755 ./bin/neoini*; chmod 0755 ./ex_init.py; chmod 0755 ./files/targetimage.sh; chmod 0755 ./files/NeoBoot.sh; chmod 0755 ./files/S50fat.sh; cd;')                        
            cmd = 'mkdir /media/neoboot;mount ' + self.mysel + ' /media/neoboot'
            system(cmd)
            cmd2 = 'mkdir ' + self.mysel + 'ImageBoot;mkdir ' + self.mysel + 'ImagesUpload' 
            system(cmd2)
            cmd3 = 'mkdir ' + self.mysel + 'ImageBoot;mkdir ' + self.mysel + 'ImagesUpload/.kernel' 
            system(cmd3)
                                    
            if fileExists('/proc/mounts'):
                fileExists('/proc/mounts')
                f = open('/proc/mounts', 'r')
                for line in f.readlines():
                    if line.find(self.mysel):
                        mntdev = line.split(' ')[0]

                f.close()
                mntid = os.system('blkid -s UUID -o value ' + mntdev + '>/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/install')
                system('chmod 755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/install')

            if os.path.isfile('/etc/init.d/volatile-media.sh'):
                    os.system('mv /etc/init.d/volatile-media.sh /etc/init.d/volatile-media.sh.org')
            if os.path.isfile('/media/neoboot/ImageBoot/.neonextboot'): 
                    os.system('rm -f /media/neoboot/ImageBoot/.neonextboot; rm -f /media/neoboot/ImageBoot/.version; rm -f /media/neoboot/ImageBoot/.Flash; rm -f /media/neoboot/ImagesUpload/.kernel/zImage*.ipk; rm -f /media/neoboot/ImagesUpload/.kernel/zImage*.bin')
                    
            out1 = open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location', 'w')
            out1.write(self.mysel)
            out1.close()
            out2 = open('/media/neoboot/ImageBoot/.neonextboot', 'w')
            out2.write('Flash ')
            out2.close()
            
            if fileExists('/etc/issue.net'):
                try:
                    lines = open('/etc/hostname', 'r').readlines()
                    imagename = lines[0][:-1]
                    image = imagename
                    open('/media/neoboot/ImageBoot/.Flash', 'w').write(image)
                except:
                    False

            out = open('/media/neoboot/ImageBoot/.version', 'w')
            out.write(PLUGINVERSION)
            out.close()
            
            self.installpakiet()

        else:
            self.session.open(MessageBox, _('Installation aborted !'), MessageBox.TYPE_INFO)

    def installpakiet(self):
        check = False
        if check == False:
            self.mysel = self['config'].getCurrent()
            if fileExists('/proc/stb/info'): #vumodel'): ogranicza tylko dla vu+
                message = _('\n ... q(-_-)p ...\nNeoBot to function properly need additional packages.\nSelect Yes and wait ...\nProces installation may take a few moments ...\nInstall ?')
                ybox = self.session.openWithCallback(self.pakiet2, MessageBox, message, MessageBox.TYPE_YESNO)
                ybox.setTitle(_('Installing packages ...'))
            else:
                self.session.open(MessageBox, _('Installation operation canceled. This is not a vuplus box !!!'), MessageBox.TYPE_INFO, 10)

    def pakiet2(self, yesno):
        if yesno:
                try:
                    system('opkg update;opkg configure;sleep 5')                    
                    #VUPLUS ARM 
                    if getCPUSoC() == '7444s' or getCPUSoC() == '7252s' or getCPUSoC() == '7376' or getCPUSoC() == '72604' or getBoxHostName() == 'vuultimo4k' or getBoxHostName() == 'vuuno4k' or getBoxHostName() == 'vusolo4k' or getBoxHostName() == 'vuzero4k' or getBoxHostName() == 'vuuno4kse' :
                        os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/' )
                        os.system('cp -Rf /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinitarm /sbin/neoinitarm')
                        os.system('cp -Rf /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinitarmvu /sbin/neoinitarmvu; cd')  
                        os.system('chmod 755 /sbin/neoinitarm; chmod 755 /sbin/neoinitarmvu')
                        os.system('opkg download kernel-image')
                        os.system('mv /home/root/*.ipk /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk' % getBoxVuModel())                    
                        os.system('dd if=/dev/mmcblk0p1 of=/media/neoboot/ImagesUpload/.kernel/flash-kernel-%s.bin' % getBoxVuModel())
                        os.system('chmod 644 /media/neoboot/ImagesUpload/.kernel/flash-kernel-%s.bin' % getBoxVuModel()) 
      
                    #VUPLUS MIPS                                                                                                                                                                                                                 
                    elif getCPUSoC() == '7335' or getCPUSoC() == '7413' or getCPUSoC() == '7325' or getCPUSoC() == '7356' or getCPUSoC() == 'bcm7356' or getCPUSoC() == '7429' or getCPUSoC() == '7424'  or getCPUSoC() == '7241' or getCPUSoC() == '7405' or getCPUSoC() == '7405(with 3D)' or getBoxHostName() == 'vuultimo' or getCPUSoC() == '7362' or getCPUSoC() == 'bcm7362' or getCPUSoC() == 'bcm7358' or getBoxHostName() == 'mbmini':   

                        if os.system('opkg list-installed | grep mtd-utils') != 0:
                            os.system('opkg install mtd-utils')
                        if os.system('opkg list-installed | grep mtd-utils-ubifs') != 0:                                                                                                                                                                                                                                                                                                                                                
                            os.system('opkg install mtd-utils-ubifs')
                        if os.system('opkg list-installed | grep mtd-utils-jffs2') != 0:
                            os.system('opkg install mtd-utils-jffs2')
                        if os.system('opkg list-installed | grep kernel-module-nandsim') != 0:
                            os.system('opkg install kernel-module-nandsim')
                        if not fileExists('/usr/lib/enigma2/python/Tools/HardwareInfoVu.pyo'):
                            os.system('ln -sfn /usr/lib/enigma2/python/Tools/HardwareInfo.pyo /usr/lib/enigma2/python/Tools/HardwareInfoVu.pyo')
                        if not fileExists('/usr/lib/enigma2/python/Tools/DreamboxHardware.pyo'):
                            os.system('ln -sfn /usr/lib/enigma2/python/Tools/StbHardware.pyo /usr/lib/enigma2/python/Tools/DreamboxHardware.pyo')
                        if not fileExists('/usr/lib/enigma2/python/Tools/DreamboxInfoHandler.pyo'):
                            os.system('ln -sfn /usr/lib/enigma2/python/Components/PackageInfo.pyo /usr/lib/enigma2/python/Tools/DreamboxInfoHandler.pyo')                            

                        os.system('cp -Rf /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinitmips /sbin/neoinitmips; cp -Rf /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinitmipsvu /sbin/neoinitmipsvu') 
                        os.system('chmod 755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/nfidump; chmod 0755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/nanddump; rm -r /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinitar*; cd')
                        os.system('chmod 755 /sbin/neoinitmips; chmod 0755 /sbin/neoinitmipsvu')
   
                        if getCPUSoC() == 'bcm7358' or getCPUSoC() == 'bcm7362' or getCPUSoC() == 'bcm7356' or getCPUSoC() == 'bcm7241' or getCPUSoC() == 'bcm7362' or getBoxHostName() == 'mbmini' or getTunerModel() == 'ini-1000sv':
                            os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; mv ./bin/fontforneoboot.ttf /usr/share/fonts; mv ./bin/libpngneo /usr/lib; cp -f ./bin/neoinitmips /sbin/neoinitmips; chmod 0755 ./bin/neobm; chmod 0755 /usr/lib/libpngneo; cd; chmod 0755 /sbin/neoinitmips; ln -sf /media/neoboot/ImageBoot/.neonextboot /etc/neoimage; rm /sbin/neoinitmips')

                        elif getBoxHostName() == 'bm750' or getBoxHostName() == 'duo' or getBoxHostName() == 'vusolo' or getBoxHostName() == 'vuuno' or getBoxHostName() == 'vuultimo':
                            os.system('cd /media/neoboot/ImagesUpload/.kernel/')
                            os.system('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/nanddump /dev/mtd1 -o -b > vmlinux.gz')
                            os.system('chmod 644 /media/neoboot/ImagesUpload/.kernel/vmlinux.gz; cd')  
                            os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; rm ./bin/neobm; rm ./neologo.mvi; cd')

                        elif getBoxHostName() == 'vusolo2' or getBoxHostName() == 'vuduo2' or getBoxHostName() == 'vusolose' or getBoxHostName() == 'vuzero':
                            os.system('cd /media/neoboot/ImagesUpload/.kernel/')
                            os.system('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/nanddump /dev/mtd2 -o -b > vmlinux.gz')
                            os.system('chmod 644 /media/neoboot/ImagesUpload/.kernel/vmlinux.gz,cd') 
                            os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; rm ./bin/neobm; rm ./neologo.mvi; cd')  
 
                        if fileExists('/tmp/plik.tar.gz'):
                            cmd = 'mkdir -p ' + self.mysel + 'ImagesUpload/.egami'    #private non-public use patch
                            system(cmd)
                            os.system('/bin/tar -xzvf /tmp/plik.tar.gz -C /;rm -fr /tmp/*.tar.gz')                                                                
                        os.system('opkg download kernel-image; sleep 2; mv /home/root/*.ipk /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk' % getBoxVuModel())
                            
                    #OctagonSF4008 DM900
                    elif getCPUSoC() == 'bcm7251' or getBoxHostName() == 'sf4008' or getCPUSoC() == 'BCM97252SSFF' or getBoxHostName() == 'dm900':
                        os.system('cp -f /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinitarm /sbin/neoinitarm; chmod 0755 /sbin/neoinitarm; ln -sfn /sbin/neoinitarm /sbin/init')                             

                    else:
                         self.messagebox = self.session.open(MessageBox, _('Canceled ... NeoBoot will not work properly !!! NeoBoot works only on VuPlus box, Ultimo4k, Solo4k, Uno4k !!!'), MessageBox.TYPE_INFO, 20)

                    os.system('touch /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neobootup.sh') 
                    cel = open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neobootup.sh', 'w')
                    cel.write('#!/bin/sh\n#DESCRIPTION=This script by gutosie\n\ntouch /tmp/.init_reboot\n\nif [ -f /etc/init.d/neobootmount.sh ] ; then\n    sync; rm -f /etc/init.d/neobootmount.sh;  \nfi \n')
                    cel.close()                                                                
                    os.system('chmod 755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neobootup.sh; ln -s /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neobootup.sh /etc/rcS.d/S50neo; touch /etc/name') 
                    cel = open('/etc/name', 'w')
                    cel.write('gutosie')
                    cel.close()
                                                                 
                    if os.system('opkg list-installed | grep python-subprocess') != 0:
                            os.system('opkg install python-subprocess')
                    if os.system('opkg list-installed | grep python-argparse') != 0:
                            os.system('opkg install python-argparse')
                    if os.system('opkg list-installed | grep curl') != 0:
                            os.system('opkg install curl')                           
                    cmd = 'opkg install --force-maintainer --force-reinstall --force-overwrite --force-downgrade kernel-image'
                    system(cmd)
                    os.system('opkg configure update-modules') 
                    
                    if getCPUtype() == 'ARMv7':       
                        os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; rm ./bin/neoinitmip*; rm -r ./bin/nanddump; rm ./bin/nfidump; rm ./bin/neobm; rm ./neologo.mvi; cd')   
                    elif getCPUtype() == 'MIPS':       
                        os.system('rm /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinitar*; rm /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/rebootbot')
                                                                                
                    self.myclose2(_('NeoBoot has been installed succesfully !' ))                                      

                except:
                        pass
        else:
            self.messagebox = self.session.open(MessageBox, _('Cancelled ... NeoBot will not work correctly !!!'), MessageBox.TYPE_INFO, 6)

    def myclose2(self, message):
        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        self.close()

class NeoBootImageChoose(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:

        skin = """
        <screen name="NeoBootImageChoose" position="center,center" size="1920,1080" title=" " flags="wfNoBorder" backgroundColor="transparent">  
        <widget name="progreso" position="590,600" size="530,15" borderWidth="1" zPosition="3" />
        <ePixmap position="-75,0" zPosition="-7" size="1996,1078" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/skin.png" />
        <ePixmap position="54,981" zPosition="-7" size="1809,55" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek.png" />  
        <ePixmap position="71,903" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />  
        <ePixmap position="71,820" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />    
        <ePixmap position="71,736" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />  
        <ePixmap position="70,655" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />             
        <ePixmap position="64,417" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />  
        <ePixmap position="1170,186" size="45,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/updown.png" alphatest="on" />  
        <ePixmap position="587,631" zPosition="-2" size="545,340" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrix.png" />  

        <eLabel position="70,149" size="1080,2" backgroundColor="blue" foregroundColor="blue" name="linia" />  
        <eLabel position="70,392" size="1080,2" backgroundColor="blue" foregroundColor="blue" name="linia2" />   

        <widget name="device_icon" position="123,490" size="146,136" alphatest="on" zPosition="2" />   
        <widget name="key_red" position="149,982" zPosition="1" size="280,48" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />                  
        <widget name="key_green" position="571,984" zPosition="1" size="276,46" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />  
        <widget name="key_yellow" position="1010,984" zPosition="1" size="275,46" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />          
        <widget name="key_blue" position="1470,983" zPosition="1" size="276,46" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="blue" />    
        <widget name="config" position="1183,256" size="659,690" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/selektor.png" font="Regular;32" itemHeight="42" scrollbarMode="showOnDemand" backgroundColor="black" transparent="1" />     
        <widget name="key_menu" position="254,419" zPosition="1" size="249,45" font="Regular;33" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#99FFFF" />  

        <eLabel backgroundColor="black" font="Regular; 35" foregroundColor="red" position="67,54" size="443,55" text=" NeoBoot ARM  -  MENU" transparent="1" />          
        <eLabel backgroundColor="black" font="Regular; 30" foregroundColor="yellow" position="140,424" size="155,41" text="MENU &gt;" transparent="1" />  
        <eLabel backgroundColor="black" font="Regular; 35" foregroundColor="#C0C0C0" position="90,659" size="80,46" text="1 &gt;" transparent="1" />  
        <eLabel backgroundColor="black" font="Regular; 35" foregroundColor="#C0C0C0" position="90,742" size="80,43" text="2 &gt;" transparent="1" />  
        <eLabel backgroundColor="black" font="Regular; 35" foregroundColor="#C0C0C0" position="90,826" size="80,42" text="3 &gt;" transparent="1" />          
        <eLabel backgroundColor="black" font="Regular; 35" foregroundColor="#C0C0C0" position="90,909" size="80,39" text="4 &gt;" transparent="1" />  

        <widget name="key_1" position="150,660" zPosition="1" size="363,46" font="Regular;32" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />          
        <widget name="key_2" position="149,742" zPosition="1" size="431,42" font="Regular;32" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />  
        <widget name="key_3" position="149,826" zPosition="1" size="367,43" font="Regular;32" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />  

        <widget name="label1" position="1179,147" size="661,99" zPosition="1" halign="center" font="Regular;35" foregroundColor="red" backgroundColor="black" transparent="1" />                  
        <widget name="label2" position="69,164" zPosition="1" size="652,66" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />  
        <widget name="label3" position="315,460" zPosition="1" size="799,124" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
        <widget name="label4" position="68,244" zPosition="1" size="606,66" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />  
        <widget name="label5" position="802,163" zPosition="1" size="340,66" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="blue" />         
        <widget name="label6" position="628,235" zPosition="1" size="516,82" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />          
        <widget name="label7" position="836,323" zPosition="1" size="308,66" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />  
        <widget name="label8" position="67,324" zPosition="1" size="666,66" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
        <widget name="label9" position="883,49" zPosition="1" size="970,56" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00FF00" /> 
        <widget name="label10" position="985,410" zPosition="1" size="125,55" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00FF00" />       
        <widget name="label13" position="610,410" zPosition="1" size="415,55" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />  
        <widget name="label14" position="534,51" zPosition="1" size="350,56" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" /> 
        <widget name="label15" position="322,584" zPosition="1" size="265,42" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
        <widget name="label19" position="69,878" zPosition="1" size="513,99" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00FF00" />         
        </screen>"""
    else:
	    skin = '<screen name="NeoBootImageChoose" position="center,center" size="1280, 720" backgroundColor="transpBlack">\n\t\t\t\t\t\t\t <ePixmap position="0,0" zPosition="-1" size="1280,720" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/1frame_base-fs8.png"  />\n\t\t\t\t\t\t\t <widget source="session.VideoPicture" render="Pig" position=" 836,89" size="370,208" zPosition="3" backgroundColor="#ff000000"/>  \n\t\t\t\t\t\t\t        <ePixmap position="870,304" zPosition="-1" size="300,14"  pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/1chan_p1_bar.png" alphatest="on" />\n\t\t\t\t\t\t\t     <widget source="Title" render="Label"  position="0,5" size="800,30" font="Regular;28" halign="left" foregroundColor="#58bcff" backgroundColor="transpBlack" transparent="1"/>     \n\t\t\t\t\t\t\t  <widget name="label9" position="100,45" zPosition="10" size="800,30" font="Regular;24"  foregroundColor="#58bcff" backgroundColor="black" halign="left"  transparent="1" />     <widget name="config"  enableWrapAround="1" position="30,150" size="270,370" itemHeight="25" font="Regular;18" zPosition="2"  selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/1channel_sel.png" foregroundColor="#00cc99" scrollbarMode="showNever" transparent="1" />      <widget name="device_icon" position="530,80" size="146,136" alphatest="on" zPosition="2" />           <widget name="progreso" position="400,200" size="300,10" borderWidth="1" zPosition="3" foregroundColor="white" />        <widget name="label3" position="380,230" zPosition="1" size="450,60" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#58ccff" />    <ePixmap position="300,310" zPosition="4" size="500,4" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/separator.png" alphatest="blend" transparent="1"  />    <widget name="label2" position="310,340" zPosition="1" size="400,22" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />    <widget name="label5" position="630,340" zPosition="1" size="340,22" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#58ccff" />    <widget name="label4" position="310,370" zPosition="1" size="606,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />  <widget name="label6" position="630,370" zPosition="1" size="516,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#58ccff" />        <widget name="label8" position="310,400" zPosition="1" size="466,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />      <widget name="label7" position="660,400" zPosition="1" size="308,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#58ccff" />    <eLabel backgroundColor="black" font="Regular; 20" foregroundColor="#58ccff" position="310,450" size="60,25" text="1 &gt;" transparent="1" />    <eLabel backgroundColor="black" font="Regular; 20" foregroundColor="#58ccff" position="310,480" size="60,25" text="2 &gt;" transparent="1" />    <eLabel backgroundColor="black" font="Regular; 20" foregroundColor="#58ccff" position="310,510" size="60,25" text="3 &gt;" transparent="1" />           <eLabel backgroundColor="black" font="Regular; 20" foregroundColor="#58ccff" position="310,540" size="60,25" text="4 &gt;" transparent="1" />     <widget name="key_1" position="360,450" zPosition="1" size="300,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />               <widget name="key_2" position="360,480" zPosition="1" size="350,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />       <widget name="key_3" position="360,510" zPosition="1" size="300,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />   <widget name="label19" position="360,540" zPosition="1" size="450,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />     <ePixmap position="920,480" zPosition="1" size="228,130" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/1matrix.png" />   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/red25.png" position="0,650" size="250,40" alphatest="blend" />   <widget name="key_red" position="0,670" zPosition="2" size="250,40"  font="Regular; 20" halign="center" backgroundColor="transpBlack" transparent="1" foregroundColor="white" />     <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/green25.png" position="200,650" size="230,36" alphatest="blend" />  <widget name="key_green" position="200,670" size="230,38" zPosition="1" font="Regular; 20"  halign="center" backgroundColor="transpBlack" transparent="1" foregroundColor="white" />   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/yellow25.png" position="400,650" size="230,36" alphatest="blend" />  <widget name="key_yellow" position="400,670" size="230,38" zPosition="1" font="Regular; 20"  halign="center" backgroundColor="transpBlack" transparent="1" foregroundColor="white" />  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/blue25.png" position="600,650" size="230,36" alphatest="blend" />  <widget name="key_blue" position="600,670" size="230,38" zPosition="1" font="Regular; 20" halign="center" backgroundColor="transpBlack" transparent="1" foregroundColor="white" />    <widget name="key_menu" position="950,640" zPosition="1" size="249,45" font="Regular;22" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#58bcff" />   <eLabel backgroundColor="black" font="Regular; 24" foregroundColor="white" position="900,650" size="155,41" text="MENU &gt;" transparent="1" />  <ePixmap position="20,135" zPosition="1" size="280,400" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/border_menu1.png"  /> 	  <widget source="global.CurrentTime" render="Label" position="780,30" size="450,55" font="RegularAA;24" valign="center" halign="center" backgroundColor="transpBlack" foregroundColor="#58bcff"  zPosition="10" transparent="1">     <convert type="ClockToText">Format:%A  %e  %B  %Y </convert>     </widget>  \t\t\t</screen>' 


    def __init__(self, session):
        Screen.__init__(self, session)
        if fileExists('/tmp/.init_reboot'):
            system('rm /tmp/.init_reboot')
         
        if fileExists('/.multinfo') and getCPUtype() == 'ARMv7':
            if os.path.exists('/proc/stb/info/boxtype'):
                if getCPUSoC() == 'bcm7251' or getBoxHostName == 'sf4008':   
                    os.system('mkdir -p /media/mmc; mount /dev/mmcblk0p4 /media/mmc')  

            if os.path.exists('/proc/stb/info/model'):
                if getTunerModel() == 'dm900' or getCPUSoC() == 'BCM97252SSFF':   
                    os.system('mkdir -p /media/mmc; mount /dev/mmcblk0p2 /media/mmc')
                    
            if  getBoxVuModel() == 'uno4k' or getBoxVuModel() == 'uno4kse' or  getBoxVuModel() == 'ultimo4k' or  getBoxVuModel() == 'solo4k':
                    os.system('mkdir -p /media/mmc; mount /dev/mmcblk0p4 /media/mmc')

            if  getBoxVuModel() == 'zero4k':
                    os.system('mkdir -p /media/mmc; mount /dev/mmcblk0p7 /media/mmc')


        self.list = []
        self.setTitle('         NeoBoot  %s  - Menu' % PLUGINVERSION + '          ' + 'Ver. update:  %s' % UPDATEVERSION)
        self['device_icon'] = Pixmap()
        self['progreso'] = ProgressBar()
        self['linea'] = ProgressBar()
        self['config'] = MenuList(self.list)
        self['key_red'] = Label(_('Boot Image'))
        self['key_green'] = Label(_('Installation'))
        self['key_yellow'] = Label(_('Remove Image '))
        self['key_blue'] = Label(_('Info'))
        self['key_menu'] = Label(_('More options'))
        self['key_1'] = Label(_('Update NeoBot'))
        self['key_2'] = Label(_('Backup image'))
        self['key_3'] = Label(_('Install Kernel'))
        self['label1'] = Label(_('Please choose an image to boot'))
        self['label2'] = Label(_('NeoBoot is running from:'))
        self['label3'] = Label('')
        self['label4'] = Label(_('NeoBoot is running image:'))
        self['label5'] = Label('')
        self['label6'] = Label('')
        self['label7'] = Label('')
        self['label8'] = Label(_('Number of images installed:'))
        self['label19'] = Label('')         
        self['label9'] = Label('')
        self['label10'] = Label('')
        self['label11'] = Label('')
        self['label12'] = Label('')
        self['label13'] = Label(_('Version update: '))
        self['label14'] = Label(_('NeoBoot version: '))
        self['label15'] = Label(_('Memory disc:'))
        self['actions'] = ActionMap(['WizardActions',
         'ColorActions',
         'MenuActions',
         'NumberActionMap',
         'SetupActions',
         'number'], {'ok': self.boot,
         'red': self.boot,
         'green': self.ImageInstall,
         'yellow': self.remove,
         'blue': self.pomoc,
         'ok': self.boot,
         'menu': self.mytools,
         '1': self.neoboot_update,
         '2': self.MBBackup,
         '3': self.ReinstallKernel,
         'back': self.close_exit})
        if not fileExists('/etc/name'):
            os.system('touch /etc/name')
        self.onShow.append(self.updateList)

    def pomoc(self):
        if fileExists('/.multinfo'):
            mess = _('Information available only when running Flash.')
            self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)
        else:
            self.session.open(Opis)

    def MBBackup(self):
        from Plugins.Extensions.NeoBoot.files.tools import MBBackup
        self.session.open(MBBackup)

    def deviceneoboot(self):
        self.session.open(Montowanie)

    def close_exit(self):
        if fileExists('/.multinfo'):            
            with open('/media/neoboot/ImageBoot/.neonextboot', 'r') as f:
                imagefile = f.readline().strip()
                f.close()
                out = open('/media/neoboot/ImageBoot/.neonextboot', 'w')
                out.write(imagefile)
                out.close()
        else:
            system('touch /tmp/.init_reboot')
            out = open('/media/neoboot/ImageBoot/.neonextboot', 'w')
            out.write('Flash')
            out.close()
        self.close()
                        
    def ReinstallKernel(self):
        from Plugins.Extensions.NeoBoot.files.tools import ReinstallKernel
        self.session.open(ReinstallKernel)

    def neoboot_update(self):
        if fileExists('/.multinfo'):
            mess = _('Downloading available only from the image Flash.')
            self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)
        else:
            out = open('/media/neoboot/ImageBoot/.neonextboot', 'w')
            out.write('Flash')
            out.close()
            message = _('\n\n\n')
            message += _('WARNING !: The update brings with it the risk of errors.\n')
            message += _('Before upgrading it is recommended that you make a backup NeoBoot.\n')
            message += _('Do you want to run the update now ?\n')
            message += _('\n')
            ybox = self.session.openWithCallback(self.chackupdate2, MessageBox, message, MessageBox.TYPE_YESNO)
            ybox.setTitle(_('The download neoboot update.'))

    def chackupdate2(self, yesno):
        if yesno:
            self.chackupdate3()
        else:
            self.session.open(MessageBox, _('Canceled update.'), MessageBox.TYPE_INFO, 7)
                                           
    def chackupdate3(self):
        os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot;curl -O --ftp-ssl https://raw.githubusercontent.com/gutosie/neoboot/master/ver.txt;sleep 3;cd /')            
        if not fileExists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ver.txt'):
            os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot;fullwget --no-check-certificate https://raw.githubusercontent.com/gutosie/neoboot/master/ver.txt; sleep 3;cd /')
            if not fileExists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ver.txt'):
                self.session.open(MessageBox, _('Unfortunately, at the moment not found an update, try again later.'), MessageBox.TYPE_INFO, 8)
        else:
            mypath = ''
            version = open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ver.txt', 'r')
            mypath = float(version.read().strip())
            version.close()
            if float(UPDATEVERSION) != mypath:
                message = _('NeoBoot has detected update.\nDo you want to update NeoBoota now ?')
                ybox = self.session.openWithCallback(self.aktualizacjamboot, MessageBox, message, MessageBox.TYPE_YESNO)
                ybox.setTitle(_('Updating ... '))
            elif fileExists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ver.txt'):
                os.system('rm /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ver.txt')
                self.session.open(MessageBox, _('Updated unnecessary, you have the latest version. Please try again later.'), MessageBox.TYPE_INFO)

    def aktualizacjamboot(self, yesno):
        if yesno:
            if fileExists('/tmp/*.zip'):
                os.system('rm /tmp/*.zip')
            os.system('cd /tmp; curl -O --ftp-ssl https://codeload.github.com/gutosie/neoboot/zip/master; mv /tmp/master /tmp/neoboot.zip; cd /')
            if not fileExists('/tmp/neoboot.zip'):
                    os.system('cd /tmp;fullwget --no-check-certificate https://codeload.github.com/gutosie/neoboot/zip/master; mv /tmp/master /tmp/neoboot.zip; sleep 3;cd ')
                    if not fileExists('/tmp/neoboot.zip'):
                        self.session.open(MessageBox, _('Unfortunately, at the moment not found an update, try again later.'), MessageBox.TYPE_INFO, 8)
            else:
                os.system('cd /tmp/; unzip -qn ./neoboot.zip; rm -f ./neoboot.zip; cp -rf ./neoboot-master/NeoBoot /usr/lib/enigma2/python/Plugins/Extensions; rm -rf /tmp/neoboot-master;  rm /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ver.txt; cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; chmod 0755 ./bin/neoini*;  chmod 0755 ./ex_init.py; chmod 0755 ./files/targetimage.sh; chmod 0755 ./files/NeoBoot.sh; chmod 0755 ./files/S50fat.sh; cd')                    
                if getCPUtype() == 'MIPS':
                    os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; cp -rf ./bin/neoinitmipsvu /sbin; chmod 755 /sbin/neoinitmipsvu')                    
                elif getCPUtype() == 'ARMv7':
                    os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; chmod 755 ./files/neobootup.sh; chmod 0755 ./bin/rebootbot; cp -rf ./bin/neoinitarm /sbin; cp -rf ./bin/neoinitarmvu /sbin; chmod 755 /sbin/neoinitarm; chmod 755 /sbin/neoinitarmvu; cd')                                                                

                restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('Completed update NeoBoot. You need to restart the E2 !!!\nRestart now ?'), MessageBox.TYPE_YESNO)
                restartbox.setTitle(_('Restart GUI now ?'))

        else:
            os.system('rm -f /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ver.txt')
            self.session.open(MessageBox, _('The update has been canceled.'), MessageBox.TYPE_INFO, 8)

    def restartGUI(self, answer):
        if answer is True:
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close()

    def installMedia(self):
        images = False
        myimages = os.listdir('/media/neoboot/ImagesUpload')
        print myimages
        for fil in myimages:
            if fil.endswith('.zip'):
                images = True
                break
            if fil.endswith('.tar.xz'):
                images = True
                break
            if fil.endswith('.nfi'):
                images = True
                break                
            else:
                images = False
                
        if images == True:
            self.ImageInstall()
        else:
            mess = _('[NeoBoot] The /media/neoboot/ImagesUpload directory is EMPTY !!!\nPlease upload the image files in .ZIP or .NFI formats to install.')
            self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)

    def MBBackup(self):
        from Plugins.Extensions.NeoBoot.files.tools import MBBackup
        self.session.open(MBBackup)

    def MBRestore(self):
        from Plugins.Extensions.NeoBoot.files.tools import MBRestore
        self.session.open(MBRestore)

    def updateList(self):
        if not fileExists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location'):
            self.session.open(NeoBootInstallation)
        else:
            self.updateListOK()

    def updateListOK(self):
        self.list = []
        pluginpath = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot'
        f = open(pluginpath + '/.location', 'r')
        mypath = f.readline().strip()
        f.close()
        icon = 'dev_usb.png'
        if 'card' in mypath or 'sd' in mypath:
            icon = 'dev_sd.png'
        elif 'ntfs' in mypath:
            icon = 'dev_sd.png'
        elif 'hdd' in mypath:
            icon = 'dev_hdd.png'
        elif 'cf' in mypath:
            icon = 'dev_cf.png'
        icon = pluginpath + '/images/' + icon
        png = LoadPixmap(icon)
        self['device_icon'].instance.setPixmap(png)
        device = '/media/neoboot'
        ustot = usfree = usperc = ''
        rc = system('df > /tmp/memoryinfo.tmp')
        if fileExists('/tmp/memoryinfo.tmp'):
            f = open('/tmp/memoryinfo.tmp', 'r')
            for line in f.readlines():
                line = line.replace('part1', ' ')
                parts = line.strip().split()
                totsp = len(parts) - 1
                if parts[totsp] == device:
                    if totsp == 5:
                        ustot = parts[1]
                        usfree = parts[3]
                        usperc = parts[4]
                    else:
                        ustot = 'N/A   '
                        usfree = parts[2]
                        usperc = parts[3]
                    break

            f.close()
            os.remove('/tmp/memoryinfo.tmp')
        if not fileExists('/usr/lib/enigma2/python/Plugins/Extensions/PowerboardCenter/PBDeviceManager.pyo'):
            perc = int(usperc[0:-1])
            self['progreso'].setValue(perc)
            green = '#00389416'
            red = '#00ff2525'
            yellow = '#00ffe875'
            orange = '#00ff7f50'
            if perc < 30:
                color = green
            elif perc < 60:
                color = yellow
            elif perc < 80:
                color = orange
            else:
                color = red
        elif fileExists('/usr/lib/enigma2/python/Plugins/Extensions/PowerboardCenter/PBDeviceManager.pyo'):
            perc2 = usperc[0:-1]
            self['progreso'].setValue(perc2)
            green = '#00389416'
            red = '#00ff2525'
            yellow = '#00ffe875'
            orange = '#00ff7f50'
            if perc2 < 30:
                color = green
            elif perc2 < 60:
                color = yellow
            elif perc2 < 80:
                color = orange
            else:
                color = red
        try:
            from skin import parseColor
            self['label13'].instance.setForegroundColor(parseColor(color))
            self['label14'].instance.setForegroundColor(parseColor(color))
            self['label15'].instance.setForegroundColor(parseColor(color))
            self['progreso'].instance.setForegroundColor(parseColor(color))
        except:
            pass

        self.availablespace = usfree[0:-3]
        strview = _('Used: ') + usperc + _('   \n   Available: ') + usfree[0:-3] + ' MB'
        self['label3'].setText(strview)
        try:
            f2 = open('/media/neoboot/ImageBoot/.neonextboot', 'r')
            mypath2 = f2.readline().strip()
            f2.close()
        except:
            mypath2 = 'Flash'

        if mypath2 == 'Flash':
            image = getImageNeoBoot()
            if not fileExists('/.multinfo'):
                if fileExists('/etc/issue.net'):
                    try:
                        obraz = open('/etc/issue.net', 'r').readlines()
                        imagetype = obraz[0][:-3]
                        image = imagetype
                        open('/media/neoboot/ImageBoot/.Flash', 'w').write(image)
                    except:
                        False
            if fileExists('/.multinfo'):
                if fileExists('/media/mmc/etc/issue.net'):
                    try:
                        obraz = open('/media/mmc/etc/issue.net', 'r').readlines()
                        imagetype = obraz[0][:-3]
                        image = imagetype
                        open('/media/neoboot/ImageBoot/.Flash', 'w').write(image)
                    except:
                        False
                elif fileExists('/etc/issue.net'):
                    try:
                        obraz = open('/etc/issue.net', 'r').readlines()
                        imagetype = obraz[0][:-1]
                        lines = open('/etc/hostname', 'r').readlines()
                        boxtype = lines[0][:-1]
                        image = imagetype[0:-2] + ' ' + boxtype
                        open('/media/neoboot/ImageBoot/.Flash', 'w').write(image)
                    except:
                        False

        elif fileExists('/media/neoboot/ImageBoot/.Flash'):
            f = open('/media/neoboot/ImageBoot/.Flash', 'r')
            image = f.readline().strip()
            f.close()
        image = ' [' + image + ']'
        self.list.append('Flash' + image)
        self['label5'].setText(mypath)
        if fileExists('/.multinfo'):
            f2 = open('/.multinfo', 'r')
            mypath3 = f2.readline().strip()
            f2.close()
            self['label6'].setText(mypath3)
        else:
            f2 = open('/media/neoboot/ImageBoot/.neonextboot', 'r')
            mypath3 = f2.readline().strip()
            f2.close()
            self['label6'].setText(mypath3)
        mypath = '/media/neoboot/ImageBoot'
        myimages = listdir(mypath)
        for fil in myimages:
            if os.path.isdir(os.path.join(mypath, fil)):
                self.list.append(fil)

        self['label7'].setText(str(len(self.list) - 1))
        self['config'].setList(self.list)
        KERNELVERSION = getKernelImageVersion()      
        strview = PLUGINVERSION + '             ' + 'Kernel %s' % KERNELVERSION
        self['label9'].setText(strview)
        self['label19'].setText(readline('/media/neoboot/ImagesUpload/.kernel/used_flash_kernel'))
        strview = UPDATEVERSION
        self['label10'].setText(strview)

    def mytools(self):
        from Plugins.Extensions.NeoBoot.files.tools import MBTools
        self.session.open(MBTools)

    def remove(self):
        self.mysel = self['config'].getCurrent()
        if 'Flash' in self.mysel:
            self.mysel = 'Flash'
        if self.mysel:
            f = open('/media/neoboot/ImageBoot/.neonextboot', 'r')
            mypath = f.readline().strip()
            f.close()
            try:
                if fileExists('/.multinfo'):
                     self.session.open(MessageBox, _('Sorry you can delete only from the image Flash.'), MessageBox.TYPE_INFO, 5)
                elif self.mysel == 'Flash':
                    self.session.open(MessageBox, _('Sorry you cannot delete Flash image'), MessageBox.TYPE_INFO, 5)
                elif mypath == self.mysel:
                    self.session.open(MessageBox, _('Sorry you cannot delete the image currently booted from.'), MessageBox.TYPE_INFO, 5)
                else:
                    out = open('/media/neoboot/ImageBoot/.neonextboot', 'w')
                    out.write('Flash')
                    out.close()
                    message = _('Delete the selected image - ') + self.mysel + _('\nDelete ?')
                    ybox = self.session.openWithCallback(self.remove2, MessageBox, message, MessageBox.TYPE_YESNO)
                    ybox.setTitle(_('Delete Confirmation'))
            except:
                print 'no image to remove'

        else:
            self.mysel

    def up(self):
        self.list = []
        self['config'].setList(self.list)
        self.updateList()

    def up2(self):
        try:
            self.list = []
            self['config'].setList(self.list)
            self.updateList()
        except:
            print ' '

    def remove2(self, yesno):
        if yesno:
            cmd = _("echo -e 'Deleting in progress...\n'")
            cmd1 = 'rm -r /media/neoboot/ImageBoot/' + self.mysel
            self.session.openWithCallback(self.up, Console, _('NeoBoot: Deleting Image'), [cmd, cmd1])
        else:
            self.session.open(MessageBox, _('Removing canceled!'), MessageBox.TYPE_INFO)

    def ImageInstall(self):
        if not fileExists('/.multinfo'):
            KERNEL_VERSION = getKernelVersionString()        
            if getCPUSoC() == 'bcm7251' or getBoxHostName() == 'sf4008' or getBoxHostName() == 'dm900' or getCPUSoC() == 'BCM97252SSFF' or getCPUSoC() == 'BCM97252SSFF' or getCPUSoC() == '7444s' or getCPUSoC() == '7252s' or getCPUSoC() == '7376' or getCPUSoC() == '72604' or getCPUSoC() == '7335' or getCPUSoC() == '7413' or getCPUSoC() == '7325' or getCPUSoC() == '7356' or getCPUSoC() == 'bcm7356' or getCPUSoC() == '7429' or getCPUSoC() == '7424' or getCPUSoC() == '7362' or getCPUSoC() == 'bcm7362' or getCPUSoC() == 'bcm7358' or getCPUSoC() == '7405' or getCPUSoC() == '7405(with 3D)' or getBoxHostName() == 'vuultimo' or getBoxHostName() == 'mbmini':                   
                self.extractImage()                
            else:
                self.messagebox = self.session.open(MessageBox, _('Nie wykryto odpowiedniego STB do instalacji !!!!'), MessageBox.TYPE_INFO, 8)
                self.close()
        else:
                self.messagebox = self.session.open(MessageBox, _('Instalacja tylko z poziomu systemu flash.'), MessageBox.TYPE_INFO, 8)
                self.close()

    def extractImage(self):
        images = False
        if fileExists('/media/neoboot/ImageBoot/.without_copying'):
            system('rm /media/neoboot/ImageBoot/.without_copying')
            
        if not os.path.exists('/media/neoboot/ImagesUpload'):
            system('mkdir /media/neoboot/ImagesUpload')                                                                      
        myimages = listdir('/media/neoboot/ImagesUpload')
        print myimages
        for fil in myimages:
            if fil.endswith('.zip'):
                images = True
                break
            if fil.endswith('.tar.xz'):
                images = True
                break
            if fil.endswith('.nfi'):
                images = True
                break                
            else:
                images = False

        if images == True:
            self.session.openWithCallback(self.up2, InstalacjaImage)
        else:
            self.ImageSystem()

    def ImageSystem(self):
        if fileExists('/media/neoboot/ImageBoot/.neonextboot'):
                self.messagebox = self.session.open(MessageBox, _('[NeoBoot] The /media/neoboot/ImagesUpload directory is EMPTY !!!\nPlease upload the image files in .ZIP or .NFI formats to install.\n'), MessageBox.TYPE_INFO, 8)
                self.close()  
        else:
            self.close()

    def boot(self):
        self.mysel = self['config'].getCurrent()
        if 'Flash' in self.mysel:
            self.mysel = 'Flash'
        if self.mysel:
            out = open('/media/neoboot/ImageBoot/.neonextboot', 'w')
            out.write(self.mysel)
            out.close()
        self.session.open(UruchamianieImage)

    def myClose(self, message):
        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        self.close()

class UruchamianieImage(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = '<screen position="center, center" size="1241, 850" title="NeoBoot">\n\t\t\t<ePixmap position="491, 673" zPosition="-2" size="365, 160" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrixhd.png" /> <widget source="list" render="Listbox" position="20, 171" size="1194, 290" scrollbarMode="showOnDemand">\n\t\t\t\t<convert type="TemplatedMultiContent">\n                \t\t{"template": [\n                    \t\t\tMultiContentEntryText(pos = (90, 1), size = (920, 66), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n                    \t\t\tMultiContentEntryPixmapAlphaTest(pos = (8, 4), size = (66, 66), png = 1),\n                    \t\t\t],\n                    \t\t\t"fonts": [gFont("Regular", 40)],\n                    \t\t\t"itemHeight": 66\n                \t\t}\n            \t\t</convert>\n\t\t</widget>\n         <widget name="label1" position="21, 29" zPosition="1" size="1184, 116" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />\n\t\t        <widget name="label2" position="22, 480" zPosition="-2" size="1205, 168" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />\n\t\t        </screen>'
    else:
        skin = '<screen position="center, center" size="835, 500" title="NeoBoot">\n\t\t\t           <ePixmap position="0,0" zPosition="-1" size="835,500" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/frame835x500.png"  />                <widget source="list" render="Listbox" position="16, 150" size="800, 40"    selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/listselection800x35.png"             scrollbarMode="showOnDemand">\n\t\t\t\t<convert type="TemplatedMultiContent">\n                \t\t{"template": [\n                    \t\t\tMultiContentEntryText(pos = (180, 0), size = (520, 36), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n                    \t\t\tMultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (36, 36), png = 1),\n                    \t\t\t],\n                    \t\t\t"fonts": [gFont("Regular", 22)],\n                    \t\t\t"itemHeight": 35\n               \t\t}\n            \t\t</convert>\n\t\t</widget>\n<widget name="label1" font="Regular; 26" position="15, 70" size="803, 58" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00cc99" /> <widget name="label2" position="40, 232" zPosition="2" size="806, 294" font="Regular;25" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00cc99" />\n\t\t        </screen>'

    __module__ = __name__
    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.select()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.close})
        self['label1'] = Label(_('Start the chosen system now ?'))
        self['label2'] = Label(_('Select OK to run the image.'))
        
    def select(self):
        self.list = []
        mypath = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot'
        if not fileExists(mypath + 'icons'):
            mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/ok.png'
        png = LoadPixmap(mypixmap)
        res = (_('OK Start image...'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):                              
        system('sync; echo 3 > /proc/sys/vm/drop_caches; chmod 755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/targetimage.sh')               
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:          
            if fileExists('/media/mmc/etc/init.d/neobootmount.sh'):
                os.system('rm -f /media/mmc/etc/init.d/neobootmount.sh;')

            #Octagon SF4008
            if getCPUSoC() == 'bcm7251' or getBoxHostName() == 'sf4008' or getCPUSoC() == 'BCM97252SSFF' or getBoxHostName() == 'dm900':
                        if getImageNeoBoot() == 'Flash':                    
                            if fileExists('/.multinfo'):   
                                os.system('cd /media/mmc; ln -sfn /sbin/init.sysvinit /media/mmc/sbin/init; /etc/init.d/reboot')                 
                            elif not fileExists('/.multinfo'): 
                                cmd3='ln -sfn /sbin/init.sysvinit /sbin/init; /etc/init.d/reboot'
                                
                        elif getImageNeoBoot() != 'Flash':                     
                                    cmd3='ln -sfn /sbin/neoinitarm /sbin/init; /etc/init.d/reboot'                                                          

                        else:
                            os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że multiboot nie wspiera tego modelu STB !!! '), MessageBox.TYPE_INFO, 8)
                            self.close()

                        self.session.open(Console, _('NeoBoot Arm....'), [cmd3])                            

            #MiracleBox, ET8500, Formuler F1, Formuler F3, Atemio6000 - MIPS    
            elif getCPUtype() != 'ARMv7' and getCPUSoC() == 'bcm7358' or getCPUSoC() == 'bcm7362' or getCPUSoC() == 'bcm7356' or getCPUSoC() == 'bcm7241' or getCPUSoC() == 'bcm7362' or getBoxHostName() == 'mbmini' or getTunerModel() == 'ini-1000sv':

                        if fileExists('/.multinfo') and getImageNeoBoot() == 'Flash':   
                                cmd0='/etc/init.d/reboot'            
                        elif not fileExists('/.multinfo') and getImageNeoBoot() == 'Flash': 
                                cmd0='ln -sfn /sbin/init.sysvinit /sbin/init; /etc/init.d/reboot'
                        elif fileExists('/.multinfo') and getImageNeoBoot() != 'Flash':   
                                cmd0='/etc/init.d/reboot'                                                                                             
                        elif not fileExists('/.multinfo') and getImageNeoBoot() != 'Flash':                      
                                cmd0='ln -sfn /sbin/neoinitmips /sbin/init; /etc/init.d/reboot'  

                        else:
                            os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że model STB nie jest wpierany przez NeoBOOT !!! '), MessageBox.TYPE_INFO, 8)
                            self.close()

                        self.session.open(Console, _('NeoBoot Arm....'), [cmd0])

            #VUPLUS ARM                                                        
            elif getCPUSoC() == '7444s' or getCPUSoC() == '7252s' or getCPUSoC() == '7376' or getCPUSoC() == '72604' or getBoxHostName() == 'vuultimo4k' or getBoxHostName() == 'vuuno4k' or getBoxHostName() == 'vusolo4k' or getBoxHostName() == 'vuzero4k' or getBoxHostName() == 'vuuno4kse' :
                        if getImageNeoBoot() == 'Flash':                                               
                            if fileExists('/.multinfo'):
                                cmd='cd /media/mmc; ln -sfn /sbin/init.sysvinit /media/mmc/sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/targetimage.sh -i start'                  
                            elif not fileExists('/.multinfo'):   
                                cmd='ln -sfn /sbin/init.sysvinit /sbin/init; /etc/init.d/reboot'                                                            

                        elif getImageNeoBoot() != 'Flash':                                                 
                            if not fileExists('/.multinfo'):  
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):   
                                    cmd='ln -sfn /sbin/neoinitarm /sbin/init; /etc/init.d/reboot'
                                           
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):     
                                    cmd='ln -sfn /sbin/neoinitarmvu /sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/targetimage.sh -i start'                   

                            elif fileExists('/.multinfo'):    
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd='opkg install --force-maintainer --force-reinstall --force-overwrite --force-downgrade /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk; cd /media/mmc; ln -sf /sbin/neoinitarm /media/mmc/sbin/init; /etc/init.d/reboot' %  getBoxVuModel()

                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/zImage.%s' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd='cd /media/mmc; ln -sfn /sbin/neoinitarmvu /media/mmc/sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/targetimage.sh -i start'                                                                                      
                        else:
                            os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że Twój model STB nie jest wpierany!!! '), MessageBox.TYPE_INFO, 8)
                            self.close()

                        self.session.open(Console, _('NeoBoot Arm....'), [cmd]) 

            #VUPLUS MIPS  mtd2            
            elif getCPUSoC() == '7356' or getCPUSoC() == '7429' or getCPUSoC() == '7424'  or getCPUSoC() == '7241' or getCPUSoC() == '7362' or getBoxHostName() == 'vusolo2' or getBoxHostName() == 'vusolose'  or getBoxHostName() == 'vuduo2' or getBoxHostName() == 'vuzero':
                        if getImageNeoBoot() == 'Flash':                    
                            if fileExists('/.multinfo'):  
                                cmd2='/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/targetimage.sh -i start'                  
                            elif not fileExists('/.multinfo'):  
                                cmd2='ln -sfn /sbin/init.sysvinit /sbin/init; /etc/init.d/reboot'
                                      
                        elif getImageNeoBoot() != 'Flash':                    
                            if not fileExists('/.multinfo'):                        
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd2='ln -sfn /sbin/neoinitmips /sbin/init; /etc/init.d/reboot'                                                                                                     
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):                                              
                                    cmd2='ln -sfn /sbin/neoinitmipsvu /sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/targetimage.sh -i start'               

                            elif fileExists('/.multinfo'):    
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd2='opkg install --force-reinstall --force-overwrite --force-downgrade /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk; /etc/init.d/reboot' % getBoxVuModel()   
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd2='/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/targetimage.sh -i start'

                        else:
                            os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że model STB nie jest wpierany przez multiboota!!! '), MessageBox.TYPE_INFO, 8)
                            self.close()

                        self.session.open(Console, _('NeoBoot Arm....'), [cmd2])
                        self.close()

            #VUPLUS MIPS mtd1              
            elif getCPUSoC() == '7335'  or getCPUSoC() == '7325' or getCPUSoC() == '7405' or getCPUSoC() == '7405(with 3D)' or getBoxHostName() == 'vuultimo' or getBoxHostName() == 'bm750' or getBoxHostName() == 'duo' or getBoxHostName() == 'vuuno' or getBoxHostName() == 'vusolo' or getBoxHostName() == 'vuduo':                              
                        if getImageNeoBoot() == 'Flash':                    
                            if fileExists('/.multinfo'):   
                                cmd1='/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/targetimage.sh -i start'                 
                            elif not fileExists('/.multinfo'):   
                                cmd1='ln -sfn /sbin/init.sysvinit /sbin/init; /etc/init.d/reboot'
                                        
                        elif getImageNeoBoot() != 'Flash':                    
                            if not fileExists('/.multinfo'):                        
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd1='ln -sfn /sbin/neoinitmips /sbin/init; /etc/init.d/reboot'                                                                 
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd1='ln -sfn /sbin/neoinitmipsvu /sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/targetimage.sh -i start'                  
                            elif fileExists('/.multinfo'):   
                                if not fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd1='opkg install --force-reinstall --force-overwrite --force-downgrade /media/neoboot/ImagesUpload/.kernel/zImage.%s.ipk; /etc/init.d/reboot' % getBoxVuModel()
                                elif fileExists('/media/neoboot/ImageBoot/%s/boot/%s.vmlinux.gz' % ( getImageNeoBoot(),  getBoxVuModel())):
                                    cmd1='/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/targetimage.sh -i start'
                        else:
                            os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że model STB nie jest wpierany!!! '), MessageBox.TYPE_INFO, 8)
                            self.close()

                        self.session.open(Console, _('NeoBoot Arm....'), [cmd1])
                        self.close()

            else:
                os.system('echo "Flash "  >> /media/neoboot/ImageBoot/.neonextboot')
                self.messagebox = self.session.open(MessageBox, _('Wygląda na to że model STB nie jest wpierany przez NEOBOOT !!! '), MessageBox.TYPE_INFO, 8)
                self.close()           
                
                
class InstalacjaImage(Screen, ConfigListScreen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = '<screen position="82,105" size="1650,875" title="NeoBoot - Installation">\n\t\t   <eLabel position="41,107" size="1541,2" backgroundColor="blue" foregroundColor="blue" name="linia" />  <eLabel position="40,744" size="1545,2" backgroundColor="blue" foregroundColor="blue" name="linia" />  <eLabel text="NeoBoot opcje dla instalowanego obrazu" font="Regular; 38" position="40,24" size="1538,74" halign="center" foregroundColor="red" backgroundColor="black" transparent="1" />\n\t\t  <widget name="config" position="38,134" size="1547,593" font="Regular; 32" itemHeight="42" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/selektor.png" scrollbarMode="showOnDemand" transparent="1" backgroundColor="transpBlack" />\n\t\t  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" position="84,820" size="178,28" alphatest="on" />\n\t\t  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/greencor.png" position="457,820" size="178,29" alphatest="on" />\n\t\t  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/yellowcor.png" position="884,823" size="169,28" alphatest="on" />\n\t\t  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/bluecor.png" position="1288,821" size="167,29" alphatest="on" />\n\t\t  <widget name="HelpWindow" position="330,310" zPosition="5" size="1,1" transparent="1" alphatest="on" />\n\t\t  <widget name="key_red" position="36,762" zPosition="1" size="284,53" font="Regular; 35" halign="center" valign="center" backgroundColor="#FF0000" transparent="1" foregroundColor="red" />\n\t\t  <widget name="key_green" position="403,760" zPosition="1" size="293,55" font="Regular; 35" halign="center" valign="center" backgroundColor="#00FF00" transparent="1" foregroundColor="green" />\n\t\t  <widget name="key_yellow" position="816,761" zPosition="1" size="295,54" font="Regular; 35" halign="center" valign="center" backgroundColor="#FFFF00" transparent="1" foregroundColor="yellow" />\n\t\t   <widget name="key_blue" position="1233,760" zPosition="1" size="272,56" font="Regular; 35" halign="center" valign="center" backgroundColor="#0000FF" transparent="1" foregroundColor="blue" />\n\t\t   </screen>'
    else:
          skin = '<screen position="0,0" size="1280,720" title="NeoBoot - Installation">\n\t\t   <ePixmap position="0,0" zPosition="-1" size="1280,720" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/1frame_base-fs8.png"  />    <eLabel text="NeoBoot opcje dla instalowanego obrazu" font="Regular; 28" position="10,30" size="700,30" halign="center" foregroundColor="#58ccff" backgroundColor="black" transparent="1" />\n\t\t  <widget name="config" position="0,150" size="780,450" font="Regular; 22" itemHeight="32" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/listselection700x32-fs8.png" scrollbarMode="showOnDemand" transparent="1" backgroundColor="transpBlack" />\n\t\t  <widget name="HelpWindow" position="100,500" zPosition="5" size="1,1" transparent="1" alphatest="on" />  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/red25.png" position="0,650" size="250,40" alphatest="blend" />   <widget name="key_red" position="0,670" zPosition="2" size="250,40"  font="Regular; 20" halign="center" backgroundColor="transpBlack" transparent="1" foregroundColor="white" />     <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/green25.png" position="200,650" size="230,36" alphatest="blend" />  <widget name="key_green" position="200,670" size="230,38" zPosition="1" font="Regular; 20"  halign="center" backgroundColor="transpBlack" transparent="1" foregroundColor="white" />   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/yellow25.png" position="400,650" size="230,36" alphatest="blend" />  <widget name="key_yellow" position="400,670" size="230,38" zPosition="1" font="Regular; 20"  halign="center" backgroundColor="transpBlack" transparent="1" foregroundColor="white" />  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/blue25.png" position="600,650" size="230,36" alphatest="blend" />         <widget source="session.VideoPicture" render="Pig" position=" 836,89" size="370,208" zPosition="3" backgroundColor="#ff000000"/>   <ePixmap position="920,500" zPosition="1" size="228,130" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/1matrix.png" />    </screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        fn = 'NewImage'
        sourcelist = []
        for fn in os.listdir('/media/neoboot/ImagesUpload'):
            if fn.find('.zip') != -1:
                fn = fn.replace('.zip', '')
                sourcelist.append((fn, fn))
                continue
            if fn.find('.tar.xz') != -1:
                fn = fn.replace('.tar.xz', '')
                sourcelist.append((fn, fn))
                continue
            if fn.find('.nfi') != -1:
                fn = fn.replace('.nfi', '')
                sourcelist.append((fn, fn))
                continue
        if len(sourcelist) == 0:
            sourcelist = [('None', 'None')]
        self.source = ConfigSelection(choices=sourcelist)
        self.target = ConfigText(fixed_size=False)
        self.CopyFiles = ConfigYesNo(default=False)
        self.CopyKernel = ConfigYesNo(default=True)
        self.TvList = ConfigYesNo(default=True) 
        self.Montowanie = ConfigYesNo(default=True)
        self.LanWlan = ConfigYesNo(default=True)
        self.Sterowniki = ConfigYesNo(default=False)                        
        self.InstallSettings = ConfigYesNo(default=False)        
        self.ZipDelete = ConfigYesNo(default=False) 
        self.RepairFTP = ConfigYesNo(default=False)
        self.SoftCam = ConfigYesNo(default=False)                                                             
        self.BlackHole = ConfigYesNo(default=False)
        self.target.value = ''
        self.curselimage = ''

        try:
            if self.curselimage != self.source.value:
                self.target.value = self.source.value[:-13]
                self.curselimage = self.source.value
        except:
            pass

        self.createSetup()
        ConfigListScreen.__init__(self, self.list, session=session)
        self.source.addNotifier(self.typeChange)
        self['actions'] = ActionMap(['OkCancelActions',
         'ColorActions',
         'CiSelectionActions',
         'VirtualKeyboardActions'], {'cancel': self.cancel,
         'red': self.cancel,
         'green': self.imageInstall,
         'yellow': self.openKeyboard}, -2)
        self['key_green'] = Label(_('Install'))
        self['key_red'] = Label(_('Cancel'))
        self['key_yellow'] = Label(_('Keyboard'))
        self['HelpWindow'] = Pixmap()
        self['HelpWindow'].hide()

    def createSetup(self):
        self.list = []
        self.list.append(getConfigListEntry(_('Source Image file'), self.source))
        self.list.append(getConfigListEntry(_('Image Name'), self.target)) 
        self.list.append(getConfigListEntry(_('Do not copy files from Flash to the installed image ?'), self.CopyFiles ))         
        self.list.append(getConfigListEntry(_('Copy the kernel of the installed system (recommended only for Vu+) ?'), self.CopyKernel ))         
        self.list.append(getConfigListEntry(_('Copy the channel list ?'), self.TvList))  
        self.list.append(getConfigListEntry(_('Copy mounting disks ? (Recommended)'), self.Montowanie))
        self.list.append(getConfigListEntry(_('Copy network settings LAN-WLAN ?'), self.LanWlan))
        self.list.append(getConfigListEntry(_('Copy the drivers ? (Recommended only other image.)'), self.Sterowniki))                                                                
        self.list.append(getConfigListEntry(_('Copy Settings to the new Image'), self.InstallSettings))                                                                                
        self.list.append(getConfigListEntry(_('Delete Image zip after Install ?'), self.ZipDelete)) 
        self.list.append(getConfigListEntry(_('Repair FTP ? (Recommended only other image if it does not work.)'), self.RepairFTP))
        self.list.append(getConfigListEntry(_('Copy settings SoftCam ?'), self.SoftCam))          
        self.list.append(getConfigListEntry(_('Path BlackHole ? (Not recommended for VuPlus)'), self.BlackHole))
     
    def typeChange(self, value):
        self.createSetup()
        self['config'].l.setList(self.list)
        if self.curselimage != self.source.value:
            self.target.value = self.source.value[:-13]
            self.curselimage = self.source.value

    def openKeyboard(self):
        sel = self['config'].getCurrent()
        if sel:
            if sel == self.target:
                if self['config'].getCurrent()[1].help_window.instance is not None:
                    self['config'].getCurrent()[1].help_window.hide()
            self.vkvar = sel[0]
            if self.vkvar == _('Image Name'):
                self.session.openWithCallback(self.VirtualKeyBoardCallback, VirtualKeyBoard, title=self['config'].getCurrent()[0], text=self['config'].getCurrent()[1].value)
        return

    def VirtualKeyBoardCallback(self, callback = None):
        if callback is not None and len(callback):
            self['config'].getCurrent()[1].setValue(callback)
            self['config'].invalidate(self['config'].getCurrent())
        return

    def imageInstall(self):
        if self.check_free_space():
            pluginpath = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot'
            myerror = ''
            source = self.source.value.replace(' ', '')
            target = self.target.value.replace(' ', '')
            for fn in os.listdir('/media/neoboot/ImageBoot'):
                if fn == target:
                    myerror = _('Sorry, an Image with the name ') + target + _(' is already installed.\n Please try another name.')
                    continue

            if source == 'None':
                myerror = _('You have to select one Image to install.\nPlease, upload your zip file in the folder: /media/neoboot/ImagesUpload and select the image to install.')
            if target == '':
                myerror = _('You have to provide a name for the new Image.')
            if target == 'Flash':
                myerror = _('Sorry this name is reserved. Choose another name for the new Image.')
            if len(target) > 35:
                myerror = _('Sorry the name of the new Image is too long.')
            if myerror:
                myerror
                self.session.open(MessageBox, myerror, MessageBox.TYPE_INFO)
            else:
                myerror
                message = "echo -e '"
                message += _('NeoBot started installing new image.\n')
                message += _('The installation process may take a few minutes.\n')
                message += _('Please: DO NOT reboot your STB and turn off the power.\n')
                message += _('Please, wait...\n')                
                message += "'"
                cmd1 = 'python ' + pluginpath + '/ex_init.py'
                cmd = '%s %s %s %s %s %s %s %s %s %s %s %s %s %s ' % (cmd1,
                 source,
                 target.replace(' ', '.'),
                 str(self.CopyFiles.value),                 
                 str(self.CopyKernel.value),                 
                 str(self.TvList.value),
                 str(self.Montowanie.value),
                 str(self.LanWlan.value),
                 str(self.Sterowniki.value),                                                                                                                        
                 str(self.InstallSettings.value), 
                 str(self.ZipDelete.value),                                                                    
                 str(self.RepairFTP.value),                                  
                 str(self.SoftCam.value), 
                 str(self.BlackHole.value))  
                print '[NEO-BOOT]: ', cmd
                self.session.open(Console, _('NEOBoot: Install new image'), [message, cmd])


    def check_free_space(self):
        if Freespace('/media/neoboot/ImagesUpload') < 500000:
            self.session.open(MessageBox, _('Not enough free space on /media/neoboot/ !!\nYou need at least 500Mb free space.\n\nExit plugin.'), type=MessageBox.TYPE_ERROR)
            return False
        return True

    def cancel(self):
        self.close()

def readline(filename, iferror = ''):
    if iferror[:3] == 'or:':
      data = iferror[3:]
    else:
      data = iferror
    try:
        if os.path.exists(filename):
            with open(filename) as f:
                data = f.readline().strip()
                f.close()
    except Exception:
        PrintException()
    return data

def Freespace(dev):
    statdev = os.statvfs(dev)
    space = statdev.f_bavail * statdev.f_frsize / 1024
    print '[NeoBoot] Free space on %s = %i kilobytes' % (dev, space)
    return space

def checkimage():
    mycheck = False
    if fileExists('/proc/stb/info'): #vumodel'): ogranicza tylko dla vu+
        mycheck = True
    else:
        mycheck = False
    return mycheck

def checkversion(session):
    version = 0
    if fileExists('/media/neoboot/ImageBoot/.version'):
        f = open('/media/neoboot/ImageBoot/.version')
        version = float(f.read())
        f.close()
    if fileExists('/media/neoboot/ImageBoot/.neonextboot'):
        f2 = open('/media/neoboot/ImageBoot/.neonextboot', 'r')
        mypath2 = f2.readline().strip()
        f2.close()
        if mypath2 != 'Flash' or mypath2 == 'Flash' and checkimage():
            if float(PLUGINVERSION) != version:
                session.open(MyUpgrade)
            else:
                session.open(NeoBootImageChoose)
        else:
            session.open(MessageBox, _('Sorry: Wrong image in flash found. You have to install in flash Vu+ or Octagon-sf4008 Image !!!'), MessageBox.TYPE_INFO, 10)
    else:
        session.open(NeoBootInstallation)

def main(session, **kwargs):
    try:
        f = open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location', 'r')
        mypath = f.readline().strip()
        f.close()
        if not os.path.exists('/media/neoboot'):
            system('mkdir /media/neoboot')
        cmd = 'mount ' + mypath + ' /media/neoboot'
        system(cmd)
        f = open('/proc/mounts', 'r')
        for line in f.readlines():
            if line.find('/media/neoboot') != -1:
                line = line[0:9]
                break

        cmd = 'mount ' + line + ' ' + mypath
        system(cmd)
        cmd = 'mount ' + mypath + ' /media/neoboot'
        system(cmd)
    except:
        pass

    checkversion(session)

def menu(menuid, **kwargs):
    if menuid == 'mainmenu':
        return [(_('NEOBOOT'),
          main,
          'neo_boot',
          1)]
    return []

from Plugins.Plugin import PluginDescriptor

def Plugins(**kwargs):
    return [PluginDescriptor(name='NeoBoot ', description='NeoBoot', where=PluginDescriptor.WHERE_MENU, fnc=menu), PluginDescriptor(name='NeoBoot', description=_('Installing multiple images'), icon='neo.png', where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main)]
