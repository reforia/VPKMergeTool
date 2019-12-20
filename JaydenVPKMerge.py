#CONFIDENTIAL
#Last Update: 2019/10/10
#Author: Jayden
#The connection was configured to connect to SMU GUILDHALL P4 Server only
import sys
import tkinter as tk
from tkinter import messagebox
#import pickle
from P4 import P4, P4Exception
import os
from os import listdir
from os.path import isfile, join
import shutil
from shutil import copyfile
import io
import winreg
import subprocess

############################## [initialize Level List]
levels = []
posters = []
thumbnails = []
localpath = ""

######################### [general Widget Auto Align Settings]
window = tk.Tk()
windowwidth = 500
windowheight = 800
widgetwidth = 16
widgetheight = 1
edge_x_padding = 120
left_x = edge_x_padding
right_x = windowwidth - edge_x_padding
center_x = windowwidth / 2
pad_y = 30

############################## [Widget Initialization]

#ip input
var_ip = tk.StringVar()
entry_ip = tk.Entry(window, textvariable = var_ip)
#usr name input
var_user_name = tk.StringVar()
entry_user_name = tk.Entry(window, textvariable = var_user_name)
#workspace input
var_workspace = tk.StringVar()
entry_workspace = tk.Entry(window,textvariable = var_workspace, show = None)

#P4 Initialization
def p4_initialization():
    global p4
    p4.disconnect()

#P4 Connection Func()
def p4_connect():
    global p4
    global ConnectResult
    global StatusLabel
    global StatusLabelText
    global entry_level_counts
    global entry_user_name
    global entry_workspace

    try:
        p4.user = entry_user_name.get()
        p4.client = entry_workspace.get()
        p4.port = entry_ip.get()
        p4.connect()
        #print(p4.port)
        if p4.connected() != False:
            ConnectResult = True
            StatusLabel.configure(background = 'green')
            p4.run_login()
            #opened = p4.run_opened()
            info = p4.run("info")
            for key in info[0]:
                print(key, "=", info[0][key])
            #print("Connected")
            #p4.fetch_client()
            #print(p4.fetch_client())
    except:
        ConnectResult = False
        StatusLabel.configure(background = 'grey')
    StatusLabelText.set("GUILDHALL P4 Connection: (" + entry_ip.get() + ") -> " + str(ConnectResult))

#P4 Disconnect Func()
def p4_disconnect():
    global ConnectResult
    global p4
    global StatusLabel
    global StatusLabelText

    p4.disconnect()
    ConnectResult = False
    StatusLabel.configure(background = 'grey')
    StatusLabelText.set("GUILDHALL P4 Connection: (" + entry_ip.get() + ") -> " + str(ConnectResult))
    tk.messagebox.showinfo(title="Jayden's VPK Merge Tool", message="P4 Connection Disconnected!")

def p4_sync():
    global p4
    #print(p4.connected())
    if p4.connected() == True:
        p4.run_sync()
        tk.messagebox.showinfo(title="Jayden's VPK Merge Tool", message= "All files are up to date!")
    else:
        #print(1)
        tk.messagebox.showerror(title="Jayden's VPK Merge Tool", message= "Failed! Connection to P4 Lost")

#connect btn
button_connect = tk.Button(window, text = 'Connect P4', width = widgetwidth, height = widgetheight, command = p4_connect)
#sync btn
button_sync = tk.Button(window, text = 'Get Latest', width = widgetwidth, height = widgetheight, command = p4_sync)
#disconnect btn
button_disconnect = tk.Button(window, text = 'Disconnect', width = widgetwidth, height = widgetheight, command = p4_disconnect)

#status label text
StatusLabelText = tk.StringVar()
#status label
StatusLabel = tk.Label(window, textvariable = StatusLabelText, bg = 'grey', fg = 'white', width = 5 * widgetwidth, height = 1)


#copyright label text
CopyrightLabelText = tk.StringVar()
#copyright label text
CopyrightLabel = tk.Label(window, textvariable = CopyrightLabelText, bg = 'black', fg = 'white', width = 5 * widgetwidth, height = 2)

