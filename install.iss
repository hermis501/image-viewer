#define MyAppName "Image Viewer"
#define MyAppVersion "1.0.6"
#define MyAppPublisher "Hermis Kasperavičius"
#define MyAppURL "http://hermisk.eu"
#define MyAppExeName "ImageViewer.exe"

[Setup]
AppId={{803D2270-256F-452E-AFC2-3F6962F945E4}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\ImageViewer
DefaultGroupName={#MyAppName}
; OutputDir=
OutputBaseFilename=image_viewer-setup
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=no
AllowNoIcons=yes
ChangesAssociations=yes
InfoBeforeFile="dist\imageViewer\changes.txt"
InfoAfterFile="dist\imageViewer\ReadMe.txt"

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: association; Description: "Associate jpg and png file types with Image Viewer"; GroupDescription: "File associations"

[Files]
Source: "dist\imageviewer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{group}\Readme"; Filename: {app}\ReadMe.txt

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, "&", "&&")}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: dirifempty; Name: "{app}"

[Registry]
Root: HKA; Subkey: "Software\Classes\.jpg"; ValueType: string; ValueName: ""; ValueData: "Image Viewer"; Flags: uninsdeletevalue; Tasks: association
Root: HKA; Subkey: "Software\Classes\.png"; ValueType: string; ValueName: ""; ValueData: "Image Viewer"; Flags: uninsdeletevalue; Tasks: association
Root: HKA; Subkey: "Software\Classes\Image Viewer"; ValueType: string; ValueName: ""; ValueData: "Image file"; Flags: uninsdeletekey; Tasks: association
Root: HKA; Subkey: "Software\Classes\Image Viewer\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\imageViewer.exe"" ""%1"""; Tasks: association

[Code]
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    if MsgBox('Do You Want To Delete settings?', mbConfirmation, MB_YESNO or MB_DEFBUTTON2) = IDYES then
    begin
        DelTree(ExpandConstant('{userappdata}\imageviewer'), True, True, True);
    end;
  end;
end;
