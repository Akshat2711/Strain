import requests
from bs4 import BeautifulSoup
from tkinter import*
from PIL import ImageTk,Image
import mysql.connector as mycon
from datetime import date
import time
from gtts import gTTS
import openai
from apikey import *
import os
from smtplib import *
import urllib.request
import speech_recognition as sr
import webbrowser
from random import*
language = 'en'#language of output
openai.api_key ="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"


con=mycon.connect(host="localhost",user="root",database="searchhistory",password="27ramome76A")
cur=con.cursor()


#called when result direct on google
def query():
    global result

    user_query = res

    URL = "https://www.google.co.in/search?q=" + user_query

    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find(class_='Z0LcW t2b5Cf').get_text()
    print(result)
    msg1.configure(text='Ans-  "'+result+'"')
    msg1.place(relx=0.46,rely=0.7,anchor='center')
    but4.place(x=0,y=750)


   

def window1():
    global win1
    global count
    win1=Tk()
    win1.title("main window")
    win1.geometry("1920x1080")
    count=-1
#list of images used as back in mainwindow 
    list1=[ImageTk.PhotoImage(Image.open("D:\code comp\p1.png")),ImageTk.PhotoImage(Image.open("D:\code comp\p2.png")),ImageTk.PhotoImage(Image.open("D:\code comp\p3.png"))]
    canvas=Canvas(win1,width=5000,height=2000,highlightthickness=0)
    canvas.create_image(0,0,anchor='nw',image=list1[0])
    canvas.pack()
    def next():
        global count
#remeber to change count==2 to no of images in (list-1)
        if count==2:
            canvas.create_image(0,0,anchor='nw',image=list1[0])
            count=0
        else:
            canvas.create_image(0,0,anchor='nw',image=list1[count+1])
            count+=1
        win1.after(5000,next)
    next()
#history being sent  to database
#sent to while loop
    def sgoogle():
        global res
        global date
#date code
        date = date.today()
        res=str(txt1.get())
#current time code
        ###################
        ###############
        t = time.localtime()
        gm=open("getmailforhis.txt","r")
        fm=gm.read()
        gm.close()
        current_time = time.strftime("%H:%M:%S", t)
        cur.execute("insert into history() values('{}','{}','{}','{}');".format(res,date,current_time,fm))
        con.commit()
        whileloop()
    def his():
        win_his=Tk()
        win_his.config(bg="black")
        win_his.title("History")
        win_his.geometry("1920x1080")
# to delete history
        def delete_his():
            gm=open("getmailforhis.txt","r")
            fm=gm.read()
            gm.close()
            cur.execute("delete from history where email='{}'".format(fm))
            con.commit()
            lbl_confirm.configure(text="REOPEN TO SEE CHANGES!")
            
        but_his=Button(win_his,text="DELETE HISTORY",font=("Helvitica",18),command=delete_his).place(x=650,y=700)
        lbl_confirm=Label(win_his,text=" ",bg="black",font=("Helvitica",15),fg="green")
        lbl_confirm.place(x=620,y=675)
        gm=open("getmailforhis.txt","r")
        fm=gm.read()
        gm.close()
        cur.execute("select * from history where email='{}'".format(fm))
        h=cur.fetchall()
        print(h)
        val_y=50
        lbl_q=Label(win_his,text="QUERY",font=("Helvitica",20),fg="red",bg="black").place(x=30,y=10)
        lbl_d=Label(win_his,text="DATE",font=("Helvitica",20),fg="red",bg="black").place(x=1150,y=10)
        lbl_t=Label(win_his,text="TIME",font=("Helvitica",20),fg="red",bg="black").place(x=1350,y=10)
        
        for h1 in h:
            lbl1=Label(win_his,text=str(h1[0]),font=("Helvitica",20),fg="red",bg="black").place(x=30,y=val_y)
            lbl2=Label(win_his,text=str(h1[1]),font=("Helvitica",20),fg="red",bg="black").place(x=1150,y=val_y)
            lbl3=Label(win_his,text=str(h1[2]),font=("Helvitica",20),fg="red",bg="black").place(x=1350,y=val_y)
            val_y+=40
            
        