#level counts
var_level_counts = tk.StringVar()
#entry level counts
entry_level_counts = tk.Entry(window, textvariable = var_level_counts)

#level description
var_level_description = tk.StringVar()
#entry level counts
entry_level_description = tk.Entry(window, textvariable = var_level_description)

#campaign_name
var_campaign_name = tk.StringVar()
#entry level counts
entry_campaign_name = tk.Entry(window, textvariable = var_campaign_name)

#file path
var_file_path = tk.StringVar()
#entry file path
entry_file_path = tk.Entry(window, textvariable = var_file_path)

#tagline
var_tagline = tk.StringVar()
#entry tagline
entry_tagline = tk.Entry(window, textvariable = var_tagline)

#author
var_author = tk.StringVar()
#entry author
entry_author = tk.Entry(window, textvariable = var_author)

#steam id
var_author_steamid = tk.StringVar()
#entry author steam id
entry_author_steamid = tk.Entry(window, textvariable = var_author_steamid)

#Spawn Level Slot Func()
def spawn_level_slot():
    global entry_level_counts
    global levels
    global widgetwidth
    global widgetheight
    global pad_y

    try:
        int(entry_level_counts.get())
        level_count = int(entry_level_counts.get())
    except:
        var_level_counts.set(str(4))
        level_count = 4
    #print(level_count)
    try:
        #Clear Existing Level Infos
        for levelbundles in levels:
            levelbundles[0].destroy()
            levelbundles[1].destroy()
            levelbundles[2].destroy()
        levels.clear()
        
        #New Level Info Slots
        for i in range(level_count):
            levelbundle = []
            #print(i)
            levelindex = tk.Label(window, text = "level " + str(i + 1))
            levelindex.place(x = left_x - 7 * widgetwidth, y = pad_y * (8 + i))
            levelbundle.append(levelindex)

            level_slot = tk.Entry(window, text = "levelname:" + str(i + 1))
            level_slot.place(x = left_x - 4 * widgetwidth, y = pad_y * (8 + i))
            levelbundle.append(level_slot)

            level_display_name = tk.Entry(window, text = "level display name" + str(i + 1))
            level_display_name.place(x = left_x + 52 * widgetheight, y = pad_y * (8 + i))
            levelbundle.append(level_display_name)

            levels.append(levelbundle)
    except:
        return

def generate_vpk():
    all_levels = fetch_levels()
    all_vguis = fetch_posters()
    all_thumbnails = fetch_thumbnails()
    dest_path = create_folder()
    copy_levels_to_folder(all_levels,dest_path)
    copy_posters_to_folder(all_vguis,dest_path)
    copy_thumbnails_to_folder(all_thumbnails, dest_path)
    #copy_secondary_content_to_folder(image, dest_path)
    generate_mission_file(dest_path)
    generate_addon_info(dest_path)
    package(dest_path)

def fetch_thumbnails():
    global p4
    global thumbnails
    global localpath
    if p4.connected() == True:
        temp_thumbnails = []
        #get local p4 directory
        clientinfo = p4.fetch_client()
        localpath = clientinfo["Root"] + entry_file_path.get() + "\materials\\vgui\maps"
        #D:\P4\LD3L4DTeam4\left4dead\maps
        #extract files from local path
        files = [f for f in listdir(localpath) if isfile(join(localpath, f))]

        for i in range(len(levels)):
            for file in files:
                print(file)
                #print(levels[i][1].get().lower() + ".bsp")
                if file == entry_campaign_name.get().lower() + str(i+1) + ".vtf":
                    temp_thumbnails.append(file)
                if file == entry_campaign_name.get().lower() + str(i+1) + ".vmt":
                    temp_thumbnails.append(file)
            # levelbundle = levels[i]
            # print(levelbundle[1].get().lower())
            # if file.lower == levelbundle[1].get().lower()+".bsp":
            #     print(file.lower())

        return temp_thumbnails
    else:
        tk.messagebox.showerror(title="Jayden's VPK Merge Tool", message= "Not Connected to P4")


