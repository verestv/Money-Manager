from tkinter import *
from tkinter import ttk
import sqlite3
from configparser import ConfigParser
import winsound
import threading

#save colours and fonts


parser = ConfigParser()
parser.read('confset.txt')
saved_root_color = parser.get('colors','root_color')
saved_list_color = parser.get('colors','list_color')
saved_datalabel_color = parser.get('colors','datalabel_color')
saved_moneylabel_color = parser.get('colors','moneylabel_color')
saved_font = parser.get('fonts','list_font')
saved_font_color =parser.get('fonts','font_color')

#summarize entry input 
def sumurry():
   try:
      value = entrymoney.get()
      x = value.split('+')
      amounts = []
      for i in x: 
         amounts.append(int(i))
      y = sum(amounts)
      return y
   except:
      return -1
      
# DELETING all records from list
def clear_list():
   global list_data
   theList.delete(0,END)
   list_data =[]

#delete records from database
def delete_all():
   conn = sqlite3.connect('days.db')
   c = conn.cursor()
   c.execute('DELETE from spending')
   conn.commit()
   conn.close()
#confirmation pop up , asking if u sure abt deleting all records
def delConfirm():
      global popD
      popD = Toplevel(root)
      popD.title('Warning')
      popD.iconbitmap('warning.ico')
      popD.geometry('390x85+740+300')
      popD.resizable(False,False)
      def playw():
         global playwin
         playwin = winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

      def Yesdel():
         clear_list()
         delete_all()
         popD.destroy()
      def Nodel():
         popD.destroy()
      labwarn = Label(popD,text='Are you sure that you want to delete all records?',font =('Times','15'))
      labwarn.grid(column=0,row=0)
      YesB = ttk.Button(popD,text='Yes',command = Yesdel)
      YesB.grid(column=0,row=1)
      NoB = ttk.Button(popD,text='No',command=Nodel)
      NoB.grid(column=0,row=2)
      th = threading.Thread(target = playw,args=[])
      th.start()
      
#delete anchor in list
def delete():
   theList.delete(ANCHOR)
   global list_data
   conn = sqlite3.connect('days.db')
   c = conn.cursor()
   #c.execute('DELETE from spending where spent_money = -1')
   c.execute('DELETE FROM spending WHERE oid = (SELECT MAX(oid) FROM spending)')
   list_data.pop()
   conn.commit()
   conn.close()

#appends elemnts from db to list and counting spent money for days , after 7 daysprint how much u spent per week
def query():
   global list_data
   conn = sqlite3.connect('days.db')
   c = conn.cursor()
   
   c.execute("SELECT *,oid FROM spending")
   
   records = c.fetchall()
   last_element = list(records).pop()
   theList.insert(0,(f'Date: {last_element[0]} - {last_element[1]} uah'))
   list_data.append(f'Date: {last_element[0]} - {last_element[1]} uah')
   x = 7
   if len(list(records))%x==0:
      weeksum = []
      for element in records[-7:]:
         for item in element:
            if element.index(item) == 1:
               weeksum.append(int(item))
      add = sum(weeksum)
      theList.insert(0,(f'You have spent {add} uah for a previous week'))
      list_data.append(f'You have spent {add} uah for a previous week')
      weeksum.clear()
      x+=7   
   conn.commit()
   conn.close()

#saving records to db
def save():

   x = sumurry()
   conn = sqlite3.connect('days.db')
   c = conn.cursor()
   c.execute('INSERT INTO spending VALUES (:date, :spentmon)',
   {
      'date' : entrydate.get(),
      'spentmon' : x
   }
   )
   entrydate.delete(0,END)
   entrymoney.delete(0,END)
   
   conn.commit()
   conn.close()

#output saved data to list after program is open
def retrievedata():
   global list_data
   list_data = []
   try:
      with open('save.txt','r',encoding = 'utf-8') as file:
         for f in file:
            theList.insert(0,f.strip())
            list_data.append(f.strip())
            #print(list_data)
   except:
       pass

#saving all updates to text file after closing app
def quit():
   global root
   with open('save.txt','w',encoding='utf-8') as file:
      for e in list_data:
         file.write(e +'\n')
   root.destroy()

