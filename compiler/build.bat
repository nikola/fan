REM signtool signwizard
REM http://nikola.github.io/ka-BOOM/
REM http://timestamp.verisign.com/scripts/timstamp.dll
del dist\ka-BOOM.exe
pyi-build ka-BOOM.spec --distpath=dist --workpath=build --noconfirm --ascii