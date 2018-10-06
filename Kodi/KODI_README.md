plugin.video.streamct
=====================
Kodi plugin pro streamovaní živého vysíláni programů České Televize.

VAROVÁNÍ: Kodi plugin ještě nebyl vyzkoušen/aktualizován na nejnovější verzy! Nemusí fungovat.

Instalace
---------

1. Stáhni si archiv [get_ct_stream_kodi.zip](https://github.com/kunesj/GetCTStream/releases) a extrahuj z něho plugin.video.streamct.zip
2. Zapni Kodi a v nastavení pod Add-ons zvol nainstalovat Add-on z archivu a zadej plugin.video.streamct.zip

Pokud instalace selže:
- Zkus restartovat Kodi
- Může také potřebovat připojení k internetu

Někdy mohou upgrady pluginu potřebovat vyčistit cache: (resetuje nastaveni)
- Windows: smaž %APPDATA%\kodi\userdata
- Linux: smaž ~/.kodi/userdata/

Problémy na Androidu
--------------------
Zařízení na kterém je Kodi nainstalován nemusí někdy podporovat formát streamu. Projeví se to tím že Kodi po spuštění streamu téměř okamžitě spadne ([Bug #1](https://github.com/kunesj/GetCTStream/issues/1)). Tento problém se dá vyřešit vypnutím hardwarové accelerace v nastavení.

```
Settings level: Expert

Settings -> Videos -> Acceleration
MediaCodec: Off
libstagefright: Off
```