def fetch_posters():
    global p4
    global posters
    global localpath
    if p4.connected() == True:
        temp_posters = []
        #get local p4 directory
        clientinfo = p4.fetch_client()
        localpath = clientinfo["Root"] + entry_file_path.get() + "\materials\\vgui"
        #D:\P4\LD3L4DTeam4\left4dead\maps
        #extract files from local path
        files = [f for f in listdir(localpath) if isfile(join(localpath, f))]

        for file in files:
            print(file)
            #print(levels[i][1].get().lower() + ".bsp")
            if file == "LoadingScreen_"+entry_campaign_name.get().lower() + ".vtf":
                temp_posters.append(file)
            if file == "LoadingScreen_"+entry_campaign_name.get().lower() + ".vmt":
                temp_posters.append(file)
            if file == "OutroTitle_"+entry_campaign_name.get().lower() + ".vtf":
                temp_posters.append(file)
            if file == "OutroTitle_"+entry_campaign_name.get().lower() + ".vmt":
                temp_posters.append(file)
            # levelbundle = levels[i]
            # print(levelbundle[1].get().lower())
            # if file.lower == levelbundle[1].get().lower()+".bsp":
            #     print(file.lower())

        return temp_posters
    else:
        tk.messagebox.showerror(title="Jayden's VPK Merge Tool", message= "Not Connected to P4")

def package(path):
    steam_hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\WOW6432Node\Valve\Steam")
    steam_location = winreg.QueryValueEx(steam_hkey, "InstallPath")
    library_file = io.open(steam_location[0] + "\steamapps\libraryfolders.vdf", mode = "r", encoding = "utf-8")
    library_location = ""
    steam_library_index = 1
    check_char_list = "\n\t\" "
    for line in library_file:
        if ":" in line:
            temp_check_char_list = check_char_list + str(steam_library_index)
            library_location = line.translate({ord(char): None for char in temp_check_char_list})
            #library_location = line.translate({ord(char): "/" for char in "\\"})
            lfd_location = library_location + "/steamapps/common/left 4 dead\\bin"
            if os.path.exists(lfd_location):
                print(library_location)
            else:
                steam_library_index += 1
    
    if os.path.exists(lfd_location):
        lfd_location = lfd_location.replace("\\", "/")
        path = path.replace("\\", "/")
        vpk_location = lfd_location + "/vpk.exe"
        execute_vpk = "& '"+vpk_location+"' @('"+path+"')"
        subprocess.Popen(['powershell.exe', execute_vpk], shell= True)
        #execute_vpk = subprocess.Popen("D:; cd "+ lfd_location + "; vpk -?")
        #execute_vpk = os.system("D:\ncd " + lfd_location + "\n" + "vpk " + path)
        #print(execute_vpk)
        tk.messagebox.showinfo(title= "Jayden's VPK Merge Tool", message= "VPK Generate Succeeded!")
    else:
        tk.messagebox.showerror(title= "Jayden's VPK Merge Tool", message= "L4D Directory Not Found! You May Have Multiple Steam App Installation Folders!")

#def copy_secondary_content_to_folder(image_dest_path)

def generate_mission_file(path):
    global entry_campaign_name
    currentpath = os.path.dirname(os.path.abspath(__file__))
    print(currentpath)
    #copyfile(currentpath + "\missioninfo.txt", path + "\missions\\" + entry_campaign_name.get().lower() + ".txt")
    fin = io.open(currentpath + "\missioninfo.txt", mode = "r", encoding = "utf-8")
    fout = io.open(path + "\missions\\" + entry_campaign_name.get().lower() + ".txt", mode = "w", encoding = "utf-8")
    for line in fin:
        if 'NameTemplate' in line:
            fout.write(line.replace('NameTemplate', entry_campaign_name.get()))
        elif 'OutroTitleTemplate' in line:
            fout.write(line.replace('OutroTitleTemplate', 'OutroTitle_' + entry_campaign_name.get().lower()))
        elif 'LoadingScreenTemplate' in line:
            fout.write(line.replace('LoadingScreenTemplate', 'LoadingScreen_' + entry_campaign_name.get().lower()))
        elif 'DisplayTitleTemplate' in line:
            fout.write(line.replace('DisplayTitleTemplate', entry_campaign_name.get()))
        elif 'AuthorTemplate' in line:
            fout.write(line.replace('AuthorTemplate', entry_author.get()))
        elif 'CoopTemplate' in line:
            fout.write(line.replace('CoopTemplate', generate_level_info()))
        elif 'DescriptionTemplate' in line:
            fout.write(line.replace('DescriptionTemplate', entry_tagline.get()))
        else:
            fout.write(line)

