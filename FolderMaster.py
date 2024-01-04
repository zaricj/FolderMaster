import PySimpleGUI as sg
from os.path import isfile, join
from os import listdir
import shutil,os,sys
import datetime as dt
from pathlib import Path


# ------Variables------
font = ("Arial", 14)
python_executable_path = sys.executable

# ------Function------
def create_folder(source,folder_name):
    try:
        path = os.path.join(source,folder_name)
        os.mkdir(path)
    except FileExistsError:
        print(">>> ERROR: Folder already exsists!")

# ---- Listing files in Directory ---- #
def list_all_files_in_directory(watchingPath: str):
    try:
        allFiles = [f for f in os.listdir(watchingPath) if isfile(join(watchingPath,f))]
        none_list = "\n".join(allFiles)
        window["-OUTPUT_WINDOW-"].update(">>> Listing all Files:\n")
        return(none_list)
    except FileNotFoundError as e:
            window["-OUTPUT_WINDOW-"].update(f">>> Exception Error!\n{e}")
            
#def move_files_to_folder(source,destination):
#    
#    onlyfiles = [f for f in listdir(source) if isfile(join(source, f))]
#    for file in onlyfiles:
#        shutil.move(f"{source}/{file}",destination)
#        window["-OUTPUT_WINDOW-"].update(f"Moved files(s): {file} to destination {destination}")
        
#---- Function for moving all or set filetype files to a new destination with the Move Button ----#
def moving_selected_filetype(ends_with: str, destination: str, source: str):
    try:
        for file in os.listdir(source):
            if file.endswith(ends_with):
                shutil.move(os.path.join(source,file), os.path.join(destination,file))
                window["-OUTPUT_WINDOW-"].update(f"Moved Files: {file}")
            elif ends_with == "all":
                shutil.move(os.path.join(source,file), os.path.join(destination,file))
    except FileNotFoundError as e:
            window["-OUTPUT_WINDOW-"].update(f">>> Exception Error!\n{e}")

def organize_files(organize_option, source):
    try:
        for file in os.listdir(source):
            if file.endswith(".jpg") or file.endswith(".png") and organize_option == "Images":
                create_folder(os.path.join(source, "Images"))
                shutil.move(os.path.join(source, file), os.path.join(source, "Images", file))
            elif file.endswith(".docx") or file.endswith(".pdf") or file.endswith(".xls") or file.endswith(".xlsx") or file.endswith(".xml") and organize_option == "Documents":
                create_folder(os.path.join(source, "Documents"),)
                shutil.move(os.path.join(source, file), os.path.join(source, "Documents", file))
            elif file.endswith(".zip") or file.endswith(".rar") or file.endswith(".pak") and organize_option == "Archives":
                create_folder(os.path.join(source, "Archives"))           
                shutil.move(os.path.join(source, file), os.path.join(source, "Archives", file))
            elif file.endswith(".mp4") or file.endswith(".avi") and organize_option == "Videos":
                create_folder(os.path.join(source, "Videos"))
                shutil.move(os.path.join(source, file), os.path.join(source, "Videos", file))
            elif file.endswith(".mp3") or file.endswith(".wav") and organize_option == "Audio":
                create_folder(os.path.join(source, "Audios"),"Audio")
                shutil.move(os.path.join(source, file), os.path.join(source, "Audio", file))
    except Exception as e:
        window["-OUTPUT_WINDOW-"].update(f">>> Exception Error!\n{e}")

def file_type(ends_with: str, source: str):
    sourcefiles = os.listdir(source)
    for file in sourcefiles:
        if file.endswith(ends_with):
            window["-OUTPUT_WINDOW-"].print(os.path.join(file))

# -------GUI------
# Add your new theme colors and settings
my_new_theme = {"BACKGROUND": "#1c1e23",
                "TEXT": "#d2d2d3",
                "INPUT": "#3d3f46",
                "TEXT_INPUT": "#d2d2d3",
                "SCROLL": "#3d3f46",
                "BUTTON": ("#ff793f", "#313641"),
                "PROGRESS": ("#ff793f", "#4a6ab3"),
                "BORDER": 1,
                "SLIDER_DEPTH": 0,
                "PROGRESS_DEPTH": 0}
