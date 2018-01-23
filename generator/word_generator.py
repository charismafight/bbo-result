#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import glob
import os
import re
import shutil
import winreg
from turtle import *
import sys
import time

import pythoncom
import win32com
from win32com.client import Dispatch

from generator import fetcher

CURRENT_FOLDER = sys.path[0]
run_time_str = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
RESULTPATH = os.path.join(CURRENT_FOLDER, "results", "Result{}.docx".format(run_time_str))
REGSTR2 = r"pn\|(.+)\|st\|.*\|md\|(\d)(.+)\|rh\|(.*)\|ah\|(.+)\|sv\|(\w)\|mb\|(.+)\|mb\|p\|mb\|p\|mb\|p\|pg\|\|pc\|(.+)\|(pg\|\||mc\|[\s\S]{1,2}\|)$"
SUIT = {
    '&spades;': '\u2660',
    '&hearts;': '\u2665',
    '&diams;': '\u2663',
    '&clubs;': '\u2666',
}


# prepare directories


def init():
    paths = [
        os.path.join(sys.path[0], "files", run_time_str),
        os.path.join(CURRENT_FOLDER, "results"),
    ]

    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)


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


def get_available_table(doc, board_no):
    # where the data should be in 1st column
    default_table_no = board_no * tableCount
    # boardsCount -1 is the max []index
    for i in range(0, tableCount):
        if r"Open" in doc.Tables[default_table_no].Rows[1].Cells[0].Range.Text:
            default_table_no = default_table_no + 1
            continue
        else:
            doc.Tables[default_table_no].Rows[1].Cells[0].Range.Text = r"Open"
            return default_table_no
    return -1

    # path:output file


def handlelin(file_path):
    # according to the user input table count
    if not os.path.exists(file_path):
        print('can\'t file lin file')
        quit(0)
    f = open(file_path)
    lines = f.readlines()
    f.close()

    f = open(file_path.replace('lin', 'result'))
    results = f.readlines()
    f.close()

    try:
        pythoncom.CoInitialize()
        w = win32com.client.Dispatch('Word.Application')
        w.Visible = 0
        w.DisplayAlerts = 0
        doc = w.Documents.Open(RESULTPATH)
        for result_num, s in enumerate(lines):
            if s in record:
                print("repeated data,pass!")
                continue
            s = s.replace("\n", '')
            player_str = re.match(REGSTR2, s).group(1)
            flag = re.match(REGSTR2, s).group(2)
            cards = re.match(REGSTR2, s).group(3)
            board = re.match(REGSTR2, s).group(5)
            vul = re.match(REGSTR2, s).group(6)
            string6 = re.match(REGSTR2, s).group(7)
            string7 = re.match(REGSTR2, s).group(8)

            if flag == "3":
                flag1 = 1
            if flag == "4":
                flag1 = 2
            if flag == "1":
                flag1 = 3
            if flag == "2":
                flag1 = 0

            # key arithmetic we need count the table number to focus the correct table
            # table and result differentiate
            tnum = get_available_table(doc, result_num)

            if tnum == -1:
                continue

            players = player_str.split(r",")
            # while "" in players:
            #    players.remove("")
            for i in range(len(players)):
                doc.Tables[tnum].Rows[12].Cells[i].Range.Text = players[(i + 1) % 4]
                # empty valid
                if players[(i + 1) % 4] == '':
                    pass
                else:
                    doc.Tables[tnum].Rows[i + 17].Cells[0].Range.Text = players[(i + 1) % 4] + r": "
            cards = cards.split(',')
            SUIT_TYPE_REGSTR = r"S(.*)H(.*)D(.*)C(.*)$"
            if cards[0] != '':
                scards_s = re.match(SUIT_TYPE_REGSTR, cards[0]).group(1)
                doc.Tables[tnum].Rows[8].Cells[1].Range.Text = u"\u2660 " + sortstr(scards_s)
                scards_h = re.match(SUIT_TYPE_REGSTR, cards[0]).group(2)
                doc.Tables[tnum].Rows[9].Cells[1].Range.Text = u"\u2665 " + sortstr(scards_h)
                scards_d = re.match(SUIT_TYPE_REGSTR, cards[0]).group(3)
                doc.Tables[tnum].Rows[10].Cells[1].Range.Text = u"\u2666 " + sortstr(scards_d)
                scards_c = re.match(SUIT_TYPE_REGSTR, cards[0]).group(4)
                doc.Tables[tnum].Rows[11].Cells[1].Range.Text = u"\u2663 " + sortstr(scards_c)

            if cards[1] != '':
                wcards_s = re.match(SUIT_TYPE_REGSTR, cards[1]).group(1)
                doc.Tables[tnum].Rows[4].Cells[0].Range.Text = u"\u2660 " + sortstr(wcards_s)
                wcards_h = re.match(SUIT_TYPE_REGSTR, cards[1]).group(2)
                doc.Tables[tnum].Rows[5].Cells[0].Range.Text = u"\u2665 " + sortstr(wcards_h)
                wcards_d = re.match(SUIT_TYPE_REGSTR, cards[1]).group(3)
                doc.Tables[tnum].Rows[6].Cells[0].Range.Text = u"\u2666 " + sortstr(wcards_d)
                wcards_c = re.match(SUIT_TYPE_REGSTR, cards[1]).group(4)
                doc.Tables[tnum].Rows[7].Cells[0].Range.Text = u"\u2663 " + sortstr(wcards_c)
            if cards[2] != '':
                ncards_s = re.match(SUIT_TYPE_REGSTR, cards[2]).group(1)
                doc.Tables[tnum].Rows[0].Cells[1].Range.Text = u"\u2660 " + sortstr(ncards_s)
                ncards_h = re.match(SUIT_TYPE_REGSTR, cards[2]).group(2)
                doc.Tables[tnum].Rows[1].Cells[1].Range.Text = u"\u2665 " + sortstr(ncards_h)
                ncards_d = re.match(SUIT_TYPE_REGSTR, cards[2]).group(3)
                doc.Tables[tnum].Rows[2].Cells[1].Range.Text = u"\u2666 " + sortstr(ncards_d)
                ncards_c = re.match(SUIT_TYPE_REGSTR, cards[2]).group(4)
                doc.Tables[tnum].Rows[3].Cells[1].Range.Text = u"\u2663 " + sortstr(ncards_c)

            ecards_s = "".join([i for i in list("AKQJT98765432") if i not in list(scards_s) + list(wcards_s) + list(ncards_s)])
            doc.Tables[tnum].Rows[4].Cells[2].Range.Text = u"\u2660 " + sortstr(ecards_s)
            ecards_h = "".join([i for i in list("AKQJT98765432") if i not in list(scards_h) + list(wcards_h) + list(ncards_h)])
            doc.Tables[tnum].Rows[5].Cells[2].Range.Text = u"\u2665 " + sortstr(ecards_h)
            ecards_d = "".join([i for i in list("AKQJT98765432") if i not in list(scards_d) + list(wcards_d) + list(ncards_d)])
            doc.Tables[tnum].Rows[6].Cells[2].Range.Text = u"\u2666 " + sortstr(ecards_d)
            ecards_c = "".join([i for i in list("AKQJT98765432") if i not in list(scards_c) + list(wcards_c) + list(ncards_c)])
            doc.Tables[tnum].Rows[7].Cells[2].Range.Text = u"\u2663 " + sortstr(ecards_c)

            for r in SUIT.items():
                results[result_num] = results[result_num].replace(r[0], r[1])
            doc.Tables[tnum].Rows[16].Cells[0].Range.Text = r"Result: " + results[result_num]
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
        pythoncom.CoInitialize()
        # backupFile(firstFile)