def generate_level_info():
    global levels
    levelinfo = ""

    for i in range(len(levels)):
        perlevelinfo = "\t\t\t\""+str(i+1)+"\"\n"
        perlevelinfo += "\t\t\t{\n"
        perlevelinfo += "\t\t\t\t\"Map\" \""+ levels[i][1].get().lower() + "\"\n"
        perlevelinfo += "\t\t\t\t\"DisplayName\" \"" + levels[i][2].get() + "\"\n"
        perlevelinfo += "\t\t\t\t\"Image\" \"maps/"+entry_campaign_name.get().lower() + str(i+1) + "\"\n"
        perlevelinfo += "\t\t\t}\n\n"
        levelinfo += perlevelinfo
    return levelinfo

def generate_addon_info(path):
    global entry_campaign_name
    global entry_tagline
    global entry_author
    global entry_author_steamid
    global entry_level_description

    currentpath = os.path.dirname(os.path.abspath(__file__))
    #print(currentpath)
    #copyfile(currentpath + "\\addoninfo.txt", path + "\\addoninfo.txt")
    fin = io.open(currentpath + "\\addoninfo.txt", mode = "r", encoding = "utf-8")
    fout = io.open(path + "\\addoninfo.txt", mode = "w", encoding = "utf-8")

    for line in fin:
        if 'addonTitleTemplate' in line:
            fout.write(line.replace('addonTitleTemplate', entry_campaign_name.get()))
        elif 'addonTaglineTemplate' in line:
            fout.write(line.replace('addonTaglineTemplate', entry_tagline.get()))
        elif 'addonAuthorTemplate' in line:
            fout.write(line.replace('addonAuthorTemplate', entry_author.get()))
        elif 'addonAuthorSteamIDTemplate' in line:
            fout.write(line.replace('addonAuthorSteamIDTemplate', entry_author_steamid.get()))
        elif 'addonDescriptionTemplate' in line:
            fout.write(line.replace('addonDescriptionTemplate', entry_level_description.get()))
        else:
            fout.write(line)

def copy_levels_to_folder(levels, path):
    global p4
    global localpath
    clientinfo = p4.fetch_client()
    localpath = clientinfo["Root"]
    print("start copying level")
    print(localpath + entry_file_path.get() + "\maps")
    print(path + "\maps")
    if os.path.exists(path + "\maps") and os.path.exists(localpath + entry_file_path.get() + "\maps"):
        for i in range(len(levels)):
            print(i)
            copyfile(localpath + entry_file_path.get() + "\maps\\" + levels[i], path + "\maps\\" + levels[i])

def copy_posters_to_folder(posters, path):
    global p4
    global localpath
    clientinfo = p4.fetch_client()
    localpath = clientinfo["Root"]
    #print(1111)
    #print(localpath)
    if os.path.exists(path + "\materials\\vgui") and os.path.exists(localpath + entry_file_path.get() + "\materials\\vgui"):
        #print(111)
        for i in range(len(posters)):
            #print(len(posters))
            copyfile(localpath + entry_file_path.get() + "\materials\\vgui\\" + posters[i], path + "\materials\\vgui\\" + posters[i])

def copy_thumbnails_to_folder(thumbnails, path):
    global p4
    global localpath
    clientinfo = p4.fetch_client()
    localpath = clientinfo["Root"]
    #print(1111)
    #print(localpath)
    if os.path.exists(path + "\materials\\vgui\maps") and os.path.exists(localpath + entry_file_path.get() + "\materials\\vgui\maps"):
        #print(111)
        for i in range(len(thumbnails)):
            #print(len(thumbnails))
            copyfile(localpath + entry_file_path.get() + "\materials\\vgui\\maps\\" + thumbnails[i], path + "\materials\\vgui\\maps\\" + thumbnails[i])


