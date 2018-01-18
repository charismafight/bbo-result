#!/usr/bin/python
# -*- coding: utf-8 -*-
import win32com
from win32com.client import Dispatch, constants
import os
import re
import glob
import sys
import shutil


def cur_file_dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path

    elif os.path.isfile(path):
        return os.path.dirname(path)


RESULTPATH = cur_file_dir() + "\\" + "Result.docx"


def sortstr(str11):
    ku = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}
    str111 = list(str11)
    if len(str111) > 1:
        if ku[str111[0]] > ku[str111[1]]:
            return str11
        else:
            return str11[::-1]
    else:
        return str11


def getAvailableTable(doc, boardNO):
    # where the data should be in 1st column
    defaultTbNO = boardNO * tableCount
    # boardsCount -1 is the max []index
    for i in range(0, tableCount):
        if r"Open" in doc.Tables[defaultTbNO].Rows[1].Cells[0].Range.Text:
            defaultTbNO = defaultTbNO + 1
            continue
        else:
            doc.Tables[defaultTbNO].Rows[1].Cells[0].Range.Text = r"Open"
            return defaultTbNO
    return -1



    # path:output file


def handlelin(fileNO):
    # according to the user input table count
    f = open(cur_file_dir() + "\\" + str(fileNO) + ".lin", 'r')
    line = f.readlines()
    results = str.replace(re.match(r"^rs\|(.+),\|$", line[1]).group(1), ',,', ',').split(r",")
    # can be 'find the regular name' or get the form.docx
    # todo
    # if
    # (len(results)==16)|(len(results)==20)|(len(results)==24)|(len(results)==32)|(len(results)==40)|(len(results)==48):
    #    formdoc=cur_file_dir()+"\\"+r"form_pairs\form_"+str(int(len(results)/2))+r".docx"
    # else:
    #    formdoc=cur_file_dir()+"\\"+r"form_pairs\form.docx"

    # wordfile=os.path.splitext(path)[0]+r".docx"
    # os.system("copy %s %s" % (formdoc,"\""+wordfile+"\""))
    # shutil.copyfile(formdoc,wordfile)
    try:
        w = win32com.client.Dispatch('Word.Application')
        w.Visible = 0
        w.DisplayAlerts = 0
        doc = w.Documents.Open(RESULTPATH)
        info2 = line[6:]
        for s in info2:
            if s in record:
                print("repeated data,pass!")
                continue
            # e......too much,shield......
            # print("Good luck!  My lovely sherry!")
            if re.match(
                    r"qx\|(.+)\|pn\|(.+)\|st\|\|md\|(\d)(.+)\|rh\|\|ah\|(.+)\|sv\|(\w)\|mb\|(.+)\|mb\|p\|mb\|p\|mb\|p\|pg\|\|$",
                    s):
                string0 = re.match(
                    r"qx\|(.+)\|pn\|(.+)\|st\|\|md\|(\d)(.+)\|rh\|\|ah\|(.+)\|sv\|(\w)\|mb\|(.+)\|mb\|p\|mb\|p\|mb\|p\|pg\|\|$",
                    s).group(1)
                string1 = re.match(
                    r"qx\|(.+)\|pn\|(.+)\|st\|\|md\|(\d)(.+)\|rh\|\|ah\|(.+)\|sv\|(\w)\|mb\|(.+)\|mb\|p\|mb\|p\|mb\|p\|pg\|\|$",
                    s).group(2)
                flag = re.match(
                    r"qx\|(.+)\|pn\|(.+)\|st\|\|md\|(\d)(.+)\|rh\|\|ah\|(.+)\|sv\|(\w)\|mb\|(.+)\|mb\|p\|mb\|p\|mb\|p\|pg\|\|$",
                    s).group(3)
                string3 = re.match(
                    r"qx\|(.+)\|pn\|(.+)\|st\|\|md\|(\d)(.+)\|rh\|\|ah\|(.+)\|sv\|(\w)\|mb\|(.+)\|mb\|p\|mb\|p\|mb\|p\|pg\|\|$",
                    s).group(4)
                board = re.match(
                    r"qx\|(.+)\|pn\|(.+)\|st\|\|md\|(\d)(.+)\|rh\|\|ah\|(.+)\|sv\|(\w)\|mb\|(.+)\|mb\|p\|mb\|p\|mb\|p\|pg\|\|$",
                    s).group(5)
                vul = re.match(
                    r"qx\|(.+)\|pn\|(.+)\|st\|\|md\|(\d)(.+)\|rh\|\|ah\|(.+)\|sv\|(\w)\|mb\|(.+)\|mb\|p\|mb\|p\|mb\|p\|pg\|\|$",
                    s).group(6)
                string6 = re.match(
                    r"qx\|(.+)\|pn\|(.+)\|st\|\|md\|(\d)(.+)\|rh\|\|ah\|(.+)\|sv\|(\w)\|mb\|(.+)\|mb\|p\|mb\|p\|mb\|p\|pg\|\|$",
                    s).group(7)
                string7 = ""
            else:
                string0 = re.match(r"qx\|(.+)\|pn\|(.+)\|st\|\|md\|(\d)(.+)\|rh\|\|ah\|(.+)\|sv\|(\w)\|mb\|(.+)\|mb\|p\|mb\|p\|mb\|p\|pg\|\|pc\|(.+)\|pg\|\|$", s).group(1)
                string1 = re.match(
                    r"qx\|(.+)\|pn\|(.+)\|st\|\|md\|(\d)(.+)\|rh\|\|ah\|(.+)\|sv\|(\w)\|mb\|(.+)\|mb\|p\|mb\|p\|mb\|p\|pg\|\|pc\|(.+)\|pg\|\|$",
                    s).group(2)
                flag = re.match(
                    r"qx\|(.+)\|pn\|(.+)\|st\|\|md\|(\d)(.+)\|rh\|\|ah\|(.+)\|sv\|(\w)\|mb\|(.+)\|mb\|p\|mb\|p\|mb\|p\|pg\|\|pc\|(.+)\|pg\|\|$",
                    s).group(3)
                string3 = re.match(
                    r"qx\|(.+)\|pn\|(.+)\|st\|\|md\|(\d)(.+)\|rh\|\|ah\|(.+)\|sv\|(\w)\|mb\|(.+)\|mb\|p\|mb\|p\|mb\|p\|pg\|\|pc\|(.+)\|pg\|\|$",
                    s).group(4)
                board = re.match(
                    r"qx\|(.+)\|pn\|(.+)\|st\|\|md\|(\d)(.+)\|rh\|\|ah\|(.+)\|sv\|(\w)\|mb\|(.+)\|mb\|p\|mb\|p\|mb\|p\|pg\|\|pc\|(.+)\|pg\|\|$",
                    s).group(5)
                vul = re.match(
                    r"qx\|(.+)\|pn\|(.+)\|st\|\|md\|(\d)(.+)\|rh\|\|ah\|(.+)\|sv\|(\w)\|mb\|(.+)\|mb\|p\|mb\|p\|mb\|p\|pg\|\|pc\|(.+)\|pg\|\|$",
                    s).group(6)
                string6 = re.match(
                    r"qx\|(.+)\|pn\|(.+)\|st\|\|md\|(\d)(.+)\|rh\|\|ah\|(.+)\|sv\|(\w)\|mb\|(.+)\|mb\|p\|mb\|p\|mb\|p\|pg\|\|pc\|(.+)\|pg\|\|$",
                    s).group(7)
                string7 = re.match(
                    r"qx\|(.+)\|pn\|(.+)\|st\|\|md\|(\d)(.+)\|rh\|\|ah\|(.+)\|sv\|(\w)\|mb\|(.+)\|mb\|p\|mb\|p\|mb\|p\|pg\|\|pc\|(.+)\|pg\|\|$",
                    s).group(8)

            if flag == "3":
                flag1 = 1
            if flag == "4":
                flag1 = 2
            if flag == "1":
                flag1 = 3
            if flag == "2":
                flag1 = 0

            # key arithmetic we need count the tableNO to focus the correct
            # table
            # table and reusltNum differentiate
            resultNum = int(re.match(r'^o(\d+)', string0).group(1)) - 1
            tnum = getAvailableTable(doc, resultNum)

            if tnum == -1:
                continue

            players = string1.split(r",")
            while "" in players:
                players.remove("")
            for i in range(len(players)):
                doc.Tables[tnum].Rows[12].Cells[i].Range.Text = players[(i + 1) % 4]
                doc.Tables[tnum].Rows[i + 17].Cells[0].Range.Text = players[(i + 1) % 4] + r": "
            cards = string3.split(r",")
            scards_s = re.match(r"S(.*)H(.*)D(.*)C(.*)$", cards[0]).group(1)
            doc.Tables[tnum].Rows[8].Cells[1].Range.Text = u"\u2660 " + sortstr(scards_s)
            scards_h = re.match(r"S(.*)H(.*)D(.*)C(.*)$", cards[0]).group(2)
            doc.Tables[tnum].Rows[9].Cells[1].Range.Text = u"\u2665 " + sortstr(scards_h)
            scards_d = re.match(r"S(.*)H(.*)D(.*)C(.*)$", cards[0]).group(3)
            doc.Tables[tnum].Rows[10].Cells[1].Range.Text = u"\u2666 " + sortstr(scards_d)
            scards_c = re.match(r"S(.*)H(.*)D(.*)C(.*)$", cards[0]).group(4)
            doc.Tables[tnum].Rows[11].Cells[1].Range.Text = u"\u2663 " + sortstr(scards_c)
            wcards_s = re.match(r"S(.*)H(.*)D(.*)C(.*)$", cards[1]).group(1)
            doc.Tables[tnum].Rows[4].Cells[0].Range.Text = u"\u2660 " + sortstr(wcards_s)
            wcards_h = re.match(r"S(.*)H(.*)D(.*)C(.*)$", cards[1]).group(2)
            doc.Tables[tnum].Rows[5].Cells[0].Range.Text = u"\u2665 " + sortstr(wcards_h)
            wcards_d = re.match(r"S(.*)H(.*)D(.*)C(.*)$", cards[1]).group(3)
            doc.Tables[tnum].Rows[6].Cells[0].Range.Text = u"\u2666 " + sortstr(wcards_d)
            wcards_c = re.match(r"S(.*)H(.*)D(.*)C(.*)$", cards[1]).group(4)
            doc.Tables[tnum].Rows[7].Cells[0].Range.Text = u"\u2663 " + sortstr(wcards_c)
            ncards_s = re.match(r"S(.*)H(.*)D(.*)C(.*)$", cards[2]).group(1)
            doc.Tables[tnum].Rows[0].Cells[1].Range.Text = u"\u2660 " + sortstr(ncards_s)
            ncards_h = re.match(r"S(.*)H(.*)D(.*)C(.*)$", cards[2]).group(2)
            doc.Tables[tnum].Rows[1].Cells[1].Range.Text = u"\u2665 " + sortstr(ncards_h)
            ncards_d = re.match(r"S(.*)H(.*)D(.*)C(.*)$", cards[2]).group(3)
            doc.Tables[tnum].Rows[2].Cells[1].Range.Text = u"\u2666 " + sortstr(ncards_d)
            ncards_c = re.match(r"S(.*)H(.*)D(.*)C(.*)$", cards[2]).group(4)
            doc.Tables[tnum].Rows[3].Cells[1].Range.Text = u"\u2663 " + sortstr(ncards_c)
            ecards_s = "".join(
                [i for i in list("AKQJT98765432") if i not in list(scards_s) + list(wcards_s) + list(ncards_s)])
            doc.Tables[tnum].Rows[4].Cells[2].Range.Text = u"\u2660 " + sortstr(ecards_s)
            ecards_h = "".join(
                [i for i in list("AKQJT98765432") if i not in list(scards_h) + list(wcards_h) + list(ncards_h)])
            doc.Tables[tnum].Rows[5].Cells[2].Range.Text = u"\u2665 " + sortstr(ecards_h)
            ecards_d = "".join(
                [i for i in list("AKQJT98765432") if i not in list(scards_d) + list(wcards_d) + list(ncards_d)])
            doc.Tables[tnum].Rows[6].Cells[2].Range.Text = u"\u2666 " + sortstr(ecards_d)
            ecards_c = "".join(
                [i for i in list("AKQJT98765432") if i not in list(scards_c) + list(wcards_c) + list(ncards_c)])
            doc.Tables[tnum].Rows[7].Cells[2].Range.Text = u"\u2663 " + sortstr(ecards_c)
            doc.Tables[tnum].Rows[16].Cells[0].Range.Text = r"Result: " + results[resultNum]
            doc.Tables[tnum].Rows[0].Cells[0].Range.Text = board
            trick = string7.split(r"|pg||pc|")
            num1 = len(trick)
            if num1 < 6:
                for i in range(len(trick) - 1):
                    doc.Tables[tnum].Rows[14 + i].Cells[0].Range.Rows.Add()
                for i in range(len(trick)):
                    everytrick = trick[i].split(r"|pc|")
                    for j in range(len(everytrick)):
                        doc.Tables[tnum].Rows[15 + i].Cells[j].Range.Text = everytrick[j][0:2]
            else:
                for i in range(4):
                    doc.Tables[tnum].Rows[14 + i].Cells[0].Range.Rows.Add()
                for i in range(5):
                    everytrick = trick[i].split(r"|pc|")
                    for j in range(len(everytrick)):
                        doc.Tables[tnum].Rows[15 + i].Cells[j].Range.Text = everytrick[j][0:2]
            bid = string6.split(r"|mb|")
            describe = []
            for bbb in bid:
                if re.match("(\d[H|C|D|S])(!?)\|an\|(.+)", bbb):
                    describe.append(re.match("(\d[H|C|D|S])(!?)\|an\|(.+)", bbb).group(1) + r": " + re.match(
                        "(\d[HCDSN])(!?)\|an\|(.+)", bbb).group(3))
                if re.match("(\dN)(!?)\|an\|(.+)", bbb):
                    describe.append(re.match("(\dN)(!?)\|an\|(.+)", bbb).group(1).replace("N", "NT") + r": " + re.match(
                        "(\d[HCDSN])(!?)\|an\|(.+)", bbb).group(3))
                if re.match("(d)(!?)\|an\|(.+)", bbb):
                    describe.append(r"X: " + re.match("(d)(!?)\|an\|(.+)", bbb).group(3))
                if re.match("(r)(!?)\|an\|(.+)", bbb):
                    describe.append(r"XX: " + re.match("(r)(!?)\|an\|(.+)", bbb).group(3))
            describe_str = "\n".join(describe)
            doc.Tables[tnum].Rows[14].Cells[0].Range.Text = describe_str
            bid.append(r"P")
            bid.append(r"P")
            bid.append(r"P")
            for i in range(int((len(bid) + flag1 - 1) / 4)):
                doc.Tables[tnum].Rows[12 + i].Cells[0].Range.Rows.Add()
            for i in range(len(bid)):
                doc.Tables[tnum].Rows[13 + int((i + flag1) / 4)].Cells[(i + flag1) % 4].Range.Text = bid[i][0:2]
                if re.match("^\dN$", bid[i][0:2]):
                    doc.Tables[tnum].Rows[13 + int((i + flag1) / 4)].Cells[(i + flag1) % 4].Range.Text = bid[i][
                                                                                                         0:2].replace(
                        "N", "NT")
                if re.match("^d$", bid[i][0:1]):
                    doc.Tables[tnum].Rows[13 + int((i + flag1) / 4)].Cells[(i + flag1) % 4].Range.Text = r"X"
                if re.match("^r$", bid[i][0:1]):
                    doc.Tables[tnum].Rows[13 + int((i + flag1) / 4)].Cells[(i + flag1) % 4].Range.Text = r"XX"

            # save the data that has already handled
            record.append(s)
    except Exception as err:
        print(err)
    finally:
        doc.Close()
        w.Quit()


