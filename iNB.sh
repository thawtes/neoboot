#!/bin/sh
#
#skrypt instaluje neoboot-a
#
if `grep -q 'osd.language=pl_PL' </etc/enigma2/settings`; then
  PL=1
fi
[ -e /tmp/neoboot.zip ] && rm -f /tmp/neoboot.zip
[ -e /tmp/neoboot-master ] && rm -rf /tmp/neoboot-master
[ $PL ] && echo "Pobieranie pliku..." || echo "Downloading the file..."
URL='https://github.com/gutosie/neoboot/archive/master.zip'
curl -kLs $URL  -o /tmp/neoboot.zip
cd /tmp/
unzip -qn ./neoboot.zip
rm -f /tmp/neoboot.zip
#kopiowanie
[ $PL ] && echo "Instalowanie..." || echo "Instaling..."
Cel="/usr/lib/enigma2/python/Plugins/Extensions"
[ -e $Cel/NeoBoot ] && rm -rf $Cel/NeoBoot/* || mkdir -p $Cel/NeoBoot
mv -f /tmp/neoboot-master/NeoBoot/* $Cel/NeoBoot
[ -e /tmp/neoboot-master ] && rm -rf /tmp/neoboot-master
cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; chmod 755 ./bin/*; chmod 755 ./ex_init.py; chmod 755 ./files/targetimage.sh; chmod 755 ./files/NeoBoot.sh; chmod 755 ./files/S50fat.sh; chmod 755 ./bin/rebootbot; cd;                        
chmod -R +x /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ubi_reader/*
if [ $PL ] ; then
  echo ""
  echo "#####################################################"
  echo "#          NEOBOOT ZOSTAL ZAINSTALOWANY             #"
  echo "#####################################################"
  echo "#                ZRESTARTUJ TUNER                   #"
  echo "#####################################################"
  echo ""
else
  echo ""
  echo "#####################################################"
  echo "#          NEOBOOT INSTALLED SUCCESSFULLY           #"
  echo "#####################################################"
  echo "#             PLEASE RESTART YOUR STB               #"
  echo "#####################################################"
  echo ""
fi
exit 0
