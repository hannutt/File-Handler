from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os.path
import os
from tkinter import messagebox
import pathlib
import datetime
import subprocess as sp
from PIL import Image,ImageTk


root = Tk()
results = []


def SearchExt():
    
    Fileext = Entry.get(extEntry)
    selExt = Entry.get(setExt)
    root.directory = filedialog.askdirectory()
    for file in os.listdir(root.directory):
        name, ext = os.path.splitext(file)
        if ext == Fileext and selExt == '':
            results.append(file)

        elif ext == selExt and Fileext == '':
            results.append(file)

    for file in results:
        listbox.insert("end", file)

    listItemTotal()

    # resultlist.selection_set(0)


def openFile(event):
    #for selectedItem in TreeView.selection():

    #global currentFile
    #muuttujaan tallennetaan treeviewssa valittu rivi
    currentFile = TreeView.item(TreeView.selection())
   
    #tulostetaan valitun rivin kohta 1, eli tiedoston nimi
    fullPathName = os.path.join(folder,currentFile['values'][1])
    #print(fullPathName)
    os.startfile(fullPathName)

def openWith(event):
    #POPUPMENU ELI AVAUTUU HIIREN OIKEALLA KAIKKIALLA
    popUpMenu.tk_popup(event.x_root,event.y_root)
    videos = ['.mp4','.wmv','.avi','.gif']
    Txt = ['.rtf','.txt']
    currentFile = TreeView.item(TreeView.selection())
    global fullPathName
    fullPathName = os.path.join(folder,currentFile['values'][1])
    #talletetaan muuttujaan valitun tiedostorivin tiedostopääte
    ext = currentFile['values'][6]
    if ext in videos:
        popUpMenu.add_command(label='Open with VLC media Player',command=openVideo)
    elif ext in Txt:
        popUpMenu.add_command(label='Open with Notepad++', command=openText)
    else:
        popUpMenu.add_command(label='Open with VLC media Player',command=openVideo)
        popUpMenu.add_command(label='Open with Notepad++', command=openText)


def createNewFile(event):
    createWindow = Toplevel(root)
    createlbl = Label(createWindow,text='Enter a file name:')
    createNewEntry = Entry(createWindow)

    createlbl.pack()
    createNewEntry.pack()

    def doCreate():

        filename = Entry.get(createNewEntry)
        fullPathName = os.path.join(folder,filename)
        #fullPathName = os.path.join(folder,filename)
        with open(fullPathName,'w') as f:
            f.write('text')
    createBtn = Button(createWindow,text='create',command=doCreate)
    createBtn.pack()
        

   
   



def openVideo():
    vlcPath = "c:/Program Files/VideoLAN/VLC/vlc.exe"
    sp.call([vlcPath,fullPathName])

def openText():
    path = "C:/Program Files/Notepad++/notepad++.exe"
    sp.call([path,fullPathName])

    



def OpenRenameWin(event):
    currentFile = TreeView.item(TreeView.selection())
    FinalCurrentFile = currentFile['values'][1]
    renameWindow = Toplevel(root)
    currentNameEntry = Entry(renameWindow)
    currentNameEntry.insert(0, FinalCurrentFile)
    currentlbl = Label(renameWindow, text='Current filename')
    Newnamelbl = Label(renameWindow, text='Enter a new name:')
    NewnameEntry = Entry(renameWindow)

    currentlbl.pack()
    currentNameEntry.pack()
    Newnamelbl.pack()
    NewnameEntry.pack()

    def doRename():
        oldname = Entry.get(currentNameEntry)
        newname = Entry.get(NewnameEntry)
        # os.path joinilla haetaan valitun tiedoston koko polku ja itse tiedosto->
        # esim c:\koodaus\testi.txt on muuttujan fulloldname sisältämä merkkijono. mikäli em.
        # tiedosto on valittuna
        fullOldName = os.path.join(folder, oldname)
        fullNewName = os.path.join(folder, newname)

        os.rename(fullOldName, fullNewName)
    renameBtn = Button(renameWindow, text='Rename', command=doRename)

    renameBtn.pack()


