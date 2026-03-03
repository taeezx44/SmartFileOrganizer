; ============================================================
;  Smart File Organizer Pro - Inno Setup Installer Script
;  
;  วิธีใช้:
;  1. รัน build_exe.bat ก่อน (สร้าง dist\SmartFileOrganizer\)
;  2. ดาวน์โหลด Inno Setup: https://jrsoftware.org/issetup.php
;  3. เปิดไฟล์นี้ใน Inno Setup Compiler แล้วกด F9
;  4. Setup.exe จะอยู่ใน dist\installer\
; ============================================================

#define MyAppName      "Smart File Organizer Pro"
#define MyAppVersion   "1.0.0"
#define MyAppPublisher "SmartOrganizer"
#define MyAppExeName   "SmartFileOrganizer.exe"
#define MyAppURL       "https://github.com/yourname/SmartFileOrganizer"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; Output installer to dist folder
OutputDir=dist\installer
OutputBaseFilename=SmartFileOrganizer_Setup_v{#MyAppVersion}
; Compression
Compression=lzma2/ultra64
SolidCompression=yes
; Require admin for install
PrivilegesRequired=admin
; Modern wizard style
WizardStyle=modern
; Minimum Windows version: Windows 10
MinVersion=10.0.17763

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon";     Description: "{cm:CreateDesktopIcon}";     GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Main application folder from PyInstaller dist
Source: "dist\SmartFileOrganizer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}";       Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Remove user data folder on uninstall (optional — comment out to keep history)
; Type: filesandordirs; Name: "{userdocs}\SmartFileOrganizer"
