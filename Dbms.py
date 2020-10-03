import tkinter as tk
from tkinter import *
import tkinter.messagebox as mb
import mysql.connector as con
from mysql.connector import errorcode
import time
import random

def addNewDB():
    global root, newDbName
    root = tk.Tk()
    root.title('Add new database')
    root.geometry('500x500+450+200')
    tk.Label(root, text = 'Add New database').pack()
    tk.Button(root, text = 'Back',command = mainMenu).place(x=20, y = 20)
    tk.Label(root, text = 'Enter Database Name').place(x = 30, y = 100)
    newDbName = tk.StringVar(root)
    tk.Entry(root, textvariable = newDbName, width = 30).place(x = 190, y = 100)
    tk.Button(root, text = 'OK',command = createDB).place(x = 225, y = 150)
    root.mainloop()

def createDB():
    try:
        cur.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(newDbName.get()))
        mb.showinfo('Alert!','{} Database has been created'.format(newDbName.get()))
    except con.Error as err:
        if err.errno == 1007:
            mb.showinfo('Alert!','Database already exist')
        elif err.errno == 1064:
            mb.showinfo('Alert!','Enter a valid Database Name')
        else:
            mb.showinfo('Alert!','Falid to Create database:{}'.format(err))


def showDatabase():
    global root
    root.destroy()
    root=tk.Tk()
    root.title('Show Database')
    root.geometry('500x500+450+200')
    tk.Button(root,text='Back',command=mainMenu).place(x=20,y=20)
    tk.Label(root,text='Show Database',font=('ubuntu',20)).pack()
    line='---------------------------------------------------'
    tk.Label(root,text=line).pack()
    scrollbar = tk.Scrollbar(root)
    scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
    Lb1=tk.Listbox(root,width=53,font=('ubuntu',12),selectbackground='green',selectmode=tk.BROWSE,yscrollcommand=scrollbar.set)
    
    cur.execute('show databases')
    listboxind=1
    for i in cur:
        Lb1.insert(listboxind,str(listboxind)+'. '+i[0])
        listboxind+=1
    
    Lb1.pack(side=tk.LEFT,fill=BOTH)
    scrollbar.config(command=Lb1.yview)
    root.mainloop()

def deleteDB():
    global root,delDbName
    root.destroy()
    root=tk.Tk()
    root.title('Delete database')
    root.geometry('500x500+450+200')
    tk.Label(root,text='Delete DataBase',font=('ubuntu',20)).pack()    
    tk.Button(root,text='Back',command=mainMenu).place(x=20,y=20)    
    tk.Label(root,text='Enter Database Name').place(x=30,y=100)
    delDbName=tk.StringVar(root)
    tk.Entry(root,textvariable=delDbName,width=30).place(x=190,y=100)
    tk.Button(root,text='OK',command = delDbFun).place(x=225,y=150)
    root.mainloop()

def delDbFun():
    try:
        cur.execute("DROP DATABASE {}".format(delDbName.get()))
        mb.showinfo('Alert!','{} Database has been deleted!!'.format(delDbName.get()))
    except con.Error as err:
        print(err.errno,err)
        if(err.errno==1008):
            mb.showinfo('Alert!','{} Database doesnot exist!!'.format(delDbName.get()))

def createTab():
    global root,tabDBName,tabName,colNum
    root.destroy()
    root=tk.Tk()
    root.title('Create new table')
    root.geometry('500x500+450+200')
    tk.Label(root,text='Create New Table',font=('ubuntu',20)).pack()    
    tk.Button(root,text='Back',command=mainMenu).place(x=20,y=20)    
    tk.Label(root,text='Enter Database Name').place(x=30,y=100)
    tabDBName=tk.StringVar(root)
    tk.Entry(root,textvariable=tabDBName,width=30).place(x=190,y=100)

    tk.Label(root,text='Enter Table Name').place(x=30,y=150)
    tabName=tk.StringVar(root)
    tk.Entry(root,textvariable=tabName,width=30).place(x=190,y=150)

    tk.Label(root,text='Number of Columns').place(x=30,y=200)
    colNum=tk.StringVar(root)
    tk.Entry(root,textvariable=colNum,width=30).place(x=190,y=200)
    
    tk.Button(root,text='OK',command = createTabFun).place(x=225,y=300)
    root.mainMenu()