def openDelWin(event):
    currentFile = TreeView.item(TreeView.selection())
    delWindow = Toplevel(root)
    delFileLbl = Label(delWindow, text='File name:')
    delFileEntry = Entry(delWindow)
    delFileEntry.insert(0, currentFile)

    delFileLbl.pack()
    delFileEntry.pack()

    def doDelete():
        fileName = Entry.get(delFileEntry)
        fullFileName = os.path.join(folder, fileName)
        result = messagebox.askquestion(
            'Warning', 'Are you sure you want to delete this file?')
        if result == 'yes':
            os.remove(fullFileName)
            messagebox.showinfo('Note', 'File'+fullFileName+' deleted.')
        else:
            messagebox.showinfo('Note', 'You cancelled delete operation.')
    delBtn = Button(delWindow, text='Delete', command=doDelete)
    delBtn.pack()

global paths
paths = []
# syötetyn kansion alikansioiden ja tiedostojen tulostus listboxiin
def showDir(event):

    viewClear()
   
    global folder
    folder = Entry.get(extEntry)
    paths.append(folder)
    extSel = Entry.get(setExt)
    if folder == '':
        messagebox.showinfo('Note', 'Enter a path!')
    else:
        dirs = os.listdir(folder)
        rootExt = os.path.splitext(folder)
        global idNum
        idNum = 0

        for file in dirs:
            idNum = idNum + 1
            if file.endswith(extSel):

        # tallennetaan jokaisen silmukassa olevan filen eli tiedoston sijainti, eli polku+tiedoston nimi muuttujaan
                fullPathName = os.path.join(folder, file)
        # tällä saadaan selville koska kutakin tiedostoa on viimeksi muokattu
                modified = os.path.getmtime(fullPathName)
        # muokkauajan formatointi VV-kk-PP HH:MM:SS muotoon
                modifiedFormatTime = datetime.datetime.fromtimestamp(modified)
            # timestampin muotoilu muotoon PP.kk.VV
                modifiedFormatTime = modifiedFormatTime.strftime('%d.%m.%Y')
                Dir = os.path.isdir(fullPathName)

        # näytetään tiedostojen pääte
                ext = pathlib.Path(fullPathName).suffix
        # thaetaan jokaisen tiedoston koko
                size = os.path.getsize(fullPathName)
                res = size / 1024
                res = round(res, 2)
                #amountbox.insert(INSERT, idNum)
        # jos dir muuttuja on false annetaan treeview tagi dirFalse ja käytetään siinä rivin taustavärinä mustaa / jos arvo on true
        # rivin tagi on DirTrue ja taustaväri vaaleanharmaa

                if Dir == False:

                    TreeView.insert(parent='', index='end', values=(
                    idNum, file, rootExt[0], res, modifiedFormatTime, Dir, ext), tags='DirFalse')
                    TreeView.tag_configure('DirFalse', background="gray", foreground="white")

                elif Dir == True:
                   
                    TreeView.insert(parent='', index='end', values=(
                    idNum, file, rootExt[0], res, modifiedFormatTime, Dir, ext), tags='DirTrue')
           
                    TreeView.tag_configure('DirTrue', background="lightgray")
                       
               
        else:

            fullPathName = os.path.join(folder, file)
        # tällä saadaan selville koska kutakin tiedostoa on viimeksi muokattu
            modified = os.path.getmtime(fullPathName)
        # muokkauajan formatointi VV-kk-PP HH:MM:SS muotoon
            modifiedFormatTime = datetime.datetime.fromtimestamp(modified)
            # timestampin muotoilu muotoon PP.kk.VV
            modifiedFormatTime = modifiedFormatTime.strftime('%d.%m.%Y')
            Dir = os.path.isdir(fullPathName)

        # näytetään tiedostojen pääte
            ext = pathlib.Path(fullPathName).suffix
        # thaetaan jokaisen tiedoston koko
            size = os.path.getsize(fullPathName)
            res = size / 1024
            res = round(res, 2)
            
           
            #listItemTotal()               
            #amountbox.insert(INSERT, idNum)
        # jos dir muuttuja on false annetaan treeview tagi dirFalse ja käytetään siinä rivin taustavärinä mustaa / jos arvo on true
        # rivin tagi on DirTrue ja taustaväri vaaleanharmaa

            if Dir == False:
                    TreeView.insert(parent='', index='end', values=(
                    idNum, file, rootExt[0], res, modifiedFormatTime, Dir, ext), tags='DirFalse')
                    TreeView.tag_configure('DirFalse', background="gray", foreground="white")

            elif Dir == True:
                  
                    TreeView.insert(parent='', index='end',values=(
                    idNum, file, rootExt[0], res, modifiedFormatTime,Dir, ext), tags='DirTrue')
                    TreeView.tag_configure('DirTrue', background="lightgray")

            #poistetaan -1 eli viimeinen rivi koska viimeinen tiedosto näkyy jostain syystä kaksi kertaa      
            lastItem = TreeView.get_children()[-1]
            TreeView.delete(lastItem)
            

