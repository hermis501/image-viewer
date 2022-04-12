#NoTrayIcon
#Include <misc.au3>
if fileexists (@tempdir&"\image_viewer-setup.exe")=0 then exit
do
sleep (200)
until not processexists ("imageviewer.exe")
local $f=fileopen (@tempdir&"\imgviewer_upd.bat", 2)
filewrite ($f, "taskkill /F /IM imageviewer.exe")
filewrite ($f, @crlf)
filewrite ($f, 'start /wait /d '&@tempdir&' image_viewer-setup.exe /SILENT /NOCANCEL /FORCECLOSEAPPLICATIONS /DIR="'&@scriptdir&'"')
filewrite ($f, @crlf)
filewrite ($f, 'del '&@tempdir&'\image_viewer-setup.exe')
filewrite ($f, @crlf)
filewrite ($f, 'start /d "'&@scriptdir&'" imageviewer.exe')
filewrite ($f, @crlf)
filewrite ($f, 'del '&@tempdir&'\imgviewer_upd.bat')
fileclose ($f)
run (@tempdir&"\imgviewer_upd.bat", "", @sw_hide)
