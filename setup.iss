; NeuroFriend all-in-one Windows installer
#define MyAppName "NeuroFriend"
#define MyAppVersion "2.1.0"
#define MyAppPublisher "V1per-Mods"
[Setup]
AppId={{D8B6F7B0-2D25-4CB7-AC2A-3CBA6B6C2A10}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\NeuroFriend
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=dist
OutputBaseFilename=NeuroFriend-Setup
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
UninstallDisplayIcon={app}\NeuroFriend.exe
SetupLogging=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "dist\NeuroFriend.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "bundle\runtime\*"; DestDir: "{app}\runtime"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "bundle\models\Qwen2.5-3B-Instruct-Q4_K_S.gguf"; DestDir: "{app}\models"; Flags: ignoreversion
Source: "THIRD_PARTY_NOTICES.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\NeuroFriend"; Filename: "{app}\NeuroFriend.exe"
Name: "{autodesktop}\NeuroFriend"; Filename: "{app}\NeuroFriend.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\NeuroFriend.exe"; Description: "Launch NeuroFriend"; Flags: postinstall nowait skipifsilent
