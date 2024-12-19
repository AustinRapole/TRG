#!/usr/bin/env python3
import sys
import sqlite3
import argparse
import math

#XXX Declare Database XXX
db = "TRGdatabase.db"

def bibList(table):
    connect = sqlite3.connect(db)
    cursor = connect.cursor()
    store = []

    temp = cursor.execute('''SELECT * FROM {};'''.format(table))
    for c in temp:
        store.append(c[0])
    return store


def find(text):
    first = False
    start = -1
    for i in range(len(text)):
        if(text[i] == "\"" and first == False):
            start = i
            first = True
    return text[start+1:len(text)-2]

def bibParser(file):
    temp = open(file, "r")
    data = temp.read()
    connect = sqlite3.connect(db)
    cursor = connect.cursor()

    split = data.split("\n\n")
    count = 0
    for s in split:
        count += 1
        start = -1
        end = -1
        con = True
        secCon = False
        thrdCon = False

        for i in range(0, len(s)):
            if(s[0] != "@"):
                con = False
            if(s[i] == "{"):
                start = i
                media = s[1:i]
                secCon = True
            if(s[i] == "}"):
                end = i+1
                thrdCon = True
        if(con == False or secCon == False or thrdCon == False):
            print("Syntax error on entry " + str(count))
            continue
        content = s[start:end]
        newtext = content.split("\n")

        text = newtext[0]
        bibkey = text[1:len(text)-1]

        author = ""
        title = ""
        year = ""

        for c in newtext:
            if(c.find("author") != -1):
                author = find(c)
            if(c.find("title") != -1):
                title = find(c)
            if(c.find("year") != -1):
                year = find(c)
        test = bibList("BIBLIOGRAPHY")
        if(bibkey not in test):
            try:
                cursor.execute('''INSERT INTO BIBLIOGRAPHY (BIBKEY,AUTHORS,TITLE,YEAR,MEDIUM,BIBTEX) VALUES(?,?,?,?,?,?)''',(bibkey,author,title,year,media,s))
                connect.commit()
            except Exception as e:
                print(e)
        else:
            print("BIBKEY is already in use")


def checkParser(file):
    temp = open(file, "r")
    data = temp.readlines()
    connect = sqlite3.connect(db)
    cursor = connect.cursor()

    for c in data:
        c = c.strip()
        temp = c.split("$")
        if(temp[0].upper() == "CHECKTWO" and len(temp) == 4):
            test = bibList("CHECKTWO")
            if(temp[1] not in test):
                try:
                    cursor.execute('''INSERT INTO CHECKTWO (BIBKEY,FORMULA,FUNCTION) VALUES(?,?,?)''',(temp[1],temp[2],temp[3]))
                    connect.commit()
                except Exception as e:
                    print(e)

            else:
                print("Bibkey is already being used" + c)

        elif(temp[0].upper() == "SANITIZEN" and len(temp) == 2):
            try:
                cursor.execute('''INSERT INTO SANITIZEN (FORMULA) VALUES(?)''',(temp[1],))
                connect.commit()
            except Exception as e:
                print(e)
        elif(temp[0].upper() == "CHECKONE" and len(temp) == 3):
            test = bibList("CHECKONE")
            if(temp[1] not in test):
                try:
                    cursor.execute('''INSERT INTO CHECKONE (BIBKEY,FORMULA) VALUES(?,?)''',(temp[1],temp[2]))
                    connect.commit()
                except Exception as e:
                    print(e)
            else:
                print("Bibkey is already being used" + c)
        else:
            print("Something went wrong with this line: " + c)

