#!/bin/sh
#script - gutosie 
    #SF4008:           bcm7251
    #MBmini:           bcm7358
    #Miraclebox Micro: bcm7362
    #Ultimo4k:         7444s
    #Solo4k:           7376
    #Uno 4K:           7252s 
    #Ultimo   :        7405(with 3D)
    #Uno      :        7405(with 3D)
    #Solo2    :        7356
    #Duo2     :        7424
    #Duo      :	       7335      
    #Solose-v2:        7241
    #Solo     :        7325
    #Zero     :        7362 

KERNEL=`uname -r` 
IMAGE=/media/neoboot/ImageBoot
IMAGENEXTBOOT=/media/neoboot/ImageBoot/.neonextboot
BOXNAME=$( cat /etc/hostname)   

#sprawdzenie modelu vu+
if [ -f /proc/stb/info/vumodel ];  then  
    VUMODEL=$( cat /proc/stb/info/vumodel )     
fi

#sprawdzenie boxtype 
if [ -f /proc/stb/info/boxtype ];  then  
    BOXTYPE=$( cat /proc/stb/info/boxtype )    
fi

#sprawdzenie typu chipa 
if [ -f /proc/stb/info/chipset ];  then  
    CHIPSET=$( cat /proc/stb/info/chipset )    
fi

#sprawdzenie wybranego systemu do rozruchu
if [ -f $IMAGENEXTBOOT ]; then
  TARGET=`cat $IMAGENEXTBOOT`
else
  TARGET=Flash
fi

#kasowanie pliku jesli istnieje
if [ -f /tmp/zImage.ipk ];  then  
    rm -f /tmp/zImage.ipk    
fi
if [ -f /tmp/zImage ];  then  
    rm -f /tmp/zImage    
fi

