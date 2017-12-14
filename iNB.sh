#!/bin/sh
#
#skrypt instaluje neoboot-a
#
[ -e /tmp/neoboot.zip ] && rm -f /tmp/neoboot.zip
[ -e /tmp/neoboot-master ] && rm -rf /tmp/neoboot-master
echo "Downloading the file..."
URL='https://github.com/gutosie/neoboot/archive/master.zip'
curl -kLs $URL  -o /tmp/neoboot.zip
cd /tmp/
unzip -qn ./neoboot.zip
rm -f /tmp/neoboot.zip
#kopiowanie
echo "Instaling..."
Cel="/usr/lib/enigma2/python/Plugins/Extensions"
[ -e $Cel/NeoBoot ] && rm -rf $Cel/NeoBoot/* || mkdir -p $Cel/NeoBoot
mv -f /tmp/neoboot-master/NeoBoot/* $Cel/NeoBoot
[ -e /tmp/neoboot-master ] && rm -rf /tmp/neoboot-master
cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; chmod 755 ./bin/*; chmod 755 ./ex_init.py; chmod 755 ./files/targetimage.sh; chmod 755 ./files/NeoBoot.sh; chmod 755 ./files/S50fat.sh; chmod 755 ./bin/rebootbot; chmod 755 /sbin/neoinit*; cd;                        
chmod -R +x /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ubi_reader/*
echo ""
echo "#####################################################"
echo "#          NEOBOOT INSTALLED SUCCESSFULL            #"
echo "#####################################################"
echo "#             PLEASE RESTART YOUR STB               #"
echo "#####################################################"
echo ""
echo "Potrzebny restart GUI. q(-_-)p Restartuje..."
sleep 5; killall -9 enigma2
exit 0
