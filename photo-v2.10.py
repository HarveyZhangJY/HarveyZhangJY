import ctypes
import hashlib
import os
import shutil
import sys
import time
from typing import BinaryIO, Any

import xlwt
from tqdm import tqdm

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12
FOREGROUND_BLUE = 0x09  # blue.
FOREGROUND_RED = 0x0c  # red.
FOREGROUND_GREEN = 0x0a  # green.
FOREGROUND_DARKRED = 0x04  # dark red.
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool


def resetColor():
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)


def printGreen(mess):
    set_cmd_text_color(FOREGROUND_GREEN)
    sys.stdout.write(mess)
    resetColor()


def printDarkRed(mess):
    set_cmd_text_color(FOREGROUND_DARKRED)
    sys.stdout.write(mess)
    resetColor()


def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    file: BinaryIO = open(filename, 'rb')
    while True:
        b = file.read(8096)
        if not b:
            break
        myhash.update(b)
    file.close()
    return myhash.hexdigest()


def listdir(path, list_name):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            list_name.append(file_path)


book = xlwt.Workbook()
sheet = book.add_sheet('重复文件')
folderfilelist = []
folderfilelist2: Any = []
time1 = 0
time2 = 0
c = set()
e = []
m = []
time3 = 0
while True:
    printGreen("1、多目录文件去重\n2、两个目录文件比较\n[1|2|n]")
    h = str(input(""))
    if h == "1":
        time1 += 1
        while 1:
            time3 += 1
            lenfolderfilelist = len(folderfilelist)
            if time3 != 1:
                folderlen = str(input("请问你要继续输入目录么？[y|n]"))
            else:
                folderlen = "y"
            if folderlen == "y":
                folder = str(input("请输入路径。\n"))
                m.append(folder)
                lenlastfolderfilelist = len(folderfilelist)
                if not folderfilelist:
                    listdir(folder, folderfilelist)
                else:
                    listdir(folder, folderfilelist2)
                for Traverse2 in range(len(folderfilelist2)):
                    if folderfilelist2[Traverse2] not in folderfilelist:
                        folderfilelist.append(folderfilelist2[Traverse2])
                print("这次发现了%d个新文件,总共%d个" % (len(folderfilelist) - lenlastfolderfilelist, len(folderfilelist)),
                      flush=True)
            else:
                break
        if time1 == 0:
            continue
        else:
            for i in tqdm(range(len(folderfilelist)), ncols=50):
                # if i == 0:
                # printGreen("\n")
                # printGreen(""+"\r",end='')
                # printGreen("现在正在读%s的MD5"%(a[i])+"\r",end='',flush=True)
                d = len(c)
                c.add(GetFileMd5(folderfilelist[i]))
                if d == len(c):
                    e.append(folderfilelist[i])
            printGreen("已发现下列重复文件")
            try:
                with tqdm(range(10), ncols=-100) as t:
                    for i in t:
                        pass
            except KeyboardInterrupt:
                t.close()
                raise
            t.close()
            for k in range(len(e)):
                print(e[k] + " ")
                sheet.write(k % 65536, k // 65536, e[k])
                sheet.col(k // 65536).width = (len(e[k]) + 10) * 256
            printGreen("共计" + str(len(e)) + "个")
            name = "重复文件" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".xls"
            book.save(name)
            print('\n重复文件名写入成功，文件名为' + name + '\n')
            f = str(input("是否要删除重复文件？[y|n]\n"))
            if f == "y":
                for j in range(len(e)):
                    os.remove(e[j])
                # shutil.rmtree()
            continue
    elif h == "2":
        folder3list = []
        printGreen("请输入备份文件目录。")
        folder2 = str(input(""))
        time4 = 0
        while 1:
            time4 += 1
            if time4 != 1:
                wannacontinue = str(input("是否继续?[y|n]"))
            else:
                wannacontinue = "y"
            if wannacontinue == "y":
                printGreen("请输入文件目录。")
                folder3 = str(input(""))
                if folder2 == folder3:
                    printDarkRed("备份文件目录不能和文件目录一样")
                elif folder2 in folder3:
                    printGreen("对不起，现在暂时无法做这个功能")
                    print("\n", flush=True)
                folder3list.append(folder3)
            else:
                break
        folder2filelist = []
        folder3filelist = []
        folder2filelistMD5 = []
        folder3filelistMD5 = []
        listdir(folder2, folder2filelist)
        for Traverse in folder3list:
            listdir(Traverse, folder3filelist)
        for writefolder2filelistMD5 in tqdm(range(len(folder2filelist)), maxinterval=0.1):
            folder2filelistMD5.append(GetFileMd5(folder2filelist[writefolder2filelistMD5]))
        for writefolder3filelistMD5 in tqdm(range(len(folder3filelist)), maxinterval=0.1):
            folder3filelistMD5.append(GetFileMd5(folder3filelist[writefolder3filelistMD5]))
        thediffrenceoffolder2filelistandfolder3filelist = []
        try:
            with tqdm(range(10), ncols=-100) as t:
                for i in t:
                    pass
        except KeyboardInterrupt:
            t.close()
            raise
        t.close()
        for findthediffrenceoffolder2filelistandfolder2filelist in range(len(folder2filelist)):
            if folder2filelist[findthediffrenceoffolder2filelistandfolder2filelist] not in folder2filelist:
                thediffrenceoffolder2filelistandfolder3filelist.append(
                    folder2filelist[findthediffrenceoffolder2filelistandfolder2filelist])
        if not thediffrenceoffolder2filelistandfolder3filelist:
            printGreen("文件目录的内容：" + str(folder3filelist) + "都已备份。")
            print("\n")
        else:
            printGreen("两个目录的内容不一样。差了%s，共计%d个未备份" % (
                thediffrenceoffolder2filelistandfolder3filelist, len(thediffrenceoffolder2filelistandfolder3filelist)))
            printGreen("您要复制不同文件吗？\n[y|n]")
            cancopy = str(input(""))
            if cancopy == "y":
                for copyfile in range(len(thediffrenceoffolder2filelistandfolder3filelist)):
                    shutil.copy(thediffrenceoffolder2filelistandfolder3filelist[copyfile],
                                folder3 + thediffrenceoffolder2filelistandfolder3filelist[copyfile].split("/")[-1])
            print("\n")
    else:
        break
