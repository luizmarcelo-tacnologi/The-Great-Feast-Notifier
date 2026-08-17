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
Source: "dist\{#MyAppExeName}"; \
    DestDir: "{app}"; \
    Flags: ignoreversion
    
[Icons]
Name: "{autoprograms}\{#MyAppName}"; \
    Filename: "{app}\{#MyAppExeName}"; \
    WorkingDir: "{app}"; \
    Tasks: startmenu

Name: "{autodesktop}\{#MyAppName}"; \
    Filename: "{app}\{#MyAppExeName}"; \
    WorkingDir: "{app}"; \
    Tasks: desktopicon
    
Name: "{autostartup}\{#MyAppName}"; \
    Filename: "{app}\{#MyAppExeName}"; \
    WorkingDir: "{app}"; \
    Tasks: startup
    
[Tasks]
Name: "startmenu"; \
    Description: "Create a &Start Menu shortcut"; \
    GroupDescription: "Shortcuts:"

Name: "desktopicon"; \
    Description: "Create a &desktop shortcut"; \
    GroupDescription: "Shortcuts:"; \
    Flags: unchecked
    
Name: "startup"; \
    Description: "Start {#MyAppName} with Windows"; \
    GroupDescription: "Startup options:"
    
[Run]
Filename: "{app}\{#MyAppExeName}"; \
    Description: "Launch {#MyAppName}"; \
    Flags: nowait postinstall skipifsilent