# Add your dictionary to the PySimpleGUI themes
sg.theme_add_new("MyTheme", my_new_theme)
# Switch your theme to use the newly added one. You can add spaces to make it more readable
sg.theme("MyTheme")

combo_list = ["all",".xls",".xlsx",".docx",".pak",".csv",".xml",".zip",".pdf",".txt",".jar",".jpg",".png",".icon",".mp4",".avi",".wav"]
organize_options = ["Images", "Documents", "Archives", "Videos", "Audio"]

layout_title = [[sg.Text("Folder Master",font="Arial 20 bold underline",text_color="#ff793f")]]
layout_time = [[sg.Text("Clock: "),sg.StatusBar("", size=(25, 1), key="-STATUSBAR-")]]
layout_end_buttons = [[sg.Button("Clear Output", key="-CLEAR_OUTPUT-"),sg.Text("|"),sg.Button("update", key="-update_FUNC-"),sg.Button("Exit")]]
layout_outputwindow = [[sg.Multiline(size=(59, 10), key="-OUTPUT_WINDOW-")]]
layout_main = [
    [sg.Text("Select Source Folder:"),sg.Input(default_text="Search for a Folder",key="-INPUT_PATH-",size=(33,1)),sg.FolderBrowse()],
    [sg.Text("Select Destination Folder:"),sg.Input(key="-OUTPUT_PATH-",size=(30,1)),sg.FolderBrowse()],
    [sg.Text("Create new Folder in Destination Folder:"),sg.Input(default_text="New folder",size=(13,1),key="-FOLDER_NAME-"),sg.Button("Create",key="-CREATE_FOLDER-")],
    [sg.Text("Select a specific file type to list or move:"),sg.Combo(combo_list, default_value= "all", size=(10, 5),key="-EXTENSION_TYPE-"),sg.Button("List Files",size=(8,1),key="-LIST_FILES-",tooltip="List all Files that the Folder Observer is watching.")],
    [sg.Text("Do you want to move file(s):"),sg.Button("Move File(s)",key="-MOVE_BUTTON-"),sg.Button("Switch Src/Dest",key="-SWITCH_OUTPUTS-")]]
layout_organize = [[sg.Text("Optional: Automatic File Organization")],
    [sg.Text("Select Organization Option:"), sg.Combo(organize_options, key="-ORGANIZE_OPTION-", size=(20, 1)),sg.Button("Organize", key="-ORGANIZE_BUTTON-" ,tooltip="Organize files based on selected option")]]

layout = [[sg.Column(layout_title,expand_x="left"),sg.VSeparator(),sg.Column(layout_time,element_justification="right")],
          [sg.Frame("Main Shit",layout_main)],
          [sg.Frame("Organize Shit",layout_organize)],
          [sg.Column(layout_outputwindow)],
          [sg.Column(layout_end_buttons)]]

window = sg.Window("Die Miesische Magmuschel", layout, font=font)

