#!/bin/sh
#
#skrypt instaluje neoboot-a
#
[ -e /tmp/neoboot.zip ] && rm -f /tmp/neoboot.zip
[ -e /tmp/neoboot-master ] && rm -rf /tmp/neoboot-master
URL='https://github.com/gutosie/neoboot/archive/master.zip'
curl -kLs $URL  -o /tmp/neoboot.zip
cd /tmp/
unzip -qn ./neoboot.zip
rm -f /tmp/neoboot.zip
#kopiowanie
Cel="/usr/lib/enigma2/python/Plugins/Extensions"
[ -e $Cel/NeoBoot ] && rm -rf $Cel/NeoBoot/* || mkdir -p $Cel/NeoBoot
mv -f /tmp/neoboot-master/NeoBoot/* $Cel/NeoBoot
[ -e /tmp/neoboot-master ] && rm -rf /tmp/neoboot-master
cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; chmod 0755 ./bin/*; chmod 0755 ./ex_init.py; chmod 0755 ./files/targetimage.sh; chmod 0755 ./files/checkpoint.sh; chmod 0755 ./files/NeoBoot.sh; chmod 0755 ./files/S50fat.sh; chmod 0755 /files/S51checkpoint.sh; chmod 0755 ./bin/rebootbot; cp /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinit* /sbin; cd;                        
chmod -R +x /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ubi_reader/*
echo "NeoBoot zainstalowany!!!"
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