def createTabFun():
    try:
        global top,name,dataType,dvalue
        cur.execute("USE {}".format(tabDBName.get()))
        cur.execute('SHOW TABLES')
        tabs = []
        for i in cur:
            tabs.append(i[0])
        if colNum.get() == '':
            mb.showinfo('Alert!','Enter the valid column Numbers')
        elif tabName.get() in tabs:
            mb.showinfo('Alert!','{} Table Already Exits'.format(tabName.get()))
        elif tabName.get() == '':
            mb.showinfo('Alert!','Enter the valid Table Name')
        else:
            top = tk.Tk()
            top.title('Tabel Details')
            top.geometry('500x500+450+200')
            tk.Label(top,text='Enter the Details',font=('ubuntu',20)).pack()
            tk.Label(top,text='Column Name',font=('ubuntu',10)).place(x=45,y=50)
            tk.Label(top,text='Data Type',font=('ubuntu',10)).place(x=210,y=50)
            tk.Label(top,text='Default Value',font=('ubuntu',10)).place(x=360,y=50)
            name=[]
            dataType=[]
            dvalue=[]
            dist=70
            for i in range(0,int(colNum.get())):
                name.append(StringVar(top))
                dataType.append(StringVar(top))
                dvalue.append(StringVar(top))
                tk.Entry(top,textvariable=name[i],width=18).place(x=20,y=dist)
                tk.Entry(top,textvariable=dataType[i],width=18).place(x=175,y=dist)
                tk.Entry(top,textvariable=dvalue[i],width=18).place(x=330,y=dist)
                dist+=25

            tk.Button(top,text='OK',command=lambda:[createTabOnSql()]).place(x=200,y=400)
            tk.Button(top,text='Cancel',command=lambda:[showInfo(2),top.destroy()]).place(x=250,y=400)
    except con.Error as err:
        print(err.errno)
        if(err.errno==1049 or err.errno==1064):
            mb.showinfo('Alert!','Enter the Vaild Database')

def createTabOnSql():
    try:
        query=''
        for i in range(0,len(name)):
            n=name[i].get()+' '+dataType[i].get()+' '+dvalue[i].get()
            query=query+n+','
        query='CREATE TABLE '+tabName.get()+'('+query[:len(query)-1].upper()+')'
        cur.execute(query)
        mb.showinfo('Alert!','{} Table Has Been Created in {} Database'.format(tabName.get(),tabDBName.get()))
    except con.Error as err:
        print(err.errno)
        if(err.errno==1064):
            mb.showinfo('Alert!','Fill all the details correctly')
        else:
            mb.showinfo('Alert!','Something Went Wrong,Try Again')


def insertInTab():
    global root,inDbName,inTabName,inValues
    root.destroy()
    root=tk.Tk()
    root.title('Insert in Table')
    root.geometry('500x500+450+200')
    tk.Label(root,text='Columns Details',font=('ubuntu',20)).pack()    
    tk.Button(root,text='Back',command=mainMenu).place(x=20,y=20)    
    tk.Label(root,text='Enter Database Name').place(x=30,y=100)
    inDbName=tk.StringVar(root)
    tk.Entry(root,textvariable=inDbName,width=30).place(x=190,y=100)
    tk.Label(root,text='Enter Table Name').place(x=30,y=150)
    inTabName=tk.StringVar(root)
    tk.Entry(root,textvariable=inTabName,width=30).place(x=190,y=150)

    tk.Button(root,text='Get Columns Name',command = getColName).place(x=180,y=190)

    tk.Label(root,text="Note-Enter string in cords(' ')").place(x=190,y=280)
    tk.Label(root,text='Enter Columns Values').place(x=30,y=300)
    inValues=tk.StringVar(root)
    tk.Entry(root,textvariable=inValues,width=30).place(x=190,y=300)
    
    #tk.Label(root,text='Software created by Mr. Engineer',font=('ubuntu',10)).place(x=140,y=470)
    tk.Button(root,text='Insert',command = onSqlInsert).place(x=225,y=350)      
    root.mainloop()

def getColName():
    try:
        global colNames
        cur.execute("USE {}".format(inDbName.get()))
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{}'".format(inTabName.get()))
        colNames=[]
        for i in cur:
            colNames.append(i[0])
            colNames.append(',')
        tk.Label(root,text='                                                             ').place(x=150,y=230)
        if(len(inTabName.get())==0):
            mb.showinfo('Alert!','Table Name is Empty')
        elif(len(colNames)==0):
            mb.showinfo('Alert!','Table Doesnot Exist')    
        tk.Label(root,text=colNames[:len(colNames)-1]).place(x=150,y=230)
    except con.Error as err:
        print(err.errno)
        print(err)
        if(err.errno==1064):
            mb.showinfo('Alert!','Enter Database Name')
        elif(err.errno==1049):
            mb.showinfo('Alert!','Database Doesnot Exist')