#ai fnc(chatgpt 3.5)        
    def ai():
        win1.destroy()
        win_ai=Tk()#mann was here(founder)  
        global countai,list2
        win_ai.title("AI")
        win_ai.geometry("1920x1080")
        countai=-1
#list of images used as back in aiwindow 
        list2=[ImageTk.PhotoImage(Image.open("D:\code comp\p4.jpg")),ImageTk.PhotoImage(Image.open("D:\code comp\p5.jpg")),ImageTk.PhotoImage(Image.open("D:\code comp\p6.jpg"))]
        canvas=Canvas(win_ai,width=5000,height=2000,highlightthickness=0)
        canvas.create_image(0,0,anchor='nw',image=list2[0])
        canvas.pack()
        def next():
            global countai
    #remeber to change count==2 to no of images in (list-1)
            if countai==2:
                canvas.create_image(0,0,anchor='nw',image=list2[0])
                countai=0
            else:
                canvas.create_image(0,0,anchor='nw',image=list2[countai+1])
                countai+=1
            win_ai.after(5000,next)
        next()
        def resai():
            aientry=txtai.get()
            dateai = date.today()
            resai=str(aientry)
    #current time code
            tai = time.localtime()
            gm=open("getmailforhis.txt","r")
            fm=gm.read()
            gm.close()
            current_timeai = time.strftime("%H:%M:%S", tai)
            cur.execute("insert into history() values('{}','{}','{}','{}');".format(resai+"[AI]",dateai,current_timeai,fm))
            con.commit()
            output = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=[{"role": "user","content":str(aientry)}])
            msgai.place(x=158, y=80)
            msgai.insert("0.0",output['choices'][0]['message']['content'])#########################


        def ai_mainback():
            win_ai.destroy()
            window1()
        #create image window
        def createimage():
            global countimg,list3
#after ai button create image action:
            def aiimg():
                global date
                idea=txtimg.get()
                sizeval=txtimg2.get()
                name=txtimg3.get()
                date = date.today()
        #current time code
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                gm=open("getmailforhis.txt","r")
                fm=gm.read()
                gm.close()
                cur.execute("insert into history() values('{}','{}','{}','{}');".format(idea+"[AI(img)]",date,current_time,fm))
                con.commit()
                response = openai.Image.create(prompt=idea,n=1,size=sizeval,)
                out=response["data"][0]["url"]


                  
                # Retrieving the resource located at the URL
                # and storing it in the file name a.png
                url = str(out)
                urllib.request.urlretrieve(url,name)
                  
                # Opening the image and displaying it (to confirm its presence)
                img = Image.open(name)
                img.show()
            win_ai.destroy()
            winimage=Tk()
            countimg=-1
    #list of images used as back in aiwindow 
            list3=[ImageTk.PhotoImage(Image.open("D:\code comp\p7.jpg")),ImageTk.PhotoImage(Image.open("D:\code comp\p8.jpg")),ImageTk.PhotoImage(Image.open("D:\code comp\p9.jpg"))]
            canvas=Canvas(winimage,width=5000,height=2000,highlightthickness=0)
            canvas.create_image(0,0,anchor='nw',image=list3[0])
            canvas.pack()
            def next():
                global countimg
        #remeber to change count==2 to no of images in (list-1)
                if countimg==2:
                    canvas.create_image(0,0,anchor='nw',image=list3[0])
                    countimg=0
                else:
                    canvas.create_image(0,0,anchor='nw',image=list3[countimg+1])
                    countimg+=1
                winimage.after(5000,next)
            next()
            def aiimgback():
                winimage.destroy()
                window1()
            
            winimage.geometry("1920x1080")
            winimage.title("CREATE IMAGE")
            txtimg=Entry(winimage,fg="white",width=10,bg="black",font=("Helvitica",30))
            txtimg.place(x=700,y=10)
            txtimg2=Entry(winimage,fg="white",width=10,bg="black",font=("Helvitica",30))
            txtimg2.place(x=700,y=60)
            txtimg3=Entry(winimage,fg="white",width=10,bg="black",font=("Helvitica",30))
            txtimg3.place(x=700,y=110)
            butimg=Button(winimage,bg="black",fg="darkblue",text="CREATE",font=("Helvitica",57),command=aiimg).place(x=925,y=10)
            lblimg1=Label(winimage,text="ENTER IDEA:\nSIZE OF IMAGE:\nNAME TO BE STORED AS:",font=("Helvitica",31),bg="black",fg="darkblue").place(x=182,y=10)
            butimgback=Button(winimage,bg="black",fg="white",text="HOME",font=("Helvitica",20),command=aiimgback).place(x=0,y=729)
