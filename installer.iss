#define MyAppName "The Great Feast Notifier"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Luiz Prado"
#define MyAppExeName "TheGreatFeastNotifier.exe"

[Setup]
AppId=TheGreatFeastNotifier
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

OutputDir=installer
OutputBaseFilename=TheGreatFeastNotifierSetup

SetupIconFile=Atlas\hypixel.ico

UninstallDisplayIcon={app}\{#MyAppExeName}

Compression=lzma
SolidCompression=yes

WizardStyle=modern

[Files]
Source: "dist\TheGreatFeastNotifier\*"; \
    DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs
    
[Icons]
Name: "{autoprograms}\{#MyAppName}"; \
    Filename: "{app}\{#MyAppExeName}"; \
    WorkingDir: "{app}"; \
    Tasks: startmenu

Name: "{autodesktop}\{#MyAppName}"; \
    Filename: "{app}\{#MyAppExeName}"; \
    WorkingDir: "{app}"; \
    Tasks: desktopicon
    
[Tasks]
Name: "startmenu"; \
    Description: "Create a &Start Menu shortcut"; \
    GroupDescription: "Shortcuts:"

Name: "desktopicon"; \
    Description: "Create a &desktop shortcut"; \
    GroupDescription: "Shortcuts:"; \
    Flags: unchecked
    
[Run]
Filename: "{app}\{#MyAppExeName}"; \
    Description: "Launch {#MyAppName}"; \
    Flags: nowait postinstall skipifsilent