if [ $TARGET = "Flash" ]; then                    
                if [ -e /.multinfo ]; then                    
                    if [ $VUMODEL = "ultimo4k" ] || [ $VUMODEL = "solo4k" ] || [ $VUMODEL = "uno4k" ] || [ $VUMODEL = "uno4kse" ] || [ $VUMODEL = "zero4k" ]; then                         
                            if [ -f /proc/stb/info/vumodel ]; then
                                if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk ] ; then
                                    dd if=/media/neoboot/ImagesUpload/.kernel/flash-kernel-$VUMODEL.bin of=/dev/mmcblk0p1
                                    cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk /tmp/zImage.ipk                                    
                                    opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk
                                fi                                                   
                            fi
                    elif [ $CHIPSET = "7356" ] || [ $CHIPSET = "7424" ] || [ $CHIPSET = "7241" ] || [ $CHIPSET = "7362" ] ; then 
                            if [ -f /proc/stb/info/vumodel ]; then
                                if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk ] ; then
                                    cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk /tmp/zImage.ipk                                    
                                    opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk
                                elif [ -e /media/neoboot/ImagesUpload/.kernel/vmlinux.gz ] ; then
                                    flash_eraseall /dev/mtd2                  
		                    nandwrite -p /dev/mtd2 //media/neoboot/ImagesUpload/.kernel/vmlinux.gz 
                                    update-alternatives --remove vmlinux vmlinux-$KERNEL || true

                                fi                            
                            fi                        
                    elif [ $CHIPSET = "7335" ] || [ $CHIPSET = "7325" ] || [ $CHIPSET = "7405(with 3D)" ]; then 
                            if [ -f /proc/stb/info/vumodel ]; then
                                if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk ] ; then
                                    cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk /tmp/zImage.ipk                                    
                                    opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk
                                elif [ -e /media/neoboot/ImagesUpload/.kernel/vmlinux.gz ] ; then
                                    flash_eraseall /dev/mtd1                  
		                    nandwrite -p /dev/mtd1 //media/neoboot/ImagesUpload/.kernel/vmlinux.gz 
                                    update-alternatives --remove vmlinux vmlinux-$KERNEL || true

                                fi                            
                            fi 
                    fi
                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true                                          
                    echo "NEOBOOT is booting image from " $TARGET
                    echo "Used Kernel: " $TARGET > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                    sleep 5; /etc/init.d/reboot

                else
                        if [ ! -e /media/neoboot/ImagesUpload/.kernel/used_flash_kernel ]; then
                            if [ $VUMODEL = "ultimo4k" ] || [ $VUMODEL = "solo4k" ] || [ $VUMODEL = "uno4k" ] || [ $VUMODEL = "uno4kse" ] || [ $VUMODEL = "zero4k" ]; then                         
                                if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk ] ; then
                                    dd if=/media/neoboot/ImagesUpload/.kernel/flash-kernel-$VUMODEL.bin of=/dev/mmcblk0p1
                                    cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk /tmp/zImage.ipk
                                    opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk                                
                                fi
                            elif [ $CHIPSET = "7335" ] || [ $CHIPSET = "7325" ] || [ $CHIPSET = "7405(with 3D)" ]; then                     
                                if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk ] ; then
                                    cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk /tmp/zImage.ipk                                    
                                    opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk
                                elif [ -e /media/neoboot/ImagesUpload/.kernel/vmlinux.gz ] ; then
                                    flash_eraseall /dev/mtd1                  
		                    nandwrite -p /dev/mtd1 //media/neoboot/ImagesUpload/.kernel/vmlinux.gz 
                                    update-alternatives --remove vmlinux vmlinux-$KERNEL || true
                                fi                            
                                
                            elif [ $CHIPSET = "7356" ] || [ $CHIPSET = "7424" ] || [ $CHIPSET = "7241" ] || [ $CHIPSET = "7362" ]; then 
                                if [ -e /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk ] ; then
                                    cp -fR /media/neoboot/ImagesUpload/.kernel/zImage.$VUMODEL.ipk /tmp/zImage.ipk                                    
                                    opkg install --force-reinstall --force-overwrite --force-downgrade --nodeps /tmp/zImage.ipk
                                elif [ -e /media/neoboot/ImagesUpload/.kernel/vmlinux.gz ] ; then
                                    flash_eraseall /dev/mtd2                  
		                    nandwrite -p /dev/mtd2 //media/neoboot/ImagesUpload/.kernel/vmlinux.gz 
                                    update-alternatives --remove vmlinux vmlinux-$KERNEL || true

                                fi                            
                            fi
                            
                            update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                            echo "Used Kernel: " $TARGET > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                            echo " NEOBOOT - zainstalowano kernel-image - " $TARGET  "Za chwile nastapi restart systemu !!!"
                            sleep 5 ; /etc/init.d/reboot

                        else                            
                            echo " NEOBOOT Start sytem - " $TARGET  "Za chwile nastapi restart !!!"
                            sleep 5; /etc/init.d/reboot
                        fi
                fi
