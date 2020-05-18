import os

_HOMEDIR = os.path.join(
    os.environ['HomeDrive'],
    os.environ['HomePath']
)

INNO_SETUP_PATH = os.path.join(
    _HOMEDIR,
    'AppData\\Local\\Programs\\Inno Setup 6\\ISCC.exe'
)

def main():
    pyinstaller_cmd = 'pyinstaller --onefile eso_addon_manager_gui.spec'
    inno_cmd = f'call "{INNO_SETUP_PATH}" /O"installer" "installer.iss"'
    print(f'>>> {pyinstaller_cmd}')
    os.system(pyinstaller_cmd)
    print(f'>>> {inno_cmd}')
    os.system(inno_cmd)


if __name__ == '__main__':
    main()