def create_folder():
    directory = os.path.expanduser("~\Desktop\\" + "\\" + entry_campaign_name.get().lower())
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(directory+"\maps"):
        os.makedirs(directory+"\maps")
    if not os.path.exists(directory+"\missions"):
        os.makedirs(directory+"\missions")
    if not os.path.exists(directory+"\materials\\vgui\maps"):
        os.makedirs(directory+"\materials\\vgui\maps")
    return directory

def fetch_levels():
    global p4
    global levels
    global localpath
    if p4.connected() == True:
        temp_levels = []
        #get local p4 directory
        clientinfo = p4.fetch_client()
        localpath = clientinfo["Root"] + entry_file_path.get()
        #D:\P4\LD3L4DTeam4\left4dead\maps
        #extract files from local path
        files = [f for f in listdir(localpath+"\maps") if isfile(join(localpath+"\maps", f))]
        print("start looping through files")
        print(localpath+"\maps")
        for i in range(len(levels)):
            for file in files:
                print(file)
                print(levels[i][1].get().lower() + ".bsp")
                if file.lower() == levels[i][1].get().lower() + ".bsp":
                    temp_levels.append(file)
                if file.lower() == levels[i][1].get().lower() + ".nav":
                    temp_levels.append(file)
                # levelbundle = levels[i]
                # print(levelbundle[1].get().lower())
                # if file.lower == levelbundle[1].get().lower()+".bsp":
                #     print(file.lower())

        return temp_levels
    else:
        tk.messagebox.showerror(title="Jayden's VPK Merge Tool", message= "Not Connected to P4")

#button fresh
button_refresh = tk.Button(window, text = 'Refresh List', width = widgetwidth, height = widgetheight, command = spawn_level_slot)

#button generate
button_generate = tk.Button(window, text = 'Generate .VPK', bg = 'green', fg = 'white', width = widgetwidth, height = widgetheight, command = generate_vpk)

############################ [P4 Connection Initialization]
p4 = P4()
p4.exception_level = 0
p4.port = entry_ip.get()
p4.user = entry_user_name.get()
p4.client = entry_workspace.get()

ConnectResult = False

############################# [main() entry]
def main():
    global window

    p4_initialization()
    draw_window()
    draw_P4_connection_GUI()
    draw_level_list()
    window.mainloop()

def draw_P4_connection_GUI():
    global p4
    global var_ip
    global entry_ip
    global var_user_name
    global entry_user_name
    global var_workspace
    global entry_workspace
    global button_connect
    global button_sync
    global button_disconnect
    global StatusLabelText
    global StatusLabel
    global widgetwidth
    global widgetheight
    global left_x
    global right_x
    global pad_y
    global ConnectResult
    global CopyrightLabel
    global CopyrightLabelText

    #Set Up P4 Connection GUI
    #IP Input
    tk.Label(window, text = 'P4 IP:Port', width = widgetwidth, height = widgetheight).place(x = left_x - 4 * widgetwidth, y = pad_y)
    var_ip.set('129.119.63.244:1666')
    entry_ip.place(x = right_x - 4 * widgetwidth, y = pad_y)

    #UsrName Input
    tk.Label(window, text = 'User Name:', width = widgetwidth, height = widgetheight).place(x = left_x - 4 * widgetwidth, y = pad_y * 2)
    var_user_name.set('tianmouz')
    entry_user_name.place(x = right_x - 4 * widgetwidth, y = pad_y * 2)

    #Workspace Input
    tk.Label(window, text = 'Workspace:', width = widgetwidth, height = widgetheight).place(x = left_x - 4 * widgetwidth, y = pad_y * 3)
    var_workspace.set('LD3L4DTeam4')
    entry_workspace.place(x = right_x - 4 * widgetwidth, y = pad_y * 3)

    #Connect/Disconnect Button
    button_connect.place(x = left_x - 4 * widgetwidth, y = pad_y * 4)

    button_sync.place(x = center_x - 4* widgetwidth, y = pad_y * 4)

    button_disconnect.place(x = right_x - 4 * widgetwidth, y = pad_y * 4)

    #Set up P4 Connection Label Bar
    StatusLabelText.set("GUILDHALL P4 Connection: (" + entry_ip.get() + ") -> " + str(ConnectResult))
    StatusLabel.pack(side = "top")

    #Set up tool Copyright Label Bar
    CopyrightLabelText.set("JAYDEN ZHANG @ SMU GUILDHALL, CONTACT: tianmouz@smu.edu")
    CopyrightLabel.pack(side = "bottom")