#design settings
def designset():
   
   global pop
   pop = Toplevel(root)
   pop.iconbitmap('design.ico')
   pop.title('Design Settings')
   pop.geometry('215x150+830+220')
   pop.resizable(False,False)
   pop.config()
   def savecm():
      opt = colours.get()
      if opt == 'White':
         root.config(bg = '#FFF8DC')
         datalabel.config(bg = '#FFF8DC')
         moneylabel.config(bg = '#FFF8DC')
         theList.config(bg='white',fg ='black')
         parser = ConfigParser()
         parser.read('confset.txt')
         parser.set('colors','root_color','#FFF8DC')
         parser.set('colors','list_color','white')
         parser.set('colors','datalabel_color','#FFF8DC')
         parser.set('colors','moneylabel_color','#FFF8DC')
         parser.set('fonts','font_color','black')
         with open('confset.txt','w') as confs:
             parser.write(confs)
      if opt == 'Blue':
         root.config(bg = '#00246B')
         datalabel.config(bg = '#00246B')
         moneylabel.config(bg = '#00246B')
         theList.config(bg='#8AB6F9',fg ='#00246B')
         parser = ConfigParser()
         parser.read('confset.txt')
         parser.set('colors','root_color','#00246B')
         parser.set('colors','list_color','#8AB6F9')
         parser.set('colors','datalabel_color','#00246B')
         parser.set('colors','moneylabel_color','#00246B')
         parser.set('fonts','font_color','#00246B')
         with open('confset.txt','w') as confs:
             parser.write(confs)
      if opt == 'Red':
         root.config(bg = '#962E2A')
         datalabel.config(bg = '#962E2A')
         moneylabel.config(bg = '#962E2A')
         theList.config(bg='#E3867D',fg='black')
         parser = ConfigParser()
         parser.read('confset.txt')
         parser.set('colors','root_color','#962E2A')
         parser.set('colors','list_color','#E3867D')
         parser.set('colors','datalabel_color','#962E2A')
         parser.set('colors','moneylabel_color','#962E2A')
         parser.set('fonts','font_color','black')
         with open('confset.txt','w') as confs:
             parser.write(confs)
      if opt == 'Yellow':
         root.config(bg = '#DC3E26')
         datalabel.config(bg = '#DC3E26')
         moneylabel.config(bg = '#DC3E26')
         theList.config(bg='#EDCD44',fg = '#A0522D')
         parser = ConfigParser()
         parser.read('confset.txt')
         parser.set('colors','root_color','#DC3E26')
         parser.set('colors','list_color','#EDCD44')
         parser.set('colors','datalabel_color','#DC3E26')
         parser.set('colors','moneylabel_color','#DC3E26')
         parser.set('fonts','font_color','#A0522D')
         with open('confset.txt','w') as confs:
             parser.write(confs)
      if opt == 'Black':
         root.config(bg = '#656E77')
         datalabel.config(bg = '#656E77')
         moneylabel.config(bg = '#656E77')
         theList.config(bg='#3B373B',fg ='white')
         parser = ConfigParser()
         parser.read('confset.txt')
         parser.set('colors','root_color','#656E77')
         parser.set('colors','list_color','#3B373B')
         parser.set('colors','datalabel_color','#656E77')
         parser.set('colors','moneylabel_color','#656E77')
         parser.set('fonts','font_color','white')
         with open('confset.txt','w') as confs:
             parser.write(confs)
      if opt == 'Green':
         root.config(bg = '#7C8363')
         datalabel.config(bg = '#7C8363')
         moneylabel.config(bg = '#7C8363')
         theList.config(bg='#31473A',fg = '#EDF4F2' )
         parser = ConfigParser()
         parser.read('confset.txt')
         parser.set('colors','root_color','#7C8363')
         parser.set('colors','list_color','#31473A')
         parser.set('colors','datalabel_color','#7C8363')
         parser.set('colors','moneylabel_color','#7C8363')
         parser.set('fonts','font_color','#EDF4F2')
         with open('confset.txt','w') as confs:
             parser.write(confs)
      else:
         pass
   def savecmF():
      try:
      
         parser = ConfigParser()
         parser.read('confset.txt')
         theList.config(font=('Times', '20', (f'bold ' + fonts.get())))
         parser.set('fonts','list_font',f'bold ' + fonts.get())
         with open('confset.txt','w') as confs:
            parser.write(confs)
      except:
         pass
   
   colops = ['Colours','White','Blue','Red','Yellow','Black','Green']
   fontops = ['Fonts','normal','italic','roman','underline','overstrike']
   colours =  StringVar()
   colours.set(colops[0])
   fonts = StringVar()
   fonts.set(fontops[0])

   dropC = ttk.OptionMenu(pop,colours,*colops)
   dropC.grid(column=2,row=0)

   dropF = ttk.OptionMenu(pop,fonts,*fontops)
   dropF.grid(column = 3,row=0)

   savebtn = ttk.Button(pop,text= 'save',command=lambda: [savecm(),savecmF()])
   savebtn.grid(column= 4,row=0)
   
        
conn = sqlite3.connect('days.db')
c = conn.cursor()
#Database creation
'''
c.execute("""CREATE TABLE spending(
   data text,
   spent_money integer
)""")
'''
conn.commit()
conn.close()

#main programm

if __name__ == '__main__':
   root = Tk()
   root.config(bg = saved_root_color)
   root.geometry('765x900+550+70')
   root.title('Money Manager')
   root.resizable(False,False)
   root.iconbitmap('dollarA.ico')
   
   theList = Listbox(root,font = ('Times', '20', saved_font) ,bg = saved_list_color,fg = saved_font_color,justify='center',highlightthickness=0,selectbackground='#cae0e0',activestyle='none',height = 24,width = 48)
   theList.place(x = 45,y = 115)

   datalabel = Label(text='Enter date(d/m/y)',bg = saved_datalabel_color,font=("Times New Roman bold", 19),width=14)
   datalabel.place(x = 14, y = 10)
   moneylabel = Label(text='Enter amount of money',bg = saved_moneylabel_color,font=("Times New Roman bold", 19),width=39)
   moneylabel.place(x = 218, y =10)
   entrydate = Entry(root,width =15,font=("Times New Roman", 20))
   entrydate.place(x = 20, y = 50)
   entrymoney = Entry(root,width =32,font=("Times New Roman", 20))
   entrymoney.place(x = 295, y = 50)

   btnsave = ttk.Button(text = 'Save',command = lambda:[save(),query()]).place(x = 630,y = 89)
   clearbtn = ttk.Button( text=" Delete all records", command=delConfirm).place(x = 443,y = 89)
   deletebtn = ttk.Button(text = 'Delete',command = delete).place(x = 550,y =89)
   quitandsave = ttk.Button(text = 'Quit and save',command=quit).place(x = 665,y = 10)
   userSettings= ttk.Button(text = 'Design Settings',command=designset).place(x =348, y = 89)
  
   retrievedata()
   root.mainloop()

