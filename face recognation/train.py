

from tkinter import *
import tkinter as tk
from tkinter import messagebox
import tkinter as tk # for UI
from tkinter import Message ,Text
import cv2,os # OS for using sys comand,CV is used to read,process,write   
import shutil # Rename,make dir and archive 
import csv #used to read write  spreadsheet and database
import numpy as np # used to perform complex calculation on n-order array
from PIL import Image, ImageTk #The ImageTk module contains support to create and modify Tkinter BitmapImage and PhotoImage 
import pandas as pd  #Creating a DataFrame,Dealing with Rows and Columns
import datetime # to get date time
import time
import tkinter.ttk as ttk
import tkinter.font as font
import csv
from playsound import playsound
import os

#LOGIN AUTHINTECATION
def loginreq():
    if E1.get()=="Admin" and E2.get()=="1234":afterlogin()

    else:

        chkpass=Label(window,text="                           Username or Password Not valid",font=('helvetica', 19, 'bold'),
                      height=3,width=190, bg='brown', fg='white')
        chkpass.place(x=350, y=210, anchor="center")


#langing_page quit fun
def close_window():

    MsgBox = tk.messagebox.askquestion ('Exit Application','Are you sure you want to exit the application',icon = 'warning')
    if MsgBox == 'yes':
       window.destroy()
    else:
        tk.messagebox.showinfo('Return','You will now return to the application screen')


def afterlogin():
    
    Id=0
    x1,x2,x3,x4=[],[],[],[]
    camSource=0
    #camSource='http://192.168.0.5:4747/mjpegfeed'
    



    window = tk.Tk()
    window.title("WELCOME")
    window.geometry("1366x786")
    
    
    dialog_title = 'QUIT'
    dialog_text = 'Are you sure?'
     
    #window.geometry('1280x720')
    window.configure(background='cyan')

    #window.attributes('-fullscreen', True)

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

#xyz
    lbl4=Label(window,text="Face-Recognition-Based-Attendance-Management-System",font=('helvetica', 33, 'bold'),
           height=2,width=60, bg='deep sky blue', fg='white')
    lbl4.place(x=700, y=90, anchor="center")

    
    lbl = tk.Label(window, text="Enter ID",width=20  ,height=2  ,fg="red"  ,bg="snow" ,font=('times', 15, ' bold ') ) 
    lbl.place(x=50, y=210)

    txt = tk.Entry(window,width=20  ,bg="snow" ,fg="red",font=('times', 20, ' bold '))
    txt.place(x=360, y=218)

    lbl2 = tk.Label(window, text="Enter Name",width=20  ,fg="red"  ,bg="snow"    ,height=2 ,font=('times', 15, ' bold ')) 
    lbl2.place(x=50, y=320)

    txt2 = tk.Entry(window,width=20  ,bg="snow"  ,fg="red",font=('times', 20, ' bold ')  )
    txt2.place(x=360, y=328)

    lbl3 = tk.Label(window, text="Notification : ",width=20  ,fg="red"  ,bg="snow"  ,height=2 ,font=('times', 15, ' bold underline ')) 
    lbl3.place(x=50, y=430)

    message = tk.Label(window, text="" ,bg="yellow"  ,fg="red"  ,width=40  ,height=2, activebackground = "red" ,font=('times', 15, ' bold ')) 
    message.place(x=365, y=430)

    lbl3 = tk.Label(window, text="Attendance : ",width=20  ,fg="red"  ,bg="snow"  ,height=2 ,font=('times', 15, ' bold  underline')) 
    lbl3.place(x=50, y=540)


    message2 = tk.Label(window, text="" ,fg="red"   ,bg="yellow",activeforeground = "red",width=40  ,height=2  ,font=('times', 15, ' bold ')) 
    message2.place(x=365, y=540)
     
    def clear():
        txt.delete(0, 'end')    
        res = ""
        message.configure(text= res)

    def clear2():
        txt2.delete(0, 'end')    
        res = ""
        message.configure(text= res)    
        
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass
     
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
     
        return False


    def TakeImages():        
        Id=(txt.get())
        name=(txt2.get())
        harcascadePath = "haarcascade_frontalface_default.xml"
        if(is_number(Id) and name.isalpha()):
            cam = cv2.VideoCapture(camSource)#to get input from camera source
            detector=cv2.CascadeClassifier(harcascadePath)
            sampleNum=0
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                    #incrementing sample number 
                    sampleNum+=1
                    #saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                    #display the frame
                    cv2.imshow('frame',img)
                #wait for 100 miliseconds 
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum>20:
                    break
            cam.release()
            cv2.destroyAllWindows() 
            res = "Images Saved for ID : " + Id +" Name : "+ name
            row = [Id , name]
            with open('EmpDetails\EmpDetails.csv','a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            message.configure(text= res)
        else:
            if(is_number(Id)):
                res = "Enter Alphabetical Name"
                message.configure(text= res)
            if(name.isalpha()):
                res = "Enter Numeric Id"
                message.configure(text= res)
        
    def TrainImages():
        recognizer = cv2.face_LBPHFaceRecognizer.create()
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector =cv2.CascadeClassifier(harcascadePath)
        faces,Id = getImagesAndLabels("TrainingImage")
        recognizer.train(faces, np.array(Id))
        recognizer.save("TrainingImageLabel\Trainner.yml")
        res = "Image Trained"#+",".join(str(f) for f in Id)
        message.configure(text= res)

    def getImagesAndLabels(path):
        #get the path of all the files in the folder
        imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
        #print(imagePaths)
        
        #create empth face list
        faces=[]
        #create empty ID list
        Ids=[]
        #now looping through all the image paths and loading the Ids and the images
        for imagePath in imagePaths:
            #loading the image and converting it to gray scale
            pilImage=Image.open(imagePath).convert('L')
            #Now we are converting the PIL image into numpy array
            imageNp=np.array(pilImage,'uint8')
            #getting the Id from the image
            Id=int(os.path.split(imagePath)[-1].split(".")[1])
            # extract the face from the training image sample
            faces.append(imageNp)
            Ids.append(Id)        
        return faces,Ids
    def TrackImages():
        aa=""
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("TrainingImageLabel\Trainner.yml")
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath);    
        df=pd.read_csv("EmpDetails\EmpDetails.csv")
        cam = cv2.VideoCapture(camSource)#to get input from camSource
        font = cv2.FONT_HERSHEY_SIMPLEX        
        col_names =  ['Id','Name','Date','Time']
        attendance = pd.DataFrame(columns = col_names)
        a=0
        while a<25:
            ret, im =cam.read()
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces=faceCascade.detectMultiScale(gray, 1.2,5)
            for(x,y,w,h) in faces:
                cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
                if(conf < 50):
                    ts = time.time()      
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    #aa=df.loc[df['Id'] == Id]['Name'].values
                    aa=getName(Id)
                    tt=str(Id)+"-"+aa
                    attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                else:
                    Id='Unknown'                
                    tt=str(Id)
                if(conf > 75):
                    noOfFile=len(os.listdir("ImagesUnknown"))+1
                    cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
                cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
            attendance=attendance.drop_duplicates(subset=['Id'],keep='first')
            cv2.imshow('im',im)
            if (cv2.waitKey(1)==ord('q')):
                break
            a+=1
        ts = time.time()      
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour,Minute,Second=timeStamp.split(":")
        if(aa!=""):#if face found
            playsound('thankyou.mp3')
            fileName="Attendance\Attendance_"+date+".csv"
            path = 'E:/py project/final files/'+fileName
     
            if os.path.exists(path):
                
                required_df = pd.read_csv(fileName)
                flag = len(required_df[required_df['Id']==Id])
                #print(required_df,"111111")
                if flag:
                   pass
                else:   
                   required_df.loc[Id] = [Id, getName(Id), date, timeStamp]

                   required_df.to_csv(fileName,index=False)
                   #print(required_df,"222222")

                
            else:
                attendance.to_csv(fileName,index=False)
                res=attendance
                message2.configure(text= res)
        else:
            res="No face Found"
            message2.configure(text= res)
            
        cam.release()
        cv2.destroyAllWindows()

    def getName(iD):
        temp=""
        with open(r'EmpDetails\EmpDetails.csv','rt')as f:
          data = csv.reader(f)
          allrows=[]
          temp=""
          for row in data:
              if (len(row)!=0):
                  allrows.append(row)
        for c in range(len(allrows)):
            for r in range(len(allrows[0])):
                if allrows[c][r]==str(iD):
                    temp=allrows[c][r+1]
        return temp