def draw_level_list():   
    global p4    
    global var_level_counts
    global entry_level_counts
    global widgetwidth
    global widgetheight
    global left_x
    global right_x
    global pad_y
    global button_refresh
    global var_level_description
    global entry_level_description
    global var_campaign_name
    global entry_campaign_name
    global button_generate
    global var_file_path
    global entry_file_path

    #Set up Level Info
    tk.Label(window, text = "Level Counts", width = widgetwidth, height = widgetheight).place(x = left_x - 8 * widgetwidth, y = pad_y * 5)
    var_level_counts.set("4")
    entry_level_counts.place(x = left_x - 0 * widgetwidth, y = pad_y * 5)

    #Map Name and Display Name
    tk.Label(window, text = "Map File Name", width = widgetwidth, height = widgetheight).place(x = left_x - 4 * widgetwidth, y = pad_y * 7)
    tk.Label(window, text = "Map Display Name", width = widgetwidth, height = widgetheight).place(x = left_x + 3.5 * widgetwidth, y = pad_y * 7)
    #Spawn Level Panel Slots
    button_refresh.place(x = left_x - 4 * widgetwidth, y = pad_y * 6)

    #Generate Button
    button_generate.pack(side = "bottom")

    #Initialize Level Slot
    spawn_level_slot()

    #Set up Campaign Name
    tk.Label(window, text = "Campaign Name", width = widgetwidth, height = widgetheight).place(x = right_x - 4 * widgetwidth, y = pad_y * 5)
    var_campaign_name.set("Finalstop")
    entry_campaign_name.place(x = right_x - 4 * widgetwidth, y = pad_y * 6)

    #Set up level description
    tk.Label(window, text = "Campaign Description", width = widgetwidth, height = widgetheight).place(x = right_x - 4 * widgetwidth, y = pad_y * 7)
    var_level_description.set("Survivors were trapped in a train station, and they must find a way out...")
    entry_level_description.place(x = right_x - 4 * widgetwidth, y = pad_y * 8)

    #Set up p4 map file path
    tk.Label(window, text = "File Path", width = widgetwidth, height = widgetheight).place(x = right_x - 4 * widgetwidth, y = pad_y * 9)
    var_file_path.set("\\left4dead")
    entry_file_path.place(x = right_x - 4 * widgetwidth, y = pad_y * 10)

    #Set up tagline
    tk.Label(window, text = "Tagline", width = widgetwidth, height = widgetheight).place(x = right_x - 4 * widgetwidth, y = pad_y * 11)
    var_tagline.set("Next stop... HELL")
    entry_tagline.place(x = right_x - 4 * widgetwidth, y = pad_y * 12)

    #Set up author
    tk.Label(window, text = "Author", width = widgetwidth, height = widgetheight).place(x = right_x - 4 * widgetwidth, y = pad_y * 13)
    var_author.set("Team4")
    entry_author.place(x = right_x - 4 * widgetwidth, y = pad_y * 14)

    #Set up author steamid
    tk.Label(window, text = "Author Steam ID", width = widgetwidth, height = widgetheight).place(x = right_x - 4 * widgetwidth, y = pad_y * 15)
    var_author_steamid.set("Atsunato, TwoPlateNate, Lenmonade, Graves")
    entry_author_steamid.place(x = right_x - 4 * widgetwidth, y = pad_y * 16)


def draw_window(width = 500,height = 800):
    #Set Up Windows
    global window
    global windowwidth
    global windowheight

    window.title("Jayden's VPK Merge Tool")

    windowwidth = width
    windowheight = height
    window.geometry(str(windowwidth)+"x"+str(windowheight))

if __name__ == '__main__':
    main()





