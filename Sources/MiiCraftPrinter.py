'''
Warning: The codes are still under construction with mess codes. Need patience to read."
It will be organized and cleaned in the future release
'''

from __future__ import absolute_import
VER = "v0.4"
'''
 MiiCraft Printer Control Program
 v0.1    2012-May-4th  [P.K.] Initial version
 v0.2    2012-May-31th [T.W.] Improve performance
 v0.3    2012-Aug-15th [T.W.] solve fill resin funtion bug
 v0.4

    Part of the MiiCraft project
    Copyright (C) 2012  Thomas Wu, Paul Kang, Young Optics

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

#from tkMessageBox import *
#from tkColorChooser import askcolor 
# Built-in libraries
import time, os, struct
from Tkinter import *             
from tkFileDialog   import askopenfilename

# External libraries
from PIL import Image, ImageTk, ImageChops
import serial

# Import from serial_emu.py in the current directory
from serial_emu import *

class CmdDialog:
    def __init__(self, parent, VariableName, Message):
        global ResinCuringTime, USBDisplayStartX, SerialTimeOut, PostCuringTime

        top = self.top = Toplevel(parent)

        Label(top, text=Message, width=40,anchor=W).pack()

        self.e = Entry(top, width=40)
        self.e.pack(padx=5)

        b = Button(top, text="OK", command=lambda: self.ok(VariableName))
        b.pack(pady=5)

    def ok(self, VariableName):
        global root, ResinCuringTime, USBDisplayStartX, SerialTimeOut, PostCuringTime
        inputText = self.e.get()
        self.top.destroy()  
        if VariableName=="Test":
            cmd = inputText.split()
            print "CmdDialog Command is", cmd[0]                   
            send_a_cmd(cmd[0], "Test command "+cmd[0]+" from TestDialog")
            return
        
        cmd = inputText.split()
        
        if VariableName=="ResinCuringTime":                           
            ResinCuringTime = float(cmd[0])
            ConfigBtn.menu.entryconfig(1, label='Resin Curing Time :   '+str(ResinCuringTime))
            print "CmdDialog ResinCuringTime=", ResinCuringTime
            return        

        if VariableName=="USBDisplayStartX":                           
            USBDisplayStartX = int(cmd[0])
            ConfigBtn.menu.entryconfig(2, label='USB Display Start X : '+str(USBDisplayStartX))            
            print "CmdDialog USBDisplayStartX=", USBDisplayStartX
            USBDisplay.geometry("%dx%d+%d+%d" % (865, 480, USBDisplayStartX, 0))
            return

        if VariableName=="SerialTimeOut":                           
            SerialTimeOut = int(cmd[0])
            ConfigBtn.menu.entryconfig(3, label='SerialTimeOut :          '+str(SerialTimeOut))
            print "CmdDialog SerialTimeOut=", SerialTimeOut
            return

        if VariableName=="PostCuringTime":                           
            PostCuringTime = float(cmd[0])
            ConfigBtn.menu.entryconfig(3, label='PostCuringTime :       '+str(PostCuringTime))
            PostCuringBtn.menu.entryconfig(1, label='Post Curing by '+str(PostCuringTime)+' seconds')
            print "CmdDialog PostCuringTime=", PostCuringTime
            return          
         
        return 


'''
def test():
    root.geometry("%dx%d+%d+%d" % (300, 200, 100, 100))
   
def set_PageNum():
    print textPageNum.get(1.0, END)

def Reset_PageNum():
    textPageNum.delete(1.0,END)
    textPageNum.insert(END,'0')    
