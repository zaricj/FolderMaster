from pathlib import Path

def fix_qrc_import() -> None:
    file_path = Path("src") / "assets" / "gui" / "ui" / "ui_FolderMaster.py"
    err_import = "import FolderMaster_rc"
    ok_import = "from . import qrc_FolderMaster"
    
    if not file_path.exists():
        print("File does not exist!")
        return

    print("Starting to fix import!")
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    modified = False
    for idx, line in enumerate(lines):
        if err_import in line and ok_import not in line:
            lines[idx] = line.replace(err_import, ok_import)
            modified = True
            break
        if idx >= 30:
            break

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print("Pre-flight check: Fixed UI layout resource imports successfully.")

fix_qrc_import()