#speech to text code
        def speech_txt():
            r=sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("say something")
                audio=r.listen(source)
#time sleep to recognize voice
                time.sleep(2)
                try:
                    inputaudio=r.recognize_google(audio)
                    print("you have said:\n"+inputaudio)
                    output = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=[{"role": "user","content":str(inputaudio)}])
                    msgai.place(x=158, y=80)
                    msgai.insert("0.0",output['choices'][0]['message']['content'])
                    ############################################
                    myobj = gTTS(text=output['choices'][0]['message']['content'], lang=language, slow=False)
                    myobj.save("micout.mp3")
                    os.system("micout.mp3")
                    dateaimic = date.today()
                    gm=open("getmailforhis.txt","r")
                    fm=gm.read()
                    gm.close()
#current time code for mic ai
                    tai = time.localtime()
                    current_timeaim = time.strftime("%H:%M:%S", tai)
                    cur.execute("insert into history() values('{}','{}','{}','{}');".format(inputaudio+"[AI(mic)]",dateaimic,current_timeaim,fm))
                    con.commit()


                except Exception as e:
                    print("error")
                    msgai.configure(text="TRY AGAIN",font=("Helvitica",29),fg="red")
                    
                
            
        txtai=Entry(win_ai,fg="white",width=40,bg="black",font=("Helvitica",30))
        txtai.place(x=220,y=10)
        lblai1=Label(win_ai,text="STR",font=("Helvitica",19),bg="black",fg="red").place(x=1429,y=0)
        lblai2=Label(win_ai,text="AI",font=("Helvitica",19),bg="black",fg="white").place(x=1479,y=0)
        lblai3=Label(win_ai,text="N",font=("Helvitica",19),bg="black",fg="red").place(x=1504,y=0)
        butai=Button(win_ai,bg="black",fg="white",text="FIND",font=("Helvitica",19),command=resai).place(x=1100,y=10)
        butai2=Button(win_ai,bg="black",fg="white",text="BACK",font=("Helvitica",19),command=ai_mainback).place(x=0,y=10)
        msgai=Text(win_ai,width=68,height=20,bg="black",fg="red",font=("Helvitica",20))
        butai3=Button(win_ai,bg="black",fg="white",text="CREATE IMAGE USING AI",font=("Helvitica",19),command=createimage).place(x=0,y=740)
        butai4=Button(win_ai,bg="black",fg="white",command=speech_txt,text="MIC",font=("Helvitica",19)).place(x=154,y=10)
    global msg1