def onSqlInsert():
    try:
        cur.execute("USE {}".format(inDbName.get()))
        colNam=''
        for i in colNames:
            if(i!=','):
                colNam=colNam+i+','
        colNam=colNam[:len(colNam)-1]
        print("INSERT INTO {}({})VALUES({})".format(inTabName.get(),colNam,inValues.get().upper()))
        cur.execute("INSERT INTO {}({})VALUES({})".format(inTabName.get(),colNam,inValues.get().upper()))
        dbs.commit()
        mb.showinfo('Alert!','Insert Successful!')
    except con.Error as err:
        print(err.errno)
        print(err)
        if(err.errno==1049):
            mb.showinfo('Alert!','{} Database Doesnot Exist'.format(inDbName.get()))
        elif(err.errno==1064):
            mb.showinfo('Alert!','Enter Valid Table Name')
        elif(err.errno==1136):
            mb.showinfo('Alert!','Column count doesnot match value count')
        elif(err.errno==1366):
            mb.showinfo('Alert!','Incorrect integer value')

def showTab():
    global root,useDbName,showTabName
    root.destroy()
    root=tk.Tk()
    root.title('Show Table')
    root.geometry('500x500+450+200')
    tk.Label(root,text='Table Details',font=('ubuntu',20)).pack()    
    tk.Button(root,text='Back',command=mainMenu).place(x=20,y=20)    
    tk.Label(root,text='Enter Database Name').place(x=30,y=100)
    useDbName=tk.StringVar(root)
    tk.Entry(root,textvariable=useDbName,width=30).place(x=190,y=100)
    tk.Label(root,text='Enter Table Name').place(x=30,y=150)
    showTabName=tk.StringVar(root)
    tk.Entry(root,textvariable=showTabName,width=30).place(x=190,y=150)
    
    #tk.Label(root,text='Software created by Mr. Engineer',font=('ubuntu',10)).place(x=140,y=470)
    tk.Button(root,text='OK',command = showTabFun).place(x=225,y=250)      
    root.mainloop()

def showTabFun():
    try:
        cur.execute("USE {}".format(useDbName.get()))
        cur.execute("SELECT * FROM {} LIMITS 35".format(showTabName.get()))
        dataList = [()]
        for i in cur:
            dataList.append(i)
        if len(dataList) == 0:
            mb.showinfo('Alert!','Table is Empty')
        else:
            top = tk.Tk()
            top.title('Result')
            top.geometry('800x800+950+200')
            tk.Label(top,text='Result',font=('ubuntu',20)).place(x=300,y=5)
            tk.Label(top,text='Top 35',font=('ubuntu',12)).place(x=310,y=40)
            
            cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{}'".format(showTabName.get()))
            col=[]
            for i in cur:
                col.append(i[0])
            print(col)             
            print(dataList)

            xdist=20
            ydist=65
            for r in range(0,len(dataList)):
                for c in range(0,len(col)):
                    if(r==0):
                        tk.Label(top,text=col[c],borderwidth=2).place(x=xdist,y=ydist)
                        xdist+=150
                    else:
                        tk.Label(top,text=dataList[r][c],borderwidth=2).place(x=xdist,y=ydist)
                        xdist+=150
                xdist=20
                ydist+=20
                
            tk.Button(top,text='Close',command=lambda:[top.destroy()]).pack(side=BOTTOM)
            top.mainloop()
    except con.Error as err:
        print(err)
        if(err.errno==1049):
            mb.showinfo('Alert!','{} Database Doesnot Exist!'.format(useDbName.get()))
        elif(err.errno==1064):
            mb.showinfo('Alert!','Please Enter Table Name!')
        elif(err.errno==1146):
            mb.showinfo('Alert!','{} Table Doesnot Exist in {} Database'.format(showTabName.get(),useDbName.get()))

            

