


Wspierane tunery: Wszytkie modele VuPlus - klony też, Octagon SF4008, MiracleBox Mini, Formuler, Edison Mini OS ( Testy- DM900)

NeoBoot nie działa jeszcze w pełni sprawnie w  modelach DM900 i OctagonSF4008 - prace nad ulepszeniem trwają..

Pierwsza instalacja neoboot-a

Uruchom poniższą komendę w terminalu wspieranego tunera:
#

opkg update 

opkg install curl 

curl -kLs https://raw.githubusercontent.com/gutosie/neoboot/master/iNB.sh|sh
#

Inny sposób na zainstalkowanie, jeśli narzędzie curl nie zadziała poprawnie, to proszę spróbować polecenia :

cd /tmp

wget https://raw.githubusercontent.com/gutosie/neoboot/master/iNB.sh

/tmp/iNB.sh
#

UWAGA!!! 
 Redystrybucja wersji programu i dokonywania modyfikacji JEST DOZWOLONE, pod warunkiem zachowania niniejszej informacji o prawach autorskich. 

Autor NIE ponosi JAKIEJKOLWIEK odpowiedzialności za skutki użytkowania tego programu oraz za wykorzystanie zawartych tu informacji.

Instalację i modyfikacje przeprowadzasz na wlasne ryzyko!!! Przed instalacją lub aktualizacją Neoboot przeczytaj uważnie wszystkie informacje zawarte tu i w wtyczce. !

Dziękuję wszystkim kolegom wpierającym projekt neoboot.

Dziękuję też kolegom wspierającym projekt.

pozdrawiam gutosie




