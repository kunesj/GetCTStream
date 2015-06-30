GetCTStream
===========

Python script pro získání streamů živého vysíláni programů České Televize. Také obsahuje plugin do přehrávače Kodi.

Příklady použití:

    getctstream --kanal ct1 # vypíše adresy streamů pro kanál ČT1
    getctstream --mpv # automaticky otevře získaný stream ČT24 v přehrávači mpv 
    getctstream --playerpath /usr/bin/cvlc # automaticky otevře získaný stream ČT24 v přehrávači cvlc
    getctstream -k ctsport --mpv --qualityid -1 # automaticky otevře získaný stream ČT Sport s nejvyssí kvalitou v přehrávači mpv 

Pro výpis možných kanálů:

    getctstream --kanal help
    
Informace o dalších parametrech příkazové řádky:

    getctstream --help
    
Pro použítí parametrů --mpv --mplayer --vlc musí přehrávače spustitelené z příkazové řádky (Path).

Instalace/Spuštění
------------------
Potřebuje nainstalované Python2 a Python balíky BeautifulSoup a requests

1. Instalace Python balíku (Linux)

    Automatická instalace potřebných knihoven atd.. (Pouze Debian)
    ```
    make install_dep_debian
    ```
    Installace aplikace:
    ```
    make install
    ```
    Nyní může skript spuštěn přímo z příkazové řádky:
    ```
    getctstream
    ```

2. Alternativně je možné po ruční installaci potřebných balíků spustit samostatný skript pomocí: (z kořenové složky)
    ```
    python -m getctstream
    ```
    
3. Kodi plugin

    Přečti si [Kodi/KODI_README.md](https://github.com/kunesj/kodi-plugin.video.streamct/blob/master/Kodi/KODI_README.md)

Build pluginy atd.
------------------

1. Kodi plugin

    ```
    make build_kodi
    ```
