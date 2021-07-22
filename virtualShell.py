#!/usr/bin/python3
# -*- coding:utf-8 -*-

# *********************************************
# *Author     : Logic (Junpeng Sun).
# *E-mail     : sunjunpeng2007@126.com
# *             littlebox2020@outlook.com
# *Description: Analog Command-Line Resolution.
# *Date       : 2021.7.14 (Wed) 13:16.
# *Remark     : If You Forget Your Password,
# *              You Can Choose To Delete Or
# *              Modify File "passwd.json",
# *              Or Re-Register The Account.
# *END
# *********************************************

# Type "help"(Case Insensitive) To Get HELP Message.

from os import name, system, chdir, getcwd, mkdir, get_terminal_size
from sys import stdin, stderr
from time import sleep
from json import load, dump
from getpass import getpass
from hashlib import md5
from datetime import datetime
from traceback import format_exc
#> from pyperclip import copy
from os.path import exists

# Global Program Version.
version = "0.2.2021.Release (Colorful Times)"

# Supported Executable Commands (Not Special Commands).
cmds = {"clear": "Clear Screen.", "exit": "Exit This Program.", "logout": "Exit This Program", "data": "Undefined.", "shift": "Undefined.", "virsual": "Undefined.", "print": "Undefined.", "restart": "Soft-Restart This Program.", "goto": "Undefined.", "tp": "Undefined.", "cd": "Toggle The Working Directory.", "reboot": "Soft-Restart This Program.", "ls": "List The Contents of The Current Directory.", "dir": "List The Contents of The Current Directory.", "cat": "Display The Specified Text File Contents.", "uname": "Display The Virtual Operating System Type.", "pwd": "Display The Current Working Directory.", "tty": "Display The Current Terminal Storage Location.", "wget": "Download Files On The Internet.", "ping": "Test Network Connectivity.", "help": "Display This Help Message.", "exec": "Execute Commands With Default-Shell.", "raise": "Manually Throw A System-Exception."}
# Emergency Default Usernames And The MD5 Code Of Passwords.
users = {'logic': '6fad807c0f7e970c379a8b6393e22501', 'administrator': 'd41d8cd98f00b204e9800998ecf8427e'}

# Clear Screen.
if name == 'nt':
    clear = lambda : system("cls")
elif name == 'posix':
    clear = lambda : system("clear")

def save_users():
    """Doc:
    Save Usernames & Password Data.
    No Parameters Are Required.
    """
    try:
        with open("./passwd.json", 'w') as record:
            dump(users, record, indent=4, ensure_ascii=False)
    except:
        print("\033[1;31;mFailed To Create Users' Data File...\n\033[0m")        

clear()

# Rebuild The Users' Data File.
if not exists("./passwd.json"):
    save_users()    
else:
    # Read Users' Data.
    try:
        with open("./passwd.json", 'r') as record:
            users = load(record)
    except:
        print("\033[1;31;mFailed To Read Users' Data File...\n\033[0m")

# Legalization Of Command.
def clearSpace(string):
    """Doc:
    Used To Clear Illegal Components From Users' Commands (Extra Spaces & "Tab").
    Requires A Parameter, The Pending Users' Command.
    """
    if string == '':
        return string
    string = string.replace('\t', ' ')
    try:
        if string[0] == ' ':
            string = string[1:]
        if string[-1] == ' ':
            string = string[:-1]
    except IndexError:
        pass
    if len(string) >= 2:
        more = 0
        index = 0
        result = ''
        for each in string:
            try:
                if each == string[index+1] == ' ':
                    more = 1
                else:
                    more = 0
            except IndexError:
                result = "%s%s" % (result, each)
                break
            if not more:
                result = "%s%s" % (result, each)
            index += 1
        if result[0] == ' ':
            result = result[1:]
        if string[-1] == ' ':
            result = result[:-1]
        return result
    else:
        return string

