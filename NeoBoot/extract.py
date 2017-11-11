#!/usr/bin/env python

import time
import sys
import os
import struct
import shutil  
 
def getCPUtype():
    cpu='UNKNOWN'
    if os.path.exists('/proc/cpuinfo'):
        with open('/proc/cpuinfo', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find('ARMv7') != -1:
            cpu='ARMv7'
        elif lines.find('mips') != -1:
            cpu='MIPS'
    return cpu   
    
media = '/media/neoboot'
mediahome = media + '/ImageBoot/'
extensions_path = '/usr/lib/enigma2/python/Plugins/Extensions/'
dev_null = ' > /dev/null 2>&1'

# Copyright (c) , gutosie  license
# 
# Redystrybucja wersji programu i dokonywania modyfikacji JEST DOZWOLONE, pod warunkiem zachowania niniejszej informacji o prawach autorskich. 
# Autor NIE ponosi JAKIEJKOLWIEK odpowiedzialnosci za skutki uztkowania tego programu oraz za wykorzystanie zawartych tu informacji.
# Modyfikacje przeprowadzasz na wlasne ryzyko!!!
# O wszelkich zmianach prosze poinformowac na  http://all-forum.cba.pl   w temacie pod nazwa  	 -#[NEOBOOT]#-

# This text/program is free document/software. Redistribution and use in
# source and binary forms, with or without modification, ARE PERMITTED provided
# save this copyright notice. This document/program is distributed WITHOUT any
# warranty, use at YOUR own risk.

def NEOBootMainEx(source, target, installsettings, zipdelete, tvlist, montowanie, LanWlan, softcam, RepairFTP, Sterowniki, movingfiles,  getImageFolder):
    media_target = mediahome + target
    list_one = ['rm -r ' + media_target + dev_null, 'mkdir ' + media_target + dev_null, 'chmod -R 0777 ' + media_target]
    for command in list_one:
        os.system(command)
    rc = NEOBootExtract(source, target, zipdelete, getImageFolder)
    list_two = ['mkdir -p ' + media_target + '/media' + dev_null,
     'rm ' + media_target + media + dev_null,
     'rmdir ' + media_target + media + dev_null,
     'mkdir -p ' + media_target + media + dev_null,               
     'cp -r ' + extensions_path + 'NeoBoot ' + media_target + extensions_path + 'NeoBoot' + dev_null]                   
    for command in list_two:
        os.system(command)        

    if movingfiles == 'True':
        cmd = 'touch /tmp/without_copying'
        rc = os.system(cmd)
                    
    if installsettings == 'True':
            if not os.path.exists('%s/ImageBoot/%s/etc/enigma2' % (media, target)):
                cmd = 'mkdir -p /etc/fstab %s/ImageBoot/%s/etc/enigma2' % (media, target)
                rc = os.system(cmd) 
            cmd = 'cp /etc/enigma2/settings %s/ImageBoot/%s/etc/enigma2' % (media, target)
            rc = os.system(cmd)            
            cmd = 'cp /etc/tuxbox/* %s/ImageBoot/%s/etc/tuxbox' % (media, target)
            rc = os.system(cmd)
            os.system('echo "Skopiowano ustawienia systemu."')
            
    if tvlist == 'True':
            if not os.path.exists('%s/ImageBoot/%s/etc/enigma2' % (media, target)):
                cmd = 'mkdir -p /etc/fstab %s/ImageBoot/%s/etc/enigma2' % (media, target)
                rc = os.system(cmd)           
            cmd = 'cp /etc/enigma2/*.tv %s/ImageBoot/%s/etc/enigma2' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp /etc/enigma2/*.radio %s/ImageBoot/%s/etc/enigma2' % (media, target)
            rc = os.system(cmd)            
            cmd = 'cp /etc/enigma2/*.tv %s/ImageBoot/%s/etc/enigma2' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp /etc/enigma2/lamedb %s/ImageBoot/%s/etc/enigma2' % (media, target)
            rc = os.system(cmd)    
            os.system('echo "Skopiowano liste tv."')

    if montowanie == 'True':
            if os.path.exists('%s/ImageBoot/%s/etc/fstab' % (media, target)):
                cmd = 'mv %s/ImageBoot/%s/etc/fstab %s/ImageBoot/%s/etc/fstab.org' % (media,
                 target,
                 media,
                 target)
                rc = os.system(cmd)         
            if os.path.exists('%s/ImageBoot/%s/etc/init.d/volatile-media.sh' % (media, target)):
                cmd = 'mv %s/ImageBoot/%s/etc/init.d/volatile-media.sh %s/ImageBoot/%s/etc/init.d/volatile-media.sh.org' % (media,
                 target,
                 media,
                 target)
                rc = os.system(cmd)
            cmd = 'cp -r /etc/fstab %s/ImageBoot/%s/etc/fstab' % (media, target)
            rc = os.system(cmd)            
            cmd = 'cp -r /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/S50fat.sh %s/ImageBoot/%s/etc/rcS.d' % (media, target)
            rc = os.system(cmd)
            os.system('echo "Skopiowano montowanie."')            

    if LanWlan == 'True':
            if os.path.exists('/etc/wpa_supplicant.wlan0.conf'):
                cmd = 'cp -r /etc/wpa_supplicant.wlan0.conf %s/ImageBoot/%s/etc/wpa_supplicant.wlan0.conf > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)    
            if os.path.exists('/etc/network/interfaces'):
                cmd = 'cp -r /etc/network/interfaces %s/ImageBoot/%s/etc/network/interfaces > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
            if os.path.exists('/etc/wpa_supplicant.conf'):
                cmd = 'cp -r /etc/wpa_supplicant.conf %s/ImageBoot/%s/etc/wpa_supplicant.conf > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
            if os.path.exists('/etc/resolv.conf'):
                cmd = 'cp -r /etc/resolv.conf %s/ImageBoot/%s/etc/resolv.conf > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
            if os.path.exists('/etc/wl.conf.wlan3'):
                cmd = 'cp -r /etc/wl.conf.wlan3 %s/ImageBoot/%s/etc/wl.conf.wlan3 > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)                                    
            os.system('echo "Skopiowano pliki sieciowe."')

    if softcam == 'True':
            if os.path.exists('/usr/bin/oscam'):
                cmd = 'cp -r /usr/bin/oscam %s/ImageBoot/%s/usr/bin/oscam > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
            if os.path.exists('/usr/bin/CCcam'):
                cmd = 'cp -r /usr/bin/CCcam %s/ImageBoot/%s/usr/bin/CCcam > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)       
            if os.path.exists('/etc/CCcam.cfg'):
                cmd = 'cp -r /etc/CCcam.cfg %s/ImageBoot/%s/etc/CCcam.cfg > /dev/null 2>&1' % (media, target)    
                rc = os.system(cmd)
            if os.path.exists('/etc/tuxbox/config'):
                cmd = 'cp -r /etc/tuxbox/config %s/ImageBoot/%s/etc/tuxbox/config > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)       
            if os.path.exists('/etc/init.d/softcam.oscam'):
                cmd = 'cp -r /etc/init.d/softcam.oscam %s/ImageBoot/%s/etc/init.d/softcam.oscam > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd) 
            if os.path.exists('/etc/init.d/softcam.cccam'):
                cmd = 'cp -r /etc/init.d/softcam.cccam %s/ImageBoot/%s/etc/init.d/softcam.cccam > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd) 
            os.system('echo "Skopiowano pliki SofCam."')

    if RepairFTP == 'True':
            if os.path.exists('%s/ImageBoot/%s/etc/vsftpd.conf' % (media, target)):
                filename = media + '/ImageBoot/' + target + '/etc/vsftpd.conf'
                if os.path.exists(filename):
                    filename2 = filename + '.tmp'
                    out = open(filename2, 'w')
                    f = open(filename, 'r')
                    for line in f.readlines():
                        if line.find('listen=NO') != -1:
                            line = 'listen=YES\n'
                        elif line.find('listen_ipv6=YES') != -1:
                            line = 'listen_ipv6=NO\n'
                        out.write(line)

                    f.close()
                    out.close()
                    os.rename(filename2, filename)
            os.system('echo "Naprawa ftp."')

    if Sterowniki == 'True':
            if os.path.exists('%s/ImageBoot/%s/lib/modules' % (media, target)):
                cmd = 'rm -r %s/ImageBoot/%s/lib/modules' % (media, target)
                rc = os.system(cmd)
            cmd = 'mkdir -p %s/ImageBoot/%s/lib/modules > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp -r /lib/modules  %s/ImageBoot/%s/lib  > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
            if os.path.exists('%s/ImageBoot/%s/lib/firmware' % (media, target)):
                cmd = 'rm -r %s/ImageBoot/%s/lib/firmware' % (media, target)
                rc = os.system(cmd)                
            cmd = 'mkdir -p %s/ImageBoot/%s/lib/firmware > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp -r /lib/firmware %s/ImageBoot/%s/lib > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)           
            os.system('echo "Skopiowano sterowniki systemu."')                        

    if not os.path.exists('/usr/lib/enigma2/python/EGAMI') and os.path.exists('%s/ImageBoot/%s/usr/lib/enigma2/python/EGAMI' % (media, target)):
            if vumodel == 'ultimo4k' or vumodel == 'solo4k' or vumodel == 'uno4k' or vumodel == 'bm750' or vumodel == 'duo' or vumodel == 'solo' or vumodel == 'uno' or vumodel == 'ultimo' or vumodel == 'solo2' or vumodel == 'duo2' or vumodel == 'solose' or vumodel == 'zero':
                if not os.path.exists('/media/neoboot/ImagesUpload/.egami/patchE.tar.gz'):
                    os.system('echo "Nie posiadasz uprawnien by uruchomic EGAMI !!! "')
                else:
                    cmd = 'cp -r /media/neoboot/ImagesUpload/.egami/patchE.tar.gz %s/ImageBoot/%s/home/root/ > /dev/null 2>&1' % (media, target)
                    rc = os.system(cmd)
                    cmd = 'rm %s/ImageBoot/%s/usr/lib/enigma2/python/mytest.pyo' % (media, target)
                    rc = os.system(cmd)
                    if os.path.exists('/usr/lib/enigma2/python/boxbranding.so'):
                        cmd = 'cp -r /usr/lib/enigma2/python/boxbranding.so %s/ImageBoot/%s/usr/lib/enigma2/python/boxbranding.so > /dev/null 2>&1' % (media, target)
                        rc = os.system(cmd)
                    os.system('echo "EGAMI-installed OK. Installation continues, wait..."')
        
            else:                          
                 pass

    if not os.path.exists('/tmp/without_copying'):                 
        cmd = 'cp -a /usr/share/enigma2/rc_models/* %s/ImageBoot/%s/usr/share/enigma2/rc_models/ > /dev/null 2>&1' % (media, target)
        rc = os.system(cmd)
        cmd = 'cp -r /usr/share/enigma2/rc_models %s/ImageBoot/%s/usr/share/enigma2 > /dev/null 2>&1' % (media, target)
        rc = os.system(cmd)
        if os.path.exists('/proc/stb/info/vumodel'):
            f1 = open('/proc/stb/info/vumodel', 'r')
            vumodel = f1.readline().strip()
            f1.close()
            if vumodel == 'ultimo4k' or vumodel == 'solo4k' or vumodel == 'uno4k':
                    os.system('mv /media/neoboot/ImagesUpload/vuplus/' + vumodel + '/kernel_auto.bin ' + media_target + '/boot/zImage.' + vumodel + '' + dev_null)       

        if os.path.exists('/usr/bin/fullwget'):
            cmd = 'cp -r /usr/bin/fullwget %s/ImageBoot/%s/usr/bin/fullwget > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)                 
        if os.path.exists('/etc/init.d/inadyn-mt'):
            cmd = 'cp -r /etc/init.d/inadyn-mt %s/ImageBoot/%s/etc/init.d/inadyn-mt > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/usr/bin/inadyn-mt'):
            cmd = 'cp -r /usr/bin/inadyn-mt %s/ImageBoot/%s/usr/bin/inadyn-mt > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/etc/inadyn.conf'):
            cmd = 'cp -r /etc/inadyn.conf %s/ImageBoot/%s/etc/inadyn.conf > /dev/null 2>&1' % (media, target)        
            rc = os.system(cmd)
        if os.path.exists('/usr/lib/enigma2/python/Plugins/SystemPlugins/FanControl'):
            cmd = 'cp -r /usr/lib/enigma2/python/Plugins/SystemPlugins/FanControl %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/SystemPlugins > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/EmuManager'):                                                                  
            cmd = 'cp -r /usr/lib/enigma2/python/Plugins/Extensions/EmuManager %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/CamdMenager'):                                                                  
            cmd = 'cp -r /usr/lib/enigma2/python/Plugins/Extensions/CamdMenager %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer'):
            cmd = 'cp -r /usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp /usr/lib/python*.*/htmlentitydefs.pyo %s/ImageBoot/%s/usr/lib/python*.* > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra'):
            cmd = 'cp -r /usr/lib/enigma2/python/Plugins/Extensions/FeedExtra %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)                             
        if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/MyUpdater'):
            cmd = 'cp -r /usr/lib/enigma2/python/Plugins/Extensions/MyUpdater %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if not os.path.exists('%s/ImageBoot/%s/usr/lib/enigma2/python/boxbranding.so' % (media, target)):
            cmd = 'cp -r /usr/lib/enigma2/python/boxbranding.so %s/ImageBoot/%s/usr/lib/enigma2/python/boxbranding.so > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        os.system('echo "Skopiowano wtyczki."')

        if getCPUtype() == 'MIPS':
            cmd = 'cp -r /etc/hostname %s/ImageBoot/%s/etc/hostname > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
            if os.path.exists('%s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions/HbbTV' % (media, target)):
                cmd = 'rm -r %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions/HbbTV' % (media, target)
                rc = os.system(cmd)

            namefile = media + '/ImageBoot/' + target + '/etc/fstab'
            namefile2 = namefile + '.tmp'
            out = open(namefile2, 'w')
            f = open(namefile, 'r')
            for line in f.readlines():
                if line.find('/dev/mtdblock2') != -1:
                    line = '#' + line
                elif line.find('/dev/root') != -1:
                    line = '#' + line
                out.write(line)

            f.close()
            out.close()
            os.rename(namefile2, namefile)
            tpmd = media + '/ImageBoot/' + target + '/etc/init.d/tpmd'
            if os.path.exists(tpmd):
                os.system('rm ' + tpmd)
            fname = media + '/ImageBoot/' + target + '/usr/lib/enigma2/python/Components/config.py'
            if os.path.exists(fname):
                fname2 = fname + '.tmp'
                out = open(fname2, 'w')
                f = open(fname, 'r')
                for line in f.readlines():
                    if line.find('if file(""/proc/stb/info/vumodel")') != -1:
                        line = '#' + line
                    out.write(line)

                f.close()
                out.close()
                os.rename(fname2, fname)

            targetfile = media + '/ImageBoot/' + target + '/etc/vsftpd.conf'
            if os.path.exists(targetfile):
                targetfile2 = targetfile + '.tmp'
                out = open(targetfile2, 'w')
                f = open(targetfile, 'r')
                for line in f.readlines():
                    if not line.startswith('nopriv_user'):
                        out.write(line)

                f.close()
                out.close()
                os.rename(targetfile2, targetfile)
            mypath = media + '/ImageBoot/' + target + '/usr/lib/opkg/info/'
            cmd = 'mkdir -p %s/ImageBoot/%s/var/lib/opkg/info > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
            if not os.path.exists(mypath):
                mypath = media + '/ImageBoot/' + target + '/var/lib/opkg/info/'
            for fn in os.listdir(mypath):
                if fn.find('kernel-image') != -1 and fn.find('postinst') != -1:
                    filename = mypath + fn
                    filename2 = filename + '.tmp'
                    out = open(filename2, 'w')
                    f = open(filename, 'r')
                    for line in f.readlines():
                        if line.find('/boot') != -1:
                            line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                        out.write(line)

                    if f.close():
                        out.close()
                        os.rename(filename2, filename)
                        cmd = 'chmod -R 0755 %s' % filename
                        rc = os.system(cmd)
                if fn.find('-bootlogo.postinst') != -1:
                    filename = mypath + fn
                    filename2 = filename + '.tmp'
                    out = open(filename2, 'w')
                    f = open(filename, 'r')
                    for line in f.readlines():
                        if line.find('/boot') != -1:
                            line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                        out.write(line)

                    f.close()
                    out.close()
                    os.rename(filename2, filename)
                    cmd = 'chmod -R 0755 %s' % filename
                    rc = os.system(cmd)
                if fn.find('-bootlogo.postrm') != -1:
                    filename = mypath + fn
                    filename2 = filename + '.tmp'
                    out = open(filename2, 'w')
                    f = open(filename, 'r')
                    for line in f.readlines():
                        if line.find('/boot') != -1:
                            line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                        out.write(line)

                    f.close()
                    out.close()
                    os.rename(filename2, filename)
                    cmd = 'chmod -R 0755 %s' % filename
                    rc = os.system(cmd)
                if fn.find('-bootlogo.preinst') != -1:
                    filename = mypath + fn
                    filename2 = filename + '.tmp'
                    out = open(filename2, 'w')
                    f = open(filename, 'r')
                    for line in f.readlines():
                        if line.find('/boot') != -1:
                            line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                        out.write(line)

                    f.close()
                    out.close()
                    os.rename(filename2, filename)
                    cmd = 'chmod -R 0755 %s' % filename
                    rc = os.system(cmd)
                if fn.find('-bootlogo.prerm') != -1:
                    filename = mypath + fn
                    filename2 = filename + '.tmp'
                    out = open(filename2, 'w')
                    f = open(filename, 'r')
                    for line in f.readlines():
                        if line.find('/boot') != -1:
                            line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                        out.write(line)

                    f.close()
                    out.close()
                    os.rename(filename2, filename)
                    cmd = 'chmod -R 0755 %s' % filename
                    rc = os.system(cmd)

        os.system('mkdir -p ' + media_target + '/media/hdd' + dev_null)
        os.system('mkdir -p ' + media_target + '/media/usb' + dev_null)
        os.system('mkdir -p ' + media_target + '/media/neoboot' + dev_null)
        os.system('mkdir -p ' + media_target + '/var/lib/opkg/info/' + dev_null)                 

    rc = RemoveUnpackDirs(getImageFolder)                      

    if '.tar.xz' not in source and not os.path.exists('%s/ImageBoot/%s/etc/fstab' % (media, target)):     
            os.system('echo "NeoBoot nie zainstalowal tego systemu ! Powodem bledu moze byc zle spakowany plik image zip lub niewlasciwe image dla modelu."')
            os.system('rm -r %s/ImageBoot/%s'% (media, target))
    else:
            os.system('touch /media/neoboot/ImageBoot/.data; echo "Data instalacji image" > /media/neoboot/ImageBoot/.data; echo " "; date  > /media/neoboot/ImageBoot/.data')
            os.system('mv -f /media/neoboot/ImageBoot/.data /media/neoboot/ImageBoot/%s/.data' % target)
            cmd = 'touch /tmp/.init_reboot'
            rc = os.system(cmd)
            out = open(mediahome + '.neonextboot', 'w')
            out.write(target)
            out.close()
            os.system('cp /media/neoboot/ImageBoot/.neonextboot /media/neoboot/ImageBoot/%s/.multinfo' % target)
            out = open(mediahome + '.neonextboot', 'w')
            out.write('Flash')
            out.close()    
            os.system('echo "Instalacja gotowa   !!! - EXIT - !!!"')
            os.system('echo "Time to complete the installation process:"; date +%T')   
            if os.path.exists('/media/neoboot/ubi') is True:
                rc = os.system('rm -r /media/neoboot/ubi')
                                     
def NEOBootExtract(source, target, zipdelete, getImageFolder):
    RemoveUnpackDirs(getImageFolder)
    sourcefile = media + '/ImagesUpload/%s.zip' % source
    if os.path.exists(sourcefile):
        os.chdir(media + '/ImagesUpload')
        os.system('unzip ' + sourcefile)
        if zipdelete == 'True': 
            os.system('rm -rf ' + sourcefile)            
        if os.path.exists(media + '/ImagesUpload/%s' % getImageFolder):
            os.chdir('%s' % getImageFolder)                                
    os.system('echo "Start time of the installation process:"; date +%T; echo "Rozpakowywanie pliku instalacyjnego..."' )
    if getCPUtype() != 'ARMv7': 
        for i in range(0, 20):
            mtdfile = '/dev/mtd' + str(i)
            if os.path.exists(mtdfile) is False:
                break
        mtd = str(i)
        if os.path.exists('/media/neoboot/ubi') is False:
            rc = os.system('mkdir /media/neoboot/ubi') 
        if getCPUtype() == 'MIPS': 
            to = '/media/neoboot/ImageBoot/' + target
            cmd = 'mkdir %s > /dev/null 2<&1' % to
            rc = os.system(cmd)
            to = '/media/neoboot/ImageBoot/' + target
            cmd = 'chmod -R 0777 %s' % to
            rc = os.system(cmd)
            rootfname = 'rootfs.bin'
            brand = ''
            if os.path.exists('/media/neoboot/ImagesUpload/flash.jffs2'):
                rootfname = 'flash.jffs2'
                rc = os.system('rm -r /media/neoboot/ImagesUpload/zbimage-linux-xload')
            if os.path.exists('/media/neoboot/ImagesUpload/image0.jffs2'):
                rootfname = 'image0.jffs2'
                rc = os.system('rm -r /media/neoboot/ImagesUpload/zbimage-linux-xload')
                rc = os.system('rm -r /media/neoboot/ImagesUpload/update.ext')
            if os.path.exists('/media/neoboot/ImagesUpload/e3hd'):
                os.chdir('e3hd')
                brand = 'e3hd'
            if os.path.exists('/media/neoboot/ImagesUpload/odinm9'):
                os.chdir('odinm9')
                brand = 'odinm9'
            if os.path.exists('/media/neoboot/ImagesUpload/en2'):
                os.chdir('en2')
                brand = 'en2'
            if os.path.exists('/media/neoboot/ImagesUpload/zgemma'):
                os.chdir('zgemma')
                brand = 'zgemma'
                rootfname = 'rootfs.bin'
                if os.path.exists('/media/neoboot/ImagesUpload/zgemma/sh1'):
                    os.chdir('sh1')
                if os.path.exists('/media/neoboot/ImagesUpload/zgemma/sh2'):
                    os.chdir('sh2')
                if os.path.exists('/media/neoboot/ImagesUpload/zgemma/h2'):
                    os.chdir('h2')
                if os.path.exists('/media/neoboot/ImagesUpload/zgemma/h3'):
                    os.chdir('h3')
                if os.path.exists('/media/neoboot/ImagesUpload/zgemma/h5'):
                    os.chdir('h5')
            if os.path.exists('/media/neoboot/ImagesUpload/hde'):
                os.chdir('hde')
                brand = 'hde'
            if os.path.exists('/media/neoboot/ImagesUpload/hdx'):
                os.chdir('hdx')
                brand = 'hdx'
            if os.path.exists('/media/neoboot/ImagesUpload/hdp'):
                os.chdir('hdp')
                brand = 'hdp'
            if os.path.exists('/media/neoboot/ImagesUpload/miraclebox'):
                os.chdir('miraclebox')
                brand = 'miraclebox'
                rootfname = 'rootfs.bin'
                if os.path.exists('/media/neoboot/ImagesUpload/miraclebox/mini'):
                    os.chdir('mini')
                if os.path.exists('/media/neoboot/ImagesUpload/miraclebox/miniplus'):
                    os.chdir('miniplus')
                if os.path.exists('/media/neoboot/ImagesUpload/miraclebox/minihybrid'):
                    os.chdir('minihybrid')
                if os.path.exists('/media/neoboot/ImagesUpload/miraclebox/twin'):
                    os.chdir('twin')
                if os.path.exists('/media/neoboot/ImagesUpload/miraclebox/ultra'):
                    os.chdir('ultra')
                if os.path.exists('/media/neoboot/ImagesUpload/miraclebox/micro'):
                    os.chdir('micro')
                if os.path.exists('/media/neoboot/ImagesUpload/miraclebox/twinplus'):
                    os.chdir('twinplus')
                if os.path.exists('/media/neoboot/ImagesUpload/miraclebox/twin4k'):
                    os.chdir('twin4k')
            if os.path.exists('/media/neoboot/ImagesUpload/sf3038'):
                os.chdir('sf3038')
            if os.path.exists('/media/neoboot/ImagesUpload/atemio'):
                os.chdir('atemio')
                if os.path.exists('/media/neoboot/ImagesUpload/atemio/5x00'):
                    os.chdir('5x00')
                if os.path.exists('/media/neoboot/ImagesUpload/atemio/6000'):
                    os.chdir('6000')
                if os.path.exists('/media/neoboot/ImagesUpload/atemio/6100'):
                    os.chdir('6100')
                if os.path.exists('/media/neoboot/ImagesUpload/atemio/6200'):
                    os.chdir('6200')
                if os.path.exists('/media/neoboot/ImagesUpload/atemio/8x00'):
                    os.chdir('8x00')
            if os.path.exists('/media/neoboot/ImagesUpload/xpeedlx'):
                os.chdir('xpeedlx')
                brand = 'xpeedlx'
            if os.path.exists('/media/neoboot/ImagesUpload/xpeedlx3'):
                os.chdir('xpeedlx3')
                brand = 'xpeedlx3'
            if os.path.exists('/media/neoboot/ImagesUpload/bwidowx'):
                os.chdir('bwidowx')
                brand = 'bwidowx'
            if os.path.exists('/media/neoboot/ImagesUpload/bwidowx2'):
                os.chdir('bwidowx2')
                brand = 'bwidowx2'
            if os.path.exists('/media/neoboot/ImagesUpload/beyonwiz'):
                os.chdir('beyonwiz')
                brand = 'beyonwiz'
                if os.path.exists('/media/neoboot/ImagesUpload/beyonwiz/hdx'):
                    os.chdir('hdx')
                if os.path.exists('/media/neoboot/ImagesUpload/beyonwiz/hdp'):
                    os.chdir('hdp')
                if os.path.exists('/media/neoboot/ImagesUpload/beyonwiz/hde2'):
                    os.chdir('hde2')
            if os.path.exists('/media/neoboot/ImagesUpload/vuplus'):
                os.chdir('vuplus')
                brand = 'vuplus'
                rootfname = 'root_cfe_auto.jffs2'
                if os.path.exists('/media/neoboot/ImagesUpload/vuplus/uno'):
                    os.chdir('uno')
                if os.path.exists('/media/neoboot/ImagesUpload/vuplus/duo'):
                    os.chdir('duo')
                if os.path.exists('/media/neoboot/ImagesUpload/vuplus/ultimo'):
                    os.chdir('ultimo')
                if os.path.exists('/media/neoboot/ImagesUpload/vuplus/solo'):
                    os.chdir('solo')
                if os.path.exists('/media/neoboot/ImagesUpload/vuplus/duo2'):
                    os.chdir('duo2')
                    rootfname = 'root_cfe_auto.bin'
                if os.path.exists('/media/neoboot/ImagesUpload/vuplus/solo2'):
                    os.chdir('solo2')
                    rootfname = 'root_cfe_auto.bin'
                if os.path.exists('/media/neoboot/ImagesUpload/vuplus/solose'):
                    os.chdir('solose')
                    rootfname = 'root_cfe_auto.bin'
                if os.path.exists('/media/neoboot/ImagesUpload/vuplus/zero'):
                    os.chdir('zero')
                    rootfname = 'root_cfe_auto.bin'
            if os.path.exists('/media/neoboot/ImagesUpload/et10000'):
                os.chdir('et10000')
                brand = 'et10000'
            if os.path.exists('/media/neoboot/ImagesUpload/et9x00'):
                os.chdir('et9x00')
                brand = 'et9x00'
            if os.path.exists('/media/neoboot/ImagesUpload/et8500'):
                os.chdir('et8500')
                brand = 'et8500'
            if os.path.exists('/media/neoboot/ImagesUpload/et8000'):
                os.chdir('et8000')
                brand = 'et8000'
            if os.path.exists('/media/neoboot/ImagesUpload/et7x00'):
                os.chdir('et7x00')
                brand = 'et7x00'
            if os.path.exists('/media/neoboot/ImagesUpload/et6x00'):
                os.chdir('et6x00')
                brand = 'et6x00'
            if os.path.exists('/media/neoboot/ImagesUpload/et5x00'):
                os.chdir('et5x00')
                brand = 'et5x00'
            if os.path.exists('/media/neoboot/ImagesUpload/et4x00'):
                os.chdir('et4x00')
                brand = 'et4x00'
            if os.path.exists('/media/neoboot/ImagesUpload/gigablue'):
                os.chdir('gigablue')
                brand = 'gigablue'
                if os.path.exists('/media/neoboot/ImagesUpload/gigablue/quad'):
                    os.chdir('quad')
            if os.path.exists('/media/neoboot/ImagesUpload/hd1200'):
                os.chdir('hd1200')
                brand = 'hd1200'
            if os.path.exists('/media/neoboot/ImagesUpload/hd500C'):
                os.chdir('hd500C')
                brand = 'hd500C'
            if os.path.exists('/media/neoboot/ImagesUpload/hd2400'):
                os.chdir('hd2400')
                brand = 'hd2400'

            rc = os.system('insmod /lib/modules/*/kernel/drivers/mtd/nand/nandsim.ko cache_file=/media/neoboot/image_cache first_id_byte=0x20 second_id_byte=0xaa third_id_byte=0x00 fourth_id_byte=0x15;sleep 5')
            cmd = 'dd if=%s of=/dev/mtdblock%s bs=2048' % (rootfname, mtd)
            rc = os.system(cmd)
            cmd = 'ubiattach /dev/ubi_ctrl -m %s -O 2048' % mtd
            rc = os.system(cmd)
            rc = os.system('mount -t ubifs ubi1_0 /media/neoboot/ubi')
            os.chdir('/home/root')            
            cmd = 'cp -r /media/neoboot/ubi/* /media/neoboot/ImageBoot/' + target
            rc = os.system(cmd)
            rc = os.system('umount /media/neoboot/ubi')
            cmd = 'ubidetach -m %s' % mtd
            rc = os.system(cmd)
            rc = os.system('rmmod nandsim')
            rc = os.system('rm /media/neoboot/image_cache')
            os.system('echo "System z pliku instalacyjnego rozpakowwany."' )

    elif getCPUtype() == 'ARMv7':         
        if os.path.exists('/media/neoboot/ImagesUpload/sf4008'):
                cmd = 'tar -jxvf /media/neoboot/ImagesUpload/sf4008/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
                rc = os.system(cmd)                 
        elif os.path.exists('/media/neoboot/ImagesUpload/dm900'):
                cmd = 'tar -jxvf /media/neoboot/ImagesUpload/dm900/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
                rc = os.system(cmd)   
        elif os.path.exists('/media/neoboot/ImagesUpload/%s.tar.xz' % source) :                  
                os.system('echo "Instalacja systemu spakowanego w plik tar.xz w toku..."')
                os.system('cp -r /media/neoboot/ImagesUpload/%s.tar.xz  /media/neoboot/ImagesUpload/rootfs.tar.xz' % source)
                cmd = 'tar -jJxvf /media/neoboot/ImagesUpload/rootfs.tar.xz -C  /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1' 
                rc = os.system(cmd)  
        elif os.path.exists('/media/neoboot/ImagesUpload/hd51'):
                cmd = 'tar -jxvf /media/neoboot/ImagesUpload/hd51/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
                rc = os.system(cmd)                                 
        elif os.path.exists('/media/neoboot/ImagesUpload/gigablue'):
                cmd = 'tar -jxvf /media/neoboot/ImagesUpload/gigablue/quad4k/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
                rc = os.system(cmd) 
        elif os.path.exists('/media/neoboot/ImagesUpload/vuplus/solo4k'):
                cmd = 'tar -jxvf /media/neoboot/ImagesUpload/vuplus/solo4k/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
                rc = os.system(cmd)
        elif os.path.exists('/media/neoboot/ImagesUpload/vuplus/uno4k'):
                cmd = 'tar -jxvf /media/neoboot/ImagesUpload/vuplus/uno4k/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
                rc = os.system(cmd)
        elif os.path.exists('/media/neoboot/ImagesUpload/vuplus/ultimo4k'):
                cmd = 'tar -jxvf /media/neoboot/ImagesUpload/vuplus/ultimo4k/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
                rc = os.system(cmd)
        elif os.path.exists('/media/neoboot/ImagesUpload/update/revo4k'):
                cmd = 'tar -jxvf /media/neoboot/ImagesUpload/update/revo4k/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
                rc = os.system(cmd)
        elif os.path.exists('/media/neoboot/ImagesUpload/update/galaxy4k'):
                cmd = 'tar -jxvf /media/neoboot/ImagesUpload/update/galaxy4k/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
                rc = os.system(cmd)
        elif os.path.exists('/media/neoboot/ImagesUpload/zgemma/h7'):
                cmd = 'tar -jxvf /media/neoboot/ImagesUpload/zgemma/h7/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
                rc = os.system(cmd)
        else:                
                sfolder = media + '/ImagesUpload/%s' % getImageFolder
                cmd = 'tar -jxvf' + sfolder + '/rootfs.tar.bz2 -C ' + media + '/ImageBoot/' + target + ' > /dev/null 2>&1'
                rc = os.system(cmd)               

        os.system('echo "System z pliku instalacyjnego rozpakowwany. Trwa dalsza instalacja..."' )

    if 'BlackHole' in source:
                ver = source.replace('BlackHole-', '')
                try:
                    text = ver.split('-')[0]
                except:
                    text = ''
                cmd = 'mkdir /media/neoboot/ImageBoot/%s/boot/blackhole' % target
                rc = os.system(cmd)
                cmd = 'cp /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/version /media/neoboot/ImageBoot/%s/boot/blackhole' % target
                rc = os.system(cmd)
                cmd = 'mv /media/neoboot/ImageBoot/%s/usr/lib/enigma2/python/Blackhole/BhUtils.pyo /media/neoboot/ImageBoot/%s/usr/lib/enigma2/python/Blackhole/BhUtils.pyo.org' % (target, target)
                rc = os.system(cmd)                
                cmd = 'cp -rf /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/utilsbh /media/neoboot/ImageBoot/%s/usr/lib/enigma2/python/Blackhole/BhUtils.pyo' % target
                rc = os.system(cmd)                
                localfile = '/media/neoboot/ImageBoot/%s/boot/blackhole/version' % target
                temp_file = open(localfile, 'w')
                temp_file.write(text)
                temp_file.close()                
                cmd = 'mv /media/neoboot/ImageBoot/%s/usr/bin/enigma2 /media/neoboot/ImageBoot/%s/usr/bin/enigma2-or' % (target, target)
                rc = os.system(cmd)                
                fail = '/media/neoboot/ImageBoot/%s/usr/bin/enigma2-or' % target
                f = open(fail, 'r')
                content = f.read()
                f.close()                
                localfile2 = '/media/neoboot/ImageBoot/%s/usr/bin/enigma2' % target
                temp_file2 = open(localfile2, 'w')
                temp_file2.write(content.replace('/proc/blackhole/version', '/boot/blackhole/version'))
                temp_file2.close()                
                cmd = 'chmod -R 0755 %s' % localfile2
                rc = os.system(cmd)
                cmd = 'rm -r /media/neoboot/ImageBoot/%s/usr/bin/enigma2-or' % target
                rc = os.system(cmd)

    return 1
    
def RemoveUnpackDirs(getImageFolder):
    os.chdir(media + '/ImagesUpload')
    if os.path.exists(media + '/ImagesUpload/%s' % getImageFolder):
        shutil.rmtree('%s' % getImageFolder)
    if os.path.exists('/media/neoboot/ImagesUpload/vuplus'):
        rc = os.system('rm -r /media/neoboot/ImagesUpload/vuplus')
    elif os.path.exists ('/media/neoboot/ImagesUpload/sf4008'): 
        rc = os.system('rm -r /media/neoboot/ImagesUpload/sf4008')
    elif os.path.exists ('/media/neoboot/ImagesUpload/dm900'): 
        rc = os.system('rm -r /media/neoboot/ImagesUpload/dm900') 
    elif os.path.exists ('/media/neoboot/ImagesUpload/hd51'): 
        rc = os.system('rm -r /media/neoboot/ImagesUpload/hd51') 
    elif os.path.exists ('/media/neoboot/ImagesUpload/gigablue'): 
        rc = os.system('rm -r /media/neoboot/ImagesUpload/gigablue')
    elif os.path.exists ('/media/neoboot/ImagesUpload/miraclebox'): 
        rc = os.system('rm -r /media/neoboot/ImagesUpload/miraclebox')
    elif os.path.exists ('/media/neoboot/ImagesUpload/update'): 
        rc = os.system('rm -r /media/neoboot/ImagesUpload/update') 
    elif os.path.exists ('/media/neoboot/ImagesUpload/rootfs.tar.xz'): 
        rc = os.system('rm -r /media/neoboot/ImagesUpload/rootfs.tar.xz') 
    elif os.path.exists ('/media/neoboot/ImagesUpload/zgemma'): 
        rc = os.system('rm -r /media/neoboot/ImagesUpload/zgemma')

#END            