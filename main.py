from time import sleep
import PySimpleGUI as sg
from os import popen, execl
from sys import exit, executable
import psutil
import schedule


def fun_dis_lis_pro():
    process_lis = []
    for proc in psutil.process_iter():
        try:
            if proc.pid != 0 and proc.pid != 4:
                process = [proc.name(), proc.pid, len(proc.connections())]
                process_lis.append(process)
        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return process_lis


task_list = fun_dis_lis_pro()

header = ["Name", "PID"]
font = ("Arial", 16)
layout_ = [
    [[sg.T("Search: "), sg.Input(tooltip="Enter Name Program", key="txt_search"),
      sg.Button("Search", key="btn_search")], [sg.Button("Guide", key="btn_gui")],
     sg.Table(task_list[:-1], headings=header, font=font, enable_events=True,
              key="__Table__", row_height=45, auto_size_columns=True, max_col_width=35,
              selected_row_colors=("#000", "#FBFEA4"), vertical_scroll_only=False,
              background_color="#fff",
              justification="left",
              text_color="#000")]]
windows = sg.Window(title="Resize Image", icon="task.ico", layout=layout_)

img_name = ""

flag1 = False
flag2 = False


def find_word(word):
    process_list = fun_dis_lis_pro()
    for process in process_list:
        if word == process[0]:
            return process_list.index(process)
    return -1


def follow_task():
    global flag1
    global flag2
    rtf = find_word(img_name)
    proc_lis = fun_dis_lis_pro()
    if img_name == "IDMan.exe":
        if rtf > -1:
            count = proc_lis[rtf][2]
            if count > 0:
                flag1 = True
            else:
                if flag1 and count <= 0:
                    popen("shutdown  /s /f /t 10")
                    exit()
                else:
                    sg.popup("No Downloading... And Will restart")
                    execl(executable, "python", __file__)
        else:
            execl(executable, "python", __file__)
    else:
        if rtf > -1:
            flag2 = True
        else:
            if flag2:
                popen("shutdown  /s /f /t 10")
                exit()
            else:
                execl(executable, "python", __file__)


def val_ele(key):
    return windows.find_element(key).get()


def ret_ele(key):
    return windows.find_element(key)


def fun():
    while True:
        try:
            schedule.run_pending()
            sleep(1)
        except:
            exit()


while True:
    event, value = windows.read()
    if event == "__Table__":
        img_name = task_list[value["__Table__"][0]][0]
        res = sg.popup_ok_cancel("Are You Sure follow program: " + img_name)
        if res in "OK":
            schedule.every(5).seconds.do(follow_task)
            fun()
    elif event == "btn_search":
        world = val_ele("txt_search").replace(" ", "^")
        if world in ("", None) or world.find("^") >= 0:
            sg.popup_error("Enter Name Program!")
        else:
            if find_word(world) == -1:
                sg.popup_error("Enter Name Program Correct!")
            else:
                ret_ele("__Table__").update(select_rows=[find_word(world)])
    elif event == sg.WIN_CLOSED:
        exit()
    elif event == "btn_gui":
        sg.popup_scrolled("IDMan.exe => Internet Download Manager", "chrome.exe => Google Chrome")