# Command Resolution.
def execute(cmd):
    """Doc:
    Used To Resolve Processed Users' Commands.
    Requires An Argument, Pending Command.
    """
    global username
    if cmd == '':
        return ''
    elif cmd[:2] == './':
        if username == "root":
            code = system("sudo " + cmd)
            return "\033[;32;mTransmited Default-Shell Execution Command As Root.\nDefault-Shell Returned \033[1;34;m%d\n\033[0m" % code
        else:
            code = system(cmd)
            return "\033[;32;mTransmited Default-Shell Execution Command.\nDefault-Shell Returned \033[1;34;m%d\n\033[0m" % code
    unit = ''
    for each in cmd:
        if each == ' ':
            break
        else:
            unit = "%s%s".lower() % (unit, each)
    if (unit == "clear") or (unit == "cls"):
        clear()
    elif (unit == "exit") or (unit == "logout"):
        print('\nLogout')
        sleep(0.5)
        exit(0)
    elif unit == "login":
        print()
        login()
        return ''
    elif (unit == "reboot") or (unit == "restart"):
        clear()
        print("LogicOS %s\nKernel- Not Mounted\n\nCopyright (c) 2020-2021 Littlebox.\nAll Rights Reserved.\n" % version)
        login()
    elif unit == "cd":
        try:
            chdir(cmd[3:])
        except FileNotFoundError:
            return "\033[1;31;mNo Such File Or Directory.\n\033[0m"
        else:
            return ''
    elif (unit == "ls") or (unit == "dir"):
        if name == "nt":
            system("dir")
        else:
            system("ls -A --color=auto")
        return ''
    elif unit == "cat":
        try:
            with open(cmd[4:], 'r') as f:
                print(f.read())
                return '\n'
        except:
            return "\033[1;31;mThere Is An Error While Reading...\n\033[0m"
    elif unit == "uname":
        return "LogicOS %s\nKernel- Not Mounted\n" % version
    elif unit == "mkdir":
        try:
            mkdir(cmd[6:])
        except Exception as reason:
            return "\033[1;31;mMake Directory Error\n%s\n\033[0m" % reason
        return ''
    elif unit == "pwd":
        return getcwd() + '\n'
    elif unit == "tty":
        return "/dev/tty0 Python-3-Virtual\n"
    elif unit == "su":
        if cmd == "su":
            usern = "root"
        else:
            usern = cmd[3:]
        if (username != usern) and (username != "root"):
            passwd = getpass("\033[1;;m" + usern + "@localhost's Password: \033[0m")
            superSign = False
        else:
            superSign = True
        if not (usern in users):
            return "\033[1;31;mAccount %s Does Not Exist\n\033[0m" % usern
        if not superSign:
            if md5(passwd.encode('utf-8')).hexdigest() == users[usern]:
                username = usern
                return ''
            else:
                return "\033[1;31;mLogin Incorrect\n\033[0m"
        else:
            username = usern
            return ''
    elif unit == 'exec':
        if username == "root":
            code = system("sudo " + cmd[5:])
            return "\033[;32;mTransmited Default-Shell Execution Command As Root.\nDefault-Shell Returned \033[1;34;m%d\n\033[0m" % code
        else:
            code = system(cmd[5:])
            return "\033[;32;mTransmited Default-Shell Execution Command.\nDefault-Shell Returned \033[1;34;m%d\n\033[0m" % code
    elif unit == "raise":
        if cmd == "raise":
            raise Exception("Exception Thrown By The User.")
        elif cmd == "raise NameError":
            raise NameError("Exception Thrown By The User.")
        else:
            try:
                exec("raise %s(\"Exception Thrown By The User.\")" % cmd[6:])
            except NameError:
                return "\033[1;31;mException Type \"%s\" Does Not Exist.\n\033[0m" % cmd[6:]
    elif unit == "help":
        cmdstr = ''
        for each in cmds:
            cmdstr += "  %s%s - %s\n" % (each, ' ' * (8 - len(each)), cmds[each])
        return """\033[1;34;mHELP For LogicOS %s

  Copyright (c) 2020-2021 Littlebox.
  All Rights Reserved.

Commands:
%s
E.O.F.
\033[0m""" % (version, cmdstr)
    elif not (unit in cmds):
        return "\033[1;31;mCommand \"%s\" Hasn't Supposed.\n\033[0m" % unit
    else:
        return "Executed\n"

print("\033[1;;mLogicOS %s\nKernel- Not Mounted\033[0m\n\nCopyright (c) 2020-2021 Littlebox.\nAll Rights Reserved.\n" % version)