#123
    clearButton = tk.Button(window, text="Clear", command=clear  ,fg="red"  ,bg="snow"  ,width=10  ,height=1 ,activebackground = "Red" ,font=('times', 15, ' bold '))
    clearButton.place(x=700, y=210)
    clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="red"  ,bg="snow"  ,width=10  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
    clearButton2.place(x=700, y=320)    
    takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="red"  ,bg="yellow"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
    takeImg.place(x=1000, y=210)
    trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,fg="red"  ,bg="yellow"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
    trainImg.place(x=1000, y=320)
    trackImg = tk.Button(window, text="Track Images", command=TrackImages  ,fg="red"  ,bg="yellow"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
    trackImg.place(x=1000, y=430)
    quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="red"  ,bg="yellow"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
    quitWindow.place(x=1000, y=540)

     
    window.mainloop()

    
#LOGIN PAGE
window = Tk()
window.title("FaceRecognation")
window.geometry("1366x786")
#window = tk.Tk()
image = Image.open('bg.jpeg')
photo_image = ImageTk.PhotoImage(image)
label = Label(window, image = photo_image)
label.pack()
canvas1 = Canvas(window, width = 400, height = 300,  relief = 'raised')
canvas1.pack()



quitButton = Button(window, text="Quit", height = 1, width = 10,command = close_window,bg='white',
                    fg='black',font=('helvetica', 15, 'bold'))
quitButton.place(x=550, y=390)

loginButton = Button(window, text="logn", height = 1, width = 10,command=loginreq , bg='white',
                     fg='black',font=('helvetica', 15, 'bold'))
loginButton.place(x=700, y=390)



lbl1 = Label(window,text="Password",height=1,width=10,font=('helvetica', 15, 'bold'), bg='white', fg='black')
lbl1.place(x=550, y=350, anchor="center")


lbl2 = Label(window,text="Username",font=('helvetica', 15, 'bold'),height=1,width=10, bg='white', fg='black')
lbl2.place(x=550, y=280, anchor="center")


lbl3=Label(window,text="welcome recognition based attendence login \n  "+" login to go to landing ",font=('helvetica', 15, 'bold'),
           height=2,width=60, bg='deep sky blue', fg='white')
lbl3.place(x=660, y=540, anchor="center")

lbl4=Label(window,text="FACE RECOGNATION BASED ATTENDENCE",font=('helvetica', 21, 'bold'),
           height=2,width=60, bg='deep sky blue', fg='white')
lbl4.place(x=660, y=100, anchor="center")



E1 = Entry(window,font=('helvetica', 12, 'bold'))
E1.place(x=740,y=280, anchor="center")

E2 = Entry(window,show="*",font=('helvetica', 12, 'bold'))
E2.place(x=740,y=350, anchor="center")


window.mainloop()

