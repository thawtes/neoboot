#!/bin/sh
# script gutosie

if [ -f /etc/vtiversion.info ] || [ -f /etc/bhversion ] || [ ! -e /boot/zImage.* ]; then
        /etc/init.d/networking stop; sync; /etc/init.d/networking start
fi
                   
if [ -f /etc/init.d/inadyn-mt ] ; then
    /etc/init.d/inadyn-mt start
fi

if [ -f /usr/bin/oscam ] ; then
    if ! ps | grep oscam | grep -v grep ; then /usr/bin/oscam -b; fi
    /etc/init.d/softcam.oscam 
fi

if [ -f /usr/bin/CCcam ] ; then
    /usr/bin/CCcam start
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
                                                
orgimag=`mount | sed '/sd/!d' | cut -d" " -f1`
    for item in $orgimag; do
       ohdd=`echo  $item | cut -d"/" -f3`
       nhdd=`mount | sed "/\$ohdd/!d" | sed q | cut -d" " -f3`

       if [ $nhdd == '/media/hdd' ]; then
           echo $nhdd
           echo "mkdir "$nhdd  >> /etc/init.d/bootup.sh
           echo "mount "$item $nhdd  >> /etc/init.d/bootup.sh
       fi

       if [ $nhdd == '/media/usb' ]; then
           echo $nhdd
           echo "mkdir "$nhdd  >> /etc/init.d/bootup.sh
           echo "mount "$item $nhdd  >> /etc/init.d/bootup.sh                      
       fi

       if [ $nhdd == '/media/neoboot' ]; then
           echo $nhdd
           echo "mkdir "$nhdd  >> /etc/init.d/bootup.sh
           echo "mount "$item $nhdd  >> /etc/init.d/bootup.sh 
       else
           echo "umount "$nhdd  >> /etc/init.d/bootup.sh
           echo "mkdir "$nhdd  >> /etc/init.d/bootup.sh
           echo "mount "$item $nhdd  >> /etc/init.d/bootup.sh 
           echo ok 
       fi    
    done
    
chmod 0755 /etc/init.d/bootup.sh; /etc/init.d/bootup.sh	
mount -a; rm -f /etc/init.d/bootup.sh
echo "file S50fat.sh delete"     
                   
if [ -f /etc/rcS.d/S50fat.sh ] ; then
                            ln -s /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/S50fat.sh /etc/rcS.d/S50neo.sh                                                        
                            telnetd on
                            echo ok  
                            rm -f /etc/rcS.d/S50fat.sh
fi 
echo ok                                                