def delTab():
    global root,delDBName,deltabName
    root.destroy()
    root=tk.Tk()
    root.title('Create new table')
    root.geometry('500x500+450+200')
    tk.Label(root,text='Create New Table',font=('ubuntu',20)).pack()    
    tk.Button(root,text='Back',command=mainMenu).place(x=20,y=20)    
    tk.Label(root,text='Enter Database Name').place(x=30,y=100)
    delDBName=tk.StringVar(root)
    tk.Entry(root,textvariable=delDBName,width=30).place(x=190,y=100)

    tk.Label(root,text='Enter Table Name').place(x=30,y=150)
    deltabName=tk.StringVar(root)
    tk.Entry(root,textvariable=deltabName,width=30).place(x=190,y=150)
    tk.Button(root,text='OK',command = delTabFun).place(x=225,y=300)
    #tk.Label(root,text='Software created by Mr. Engineer',font=('ubuntu',10)).place(x=140,y=470)
    root.mainloop()

def delTabFun():
    try:
        cur.execute("USE {}".format(delDBName.get()))
        cur.execute("DROP TABLE {}".format(deltabName.get()))
        mb.showinfo('Alert!','table has been deleted!')
    except con.Error as err:
        print(err.errno)
        print(err)
        if(err.errno==1049):
            mb.showinfo('Alert!','Database Doesnot Exist!')
        elif(err.errno==1064):
            mb.showinfo('Alert!','Enter Database/Table Name!')
        if(err.errno==1051):
            mb.showinfo('Alert!','Table Doesnot Exist!')
    
def showInfo(c):
    if(c==1):
        mb.showinfo('Caution!','You are Logged Out!!')
    elif(c==2):
        mb.showinfo('Caution!','Canceled Table creation!!')

def logoutFun():
    cur.close()
    showInfo(c=1)
    secureLogin()
    
def secureLogin():
    global root , hostName , userName , passWord
    root.destroy()
    root = tk.Tk()
    root.geometry('500x500+450+200')
    root.title('Welcome to DBMS software')
    tk.Label(root, text = 'DBMS Software', font=('ubuntu',20)).place(x = 145, y = 50)

    tk.Label(root, text = 'Hostname').place(x=115, y =150)
    hostName = tk.StringVar(root)
    tk.Entry(root, textvariable = hostName, width = 25).place(x = 200, y = 150)

    tk.Label(root , text = 'Username').place(x = 115, y = 180)
    userName = tk.StringVar(root)
    tk.Entry(root, textvariable = userName, width = 25).place(x = 200 , y = 180)

    tk.Label(root , text = 'Password').place(x = 115, y = 210)
    passWord = tk.StringVar(root)
    tk.Entry(root, textvariable = passWord, width = 25, show='*').place(x=200,y=210)

    tk.Button(root, text='Login', command = validDetails).place(x = 230, y = 300)
    root.mainloop()

def validDetails():
    global cur , dbs
    hostname = hostName.get()
    username = userName.get()
    pswd = passWord.get()
    try:
        dbs = con.connect(host=hostname , user = username, passwd = pswd)
        cur = dbs.cursor()
        mainMenu()
    except con.Error as err:
        if err.errno == 2003:
            mb.showinfo('Alert!','   Access Denied! \nEnter Valid Hostname!')
        elif err.errno == 1049:
            mb.showinfo('Alert!','Database Doesnot Exist!')
        elif err.errno == 1045:
            mb.showinfo('Alert!','   Access Denied!\nEnter Valid Username or \n   password!')
        else:
            mb.showinfo('Alert!','Something Worng!!')
            
def mainMenu():
    global root
    root.destroy()
    root = tk.Tk()
    root.geometry('500x400+450+200')
    root.title('Welcome to DBMS Software')
    tk.Label(root,text='DBMS Software',font=('ubuntu',20)).place(x=145,y=50)
    tk.Label(root,text='Logged In as- {}'.format(userName.get().capitalize()),font=('ubuntu')).place(x=165,y=100)
    tk.Button(root,text='Add Database  ',command=addNewDB).place(x=70,y=200)
    tk.Button(root,text='Show Database',command=showDatabase).place(x=70,y=250)
    tk.Button(root,text='Delete Databases',command=deleteDB).place(x=70,y=300)
    tk.Button(root,text='Create Table',command=createTab).place(x=300,y=200)
    tk.Button(root,text='Show Table',command=showTab).place(x=300,y=250)
    tk.Button(root,text='Insert In Table',command=insertInTab).place(x=300,y=300)
    tk.Button(root,text='Delete Table',command=delTab).place(x=300,y=350)    
    tk.Button(root,text='Logout',command=logoutFun).place(x=20,y=20)
    root.mainloop()

root= tk.Tk()   
secureLogin()
    
    
    
