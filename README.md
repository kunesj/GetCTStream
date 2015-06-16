GetCTStream
===========

Python script pro získání streamů živého vysíláni programů České Televize. Také obsahuje plugin do přehrávače Kodi.

Příklady použití:

    python get_ct_stream.py --kanal ct1 # vypíše adresy streamů pro kanál ČT1
    python get_ct_stream.py --mpv # automaticky otevře získaný stream ČT24 v přehrávači mpv 
    python get_ct_stream.py --playerpath /usr/bin/cvlc # automaticky otevře získaný stream ČT24 v přehrávači cvlc

Informace o dalších parametrech příkazové řádky:

    python get_ct_stream.py --help
    
Pro použítí parametrů --mpv --mplayer --vlc musí přehrávače spustitelené z příkazové řádky (Path).

Instalace/Spuštění
------------------
Potřebuje nainstalované Python2 a Python balíky BeautifulSoup a requests

1. Samostatný skript lze spustit pomocí

    python get_ct_stream.py

2. Kodi plugin

    Přečti si [Kodi/KODI_README.md](https://github.com/kunesj/kodi-plugin.video.streamct/blob/master/Kodi/KODI_README.md)

Build
-----
Výsledné archivy jsou vždy ve složce dist

1. Kodi plugin

    make build_kodi

