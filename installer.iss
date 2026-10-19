[Setup]
AppName=Bumbu
AppVersion=0.1.0
AppPublisher=nerdynikhil
DefaultDirName={autopf}\Bumbu
DefaultGroupName=Bumbu
OutputDir=dist
OutputBaseFilename=BumbuSetup
PrivilegesRequired=lowest
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\Bumbu.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\Bumbu"; Filename: "{app}\Bumbu.exe"
Name: "{group}\Uninstall Bumbu"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Bumbu"; Filename: "{app}\Bumbu.exe"; Tasks: desktopicon
Name: "{userstartup}\Bumbu"; Filename: "{app}\Bumbu.exe"; Tasks: startup

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"
Name: "startup"; Description: "Start Bumbu when Windows starts"; Flags: unchecked

[Run]
Filename: "{app}\Bumbu.exe"; Description: "Launch Bumbu"; Flags: nowait postinstall skipifsilent
