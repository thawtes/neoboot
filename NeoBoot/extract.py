#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ver. 6.35
import time, sys, os, struct, shutil 

def getBoxHostName():
    if os.path.exists('/etc/hostname'):
        with open('/etc/hostname', 'r') as f:
            myboxname = f.readline().strip()
            f.close()   
    return myboxname 

def getCPUSoC():
    chipset='UNKNOWN'
    if os.path.exists('/proc/stb/info/chipset'):
        with open('/proc/stb/info/chipset', 'r') as f:
            chipset = f.readline().strip()
            f.close()     
        if chipset == '7405(with 3D)':
            chipset == '7405'
                                            
    return chipset
      
def getBoxVuModel():
    vumodel='UNKNOWN'
    if os.path.exists("/proc/stb/info/vumodel") and not os.path.exists("/proc/stb/info/boxtype"):
        with open('/proc/stb/info/vumodel', 'r') as f:
            vumodel = f.readline().strip()
            f.close() 
    return vumodel

def getCPUtype() :
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
    
def getKernelVersion():
    try:
        return open('/proc/version', 'r').read().split(' ', 4)[2].split('-', 2)[0]
    except:
        return _('unknown')
             
media = '/media/neoboot'
mediahome = media + '/ImageBoot/'
extensions_path = '/usr/lib/enigma2/python/Plugins/Extensions/'
dev_null = ' > /dev/null 2>&1'

