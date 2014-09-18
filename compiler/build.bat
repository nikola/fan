REM https://forum.startcom.org/viewtopic.php?f=15&t=1654&st=0&sk=t&sd=a
REM signtool signwizard
REM ka-BOOM.exe
REM A movie compilation and playback app for Windows.
REM https://github.com/nikola/ka-BOOM
REM http://timestamp.verisign.com/scripts/timstamp.dll
del dist\ka-BOOM.exe
pyi-build ka-BOOM.spec --distpath=dist --workpath=build --noconfirm --ascii