#paluu edelliseen tiedostopolkuun
def goBack():
    idNum = 0
    for i in range(len(paths)):
        folder = paths[i]
        previous = paths[i-1]
    extEntry.delete(0,"end")
    extEntry.insert(0,previous)
    dirs = os.listdir(previous)
    rootExt = os.path.splitext(previous)
    for file in dirs:
            idNum = idNum + 1
            
        # tallennetaan jokaisen silmukassa olevan filen eli tiedoston sijainti, eli polku+tiedoston nimi muuttujaan
            fullPathName = os.path.join(previous, file)
        # tällä saadaan selville koska kutakin tiedostoa on viimeksi muokattu
            modified = os.path.getmtime(fullPathName)
        # muokkauajan formatointi VV-kk-PP HH:MM:SS muotoon
            modifiedFormatTime = datetime.datetime.fromtimestamp(modified)
            # timestampin muotoilu muotoon PP.kk.VV
            modifiedFormatTime = modifiedFormatTime.strftime('%d.%m.%Y')
            Dir = os.path.isdir(fullPathName)

        # näytetään tiedostojen pääte
            ext = pathlib.Path(fullPathName).suffix
        # thaetaan jokaisen tiedoston koko
            size = os.path.getsize(fullPathName)
            res = size / 1024
            res = round(res, 2)
            #amountbox.insert(INSERT, idNum)
        # jos dir muuttuja on false annetaan treeview tagi dirFalse ja käytetään siinä rivin taustavärinä mustaa / jos arvo on true
        # rivin tagi on DirTrue ja taustaväri vaaleanharmaa

            if Dir == False:

                TreeView.insert(parent='', index='end', values=(
                idNum, file, rootExt[0], res, modifiedFormatTime, Dir, ext), tags='DirFalse')

            elif Dir == True:

                TreeView.insert(parent='', index='end', values=(
                idNum, file, rootExt[0], res, modifiedFormatTime, Dir, ext), tags='DirTrue')
            TreeView.tag_configure(
                'DirFalse', background="gray", foreground="white")
            TreeView.tag_configure('DirTrue', background="lightgray")

def history():
    historywindow = Toplevel(root)
    historybox = Listbox(historywindow)
    
    for item in paths:
        historybox.insert("end",item)
    
    historybox.pack()
    
    def getSel():
        
        #tallennetaan valittu polku muuttujaan
        currentPath = historybox.curselection()
        if currentPath:

            index = currentPath[0]
            val = historybox.get(index)
            extEntry.delete(0,END)
            extEntry.insert(0,val)
            
    insertBtn = Button(historywindow,text='Insert',command=getSel)
    insertBtn.pack()
         