while True:
    event, values = window.read(timeout=1000)  # Add a timeout to allow periodic updates
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    
    # VARIABLES
    running = True
    new_folder = True
    source = values["-INPUT_PATH-"]
    destination = values["-OUTPUT_PATH-"]
    folder_name = values["-FOLDER_NAME-"]
    ends_with = values["-EXTENSION_TYPE-"]

    # EVENT HANDLING
    if running:
        time_now = dt.datetime.now().strftime("%x %H:%M:%S")
        window["-STATUSBAR-"].update(time_now)
        
    if event == "-CREATE_FOLDER-":
        if len(destination) == 0:
            window["-OUTPUT_WINDOW-"].update(">>> ERROR: No Destination Folder selected!")
        elif len(folder_name) == 0:
            window["-OUTPUT_WINDOW-"].update(">>> ERROR: No Folder name set.")
        elif len(destination) > 0 and len(folder_name) > 0:
            window.perform_long_operation(lambda: create_folder(destination,folder_name),"-OUTPUT_WINDOW-")
            window["-OUTPUT_PATH-"].update(f"{destination}{folder_name}")
    
    if event == "-ORGANIZE_BUTTON-":
        organize_option = values["-ORGANIZE_OPTION-"]
        if len(source) > 0 and len(organize_option) > 0:
            window.perform_long_operation(lambda: organize_files(organize_option, source), "-OUTPUT_WINDOW-")
        elif len(source) == 0 and len(organize_option) > 0:
            window["-OUTPUT_WINDOW-"].update(">>> ERROR: Please select source folder.")
        elif len(organize_option) == 0 and len(source) > 0:
            window["-OUTPUT_WINDOW-"].update(">>> ERROR: Please select an organization option.")
    