def gen_word(table_count, boards_count):
    # template file name rule:form_tableCount_boardCount.docx
    formdoc = CURRENT_FOLDER + r"\template\form_" + str(table_count) + "_" + str(boards_count) + r".docx"
    print("checking " + formdoc)
    if not os.path.exists(formdoc):
        print("can't find template word:" + formdoc)
        input("Press Enter to quit:")
        quit()
    shutil.copyfile(formdoc, RESULTPATH)
    print("valid")


# files=glob.glob(r"C:\*.lin")
# print(r"Total: "+str(len(files))+r"files")
# for ini_file in files:
def end_with(s, *endstring):
    array = map(s.endswith, endstring)
    if True in array:
        return True
    else:
        return False


def backup(path):
    # shutil.move(path, CURRENT_FOLDER + '/' + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + ".lin")
    print('file was copied')


def mktime(t):
    return int(time.mktime(t))


# Main
init()
tableCount = 2
boardsCount = 20
# todo
# tableCount = int(input("Please input table count:"))
# boardsCount = int(input("Please input boards count:"))
start_time = datetime.datetime.strptime(input('Please input when the game start(eg:20180101):'), '%Y%m%d')
end_time = start_time + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)
game_key_word = 'Orange'
# todo to be delete or optimize into loop
gen_word(tableCount, boardsCount)
# data record
record = []
# generate files by bbo_id
players = open('bbo_id').readlines()
for x in players:
    x = x.strip('\n')
    p = os.path.join(CURRENT_FOLDER, 'files', run_time_str, "{}.lin".format(x))
    # todo gamekeyword
    fetcher.fetch(p, x, mktime(start_time.timetuple()), mktime(end_time.timetuple()), 'Untitled')
    handlelin(p)
print(r"Finished!Press Enter to close window.")
input()