def viewClear():
    for file in TreeView.get_children():
        TreeView.delete(file)

# listboxissa olevien itemin kokonaismäärän lasku


def listItemTotal(item_iid="")->int:
    count = 0
    for item in TreeView.get_children(item=item_iid):
        count +=1
    #amount = len(TreeView.get_children())

    amountbox.insert(INSERT, count, END)
    #amountbox.insert(INSERT, '\n', END)

root.title('FSH')
root.geometry("500x500")
root.bind('<Double-1>', openFile)
root.bind('<Alt-r>', OpenRenameWin)
root.bind('<Alt-d>', openDelWin)
root.bind('<Button-3>',openWith)
root.bind('<Alt-c>',createNewFile)

#POP UP MENU, ELI HIIREN OIKEALLA AVAUTUVA
popUpMenu = Menu(root,tearoff=False)

frame1 = Frame(root)
frame2 = Frame(root)
frame3 = Frame(root)
frame4 = Frame(root)
frame5 = Frame(root)
extensions = ['.txt', '.pdf', '.eps']
#titlelbl = Label(root, text='File System Handler')
#canvas määritykset
canvas = Canvas(root,height=100,width=100)
#ensimmäisellä ja toisella numeroilla määritetään rectangeln leveys ja pituus
canvas.create_rectangle(140,70,0,0,fill='lightgray',outline='blue',width=3)
#ensimmäinen parametri on tekstin sijainti leveyssuunnassa,toinen parametri on tekstin sijainti pituus suunnassa
canvas.create_text(46,35,text='File Handler',fill='black',font=('Segoe Ui',12))
selextlbl = Label(frame1, text='Select file ext:')
selEntryLbl = Label(frame2, text=' path + enter:')
totallbl = Label(frame5, text='Files total:')
setExt = ttk.Combobox(frame1, width=5, values=extensions)
extEntry = Entry(frame2)


TreeView = ttk.Treeview(frame3)
TreeView['columns'] = ['fileInfo']
TreeView['columns'] = ['ID', 'Name', 'Path',
                       'Size', 'Created', 'Directory', 'Type']
TreeView.column('#0', width=0, stretch=NO)
TreeView.column('ID', anchor=W, width=15)
TreeView.column('Name', anchor=W)
TreeView.column('Path', anchor=W)
TreeView.column('Size', anchor=W, width=35)
TreeView.column('Created', anchor=W)
TreeView.column('Directory', anchor=W)
TreeView.column('Type', anchor=W, width=35)

TreeView.heading('ID', text='ID')
TreeView.heading('Name', text='Name')
TreeView.heading('Path', text='Path')
TreeView.heading('Size', text='Size')
TreeView.heading('Created', text='Created')
TreeView.heading('Directory', text='Directory')
TreeView.heading('Type', text='Type')

root.bind('<Return>', showDir)
#root.bind('<Alt-c>',viewClear)
searchBtn = Button(root, text='Search', command=SearchExt)
amountbox = Text(frame5, width=2, height=1)
#openBtn = Button (root,text='Open',command=openFile)
dirBtn = Button(root, text='Dir', command=showDir)
backBtn = Button(root, text='<--', command=goBack)
historybtn = Button(root,text='History',command=history)


#titlelbl.pack()
canvas.pack()
frame1.pack()

selextlbl.pack(side=LEFT)
setExt.pack(pady=2, padx=2, side=RIGHT)

frame2.pack()
selEntryLbl.pack(side=LEFT)
extEntry.pack(side=RIGHT, pady=2, padx=2)
searchBtn.pack()

frame3.pack()

frame4.pack()
TreeView.pack(side=RIGHT)
frame5.pack()
totallbl.pack(side=LEFT)
amountbox.pack(side=RIGHT, pady=2, padx=2)

# openBtn.pack()
dirBtn.pack()
backBtn.pack()
historybtn.pack()

mainloop()
