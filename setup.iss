[Setup]
; Identificadores únicos do aplicativo
AppId={{5C1D8D27-A845-42FC-80B5-1C906DE4A559}
AppName=Sistema Cãobalhota
AppVersion=1.0
AppPublisher=Pro System
; Pasta padrão de instalação (Arquivos de Programas)
DefaultDirName={autopf}\Cãobalhota
DefaultGroupName=Sistema Cãobalhota
; Ícone do executável (se tiver um, coloque o caminho aqui, senão pode apagar ou comentar essa linha)
; SetupIconFile=assets\icon.ico
; Definindo a pasta onde o instalador final será salvo e o nome do instalador
OutputDir=Instalador
OutputBaseFilename=Instalador_Caobalhota
Compression=lzma
SolidCompression=yes
; Permissões de administrador necessárias
PrivilegesRequired=admin

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Adicione aqui o arquivo executável gerado pelo PyInstaller
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
; Se houver imagens ou o config.ini que precisem ir por padrão, mas como criamos o config.ini auto-gerado, só o main.exe basta!
; Caso precise no futuro: Source: "config.ini"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Atalhos no Menu Iniciar e na Área de Trabalho
Name: "{group}\Sistema Cãobalhota"; Filename: "{app}\main.exe"
Name: "{group}\{cm:UninstallProgram,Sistema Cãobalhota}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Sistema Cãobalhota"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Run]
; Iniciar o sistema depois da instalação
Filename: "{app}\main.exe"; Description: "{cm:LaunchProgram,Sistema Cãobalhota}"; Flags: nowait postinstall skipifsilent