#to open google visible when query 2 fnc runs
    def opengoogle():
        q=txt1.get()
        webbrowser.open('https://google.com/'+'search?q='+q)
    def logout():
        win1.destroy()
        login()
    global but4
    txt1=Entry(win1,bg="black",fg="white",width=40,font=("Helvitica",30))
    txt1.place(x=220,y=350)
    but1=Button(win1,bg="black",fg="white",text="search",font=("Helvitica",19),command=sgoogle).place(x=1102,y=350)
    lbl1=Label(win1,text="STR",font=("Helvitica",60),bg="black",fg="white").place(x=560,y=200)
    lbl2=Label(win1,text="N",font=("Helvitica",60),bg="black",fg="white").place(x=804,y=200)
    but2=Button(win1,text="History",font=("Helvitica",18),bg="black",fg="red",command=his).place(x=1438,y=0)
    but3=Button(win1,text="AI",font=("Helvitica",36),bg="red",fg="black",command=ai).place(x=725,y=200)
    but4=Button(win1,font=("Helvitica",14),text="OPEN IN BROWSER",command=opengoogle,bg="red",fg="black")
    msg1=Message(win1,text="",font=("Helvitica",20),fg="white",bg="black",aspect=100,justify=CENTER)
    but5=Button(win1,font=("Helvitica",14),text="LOG OUT",command=logout,bg="red",fg="black").place(x=1434,y=750)
    msg1.place(relx=100,rely=0.7,anchor='center')
    #to diplay welcome message
    f=open("himsgfile(code1).txt","r")
    namehello=f.read()
    f.close()
    lbl3=Label(win1,text="Welcome "+namehello,font=("Helvitica",20),bg="black",fg="red").place(x=0,y=0)
#called when result no direct on google
def query2(res2):
    global result
    user_query = res2

    URL = "https://www.google.co.in/search?q=" + user_query

    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find(class_='VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf').get_text()
    print(result)
    msg1.configure(text='Ans-  "'+result+'"')
    but4.place(x=0,y=750)
    msg1.place(relx=0.46,rely=0.7,anchor='center')
#deciding whether result directly on google or not
def whileloop():
    while True:
        try:
            query()
        except Exception:
            query2(res)
        break

def login():
    loginwin=Tk()
    global count_login
    count_login=-1
    #list of images used as back in aiwindow 
    list4=[ImageTk.PhotoImage(Image.open("D:\code comp\p10.jpg")),ImageTk.PhotoImage(Image.open("D:\code comp\p11.jpg")),ImageTk.PhotoImage(Image.open("D:\code comp\p12.jpg"))]
    canvaslogin=Canvas(loginwin,width=5000,height=2000,highlightthickness=0)
    canvaslogin.create_image(0,0,anchor='nw',image=list4[0])
    canvaslogin.pack()