#----START List all files in the directory that you're watching START----#       
    if event == "-LIST_FILES-":
        if len(source) > 0 and ends_with == "all":
            window["-OUTPUT_WINDOW-"].update(list_all_files_in_directory(source))
        elif ends_with == ".xls" and len(source) > 0:
            window["-OUTPUT_WINDOW-"].update(f">>> Files with filetype: {ends_with}\n")
            window.perform_long_operation(lambda: file_type (ends_with, source),"-OUTPUT_WINDOW")
        elif ends_with == ".xlsx" and len(source) > 0:
            window["-OUTPUT_WINDOW-"].update(f">>> Files with filetype: {ends_with}\n")
            window.perform_long_operation(lambda: file_type (ends_with, source),"-OUTPUT_WINDOW")
        elif ends_with == ".mp4" and len(source) > 0:
            window["-OUTPUT_WINDOW-"].update(f">>> Files with filetype: {ends_with}\n")
            window.perform_long_operation(lambda: file_type (ends_with, source),"-OUTPUT_WINDOW")
        elif ends_with == ".avi" and len(source) > 0:
            window["-OUTPUT_WINDOW-"].update(f">>> Files with filetype: {ends_with}\n")
            window.perform_long_operation(lambda: file_type (ends_with, source),"-OUTPUT_WINDOW")
        elif ends_with == ".wav" and len(source) > 0:
            window["-OUTPUT_WINDOW-"].update(f">>> Files with filetype: {ends_with}\n")
            window.perform_long_operation(lambda: file_type (ends_with, source),"-OUTPUT_WINDOW")
        elif ends_with == ".xml" and len(source) > 0:
            window["-OUTPUT_WINDOW-"].update(f">>> Files with filetype: {ends_with}\n")
            window.perform_long_operation(lambda: file_type (ends_with, source),"-OUTPUT_WINDOW")
        elif ends_with == ".zip" and len(source) > 0:
            window["-OUTPUT_WINDOW-"].update(f">>> Files with filetype: {ends_with}\n")
            window.perform_long_operation(lambda: file_type (ends_with, source),"-OUTPUT_WINDOW")
        elif ends_with == ".pdf" and len(source) > 0:
            window["-OUTPUT_WINDOW-"].update(f">>> Files with filetype: {ends_with}\n")
            window.perform_long_operation(lambda: file_type (ends_with, source),"-OUTPUT_WINDOW")
        elif ends_with == ".pak" and len(source) > 0:
            window["-OUTPUT_WINDOW-"].update(f">>> Files with filetype: {ends_with}\n")
            window.perform_long_operation(lambda: file_type (ends_with, source),"-OUTPUT_WINDOW")
        elif ends_with == ".jar" and len(source) > 0:
            window["-OUTPUT_WINDOW-"].update(f">>> Files with filetype: {ends_with}\n")
            window.perform_long_operation(lambda: file_type (ends_with, source),"-OUTPUT_WINDOW")
        elif ends_with == ".txt" and len(source) > 0:
            window["-OUTPUT_WINDOW-"].update(f">>> Files with filetype: {ends_with}\n")
            window.perform_long_operation(lambda: file_type (ends_with, source),"-OUTPUT_WINDOW")
        elif ends_with == ".jpg" and len(source) > 0:
            window["-OUTPUT_WINDOW-"].update(f">>> Files with filetype: {ends_with}\n")
            window.perform_long_operation(lambda: file_type (ends_with, source),"-OUTPUT_WINDOW")
        elif ends_with == ".png" and len(source) > 0:
            window["-OUTPUT_WINDOW-"].update(f">>> Files with filetype: {ends_with}\n")
            window.perform_long_operation(lambda: file_type (ends_with, source),"-OUTPUT_WINDOW")
        elif ends_with == ".csv" and len(source) > 0:
            window["-OUTPUT_WINDOW-"].update(f">>> Files with filetype: {ends_with}\n")
            window.perform_long_operation(lambda: file_type (ends_with, source),"-OUTPUT_WINDOW")
        elif ends_with == ".icon" and len(source) > 0:
            window["-OUTPUT_WINDOW-"].update(f">>> Files with filetype: {ends_with}\n")
            window.perform_long_operation(lambda: file_type (ends_with, source),"-OUTPUT_WINDOW")
        elif ends_with == ".docx" and len(source) > 0:
            window["-OUTPUT_WINDOW-"].update(f">>> Files with filetype: {ends_with}\n")
            window.perform_long_operation(lambda: file_type (ends_with, source),"-OUTPUT_WINDOW")
        elif ends_with == "" and len(source) > 0:
            window["-OUTPUT_WINDOW-"].update(f">>> ERROR: Use the listbox to set a filetype to look for.")
        else:
            window["-OUTPUT_WINDOW-"].update(">>> ERROR: No path set, running on errors :)")
    #----END List all files in the directory that you're watching END----#
    
    if event == "-update_FUNC-":
        try:
            if len(source) > 1:
                onlyfiles = [f for f in listdir(source) if isfile(join(source, f))]
                for file in onlyfiles:
                    filename = Path(file).stem
                    file_extension = Path(file).suffix
                    window["-OUTPUT_WINDOW-"].update(f"{filename}{file_extension}")
            elif len(source) == 0:
                window["-OUTPUT_WINDOW-"].update(">>> ERROR: Input Folder path is empty!")
        except FileNotFoundError as e:
            window["-OUTPUT_WINDOW-"].update(e)
    
     #---- START Moving Files Button START ----#
    if event == "-MOVE_BUTTON-":
        if len(destination) > 0 and len(source) > 0:
             window.perform_long_operation(lambda: moving_selected_filetype(ends_with,destination,source),"-OUTPUT_WINDOW-")
        elif len(destination) > 0 and len(source) == 0:
            window["-OUTPUT_WINDOW-"].update(">>> ERROR: Source folder input is empty!")
        elif len(source) > 0 and len(destination) == 0:
            window["-OUTPUT_WINDOW-"].update(">>> ERROR: Destination folder input is empty!")
        else:
            window["-OUTPUT_WINDOW-"].update(">>> ERROR: No Source and Destination path set, running on errors. Please set both paths.")
     #---- END Moving Files Button END ----#
    
#    if event == "-MOVE_BUTTON-":
#        if len(destination) > 0:
#            window.perform_long_operation(lambda: move_files_to_folder(source,destination),"-OUTPUT_WINDOW-")
#        elif len(destination) == 0:
#            window["-OUTPUT_WINDOW-"].update(">>> ERROR: No destination Folder set.")
            
    if event == "-CLEAR_OUTPUT-":
        window["-OUTPUT_WINDOW-"].update("")
        
#----START Swapping Watching folder path with Move folder path event START----#
    if event == "-SWITCH_OUTPUTS-" and len(source) > 0 and len(destination) > 0:
        window["-INPUT_PATH-"].update(destination)
        window["-OUTPUT_PATH-"].update(source)
    #----END Swapping Watching folder path with Move folder path event END----#   
window.close()