# Register & Log in.
def login():
    """Doc:
    Used To Handle User Login Operations. 
    No Parameters Are Required.
    """
    global username
    print("\033[1;32;mType \"register\" To Register New Accounts\n\033[0m")
    while True:
        username = input("\033[1;;mLogin: \033[0m")
        if username.lower() == 'register':
            username = input("\033[1;;mUsername: \033[0m")
            if username in users:
                print("\033[1;31;mAccount \"%s\" Already Exists!\n\033[0m" % username.title())
                continue
            passwd = getpass("\033[1;;mSet %s's Password: \033[0m" % username)
            passwd_again = getpass("\033[1;;mType Password Again: \033[0m")
            if not passwd == passwd_again:
                print("\n\033[1;31;mPasswords Are Inconsistent\n\033[0m")
                continue
            users[username] = md5(passwd.encode('utf-8')).hexdigest()
            save_users()
            print("\033[1;32;mRegistered\nLog In Now!\n\033[0m")
            continue
        passwd = getpass("\033[1;;m" + username + "@localhost's Password: \033[0m")
        if (username in users) and (md5(passwd.encode('utf-8')).hexdigest() == users[username]):
            print("\n\033[1;34;mWelcome Home, %s." % username.title())
            if int(datetime.now().strftime('%H')) < 6:
                hello = "Early hours of the new day, 加班有度, 减少劳累吧..."
            elif int(datetime.now().strftime('%H')) < 11:
                hello = "Good morning, 早上好, 煮一杯咖啡吧(๑´0`๑)"
            elif int(datetime.now().strftime('%H')) < 14:
                hello = "It's noon, 借一盏茶意, 休息一下吧(◦˙▽˙◦)"
            elif int(datetime.now().strftime('%H')) < 18:
                hello = "Good afternoon, 下午工作努力哦⊙∀⊙!"
            elif int(datetime.now().strftime('%H')) < 21:
                hello = "Hi, evening, 晚风吹过好时光..."
            else:
                hello = "Night, sleep, 带着一天的困倦拥抱明天..."
            print(hello, end = ' \033[0m\n\n')
            break
        else:
            print("\n\033[1;31;mLogin Incorrect\n\033[0m")

def getDirname():
    """Doc:
    Used To Get The Directory's "Lastname".
    No Parameters Are Required.
    """
    tempname = getcwd()
    if tempname == '/':
        return tempname
    dirname = ''
    for index in range(1, len(tempname)):
        if (tempname[-index] == '/') or (tempname[-index] == tempname[-index-1] == '\\'):
            return dirname[::-1]
        else:
            dirname = "%s%s" % (dirname, tempname[-index])
    return dirname[::-1]

if __name__ == '__main__':
    while True:
        try:
            login()
            # Simulation Shell.
            while True:
                if username == "root":
                    cmd = clearSpace(input("\033[1;;m[%s@localhost %s]# \033[0m" % (username, getDirname())))
                else:
                    cmd = clearSpace(input("\033[1;;m[%s@localhost %s]$ \033[0m" % (username, getDirname())))
                if cmd == '':
                    continue
                elif (cmd.lower() == "exit") or (cmd.lower() == "logout"):
                    print("\nLogout")
                    sleep(0.5)
                    exit(0)
                elif (cmd.lower() == "clear") or (cmd.lower() == "cls"):
                    clear()
                    continue
                elif (cmd.lower()[:5] == "echo ") or (cmd.lower()[:7] == "printf "):
                    if name == 'posix':
                        system(cmd)
                    else:
                        system("echo %s" % name[4:])
                    continue
                print(execute(cmd), end = '')
        except KeyboardInterrupt:
            exit(0)
        except Exception as reason:
            clear()
            if get_terminal_size().columns >= 48:
                stderr.write("""\033[1;31;m##     #  $$$$$$ $$$$$$  $$$$$$   $$$$$  $$$$$$
      #   $$     $$   $$ $$   $$ $$   $$ $$   $$
      #   $$$$$  $$$$$$  $$$$$$  $$   $$ $$$$$$
      #   $$     $$  $$  $$  $$  $$   $$ $$  $$
##     #  $$$$$$ $$   $$ $$   $$  $$$$$  $$   $$\n\n""")
            stderr.write("\033[1;31;mWarning:\n\nAn Unknown ERROR Occurred While Virtual-Mode Was Running.\nDon't Worry, You Can Choose To Feed Error Messages Back To Us, Which Will Help Us Analyze The Problem And Provide Solutions.\n\nBrief Description of The Error Causes:\n  %s\n\nDetail:\n  " % reason)
            for each in format_exc():
                if each != '\n':
                    stderr.write(each)
                else:
                    stderr.write('\n  ')
            stderr.write('\n')
            stderr.write("Please Send Us Detail Or The Entire Report To Give You A Better Experience.\n\n")
            stderr.write("E-mail: sunjunpeng2007@126.com\n%slittlebox2020@outlook.com\n" % (' ' * 8))
            stderr.write("Phone : +86 170 8537 0312\n\n")
            input("\033[0mType ENTER To Continue...")
            clear()
            print("LogicOS %s\nKernel- Not Mounted\n\nCopyright (c) 2020-2021 Littlebox.\nAll Rights Reserved.\n" % version)