def NEOBootMainEx(source, target, CopyFiles, CopyKernel, TvList, Montowanie, LanWlan, Sterowniki, InstallSettings, ZipDelete, RepairFTP, SoftCam, BlackHole):
    media_target = mediahome + target
    list_one = ['rm -r ' + media_target + dev_null, 'mkdir ' + media_target + dev_null, 'chmod -R 0777 ' + media_target]
    for command in list_one:
        os.system(command)
    rc = NEOBootExtract(source, target, ZipDelete, BlackHole)    
    if not os.path.exists('%s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions' % (media, target)):
        os.system('mkdir -p %s/ImageBoot/%s/usr/lib/' % (media, target))
        os.system('mkdir -p %s/ImageBoot/%s/usr/lib/enigma2' % (media, target))
        os.system('mkdir -p %s/ImageBoot/%s/usr/lib/enigma2/python' % (media, target))
        os.system('mkdir -p %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins' % (media, target))
        os.system('mkdir -p %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions' % (media, target))
                
    list_two = ['mkdir -p ' + media_target + '/media' + dev_null,
     'rm ' + media_target + media + dev_null,
     'rmdir ' + media_target + media + dev_null,
     'mkdir -p ' + media_target + media + dev_null,
     'cp -rf ' + extensions_path + 'NeoBoot ' + media_target + extensions_path + 'NeoBoot' + dev_null]
    for command in list_two:
        os.system(command)

    if CopyFiles == 'True':
        os.system('echo "No copying of files..."')
        os.system('touch  /media/neoboot/ImageBoot/.without_copying')              

    if not os.path.exists('/media/neoboot/ImageBoot/.without_copying'):
        os.system('mkdir -p ' + media_target + '/media/hdd' + dev_null)
        os.system('mkdir -p ' + media_target + '/media/usb' + dev_null)
        os.system('mkdir -p ' + media_target + '/media/neoboot' + dev_null)
        os.system('mkdir -p ' + media_target + '/var/lib/opkg/info/' + dev_null)        
        cmd = 'cp -a /usr/share/enigma2/rc_models/* %s/ImageBoot/%s/usr/share/enigma2/rc_models/ > /dev/null 2>&1' % (media, target)
        rc = os.system(cmd)
        cmd = 'cp -r /usr/share/enigma2/rc_models %s/ImageBoot/%s/usr/share/enigma2 > /dev/null 2>&1' % (media, target)
        rc = os.system(cmd)            

        if CopyKernel == 'True':        
            if getCPUSoC() == '7335' or getCPUSoC() == '7325' or getCPUSoC() == '7405' or getCPUSoC() == '7356' or getCPUSoC() == '7424' or getCPUSoC() == '7241' or getCPUSoC() == '7362' or getBoxHostName() == 'vuultimo':
                os.system('mv /media/neoboot/ImagesUpload/vuplus/' + getBoxVuModel() + '/kernel_cfe_auto.bin ' + media_target + '/boot/' + getBoxVuModel() + '.vmlinux.gz' + dev_null)        
                os.system('echo "Skopiowano kernel.bin STB-MIPS"')
            elif getCPUSoC() == '7444s' or getCPUSoC() == '7376' or getCPUSoC() == '7252s' or getCPUSoC() == '72604':
                os.system('mv /media/neoboot/ImagesUpload/vuplus/' + getBoxVuModel() + '/kernel_auto.bin ' + media_target + '/boot/zImage.' + getBoxVuModel() + '' + dev_null)
                os.system('echo "Skopiowano kernel.bin STB-ARM"')                

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

        if TvList == 'True':
            if not os.path.exists('%s/ImageBoot/%s/etc/enigma2' % (media, target)):
                cmd = 'mkdir -p %s/ImageBoot/%s/etc/enigma2' % (media, target)
                rc = os.system(cmd)
            cmd = 'cp /etc/enigma2/*.tv %s/ImageBoot/%s/etc/enigma2' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp /etc/enigma2/*.radio %s/ImageBoot/%s/etc/enigma2' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp /etc/enigma2/*.tv %s/ImageBoot/%s/etc/enigma2' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp /etc/enigma2/lamedb %s/ImageBoot/%s/etc/enigma2' % (media, target)
            rc = os.system(cmd)
            os.system('echo "Skopiowano list\xc4\x99 tv."')

        if Montowanie == 'True':
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

        if LanWlan == 'True':
            os.system('echo "Skopiowano pliki sieciowe."')
            if os.path.exists('/etc/wpa_supplicant.wlan0.conf'):
                cmd = 'cp -Rpf /etc/wpa_supplicant.wlan0.conf %s/ImageBoot/%s/etc/wpa_supplicant.wlan0.conf > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
            if os.path.exists('/etc/network/interfaces'):
                cmd = 'cp -r /etc/network/interfaces %s/ImageBoot/%s/etc/network/interfaces > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
            if os.path.exists('/etc/wpa_supplicant.conf'):
                cmd = 'cp -Rpf /etc/wpa_supplicant.conf %s/ImageBoot/%s/etc/wpa_supplicant.conf > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
            if os.path.exists('/etc/resolv.conf'):
                cmd = 'cp -Rpf /etc/resolv.conf %s/ImageBoot/%s/etc/resolv.conf > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
            if os.path.exists('/etc/wl.conf.wlan3'):
                cmd = 'cp -r /etc/wl.conf.wlan3 %s/ImageBoot/%s/etc/wl.conf.wlan3 > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
            os.system('echo "Skopiowano montowanie."')

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

        if InstallSettings == 'True':
            if not os.path.exists('%s/ImageBoot/%s/etc/enigma2' % (media, target)):
                cmd = 'mkdir -p /etc/fstab %s/ImageBoot/%s/etc/enigma2' % (media, target)
                rc = os.system(cmd)
            cmd = 'cp /etc/enigma2/settings %s/ImageBoot/%s/etc/enigma2' % (media, target)
            rc = os.system(cmd)
            if not os.path.exists('%s/ImageBoot/%s/etc/tuxbox/config' % (media, target)):
                cmd = 'mkdir -p /etc/fstab %s/ImageBoot/%s/etc/tuxbox/config' % (media, target)
                rc = os.system(cmd)
                cmd = 'mkdir -p /etc/fstab %s/ImageBoot/%s/etc/tuxbox/scce' % (media, target)
                rc = os.system(cmd)
            cmd = 'cp -a /etc/tuxbox/* %s/ImageBoot/%s/etc/tuxbox' % (media, target)
            rc = os.system(cmd)
            os.system('echo "Skopiowano ustawienia systemu."')

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

        if SoftCam == 'True':
            if os.path.exists('/usr/bin/oscam'):
                cmd = 'cp -r -f -p /usr/bin/oscam %s/ImageBoot/%s/usr/bin/ > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
            if os.path.exists('/usr/bin/CCcam'):
                cmd = 'cp -r -f -p /usr/bin/CCcam %s/ImageBoot/%s/usr/bin/ > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)       
            if os.path.exists('/etc/CCcam.cfg'):
                cmd = 'cp -r -f /etc/CCcam.cfg %s/ImageBoot/%s/etc/ > /dev/null 2>&1' % (media, target)    
                rc = os.system(cmd)
            if os.path.exists('/etc/tuxbox/config'):
                cmd = 'cp -r -f /etc/tuxbox/config %s/ImageBoot/%s/etc/tuxbox/ > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)       
            if os.path.exists('/etc/init.d/softcam.oscam'):
                cmd = 'cp -r -f -p /etc/init.d/softcam.oscam %s/ImageBoot/%s/etc/init.d/ > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd) 
            if os.path.exists('/etc/init.d/softcam.cccam'):
                cmd = 'cp -r -f -p /etc/init.d/softcam.cccam %s/ImageBoot/%s/etc/init.d/ > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd) 

        if not os.path.exists('/usr/lib/enigma2/python/EGAMI') and os.path.exists('%s/ImageBoot/%s/usr/lib/enigma2/python/EGAMI' % (media, target)):
            if getBoxVuModel() == 'ultimo4k' or getBoxVuModel() == 'solo4k' or getBoxVuModel() == 'uno4k' or getBoxVuModel() == 'bm750' or getBoxVuModel() == 'duo' or getBoxVuModel() == 'solo' or getBoxVuModel() == 'uno' or getBoxVuModel() == 'ultimo' or getBoxVuModel() == 'solo2' or getBoxVuModel() == 'duo2' or getBoxVuModel() == 'solose' or getBoxVuModel() == 'zero':
                if not os.path.exists('/media/neoboot/ImagesUpload/.egami/patchE.tar.gz'):
                    os.system('echo "System EGAMI nie jest przeznaczony tego odbiornika !!! "')
                else:
                    cmd = 'cp -r /media/neoboot/ImagesUpload/.egami/patchE.tar.gz %s/ImageBoot/%s/home/root/ > /dev/null 2>&1' % (media, target)
                    rc = os.system(cmd)
                    cmd = 'rm %s/ImageBoot/%s/usr/lib/enigma2/python/mytest.pyo' % (media, target)
                    rc = os.system(cmd)
                    if not os.path.exists('/usr/lib/enigma2/python/boxbranding.so'):
                        cmd = 'cp -r /usr/lib/enigma2/python/boxbranding.so %s/ImageBoot/%s/usr/lib/enigma2/python/boxbranding.so > /dev/null 2>&1' % (media, target)
                        rc = os.system(cmd)
                    cmd = 'cp -r /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/S50fat.sh %s/ImageBoot/%s/etc/rcS.d' % (media, target)
                    rc = os.system(cmd)
                    os.system('echo "EGAMI-installed OK. Installation continues, wait..."')
                                                                                                                                   
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
    os.system('echo "Zako\xc5\x84czono instalacj\xc4\x99 nowego systemu. EXIT "')
    os.system('echo "End of installation:"; date +%T')                                                                        
    if '.tar.xz' not in source and not os.path.exists('%s/ImageBoot/%s/etc/issue' % (media, target)):
            os.system('echo ""; echo "Nie zainstalowano systemu ! Powodem b\xc5\x82\xc4\x99du instalacji mo\xc5\xbce by\xc4\x87 \xc5\xbale spakowany plik image w zip lub nie jest to sytem dla Twojego modelu ."')
            os.system('echo "Instalowany system moze sie nie uruchomic poprawnie! Sprawdz poprawnosc kataogow w instalwoanym image!!!"')
            os.system('rm -r %s/ImageBoot/%s' % (media, target))

    if os.path.exists('/media/neoboot/ubi'):
        os.system('rm -rf /media/neoboot/ubi')          
    if os.path.exists('/media/neoboot/image_cache/'):
        os.system('rm /media/neoboot/image_cache')
    if os.path.exists('/media/neoboot/ImageBoot/.without_copying'):
        os.system('rm /media/neoboot/ImageBoot/.without_copying') 
    rc = os.system('sync')
    os.system("echo 3 > /proc/sys/vm/drop_caches")
    rc = RemoveUnpackDirs()

def NEOBootExtract(source, target, ZipDelete, BlackHole):
    os.system('echo "Start of installation:"; date +%T')
    RemoveUnpackDirs()

    if os.path.exists('/media/neoboot/ImageBoot/.without_copying'):
        os.system('rm /media/neoboot/ImageBoot/.without_copying') 
    if os.path.exists('/media/neoboot/image_cache'):
        os.system('rm -rf /media/neoboot/image_cache')

    sourcefile = media + '/ImagesUpload/%s.zip' % source
    sourcefile2 = media + '/ImagesUpload/%s.nfi' % source

    os.system('echo "This may take a few minutes to complete...."')

    #Instalacja *.nfi
    if os.path.exists(sourcefile2) is True:
        if sourcefile2.endswith('.nfi'):
            os.system('echo "Instalacja systemu skapowanego w plik nfi..."')
            to = '/media/neoboot/ImageBoot/' + target
            cmd = 'mkdir %s > /dev/null 2<&1' % to
            rc = os.system(cmd)
            to = '/media/neoboot/ImageBoot/' + target
            cmd = 'chmod -R 0777 %s' % to
            rc = os.system(cmd)
            cmd = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/nfidump ' + sourcefile2 + ' /media/neoboot/ImageBoot/' + target
            rc = os.system(cmd)
            if ZipDelete == 'True':
                rc = os.system('rm -rf ' + sourcefile2)
            else:
                os.system('echo "NeoBoot keep the file:  %s  for reinstallation."' % sourcefile2)
    #Instalacja *.zip
    elif os.path.exists(sourcefile) is True:
        os.system('unzip ' + sourcefile)
        if ZipDelete == 'True':
            os.system('rm -rf ' + sourcefile)
        os.system('echo "Rozpakowywanie pliku instalacyjnego..."')

    #Instalacja MIPS
    if getCPUtype() == 'MIPS':                 
        if os.path.exists('/media/neoboot/ubi') is False:
            rc = os.system('mkdir /media/neoboot/ubi')
        to = '/media/neoboot/ImageBoot/' + target
        cmd = 'mkdir %s > /dev/null 2<&1' % to
        rc = os.system(cmd)
        to = '/media/neoboot/ImageBoot/' + target
        cmd = 'chmod -R 0777 %s' % to
        rc = os.system(cmd)
        rootfname = 'rootfs.bin'
        brand = ''
        #NANDSIM
        if os.path.exists('/lib/modules/%s/kernel/drivers/mtd/nand/nandsim.ko' % getKernelVersion()):
            for i in range(0, 20):
                    mtdfile = '/dev/mtd' + str(i)
                    if os.path.exists(mtdfile) is False:
                        break
                
            mtd = str(i)
            os.chdir(media + '/ImagesUpload')
            #zgemma
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
            #miraclebox
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
            #atemio
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
                    if os.path.exists('/media/neoboot/ImagesUpload/atemio/8x00'):
                        os.chdir('8x00')
            #Xtrend
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
            #formuler
            if os.path.exists('/media/neoboot/ImagesUpload/formuler1'):
                os.chdir('formuler1')
                brand = 'formuler1'
            if os.path.exists('/media/neoboot/ImagesUpload/formuler2'):
                os.chdir('formuler2')
                brand = 'formuler2'
            if os.path.exists('/media/neoboot/ImagesUpload/formuler3'):
                os.chdir('formuler3')
                brand = 'formuler3'
            if os.path.exists('/media/neoboot/ImagesUpload/formuler4turbo'):
                os.chdir('formuler4turbo')
                brand = 'formuler4turbo'
            #inne
            if os.path.exists('/media/neoboot/ImagesUpload/sf3038'):
                os.chdir('sf3038')
            if os.path.exists('/media/neoboot/ImagesUpload/xpeedlx'):
                os.chdir('xpeedlx')
                brand = 'xpeedlx'
            if os.path.exists('/media/neoboot/ImagesUpload/xpeedlx3'):
                os.chdir('xpeedlx3')
                brand = 'xpeedlx3'
            #VuPlus
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
                    
            #Instalacja image                                     
            rc = os.system('insmod /lib/modules/%s/kernel/drivers/mtd/nand/nandsim.ko cache_file=/media/neoboot/image_cache first_id_byte=0x20 second_id_byte=0xaa third_id_byte=0x00 fourth_id_byte=0x15;sleep 5' % getKernelVersion())
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

        #UBI_READER
        elif os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ubi_reader/ubi_extract_files.py'):
            #zgemma
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
            #miraclebox
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
            #atemio
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
                    if os.path.exists('/media/neoboot/ImagesUpload/atemio/8x00'):
                        os.chdir('8x00')
            #Xtrend
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
            #formuler
            if os.path.exists('/media/neoboot/ImagesUpload/formuler1'):
                os.chdir('formuler1')
                brand = 'formuler1'
            if os.path.exists('/media/neoboot/ImagesUpload/formuler2'):
                os.chdir('formuler2')
                brand = 'formuler2'
            if os.path.exists('/media/neoboot/ImagesUpload/formuler3'):
                os.chdir('formuler3')
                brand = 'formuler3'
            if os.path.exists('/media/neoboot/ImagesUpload/formuler4turbo'):
                os.chdir('formuler4turbo')
                brand = 'formuler4turbo'
            #inne
            if os.path.exists('/media/neoboot/ImagesUpload/sf3038'):
                os.chdir('sf3038')
            if os.path.exists('/media/neoboot/ImagesUpload/xpeedlx'):
                os.chdir('xpeedlx')
                brand = 'xpeedlx'
            if os.path.exists('/media/neoboot/ImagesUpload/xpeedlx3'):
                os.chdir('xpeedlx3')
                brand = 'xpeedlx3'
            #vuplus
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

            #Instalacja image               
            cmd = 'chmod 777 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ubi_reader/ubi_extract_files.py'
            rc = os.system(cmd)
            cmd = 'python /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ubi_reader/ubi_extract_files.py rootfs.bin -o /media/neoboot/ubi'
            rc = os.system(cmd)
            os.chdir('/home/root')
            os.system('mv /media/neoboot/ubi/rootfs/* /media/neoboot/ImageBoot/%s/' % target)                
            cmd = 'chmod -R +x /media/neoboot/ImageBoot/' + target
            rc = os.system(cmd)
        else:
            os.system('echo "NeoBoot wykryl blad !!! Prawdopodobnie brak ubi_reader lub nandsim."')

    #ARM
    elif getCPUtype() == 'ARMv7':
        if os.path.exists('/media/neoboot/ImagesUpload/sf4008'):
            os.system('echo "Instalacja systemu Octagon SF4008."')
            cmd = 'chmod 777 /media/neoboot/ImagesUpload/sf4008/rootfs.tar.bz2; tar -jxvf /media/neoboot/ImagesUpload/sf4008/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('/media/neoboot/ImagesUpload/dm900'):
            os.system('echo "Instalacja systemu Dreambox DM900."')
            cmd = 'chmod 777 /media/neoboot/ImagesUpload/dm900/rootfs.tar.bz2; tar -jxvf /media/neoboot/ImagesUpload/dm900/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('/media/neoboot/ImagesUpload/%s.tar.xz' % source):
            os.system('echo "Instalacja systemu spakowanego w plik tar.xz w toku..."')
            os.system('cp -r /media/neoboot/ImagesUpload/%s.tar.xz  /media/neoboot/ImagesUpload/rootfs.tar.xz' % source)
            cmd = 'chmod 777 /media/neoboot/ImagesUpload/rootfs.tar.xz; tar -jJxvf /media/neoboot/ImagesUpload/rootfs.tar.xz -C  /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('/media/neoboot/ImagesUpload/hd51'):
            os.system('echo "Instalacja systemu HD51."')
            cmd = 'chmod 777 /media/neoboot/ImagesUpload/hd51/rootfs.tar.bz2; tar -jxvf /media/neoboot/ImagesUpload/hd51/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('/media/neoboot/ImagesUpload/gigablue'):
            os.system('echo "Instalacja systemu GigaBlue."')
            cmd = 'chmod 777 /media/neoboot/ImagesUpload/gigablue/quad4k/rootfs.tar.bz2; tar -jxvf /media/neoboot/ImagesUpload/gigablue/quad4k/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('/media/neoboot/ImagesUpload/vuplus/solo4k'):
            os.system('echo "Instalacja systemu VuPlus Solo4K."')
            cmd = 'chmod 777 /media/neoboot/ImagesUpload/vuplus/solo4k/rootfs.tar.bz2; tar -jxvf /media/neoboot/ImagesUpload/vuplus/solo4k/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('/media/neoboot/ImagesUpload/vuplus/uno4k'):
            os.system('echo "Instalacja systemu dla modelu VuPlus Uno4K."')
            cmd = 'chmod 777 /media/neoboot/ImagesUpload/vuplus/uno4k/rootfs.tar.bz2; tar -jxvf /media/neoboot/ImagesUpload/vuplus/uno4k/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('/media/neoboot/ImagesUpload/vuplus/uno4kse'):
            os.system('echo "Instalacja systemu VuPlus Uno4kse."')
            cmd = 'chmod 777 /media/neoboot/ImagesUpload/vuplus/uno4kse/rootfs.tar.bz2; tar -jxvf /media/neoboot/ImagesUpload/vuplus/uno4kse/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('/media/neoboot/ImagesUpload/vuplus/zero4k'):
            os.system('echo "Instalacja systemu VuPlus zero4K."')
            cmd = 'chmod 777 /media/neoboot/ImagesUpload/vuplus/zero4k/rootfs.tar.bz2; tar -jxvf /media/neoboot/ImagesUpload/vuplus/zero4k/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('/media/neoboot/ImagesUpload/vuplus/ultimo4k'):
            os.system('echo "Instalacja systemu VuPlus Ultimo4K."')
            cmd = 'chmod 777 /media/neoboot/ImagesUpload/vuplus/ultimo4k/rootfs.tar.bz2; tar -jxvf /media/neoboot/ImagesUpload/vuplus/ultimo4k/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('/media/neoboot/ImagesUpload/update/revo4k'):
            os.system('echo "Instalacja systemu Revo4k."')
            cmd = 'chmod 777 /media/neoboot/ImagesUpload/update/revo4k/rootfs.tar.bz2; tar -jxvf /media/neoboot/ImagesUpload/update/revo4k/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('/media/neoboot/ImagesUpload/update/galaxy4k'):
            os.system('echo "Instalacja systemu Galaxy4k."')
            cmd = 'chmod 777 /media/neoboot/ImagesUpload/update/galaxy4k/rootfs.tar.bz2; tar -jxvf /media/neoboot/ImagesUpload/update/galaxy4k/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('/media/neoboot/ImagesUpload/zgemma/h7'):
            os.system('echo "Instalacja systemu Zgemma H7."')
            cmd = 'chmod 777 /media/neoboot/ImagesUpload/zgemma/h7/rootfs.tar.bz2; tar -jxvf /media/neoboot/ImagesUpload/zgemma/h7/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('/media/neoboot/ImagesUpload/miraclebox/mini4k'):
            os.system('echo "Instalacja systemu Miraclebox mini4k."')
            cmd = 'chmod 777 /media/neoboot/ImagesUpload/miraclebox/mini4k/rootfs.tar.bz2; tar -jxvf /media/neoboot/ImagesUpload/miraclebox/mini4k/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('/media/neoboot/ImagesUpload/miraclebox/ultra4k'):
            os.system('echo "Instalacja systemu Miraclebox ultra4k."')
            cmd = 'chmod 777 /media/neoboot/ImagesUpload/miraclebox/ultra4k/rootfs.tar.bz2; tar -jxvf /media/neoboot/ImagesUpload/miraclebox/ultra4k/rootfs.tar.bz2 -C /media/neoboot/ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        else:
            os.system('echo "NeoBoot wykryl blad !!! Prawdopodobnie brak pliku instalacyjnego."')

    if BlackHole == 'True':
        if 'BlackHole' in source and os.path.exists('%s/ImageBoot/%s/usr/lib/enigma2/python/Blackhole' % (media, target)):
            ver = source.replace('BlackHole-', '')
            try:
                text = ver.split('-')[0]
            except:
                text = ''  
                      
            cmd = 'mkdir /media/neoboot/ImageBoot/%s/boot/blackhole' % target
            rc = os.system(cmd)
            cmd = 'cp -f /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/version /media/neoboot/ImageBoot/%s/boot/blackhole' % target
            rc = os.system(cmd)
            cmd = 'mv /media/neoboot/ImageBoot/%s/usr/lib/enigma2/python/Blackhole/BhUtils.pyo /media/neoboot/ImageBoot/%s/usr/lib/enigma2/python/Blackhole/BhUtils.pyo.org' % (target, target)
            rc = os.system(cmd)
            cmd = 'cp -rf /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/utilsbh /media/neoboot/ImageBoot/%s/usr/lib/enigma2/python/Blackhole/BhUtils.py' % target
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

def RemoveUnpackDirs():
    os.chdir(media + '/ImagesUpload')
    if os.path.exists('/media/neoboot/ImagesUpload/vuplus'):
        rc = os.system('rm -r /media/neoboot/ImagesUpload/vuplus')
    elif os.path.exists('/media/neoboot/ImagesUpload/sf4008'):
        rc = os.system('rm -r /media/neoboot/ImagesUpload/sf4008')
    elif os.path.exists('/media/neoboot/ImagesUpload/dm900'):
        rc = os.system('rm -r /media/neoboot/ImagesUpload/dm900')
    elif os.path.exists('/media/neoboot/ImagesUpload/hd51'):
        rc = os.system('rm -r /media/neoboot/ImagesUpload/hd51')
    elif os.path.exists('/media/neoboot/ImagesUpload/gigablue'):
        rc = os.system('rm -r /media/neoboot/ImagesUpload/gigablue')
    elif os.path.exists('/media/neoboot/ImagesUpload/miraclebox'):
        rc = os.system('rm -r /media/neoboot/ImagesUpload/miraclebox')
    elif os.path.exists('/media/neoboot/ImagesUpload/update'):
        rc = os.system('rm -r /media/neoboot/ImagesUpload/update')
    elif os.path.exists('/media/neoboot/ImagesUpload/rootfs.tar.xz'):
        rc = os.system('rm -r /media/neoboot/ImagesUpload/rootfs.tar.xz')
    elif os.path.exists('/media/neoboot/ImagesUpload/*.nfi'):
        rc = os.system('rm -r /media/neoboot/ImagesUpload/*.nfi')
    elif os.path.exists('/media/neoboot/ImagesUpload/zgemma'):
        rc = os.system('rm -r /media/neoboot/ImagesUpload/zgemma')       
    elif os.path.exists('/media/neoboot/ImagesUpload/formuler1'):
        rc = os.system('rm -r /media/neoboot/ImagesUpload/formuler1')
    elif os.path.exists('/media/neoboot/ImagesUpload/formuler3'):
        rc = os.system('rm -r /media/neoboot/ImagesUpload/formuler3')
    elif os.path.exists('/media/neoboot/ImagesUpload/formuler4turbo'):
        rc = os.system('rm -r /media/neoboot/ImagesUpload/formuler4turbo')                        
    elif os.path.exists('/media/neoboot/ImagesUpload/et*'):
        rc = os.system('rm -r /media/neoboot/ImagesUpload/et*')                
    elif os.path.exists('/media/neoboot/ImagesUpload/xpeedl*'):
        rc = os.system('rm -r /media/neoboot/ImagesUpload/xpeedl*')
    os.system('echo "..........................................."')
    
#END            