; Script Inno Setup — compile avec build.bat (ou ISCC.exe installer\VidDrop.iss)

#define AppName "VidDrop"
#define AppVersion "1.0.0"
#define WinGet "{localappdata}\Microsoft\WindowsApps\winget.exe"

[Setup]
AppId={{6F1C2A7E-9B3D-4E51-A8C2-VIDDROP00001}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=VidDrop
DefaultDirName={localappdata}\Programs\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=..\build\installer
OutputBaseFilename=VidDrop-Setup-{#AppVersion}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\VidDrop.exe
CloseApplications=yes

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Tasks]
Name: "desktopicon"; Description: "Créer un raccourci sur le Bureau"; GroupDescription: "Raccourcis :"
Name: "deps"; Description: "Installer ffmpeg et Node.js via winget s'ils manquent (YouTube, 1080p, MP3)"; GroupDescription: "Dépendances :"; Check: DepsMissing

[Files]
Source: "..\build\dist\VidDrop\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\VidDrop.exe"
Name: "{group}\Désinstaller {#AppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\VidDrop.exe"; Tasks: desktopicon

[Run]
Filename: "{#WinGet}"; Parameters: "install -e --id Gyan.FFmpeg --silent --accept-package-agreements --accept-source-agreements"; StatusMsg: "Installation de ffmpeg..."; Tasks: deps; Check: not HasTool('ffmpeg.exe'); Flags: runhidden waituntilterminated skipifdoesntexist
Filename: "{#WinGet}"; Parameters: "install -e --id OpenJS.NodeJS.LTS --silent --accept-package-agreements --accept-source-agreements"; StatusMsg: "Installation de Node.js..."; Tasks: deps; Check: not HasTool('node.exe'); Flags: runhidden waituntilterminated skipifdoesntexist
Filename: "{app}\VidDrop.exe"; Description: "Lancer VidDrop"; Flags: nowait postinstall skipifsilent

[Code]
function HasTool(Exe: String): Boolean;
begin
  Result := FileSearch(Exe, GetEnv('PATH')) <> '';
end;

function DepsMissing: Boolean;
begin
  Result := not (HasTool('ffmpeg.exe') and (HasTool('node.exe') or HasTool('deno.exe')));
end;
