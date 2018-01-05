


Wspierane tunery: Wszytkie modele VuPlus - klony też, Octagon SF4008, MiracleBox Mini, Formuler ( Testy- DM900)

NeoBoot nie działa jeszcze w pełni sprawnie w  modelach DM900 i OctagonSF4008 - prace nad ulepszeniem trwają..

Pierwsza instalacja neoboot-a

Uruchom poniższą komendę w terminalu wspieranego tunera:
#

opkg update 

opkg install curl 

curl -kLs https://raw.githubusercontent.com/gutosie/neoboot/master/iNB.sh|sh



#

lub pobrać plik ipk: 

http://www.sat-4-all.com/board/index.php?app=core&module=attach&section=attach&attach_id=11571

wypakować z zip


wkleić do /tmp plik o nazwie NeoBoot-BY-gutosie_20180102-iNB.sh-packed.Lucek_all.ipk

zainstalować poleceniem:

opkg install --force-overwrite /tmp/*.ipk

#
UWAGA!!! 
 Redystrybucja wersji programu i dokonywania modyfikacji JEST DOZWOLONE, pod warunkiem zachowania niniejszej informacji o prawach autorskich. 

Autor NIE ponosi JAKIEJKOLWIEK odpowiedzialności za skutki użytkowania tego programu oraz za wykorzystanie zawartych tu informacji.

Instalację i modyfikacje przeprowadzasz na wlasne ryzyko!!! Przed instalacją lub aktualizacją Neoboot przeczytaj uważnie wszystkie informacje zawarte tu i w wtyczce. !

Dziękuję wszystkim kolegom wpierającym projekt neoboot.

Dziękuję też kolegom wspierającym projekt.

pozdrawiam gutosie