##############
    def next():
        global count_login
        #remeber to change count==2 to no of images in (list-1)
        if count_login==2:
            canvaslogin.create_image(0,0,anchor='nw',image=list4[0])
            count_login=0
        else:
            canvaslogin.create_image(0,0,anchor='nw',image=list4[count_login+1])
            count_login+=1
        loginwin.after(9000,next)
    next()
    loginwin.title("LOGIN")
    loginwin.geometry("1920x1080")
    def back_sign_login():
        loginwin.destroy()
        login()
    def signupcmd():
         gmaillogin.place(x=650,y=400)
         passlogin.place(x=650,y=450)
         lbl1_login.place(x=530,y=400)
         lbl2_login.place(x=530,y=450)
         lbl3_login.place(x=530,y=500)
         lbl4_login.place(x=530,y=350)
         signinbut.place(x=10000,y=700)###code to remove button from screen
         signupbut.place(x=10000,y=650)####code to remove button from screen
         namelogin.place(x=646,y=350)
         gmaillogin.place(x=648,y=400)
         passlogin.place(x=650,y=450)
         otplogin.place(x=647,y=500)
         contbut2.place(x=1218,y=730)
         backbtn.place(x=0,y=729)
         otpbtn.place(x=1070,y=349)
        
            
    def signincmd():
         otplogin.place(x=3000,y=500)
         contbut2.place(x=3000,y=700)
         namelogin.place(x=3000,y=350)
         lbl3_login.place(x=3000,y=500)
         lbl4_login.place(x=3000,y=350)
         lbl5_login.place(x=3000,y=350)
         otpbtn.place(x=3000,y=100)
         ####################above 6 line code just to remove button and labels out of screen
         gmaillogin.place(x=648,y=400)
         passlogin.place(x=650,y=450)
         lbl1_login.place(x=530,y=400)
         lbl2_login.place(x=530,y=450)
         signinbut.place(x=10000,y=700)
         signupbut.place(x=10000,y=650)
         contbut.place(x=1372,y=730)
         backbtn.place(x=0,y=729)
    
    def getotp():
        global rando
        gm=str(gmaillogin.get())
        na=str(namelogin.get())
        rando=randint(1000,10000)
        send="Hi "+na+",\n"+"OTP for your STRAIN browser is  "+str(rando)
        s_e="cs.pr0j3ct.xii@gmail.com"#sender email
        passwd="omtghmrwfehjgcqb"#pass of sender
        server=SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(s_e,passwd)
        server.sendmail(s_e,gm,send)
       
        
    def cont_to_signin():
        o=otplogin.get()
        ####################################label for account created?
        if str(rando)==o:
            pa=str(passlogin.get())
            na=str(namelogin.get())
            gm=str(gmaillogin.get())
            
            cur.execute("select* from logininf;")
            allinf=cur.fetchall()
            for i in allinf:
                if i[1]==gm:
                
                    lbl5_login.configure(text="account already exist!")
                    lbl5_login.place(x=650,y=290)
                else:
                    cur.execute("insert into logininf() values('{}','{}','{}');".format(na,gm,pa))
                    con.commit()
                    signincmd()
                            
            
        else:
            lbl5_login.configure(text="otp incorrect")
            lbl5_login.place(x=650,y=290)
        
        
    
        
    def cont_to_main():
        g=gmaillogin.get()
        p=passlogin.get()
        cur.execute("select* from logininf;")
        allinf=cur.fetchall()
        for i in allinf:
            if (g,p)==(i[1],i[2]):
                gm=open("getmailforhis.txt","w")
                gm.write(str(g))
                gm.close()
                f=open("himsgfile(code1).txt","w")
                f.write(i[0])
                f.close()
                loginwin.destroy()
                window1()
                break
            else:
                lbl5_login.configure(text="TRY AGAIN!")
                lbl5_login.place(x=650,y=305)
        
        
    #login image
    signinbut=Button(loginwin,fg="red",bg="purple4",text="SIGN IN",font=("Helvitica",20),command=signincmd)
    signinbut.place(x=690,y=700)
    signupbut=Button(loginwin,fg="red",bg="purple4",text="SIGN UP",font=("Helvitica",19),command=signupcmd)
    signupbut.place(x=690,y=650)
    gmaillogin=Entry(loginwin,bg="purple4",fg="black",width=20,font=("Helvitica",28))
    passlogin=Entry(loginwin,bg="purple4",fg="black",width=20,font=("Helvitica",28))
    namelogin=Entry(loginwin,bg="purple4",fg="black",width=20,font=("Helvitica",28))#remove place on sign up
    otplogin=Entry(loginwin,bg="purple4",fg="black",width=20,font=("Helvitica",28))
    lbl1_login=Label(loginwin,text="EMAIL:",font=("Helvitica",26),bg="purple4",fg="red")
    lbl2_login=Label(loginwin,text="PASS.:",font=("Helvitica",27),bg="purple4",fg="red")
    lbl3_login=Label(loginwin,text="OTP.  :",font=("Helvitica",27),bg="purple4",fg="red")
    lbl4_login=Label(loginwin,text="NAME:",font=("Helvitica",27),bg="purple4",fg="red")#remove place on sign up
    lbl5_login=Label(loginwin,text="TRY AGAIN!",font=("Helvitica",27),bg="purple4",fg="red")
    contbut=Button(loginwin,bg="purple4",fg="red",text="CONTINUE",font=("Helvitica",20),command=cont_to_main)
    contbut2=Button(loginwin,bg="purple4",fg="red",text="CONTINUE TO SIGN IN",font=("Helvitica",20),command=cont_to_signin)
    backbtn=Button(loginwin,bg="purple4",fg="red",text="BACK",font=("Helvitica",20),command=back_sign_login)
    otpbtn=Button(loginwin,fg="purple4",bg="red",text="G\nE\nT\n \nO\nT\nP",font=("Helvitica",17),command=getotp)
    
    
    
    loginwin.mainloop()
     
login()
