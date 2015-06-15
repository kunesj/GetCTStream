plugin.video.streamct
=====================
!Zatím nefunguje na Androidu!

Kodi plugin pro streamovaní živého vysíláni programu ČT24.

Instalace
---------

1. Stáhni si archiv kodi_plugin.video.streamct.zip (nebo ho vytvoř, viz. Build)
2. Zapni Kodi a v nastavení pod Add-ons zvol nainstalovat Add-on z archivu

Pokud instalace selže:
- Zkus restartovat Kodi
- Může také potřebovat připojení k internetu

Někdy mohou upgrady pluginu potřebovat vyčistit cache: (resetuje nastaveni)
- Windows: smaž %APPDATA%\kodi\userdata
- Linux: smaž ~/.kodi/userdata/

Build (Linux)
-------------
Z kořenového adresáře spusť:

    make build_kodi

Výsledný archiv je ve složce dist
