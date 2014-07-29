REM signtool signwizard
REM http://timestamp.verisign.com/scripts/timstamp.dll
REM http://nikola.github.io/ka-BOOM/
del dist\ka-BOOM.exe
pyi-build ka-BOOM.spec --distpath=dist --workpath=build --noconfirm --ascii