'''
###### Menu Commands

########## File Commands    
def my_quit():
    close_serial()
    root.destroy()
    root.quit()

def OpenFile():
    global NVPConnected, VaildIdxLoaded
    global dirname, prefixname, extname, startname, endname
    global start_num, end_num, total_num
    newfilename = askopenfilename()
    indexFile = open(newfilename)
    head   = indexFile.readline()
    if 'NVP Index file' in head:
        prefix     = indexFile.readline().split()
        ext        = indexFile.readline().split()
        num_start  = indexFile.readline().split()
        num_end    = indexFile.readline().split()
        num_total  = indexFile.readline().split()
        dirname    = os.path.dirname(newfilename)
        prefixname = prefix[1]
        extname    = ext[1]
        startname  = num_start[1]
        endname    = num_end[1]

        start_num = int(startname)
        end_num   = int(endname)
        total_num = end_num - start_num +1

        print "OpenFile ", start_num, end_num, total_num
        CurrentDir.set("Directory :  "+ dirname)
        Prefix_Ext.set("File Prefix:  "+prefixname+"\t\t\tFile Ext:  "+extname)
        Start_End.set ("Start from:  "+startname+"\t\t\tEnd At :  "+endname)
        
        imageFile = dirname+"/"+prefixname+startname+"."+extname
        image1         = Image.open(imageFile)
        image1_preview = image1.resize((432,270))
        image2 = ImageTk.PhotoImage(image1_preview)
        PreViewImage.configure(image= image2)
        PreViewImage.image = image2

        PreviewName.set("Preview Images - "+prefixname+startname+"."+extname)

        VaildIdxLoaded = True
        if NVPConnected:
            EnableInitControlBtns()
            
        
########## End Of File Commands

########## COM Commands

def com_search_open():
    global root, ser, NVPConnected, VaildIdxLoaded, SerialTimeOut
    COMList= enumerate_serial_ports() # Get the COM Port List
    
    for i in COMList:
        key = i
        try:
            ser = serial.Serial(key, 9600, timeout=SerialTimeOut)
            #print key, " Opened!"
            StatusText.set("Connect to "+key)
            root.update()
            header = ser.readline()
            if '2012' in header:
                #print "NVP is Found"
                StatusText.set("Printer is found at "+key)
                root.update()
#                ser.write('f1')
                ser.readline()
                ser.readline()                
                NVPConnected = True
                NVPConnectText.set("Printer Connected")
                root.update()
                
                ResinBtn.menu.entryconfig(1, state=NORMAL)
                ResinBtn.menu.entryconfig(2, state=NORMAL)
                TestBtn.menu.entryconfig (1, state=NORMAL)
                TestBtn.menu.entryconfig (2, state=NORMAL)
                PostCuringBtn.menu.entryconfig(1, state=NORMAL)
                
                if VaildIdxLoaded: EnableInitControlBtns()
                
                break
                
            ser.close()
            #print key, " Closed!"
            StatusText.set("Not Printer, close "+key)
            root.update()
        except SerialException, e:
            #print e
            StatusText.set("e")
            root.update()
            
COMList= enumerate_serial_ports() # Get the COM Port List

# define functions of every COM Port, these functions will be added when define COM menu's Manual Connect item    
openserials={}
for i in COMList:
    def item_openserial(name):
        def new_openserial():
            close_serial()
            global root, ser, NVPConnected, VaildIdxLoaded
            #print name
            StatusText.set("Connect to "+name)
            root.update()
            try:
                ser = serial.Serial(name, 9600, timeout=SerialTimeOut)
                header = ser.readline()
                if '2012' in header:
                    #print "NVP is Found"
                    StatusText.set("Printer is found at "+name)
                    root.update()
#                    ser.write('f1')
                    ser.readline()
                    ser.readline()                    
                    NVPConnected = True
                    NVPConnectText.set("Printer Connected")
                    root.update()

                    ResinBtn.menu.entryconfig(1, state=NORMAL)
                    ResinBtn.menu.entryconfig(2, state=NORMAL)
                    TestBtn.menu.entryconfig (1, state=NORMAL)
                    TestBtn.menu.entryconfig (2, state=NORMAL)
                    PostCuringBtn.menu.entryconfig(1, state=NORMAL)

                    
                    if VaildIdxLoaded: EnableInitControlBtns()
                else:
                    ser.close()
                    #print "NVP is NOT Found"
                    StatusText.set("Printer is NOT found at "+name)
                    root.update()
            except SerialException, e:
                #print e
                StatusText.set(e)
                root.update()

        return new_openserial
    openserials[i] = item_openserial(i)

#print openserials

COMList= enumerate_serial_ports() # Get the COM Port List again, the loop above makes the previous COMList empty

def close_serial():
    global root, ser, NVPConnected, VaildIdxLoaded
    serial_opened = True
    try:
        ser.write('j4')   # why f4?
    except NameError, e:        
        #print e
        serial_opened = False
    except ValueError, e:        
        print e
        StatusText.set(e)
        root.update()
        serial_opened = False
        
    if serial_opened:
        #print "Close the serial port"
        ser.close()
        StatusText.set("Serial port is closed")
        NVPConnected = False
        NVPConnectText.set("Printer Not Connected")
        root.update()

        ResinBtn.menu.entryconfig(1, state=DISABLED)
        ResinBtn.menu.entryconfig(2, state=DISABLED)
        TestBtn.menu.entryconfig (1, state=DISABLED)
        TestBtn.menu.entryconfig (2, state=DISABLED)
        PostCuringBtn.menu.entryconfig(1, state=DISABLED)
        DisableAllControlBtns()
        
########## End Of COM Commands

########## Resin Commands        
def FillResin():
    global root, ser, state

    ack =''
    ser.write('g')
    NVPback = ser.readline()
    cmdback = NVPback.split()

    if cmdback[0]!="g":
        StatusText.set("Printer no responses to cmd g")
        root.update()
        return

    if cmdback[1]=="OK":
        StatusText.set("Resin is filled")
        root.update()
        return

    StatusText.set("Filling resin ...")
    root.update()
    
    while ack != 'OK':
        NVPback = ser.readline()
        if NVPback!='': cmdback = NVPback.split()
        ack = cmdback[0]
        root.update()
        if ack == 'NG':
            StatusText.set("Please check the Resin Tank and Cartridge")
            root.update()
            state = 'R'
            break
        if ack == 'OK':
            StatusText.set("Resin is filled")
            root.update()
            state = '0'
            break

def RedrawResin():
    global root, ser

    ack =''
    ser.write('i')
    NVPback = ser.readline()
    cmdback = NVPback.split()
    if cmdback[0]!="i":
        #print "NVP no response to cmd i"
        StatusText.set("Printer no responses to cmd i")
        root.update()
        return

    StatusText.set("Redrawing resin ...")
    root.update()
    
    while ack != 'OK':
        NVPback = ser.readline()
        if NVPback!='': cmdback = NVPback.split()
        ack = cmdback[0]        

    StatusText.set("Resin is redrew")
    root.update()
    
########## End Of Resin Commands

###### End Of Menu Commands

def EnableInitControlBtns():
    BtnInit.config(state=NORMAL)
    BtnPrint.config(state=DISABLED)
    BtnPause.config(state=DISABLED)
    BtnStop.config(state=DISABLED)
    BtnSpeed.config(state=DISABLED)
    BtnLayer.config(state=DISABLED)

def EnablePrintControlBtns():
    BtnInit.config(state=DISABLED)
    BtnPrint.config(state=NORMAL)
    BtnPause.config(state=DISABLED)
    BtnStop.config(state=DISABLED)
    BtnSpeed.config(state=NORMAL)
    BtnLayer.config(state=NORMAL)
    
def EnableAllControlBtns():
    BtnInit.config(state=NORMAL)
    BtnPrint.config(state=NORMAL)
    BtnPause.config(state=NORMAL)
    BtnStop.config(state=NORMAL)
    BtnSpeed.config(state=NORMAL)
    BtnLayer.config(state=NORMAL)
    
def DisableAllControlBtns():
    BtnInit.config(state=DISABLED)
    BtnPrint.config(state=DISABLED)
    BtnPause.config(state=DISABLED)
    BtnStop.config(state=DISABLED)
    BtnSpeed.config(state=DISABLED)
    BtnLayer.config(state=DISABLED)
    
    

GoHome      = "a"; GoHomeMsg    = "Going to the Home position ..."
GoStart     = "b"; GoStartMsg   = "Going to the Printing position ..."
MoveAlayer  = "d"; MoveAlayerMsg= "Moving to next layer ..."
LEOn        = "r"; LEOnMsg      = "Curing the Resin ..."
LEOff       = "s"; LEOffMsg     = "Off UV ..."
PostCure    = "k"; PostCureMsg  = "Post Curing ..."
Checkup     = "u"; CheckupMsg   = "Platform up ..."
Checkdown   = "v"; CheckdownMsg = "Platform down ..."
PostUVOn    = "p"; PostUVOnMsg  = "Turn on Post UV ..."
PostUVOff   = "q"; PostUVOffMsg = "Turn off Post UV ..."


def send_a_cmd(cmd, message):
    global root, ser, state, PrintPause

    print "send_a_cmd", cmd, message

    ResinBtn.menu.entryconfig(1, state=DISABLED)
    ResinBtn.menu.entryconfig(2, state=DISABLED)
    PostCuringBtn.menu.entryconfig(1, state=DISABLED)
    
    ser.write(cmd)
    NVPback = ser.readline()
    print "send_a_cmd", NVPback
    cmdback = NVPback
    if cmdback[0] !=cmd:
        print "Printer no response to cmd "+cmd
        StatusText.set("Printer no responses to cmd "+cmd)
        root.update()
    if cmdback[2:4] =='OK':
        StatusText.set(message)
        root.update()
        state = '0'
    else:
       ack =''
       while ack != 'OK':
           StatusText.set(message)
           root.update()
           NVPback = ser.readline()
           if NVPback!='':
               cmdback = NVPback
               print cmdback

               if cmdback[0:2] =='NG':
                   state = 'N'
                   break
               state = '0'
               ack = cmdback[0:2]

    ResinBtn.menu.entryconfig(1, state=NORMAL)
    ResinBtn.menu.entryconfig(2, state=NORMAL)
    PostCuringBtn.menu.entryconfig(1, state=NORMAL)   

def build_a_layer(layer_num):
    
    global dirpathname, prefixname, extname, startname, endname
    global start_num, end_num, total_num, PrintPause, state
    global CountTimesR, ResinCuringTime, TimeMovelayer, TimeRemain

    if PrintPause:
        StatusText.set("Print will be Paused after finishing current layer ("+str(layer_num+1)+") ...")
        root.update

    if state == 'M':
        return False

    ResinBtn.menu.entryconfig(1, state=DISABLED)
    ResinBtn.menu.entryconfig(2, state=DISABLED)
    PostCuringBtn.menu.entryconfig(1, state=DISABLED)


    # show preview
    layername = str(layer_num+start_num)
    imageFile = dirname+"/"+prefixname+layername+"."+extname
    image_im         = Image.open(imageFile)

    if image_im.mode != "RGB":
        image_im = image_im.convert("RGB")

    im_filter = Image.open("CorrectRGB_MASK.png")

    if im_filter.mode != "RGB":
        im_filter = im_filter.convert("RGB")
        
    im_out = ImageChops.multiply(im_filter, image_im)
    Full_Image = Image.new("RGB", (864,480))
    Full_Image.paste(im_out, (0,0,768,480))

    image_tk         = ImageTk.PhotoImage(Full_Image)    
    image_preview    = image_im.resize((432,270))
    image_preview_tk = ImageTk.PhotoImage(image_preview)
    PreViewImage.configure(image= image_preview_tk)
    PreViewImage.image = image_preview_tk

    PreviewName.set("Preview Images - "+prefixname+layername+"."+extname)
    root.update()


    # Delay for resin curing
    USBShow(image_tk)

    # Fill resin

    BtnPause.config(state=DISABLED)
    FillResin()
    if state == 'R':
        BtnInit.config(state=NORMAL)
        Initiate_updown.set("Continue")
        root.update()
        while state == 'R':
            root.update()
    BtnPause.config(state=NORMAL)

    # Move a layer 
    if layer_num >0:
        TimeMovelayer_up = time.time()
        send_a_cmd(MoveAlayer, MoveAlayerMsg)
        TimeMovelayer_down = time.time()
        TimeMovelayer = (TimeMovelayer_down-TimeMovelayer_up)
        print "TimeMovelayer = "+str(TimeMovelayer)
        ResinBtn.menu.entryconfig(1, state=DISABLED)
        ResinBtn.menu.entryconfig(2, state=DISABLED)
        PostCuringBtn.menu.entryconfig(1, state=DISABLED)  

    if layer_num ==0:
        print "wait a moment for section image initiate ..."
        CountTimesR = int(ResinCuringTime/0.1)
#        for i in range(CountTimesR):
        for i in range(20):
            root.update()
            if PrintPause:
                StatusText.set("Print will be Paused after finishing current layer ("+str(layer_num+1)+") ...")
                root.update()
            time.sleep(0.1)

        print "Count Times:"+str(CountTimesR)
        
    # wait resin stable
    time.sleep(0.4)
        
    # show picture -- to be implemented
    # Turn On Light Engine Light
    send_a_cmd(LEOn, "Layer "+str(layer_num+1)+"/"+str(total_num)+": "+LEOnMsg)

    ResinBtn.menu.entryconfig(1, state=DISABLED)
    ResinBtn.menu.entryconfig(2, state=DISABLED)
    PostCuringBtn.menu.entryconfig(1, state=DISABLED)  

    if layer_num <3:
        for i in range(CountTimesR*5):
            root.update()
            if PrintPause:
                StatusText.set("Print will be Paused after finishing current layer ("+str(layer_num+1)+") ...")
                root.update()
            time.sleep(0.1)

    if ((layer_num == 3) | (layer_num == 4)):
        for i in range(CountTimesR*2):
            root.update()
            if PrintPause:
                StatusText.set("Print will be Paused after finishing current layer ("+str(layer_num+1)+") ...")
                root.update()
            time.sleep(0.1)
            
        
    # Using the loop instead of time.sleep(ResinCuringTime) to improve the response of the GUI
    timestart = time.time()
    for i in range(CountTimesR):
        root.update()
        if PrintPause:
            StatusText.set("Print will be Paused after finishing current layer ("+str(layer_num+1)+") ...")
            root.update()
        time.sleep(0.1)
    timeend = time.time()
    elapsed = timeend - timestart
    if (elapsed - ResinCuringTime)>0.1 :        
        CountTimesR=CountTimesR+int((ResinCuringTime-elapsed)/0.1)
    if elapsed < ResinCuringTime:
        CountTimesR=CountTimesR+int((ResinCuringTime-elapsed)/0.1)+1
        
    print "Real %.3f second Curing" % (elapsed)
   
    # turn off light engine Light-- to be implemented
    send_a_cmd(LEOff, LEOffMsg)

    ResinBtn.menu.entryconfig(1, state=DISABLED)
    ResinBtn.menu.entryconfig(2, state=DISABLED)
    PostCuringBtn.menu.entryconfig(1, state=DISABLED)

    if PrintPause:
        StatusText.set("Print is Paused")
        state = 'U'
        ResinBtn.menu.entryconfig(1, state=NORMAL)
        ResinBtn.menu.entryconfig(2, state=NORMAL)      
        root.update()
        
    while PrintPause:
        time.sleep(0.1)
        BtnInit.config(state=NORMAL)
        root.update()

    ResinBtn.menu.entryconfig(1, state=DISABLED)
    ResinBtn.menu.entryconfig(2, state=DISABLED)
    PostCuringBtn.menu.entryconfig(1, state=DISABLED)   
        
    if state == 'M':
        return False

    if layer_num >0:
        TimeRemain = (0.4+0.1+TimeMovelayer+ResinCuringTime)*(total_num-layer_num-1)
        TimeRemain_min = int(TimeRemain/60)+1

        if TimeRemain_min >1:
            TimeRemainText.set(": Left "+str(TimeRemain_min)+" minutes")
        else :
            TimeRemainText.set(": Less than 1 minute")

    # wait resin stable
    time.sleep(0.1)

    return True
   
def ControlInit():

    global state, resin_state, root
    global PrintPause, PrintStop

    PrintPause = False
    PrintStop  = False

    Initiate_updown.set("Initiate")
    Pause_Resume.set("Pause")

    ResinBtn.menu.entryconfig(1, state=DISABLED)
    ResinBtn.menu.entryconfig(2, state=DISABLED)
    PostCuringBtn.menu.entryconfig(1, state=DISABLED)
    
    root.update
    
    #DisableAllControlBtns()
    BtnInit.config(state=DISABLED)
    BtnPrint.config(state=DISABLED)
    BtnPause.config(state=DISABLED)    
    BtnStop.config(state=NORMAL)
    BtnSpeed.config(state=DISABLED)
    BtnLayer.config(state=DISABLED)
    root.update()
    
    # Set Z-Axis Home
    state = 'A'
    send_a_cmd(GoHome, GoHomeMsg)

    if state == '0':
        EnablePrintControlBtns()
        StatusText.set("Home")
        root.update()
    else :
        StatusText.set("Processing closed by Stop")
        root.update()
        EnableInitControlBtns()

    # this is for abort processing
    state = 'M'
    resin_state = '0'

    PrintPause = False

    ResinBtn.menu.entryconfig(1, state=NORMAL)
    ResinBtn.menu.entryconfig(2, state=NORMAL)
    PostCuringBtn.menu.entryconfig(1, state=NORMAL)


def ControlPrint():
    global ResinCuringTime
    global start_num, end_num, total_num
    global PrintPause, PrintStop
    global root, imageBlank_tk
    global state, resin_state

    PrintPause = False
    PrintStop  = False

    ResinBtn.menu.entryconfig(1, state=DISABLED)
    ResinBtn.menu.entryconfig(2, state=DISABLED)
    PostCuringBtn.menu.entryconfig(1, state=DISABLED)   
    
    print "ControlPrint ", start_num, end_num, total_num

    BtnInit.config(state=DISABLED)
    BtnPrint.config(state=DISABLED)
    BtnPause.config(state=DISABLED)
    BtnSpeed.config(state=DISABLED)
    BtnLayer.config(state=DISABLED)

    resin_state = '1'

    FillResin()
    if state == 'R':
        BtnInit.config(state=NORMAL)
        Initiate_updown.set("Continue")
        root.update()
        while state == 'R':
            root.update()

    BtnPrint.config(state=DISABLED)
    BtnStop.config(state=NORMAL)
        
    # Set Z-Axis Start Position
    state = 'B'
    send_a_cmd(GoStart, GoStartMsg)
    state = '0'

    ResinBtn.menu.entryconfig(1, state=DISABLED)
    ResinBtn.menu.entryconfig(2, state=DISABLED)
    PostCuringBtn.menu.entryconfig(1, state=DISABLED)
     
    # initialize others -- to be implemented

    # check status -- to be implemented
  
    if PrintStop:
        StatusText.set("Print is Aborted")            
        root.update()
        panel.configure(image = imageBlank_tk)
        panel.image = imageBlank_tk
        EnableInitControlBtns()

        ResinBtn.menu.entryconfig(1, state=NORMAL)
        ResinBtn.menu.entryconfig(2, state=NORMAL)
        PostCuringBtn.menu.entryconfig(1, state=NORMAL)

        return    
    
    StatusText.set("Printing")

    PrintPause    = False
    PrintStop     = False
    
    BtnPause.config(state=NORMAL)    
    BtnStop.config(state=DISABLED)    
    root.update()
   
    for i in range(total_num):
        print "Layer: ",i
        build_a_layer(i)
        if PrintPause:
            StatusText.set("Print is Paused")
            root.update()
            panel.configure(image = imageBlank_tk)
            panel.image = imageBlank_tk             
            return            
 
    TimeRemainText.set(" ")
    if state == 'M':
        return
    
    send_a_cmd(MoveAlayer, MoveAlayerMsg)

    ResinBtn.menu.entryconfig(1, state=DISABLED)
    ResinBtn.menu.entryconfig(2, state=DISABLED)
    PostCuringBtn.menu.entryconfig(1, state=DISABLED)

    PrintPause    = False
    PrintStop     = False
        
    BtnPause.config(state=DISABLED)    
    BtnStop.config(state=NORMAL)
    root.update()
    state = 'A'
    resin_state = '0'
    send_a_cmd(GoHome, "Print Done! "+GoHomeMsg)

    if state == '0':
        EnablePrintControlBtns()
        StatusText.set("Print Done!")
        root.update()
    else :
        StatusText.set("Processing broken by Stop")
        root.update()
        EnableInitControlBtns()  
    
def ControlPause():
    global PrintPause, PrintStop, root, state
    print "Pause is clicked"
    if PrintPause == False:
        PrintPause = True
        Pause_Resume.set("Resume")
        Initiate_updown.set("Check")        
        
    else :
        PrintPause = False
        Initiate_updown.set("Initiate")
        Pause_Resume.set("Pause")
        BtnInit.config(state=DISABLED)
        StatusText.set("Print Process continue ...")
        root.update()
    

def ControlStop():
    global PrintPause, PrintStop, ser, state
    PrintStop = True

    TimeRemainText.set(" ")
    
   #EnableAllControlBtns()  
    if ((state == 'A') | (state == 'B') | (state == 'K')):
        print "send_break", state
        ser.write('t')
        return
    if state == 'V':
        print "Abort print from ", state
        ser.write('t')
        ControlInit()
        return False
        

def ControlIniSwitch():
    global PrintPause, state, resin_state
    if state == 'R':
        state = '0'
        Initiate_updown.set("Initiate")
        BtnInit.config(state=DISABLED)
        if resin_state == '1':
            return
    if PrintPause == False:
        ControlInit()
    if PrintPause == True:
        CheckModel()
                


def CheckModel():
    global state, ser, PrintStop, PrintPause, root

    if state == 'U':
        BtnPause.config(state=DISABLED)
        BtnInit.config(state=DISABLED)
        StatusText.set(CheckupMsg)
        root.update()
        print "check"
        
        send_a_cmd(Checkup, CheckupMsg)

        ResinBtn.menu.entryconfig(1, state=DISABLED)
        ResinBtn.menu.entryconfig(2, state=DISABLED)
        PostCuringBtn.menu.entryconfig(1, state=DISABLED)

        Initiate_updown.set("Continue")
        StatusText.set("Continue or press ''Stop'' to Abort Print")
        BtnInit.config(state=NORMAL)
        BtnStop.config(state=NORMAL)
        root.update()
        state = 'V'
        return

    if state == 'V':
        BtnInit.config(state=DISABLED)
        BtnStop.config(state=DISABLED)
        StatusText.set(CheckdownMsg)
        root.update()
        print "continue"
        send_a_cmd(Checkdown, CheckdownMsg)

        PostCuringBtn.menu.entryconfig(1, state=DISABLED)
        
        Initiate_updown.set("Check")
        StatusText.set("Press ''Resume'' to continue Print")
        BtnPause.config(state=NORMAL)
        BtnInit.config(state=NORMAL)
        root.update()
        state = 'U'
        return
 

def SettingSpeed():
    global speed_print, thick_layer, MoveAlayer
    
    if speed_print==0:
        PrintSpeed.set("Slow")
        speed_print=1

    else:
        PrintSpeed.set("Normal")
        speed_print=0

    if speed_print+thick_layer==0:
        MoveAlayer  = "d"
    if speed_print+thick_layer==1:
        MoveAlayer  = "f"
    if speed_print+thick_layer==2:
        MoveAlayer  = "c"
    if speed_print+thick_layer==3:
        MoveAlayer  = "e"

def SettingThickness():
    global speed_print, thick_layer, MoveAlayer
    
    if thick_layer==0:
        PrintThickness.set("50 micro")
        thick_layer=2
    else:
        PrintThickness.set("100 micro")
        thick_layer=0

    if speed_print+thick_layer==0:
        MoveAlayer  = "d"
    if speed_print+thick_layer==1:
        MoveAlayer  = "f"
    if speed_print+thick_layer==2:
        MoveAlayer  = "c"
    if speed_print+thick_layer==3:
        MoveAlayer  = "e"


def USBShow(imageTk):
    panel.configure(image = imageTk)
    #panel.image = image_tk    
    return

def testDialog():
    global root
    d = CmdDialog(root, "Test", "Input a Printer Command")
    root.wait_window(d.top)

def ResinCuringTimeDialog():
    global root
    d = CmdDialog(root, "ResinCuringTime", "Input ResinCuringTime")
    root.wait_window(d.top)

def USBDisplayStartXDialog():
    global root
    d = CmdDialog(root, "USBDisplayStartX", "Input USBDisplayStartX")
    root.wait_window(d.top)

def SerialTimeOutDialog():
    global root
    d = CmdDialog(root, "SerialTimeOut", "Input SerialTimeOut")
    root.wait_window(d.top)      

def PostCuringTimeDialog():
    global root
    d = CmdDialog(root, "PostCuringTime", "Input PostCuringTime")
    root.wait_window(d.top) 
    
def ReadIni():
    global ResinCuringTime, USBDisplayStartX, SerialTimeOut, PostCuringTime
    try:
        #f_ini = open("NVP.ini","r")
        f_ini = open("MiiCraftSuite.ini","r")
        readLines = f_ini.readlines()
        for i in readLines:          
            if 'ResinCuringTime' in i:
                parameters = i.split()
                ResinCuringTime = float(parameters[1])
                continue
            if 'USBDisplayStartX' in i:
                parameters = i.split()
                USBDisplayStartX = int(parameters[1])            
                continue
            if 'SerialTimeOut' in i:
                parameters = i.split()
                SerialTimeOut = int(parameters[1])            
                continue
            if 'PostCuringTime' in i:
                parameters = i.split()
                PostCuringTime = float(parameters[1])            
                continue              
        f_ini.close()
    except IOError, e:
        print e    
    
def PostCuring():
    global root, ser, state, PostCuringTime, PrintStop

    send_a_cmd(PostUVOn, PostUVOnMsg)

    state = 'K'
    #send_a_cmd(PostCure, PostCureMsg)
    ser.write('k')

    BtnInit.config(state=DISABLED)
    BtnPrint.config(state=DISABLED)
    BtnPause.config(state=DISABLED)    
    BtnStop.config(state=NORMAL)

    PrintStop = False

    NVPback = ser.readline()
    print "send_a_cmd", NVPback
    cmdback = NVPback
    print cmdback
    if cmdback[0] !='k':
        print "Printer no response to cmd "+'k'
        StatusText.set("Printer no responses to cmd "+'k')
        root.update()
    else:
        StatusText.set("Post Curing complete in "+str(PostCuringTime)+" seconds")
        root.update()

    i = 0
    while ( i < PostCuringTime):
        root.update()
        i = i + 0.1
#        print "PostCuring", i, PostCuringTime
        time.sleep(0.1)
        j=PostCuringTime-i+1
        StatusText.set("Post Curing complete in "+str(int(j))+" seconds")
        if PrintStop:
            break
        
    if PrintStop == False:
       ser.write('t')

    ack =''
    while ack != 'OK':
        StatusText.set("Post Curing finishing ...")
        root.update()
        NVPback = ser.readline()
        if NVPback!='':
            cmdback = NVPback
            print cmdback
            state = '0'
            ack = cmdback[0:2]

    send_a_cmd(PostUVOff, PostUVOffMsg)
            
    StatusText.set("Post Curing Complete!")
    

    if NVPConnected and VaildIdxLoaded:
        EnableInitControlBtns()
    else :
        DisableAllControlBtns()

    root.update()
    state = '0'
    
#    ser.readline()
    return
    
def not_implemented_yet():
    global ser
    print ser.readline()
    print "not_implemented_yet"
    return

global ser, SerialTimeOut
global ResinCuringTime, USBDisplayStartX, PostCuringTime
# defaults
ResinCuringTime  = 5     # 5 seconds
USBDisplayStartX = 1366  # Assume the primary screen is 1366x768, eg. HP 8440p
PostCuringTime   = 10
SerialTimeOut    = 1
    
global dirpathname, prefixname, extname, startname, endname
global start_num, end_num, total_num
global state, resin_state
global speed_print, thick_layer
speed_print = 0 # 0=normal, 1=slow 
thick_layer = 0 # 0=100micro, 2=50micro
state = '0'
resin_state = '0' # 0=initial, 1=ptinting

global NVPConnected, VaildIdxLoaded, PrintPause, PrintStop
NVPConnected   = False
VaildIdxLoaded = False
PrintPause     = False
PrintStop      = False




global root, imageBlank

ReadIni()
print "ResinCuringTime:",  ResinCuringTime
print "USBDisplayStartX:", USBDisplayStartX
print "SerialTimeOut",     SerialTimeOut
print "PostCuringTime",    PostCuringTime

root = Tk()
root.title("MiiCraftPrinter " + VER)
#root.overrideredirect(1)
#root.geometry("%dx%d+%d+%d" % (880, 800, 100, 100))
root.resizable(0,0)
#root.protocol("WM_DELETE_WINDOW","pass")
root.protocol("WM_DELETE_WINDOW",my_quit)

# USB Display ###########################################
# 8440p LCD is 1366x768, the ASUS 22" monitor is 1680x1050
# USB Display is 860x480
USBDisplay = Toplevel()
USBDisplay.overrideredirect(1)

USBDisplay.geometry("%dx%d+%d+%d" % (865, 480, USBDisplayStartX, 0))

imageBlank  = Image.new("P", (864,480),0)
imageBlank_tk  = ImageTk.PhotoImage(imageBlank)

panel = Label(USBDisplay, image=imageBlank_tk)
panel.pack(side='top', fill='both', expand='yes')
#########################################################

PreviewName    = StringVar()
CurrentDir     = StringVar()
Prefix_Ext     = StringVar()
Start_End      = StringVar()
StatusText     = StringVar()
NVPConnectText = StringVar()
Pause_Resume   = StringVar()
Initiate_updown= StringVar()
TimeRemainText = StringVar()
PrintSpeed     = StringVar()
PrintThickness = StringVar()


PreviewName.set("Preview Images")
CurrentDir.set("Directory :")
Prefix_Ext.set("File Prefix:\t\t\tFile Ext:")
Start_End.set ("Start from:\t\t\tEnd At :")
StatusText.set("Load a valid Idx file and Connect to Printer")
NVPConnectText.set("Printer NOT Connected")
Pause_Resume.set("Pause")
Initiate_updown.set("Initiate")
TimeRemainText.set(" ")
PrintSpeed.set("Normal")
PrintThickness.set("100 micro")

#menu
mBar = Frame(root, relief=RAISED, borderwidth=2)
mBar.pack(fill=X)
FileBtn = Menubutton(mBar, text='File')
FileBtn.pack(side=LEFT, padx="2m")
FileBtn.menu = Menu(FileBtn)
FileBtn.menu.add_command(label='Open Image Index File ...', command=OpenFile)
FileBtn.menu.add('separator')
FileBtn.menu.add_command(label='Quit', command=my_quit)
FileBtn['menu'] = FileBtn.menu

COMBtn = Menubutton(mBar, text='Connect')
COMBtn.pack(side=LEFT, padx="2m")
COMBtn.menu = Menu(COMBtn)
COMBtn.menu.add_command(label='Auto Search and Connect', command=com_search_open)
COMBtn.menu.choices = Menu(COMBtn.menu)

# See http://stackoverflow.com/questions/728356/dynamically-creating-a-menu-in-tkinter-lambda-expressions
for i in COMList:

    COMBtn.menu.choices.add_command(label=i, command =openserials[i])

COMBtn.menu.add_cascade(label='Connect Manually', menu=COMBtn.menu.choices)
FileBtn.menu.add('separator')
COMBtn.menu.add_command(label='Disconnect Serial', command=close_serial)
COMBtn['menu'] = COMBtn.menu

ConfigBtn = Menubutton(mBar, text='Config')
ConfigBtn.pack(side=LEFT, padx="2m")
ConfigBtn.menu = Menu(ConfigBtn)
ConfigBtn.menu.add_command(label='Resin Curing Time :   '+str(ResinCuringTime),  command = ResinCuringTimeDialog)
ConfigBtn.menu.add_command(label='USB Display Start X : '+str(USBDisplayStartX), command = USBDisplayStartXDialog)
ConfigBtn.menu.add_command(label='Post Curing Time :     '+str(PostCuringTime), command = PostCuringTimeDialog)
ConfigBtn.menu.add_command(label='SerialTimeOut :          '+str(SerialTimeOut), command = SerialTimeOutDialog)
ConfigBtn['menu'] = ConfigBtn.menu

ResinBtn = Menubutton(mBar, text='Resin')
ResinBtn.pack(side=LEFT, padx="2m")
ResinBtn.menu = Menu(ResinBtn)
ResinBtn.menu.add_command(label='Fill Resin',   command=FillResin)
ResinBtn.menu.add_command(label='Redraw Resin', command=RedrawResin)
ResinBtn['menu'] = ResinBtn.menu
ResinBtn.menu.entryconfig(1, state=DISABLED)
ResinBtn.menu.entryconfig(2, state=DISABLED)


PostCuringBtn = Menubutton(mBar, text='Post Curing')
PostCuringBtn.pack(side=LEFT, padx="2m")
PostCuringBtn.menu = Menu(PostCuringBtn)
PostCuringBtn.menu.add_command(label='Post Curing by '+str(PostCuringTime)+' seconds',  command = PostCuring)
PostCuringBtn['menu'] = PostCuringBtn.menu
PostCuringBtn.menu.entryconfig(1, state=DISABLED)

TestBtn = Menubutton(mBar, text='Test')
TestBtn.pack(side=LEFT, padx="2m")
TestBtn.menu = Menu(TestBtn)
TestBtn.menu.add_command(label='Test a command',   command=testDialog)
TestBtn.menu.add_command(label='Read a line in',    command=not_implemented_yet)
TestBtn['menu'] = TestBtn.menu
TestBtn.menu.entryconfig(1, state=DISABLED)
TestBtn.menu.entryconfig(2, state=DISABLED)

f = Frame(root, width=461, height=616)

#PreView Image Frame
PreViewFrame = Frame(f, relief=GROOVE, borderwidth=2)
PreViewFrame.place(x=10, y=15, anchor=NW)
Label(f, textvariable=PreviewName, font=("Helvetica", 10, 'bold')).place(x=20, y=15,anchor=W)
imageFile = os.getcwd()+"\\splash.png"
imageSplash = ImageTk.PhotoImage(Image.open(imageFile))
PreViewImage = Label(PreViewFrame, image=imageSplash)
PreViewImage.pack(pady=10)

#Data Frame
DataFrame = Frame(f,  relief=GROOVE, borderwidth=2)
DataFrame.place(x=10, y=320, anchor=NW)
Label(DataFrame, textvariable=CurrentDir, font=("Helvetica", 10, 'bold'), width=52, anchor=W).grid(row=0, sticky=W, padx=7,pady=5)
Label(DataFrame, textvariable=Prefix_Ext, font=("Helvetica", 10, 'bold'), width=52, anchor=W).grid(row=1, sticky=W, padx=7,pady=5)
Label(DataFrame, textvariable=Start_End,  font=("Helvetica", 10, 'bold'), width=52, anchor=W).grid(row=2, sticky=W, padx=7,pady=5)

FilePrefix = Text(DataFrame, height=1, width=33, font=("Helvetica", 10, 'bold'))
ImageCount = Text(DataFrame, height=1, width=33, font=("Helvetica", 10, 'bold'))


# NVP Setting Frame
SettingFrame = Frame(f, relief=GROOVE, borderwidth=2)
SettingFrame.place(x=10, y=429, anchor=NW)
Label(f, text="Setting", font=("Helvetica", 10, 'bold')).place(x=15, y=431,anchor=W)
Label(f, text="Print Speed:", font=("Helvetica", 10, 'bold')).place(x=20, y=455,anchor=W)
Label(f, text="Thickness:", font=("Helvetica", 10, 'bold')).place(x=240, y=455,anchor=W)
BtnSpeed  = Button(SettingFrame, textvariable=PrintSpeed, font=("Helvetica", 10, 'bold'), command= SettingSpeed, width=9, state=DISABLED)
BtnSpeed.pack(side=LEFT,padx=115, pady=12)
BtnLayer = Button(SettingFrame, textvariable=PrintThickness, font=("Helvetica", 10, 'bold'), command= SettingThickness, width=9, state=DISABLED)
BtnLayer.pack(side=LEFT,padx=21, pady=12)


# NVP Control Frame
ControlFrame = Frame(f, relief=GROOVE, borderwidth=2)
ControlFrame.place(x=10, y=494, anchor=NW)
Label(f, text="Control", font=("Helvetica", 10, 'bold')).place(x=15, y=496,anchor=W)
BtnInit = Button(ControlFrame, textvariable=Initiate_updown, font=("Helvetica", 10, 'bold'), command= ControlIniSwitch, width=9, state=DISABLED)
BtnInit.pack(side=LEFT,padx=13, pady=12)
BtnPrint = Button(ControlFrame, text="Print", font=("Helvetica", 10, 'bold'), command= ControlPrint, width=9, state=DISABLED)
BtnPrint.pack(side=LEFT,padx=13, pady=12)
BtnPause = Button(ControlFrame, textvariable=Pause_Resume, font=("Helvetica", 10, 'bold'), command= ControlPause, width=9, state=DISABLED)
BtnPause.pack(side=LEFT,padx=14, pady=12)
BtnStop  = Button(ControlFrame, text="Stop", font=("Helvetica", 10, 'bold'), command= ControlStop, width=9, state=DISABLED)
BtnStop.pack(side=LEFT,padx=14, pady=12)


# Status Frame
StatusFrame = Frame(f, relief=GROOVE, borderwidth=2)
StatusFrame.place(x=10, y=559, anchor=NW)
Label(f, text="Status", font=("Helvetica", 10, 'bold')).place(x=15, y=561,anchor=W)
Label(f, textvariable=TimeRemainText, font=("Helvetica", 10, 'bold')).place(x=60, y=561,anchor=W)
Label(f, textvariable=NVPConnectText, font=("Helvetica", 10, 'bold')).place(x=290, y=561,anchor=W)
Label(StatusFrame, textvariable=StatusText, font=("Helvetica", 10, 'bold'), width=52, anchor=W, wraplength=400, justify=LEFT).grid(row=0, sticky=W, padx=7,pady=10)


f.pack()

root.mainloop()