else
              	    
    if [ -f /proc/stb/info/vumodel ]; then
            if [ $VUMODEL = "ultimo4k" ] || [ $VUMODEL = "solo4k" ] || [ $VUMODEL = "uno4k" ] || [ $VUMODEL = "uno4kse" ] || [ $VUMODEL = "zero4k" ]; then 
                        if [ -e /.multinfo ] ; then
                                INFOBOOT=$( cat /.multinfo )
                                if [ $TARGET = $INFOBOOT ] ; then
                                    echo "NEOBOOT is booting image from " $TARGET
                                    sleep 5; /etc/init.d/reboot
                                else                                              
                                    cp -f $IMAGE/$TARGET/boot/zImage.$VUMODEL /tmp/zImage
                                    dd if=/tmp/zImage of=/dev/mmcblk0p1 
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " VUPLUS z procesorem arm zostal zmieniony!!!"
                                    echo "Used Kernel: " $TARGET   > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                    sleep 5; /etc/init.d/reboot                              
                                fi
                        else              
                                    cp -fR $IMAGE/$TARGET/boot/zImage.$VUMODEL /tmp/zImage
                                    dd if=/tmp/zImage of=/dev/mmcblk0p1 
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " VU+ zmieniony."
                                    echo "Za chwile nastapi restart systemu..."
                                    echo "Used Kernel: " $TARGET  > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                    sleep 5; /etc/init.d/reboot
                        fi
                        
            elif [ $CHIPSET = "7356" ] || [ $CHIPSET = "7424" ] || [ $CHIPSET = "7241" ] || [ $CHIPSET = "7362" ]; then	     
                        if [ -e /.multinfo ] ; then
                                INFOBOOT=$( cat /.multinfo )
                                if [ $TARGET = $INFOBOOT ] ; then
                                    echo "NEOBOOT is booting image from " $TARGET
                                    sleep 3; /etc/init.d/reboot
                                else                                  
                                    cp -f $IMAGE/$TARGET/boot/$VUMODEL.vmlinux.gz /tmp/vmlinux.gz 
                                    flash_eraseall /dev/mtd2
		                    nandwrite -p /dev/mtd2 //tmp/vmlinux.gz 
		                    rm -f //tmp/vmlinux.gz
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " z procesorem mips zostal zmieniony!!!"
                                    echo "Used Kernel: " $TARGET   > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                    sleep 3; /etc/init.d/reboot 
                                fi
                        else
                                    cp -f $IMAGE/$TARGET/boot/$VUMODEL.vmlinux.gz /tmp/vmlinux.gz
                                    flash_eraseall /dev/mtd2                                    
		                    nandwrite -p /dev/mtd2 /tmp/vmlinux.gz 
		                    rm -f /tmp/vmlinux.gz
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " z procesorem mips zostal zmieniony!!!"
                                    echo "Used Kernel: " $TARGET   > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                    sleep 3; /etc/init.d/reboot
                        fi

            elif [ $CHIPSET = "7424" ] || [ $CHIPSET = "7325" ] || [ $CHIPSET = "7405(with 3D)" ]; then	     
                        if [ -e /.multinfo ] ; then
                                INFOBOOT=$( cat /.multinfo )
                                if [ $TARGET = $INFOBOOT ] ; then
                                    echo "NEOBOOT is booting image from " $TARGET
                                    sleep 5; /etc/init.d/reboot
                                else                                    
                                    cp -fR $IMAGE/$TARGET/boot/$VUMODEL.vmlinux.gz /tmp/vmlinux.gz
                                    flash_eraseall /dev/mtd1
		                    nandwrite -p /dev/mtd1 //tmp/vmlinux.gz  
		                    rm -f /tmp/vmlinux.gz
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " z procesorem mips zostal zmieniony!!!"
                                    echo "Used Kernel: " $TARGET   > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                    sleep 5; /etc/init.d/reboot 
                                fi
                        else
                                    cp -fR $IMAGE/$TARGET/boot/$VUMODEL.vmlinux.gz /tmp/vmlinux.gz
                                    flash_eraseall /dev/mtd1
		                    nandwrite -p /dev/mtd1 /tmp/vmlinux.gz  
                                    rm -f /tmp/vmlinux.gz                                    
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " z procesorem mips zostal zmieniony!!!"
                                    echo "Used Kernel: " $TARGET   > /media/neoboot/ImagesUpload/.kernel/used_flash_kernel
                                    echo "Typ procesora: " $CHIPSET " STB"   
                                    sleep 20; /etc/init.d/reboot 
                        fi

            else
                    echo "$TARGET "  > /media/neoboot/ImageBoot/.neonextboot
                    echo "Error - Is not stb model vuplus or OctagonSF4008 !!! "
                    exit 0
            fi
    else
                 echo "Is not stb model vuplus or Octagonsf4008 !!!"
                 exit 0

    fi
fi
exit 0
