#!/bin/sh
# script gutosie

if [ ! -e /usr/bin/ipkg ]; then 
   ln -sfn /usr/bin/opkg /usr/bin/ipkg
fi
if [ ! -e /usr/bin/ipkg-cl ]; then 
   ln -sfn /usr/bin/opkg-cl /usr/bin/ipkg-cl
fi

if [ -f /etc/vtiversion.info ] || [ -f /etc/bhversion ] || [ ! -e /boot/zImage.* ]; then
        /etc/init.d/networking stop; sync; /etc/init.d/networking start
fi
                   
if [ -f /etc/init.d/inadyn-mt ] ; then
    /etc/init.d/inadyn-mt start
fi

if [ -f /usr/bin/oscam ] ; then
    if ! ps | grep oscam | grep -v grep ; then 
        /usr/bin/oscam -b 
        echo "START OSCam.."        
    fi
elif [ -f /usr/bin/CCcam ] ; then
    if ! ps | grep CCcam | grep -v grep ; then 
        /usr/bin/CCcam stop || start || restart  
        echo "START CCCam.."
    fi
fi
                                                
if [ -f /home/root/*.tar.gz ] ; then
    /bin/tar -xzvf /home/root/*.tar.gz -C /; rm /home/root/*.tar.gz
fi

if [ ! -e /media/usb ] ; then
        mkdir -p /media/usb
fi

if [ ! -e /media/hdd ] ; then
        mkdir -p /media/hdd 
fi
                                                
mount -a
   
                   
if [ -f /etc/rcS.d/S50fat.sh ] ; then
                            ln -s /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/S50fat.sh /etc/rcS.d/S50neo.sh                                                        
                            telnetd on
                            echo ok  
                            rm -f /etc/rcS.d/S50fat.sh
                            echo "file S50fat.sh delete"  
fi 
echo ok                                                