def printFun(table):
    connect = sqlite3.connect(db)
    cursor = connect.cursor()
    if(table == "CHECKONE"):
        conut = 0
        cursor.execute("Select * from {};".format(table))
        for i in cursor:
            conut += 1
            print("-------------------------------------- ROW {} --------------------------------------".format(conut))
            print("Bibkey: \t" +i[0])
            print("Formula: \t" +i[1])
            print("\n")
    elif(table == "CHECKTWO"):
        conut = 0
        cursor.execute("Select * from {};".format(table))
        for i in cursor:
            conut += 1
            print("-------------------------------------- ROW {} --------------------------------------".format(conut))
            print("Bibkey: \t" +i[0])
            print("Formula: \t" +i[1])
            print("Function: \t" +i[2])
            print("\n")
    elif(table == "SANITIZEN"):
        conut = 0
        cursor.execute("Select * from {};".format(table))
        for i in cursor:
            conut += 1
            print("-------------------------------------- ROW {} --------------------------------------".format(conut))
            print("Formula: \t" +i[0])
            print("\n")
    elif(table == "BIBLIOGRAPHY"):
        conut = 0
        cursor.execute("Select * from {};".format(table))
        for i in cursor:
            bibtab = i[5].split("\n")
            tabbed = '\n\t\t'.join(bibtab)
            conut += 1
            print("-------------------------------------- ROW {} --------------------------------------".format(conut))
            print("Bibkey: \t" +i[0])
            print("Author: \t" +i[1])
            print("Title:  \t" +i[2])
            print("Year:   \t" + str(i[3]))
            print("Medium: \t" +i[4])
            print("Bibtex: \t" + tabbed)
            print("\n")
    else:
        print("Invalid Table Name, Valid Tables: [CHECKONE, CHECKTWO, SANITIZEN, BIBLIOGRAPHY]")
            
def addFun(file):
    temp = open(file, "r")
    data = temp.read()
    if(data[0] == "@"):
        bibParser(file)
    else:
        checkParser(file)

def delFun(file):
    connect = sqlite3.connect(db)
    cursor = connect.cursor()
    temp = open(file, "r")
    data = temp.readlines()
    count = 0
    for c in data:
        count += 1
        c = c.strip()
        temp = c.split("$")
        if(len(temp) == 2):
            if(temp[0] == "SANITIZEN"):
                try:
                    cursor.execute('''Delete from {} where FORMULA=?;'''.format(temp[0]), (temp[1],))
                    connect.commit()
                except Exception as e:
                    print(e)
            else:
                try:
                    cursor.execute('''Delete from {} where BIBKEY=?;'''.format(temp[0]), (temp[1],))
                    connect.commit()
                except Exception as e:
                    print(e)
        else:
            print("Invalid number of inputs on line: " + str(count))
            

def upFun(file):
    connect = sqlite3.connect(db)
    cursor = connect.cursor()
    temp = open(file, "r")
    data = temp.readlines()
    count = 0
    for c in data:
        count += 1
        c = c.strip()
        temp = c.split("$")
        if(len(temp) == 4):
            if(temp[0] == "SANITIZEN"):
                try:
                    query = '''UPDATE {} SET {} = ? WHERE FORMULA = ?;'''.format(temp[0], temp[2])
                    cursor.execute(query, (temp[1],temp[3]))
                    connect.commit()
                except Exception as e:
                    print(e)
            elif(temp[0] == "CHECKONE" or temp[0] == "CHECKTWO" or temp[0] == "BIBLIOGRAPHY"):
                try:
                    query = '''UPDATE {} SET {} = ? WHERE BIBKEY = ?;'''.format(temp[0], temp[2])
                    cursor.execute(query, (temp[1],temp[3]))
                    connect.commit()
                except Exception as e:
                    print(e)
            else:
                print("Invalid table name on line " + str(count))
        else:
            print("Invalid number of inputs on line: " + str(count))
#Declare argc
argc = len(sys.argv)

def main():
  print("Admin Tool")
  parser = argparse.ArgumentParser(
      prog = 'ToadallyRealGraphs',
      description = 'Admin tool for BibTeX database')
  group = parser.add_mutually_exclusive_group()
  group.add_argument('-a', '--add', action = 'store_true', help = 'Add information')
  group.add_argument('-u', '--update', action = 'store_true', help = 'Update information')
  group.add_argument('-p', '--print', action = 'store_true', help = 'Print elements')
  group.add_argument('-d', '--delete', action = 'store_true', help = 'Delete row from table')
  group.add_argument('-l', '--list', action = 'store_true', help = 'List table names')
  parser.add_argument('-f', '--file', help = 'Import from file')
  parser.add_argument('-t', '--table', help = 'Select a table')

  args = parser.parse_args()

#Arguments for flags are stored in args.FLAGNAME
#Check if the argument exists (IS TRUE)
#Run Correlating function while passing in the argument
  
  if args.table:
    pass
  if args.add:
    addFun(args.file)
  if args.update:
    upFun(args.file)
  if args.file:
    pass
  if args.print:
    printFun(args.table)
  if args.delete:
    delFun(args.file)
  if args.list:
    print("CHECKONE")
    print("CHECKTWO")
    print("SANITIZEN")
    print("BIBLIOGRAPHY")


#print(args)

if __name__ == '__main__':
    main()