def genWord():
    # template file name rule:form_tableCount_boardCount.docx
    formdoc = cur_file_dir() + "\\" + r"form_" + str(tableCount) + "_" + str(boardsCount) + r".docx"
    print("searching word")
    if not os.path.exists(formdoc):
        print("cant find template word：" + formdoc)
        input("Press Enter to quit:")
        quit()
    shutil.copyfile(formdoc, RESULTPATH)
    print("file was copied")


def linsValid():
    for i in range(1, tableCount + 1):
        if os.path.exists(cur_file_dir() + "\\" + str(i) + ".lin"):
            print("file checking passed")
            continue
        else:
            return False
    return True


# files=glob.glob(r"D:\*.lin")
# print(r"Total: "+str(len(files))+r"files")
# for ini_file in files:






# Main
tableCount = int(input("Please input table count:"))
boardsCount = int(input("Please input boards count:"))
# linCount = int(input("Please input lin file Count:"))
# first check the lins valid
if not linsValid():
    print("error!we need 1 to N(tableCounts) .lin files")
    input("Press Enter to quit:")
    quit()
# secondly choose a template and make a copy
genWord()
# then circulate the tablecount and read diffrent lin file to fill data
# update:change the circulation to lin file
# for i in range(0,tableCount):
linFiles = glob.glob(cur_file_dir() + r"\*.lin")
# data record
record = []
for i in range(1, len(linFiles) + 1):
    print("handle the " + str(i) + ".lin")
    handlelin(i)
print(r"Finished!")
input("Press Enter to continue: ")
