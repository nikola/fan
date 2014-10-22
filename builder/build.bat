REM A movie compilation and playback app for Windows.
REM https://github.com/nikola/fan
REM signtool signwizard
REM http://timestamp.verisign.com/scripts/timstamp.dll
del dist\fan.exe
pyi-build fan.spec --distpath=dist --workpath=build --noconfirm --ascii