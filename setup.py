'''
MiiCraft Suite setup script
 v0.1 Initial version
 v0.4 2012-July-16th 1. Move the skeinforge initializing to the last
                     2. Input "Enter" or "Y/y" as Yes and others as No for install packages
                     3. Remove goldberg.stl
 v0.5 2012-Aug-9th   1. Add the reminder for user to copy the uniformity correction mask 
                     
 Part of the MiiCraft project
 Copyright(c) 2012 Paul Kang

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software Foundation,
 Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''

import sys
import os, os.path
import zipfile

MiiCraft_VER = "_V05"

prerequisties =[
'PIL http://www.pythonware.com/products/pil/',
'pyserial http://sourceforge.net/projects/pyserial/files/pyserial/2.5/',
'VPython http://vpython.org/contents/download_windows.html',
'Skeinforge http://fabmetheus.crsndoo.com/',
'ImageMagick http://www.imagemagick.org/script/binary-releases.php?ImageMagick=gtf6ucp7rjj2bu991lqg0839v3#windows']

prerequisty_keys =[
'PIL',
'pyserial',
'VPython',
'reprap_python_beanshell',
'ImageMagick']

checked = [False, False, False, False, False]

#Print Prerequistes
print """
MiiCraft Suite is based on Open Source. It requires the prerequisties below,
    - Python 2.x (Python 2.6.6 is recommended)
      http://www.python.org/download/

    - Python Image Library (PIL 1.1.7 is recommended)
      http://www.pythonware.com/products/pil/

    - PySerial (v2.5 is recommended)
      http://sourceforge.net/projects/pyserial/files/pyserial/2.5/

    - VPython (v2.6.5.72 is recommended)
      http://vpython.org/contents/download_windows.html
                
    - Skeinforge (50_reprap_python_beanshell.zip is recommended)
      http://fabmetheus.crsndoo.com/

    - ImageMagik (v6.7.6-1Q16 is recommended)
      http://www.imagemagick.org/script/binary-releases.php?ImageMagick=gtf6ucp7rjj2bu991lqg0839v3#windows
"""

# All the files for setup are placed in Sources directory
Setup_CWD = os.getcwd()
print "Change from "+Setup_CWD+" to "+Setup_CWD+"\\Sources\\\n"
try:
    os.chdir('Sources')
except:
    print "Error! Sources doesn't exist!"
    quit()

# Get all filenames in Source directory
dirList = os.listdir(".")

# Check if the prerequisty files exist
print 'Check prerequisties ...'
print ''
for j in range(len(prerequisty_keys)):
    for i in dirList:
        if prerequisty_keys[j] in i:
            print "....", i, 'is found'
            print
            checked[j]= i

# Quit if any prerequisty is missing                       
for j in range(len(prerequisty_keys)):
    if checked[j] == False:
        print '############### Error! #######################'
        print 'Prerequisty is not found!, please visit '+ prerequisties[j]
        print 'Download the ' + prerequisty_keys[j] + ' prerequisty first.'
        raw_input("Press Enter Key to exit")
        exit()
      
# Install PIL
to_install = raw_input("Press Enter Key to Install PIL ... (Enter or y as yes, others as No)")
if to_install =='' or to_install =='Y' or to_install =='y':
    print 'Install PIL ...'
    os.system(checked[0])
else:
    print 'Skip installing PIL'
print

# Install pyserial
to_install = raw_input("Press Enter Key to Install PySerial ... (Enter or y as yes, others as No)")
if to_install =='' or to_install =='Y' or to_install =='y':
    print 'Install pyserial ...'
    os.system(checked[1])
else:
    print 'Skip installing PySerial'    
print

# Install VPython
to_install = raw_input("Press Enter Key to Install VPython ... (Enter or y as yes, others as No)")
if to_install =='' or to_install =='Y' or to_install =='y':
    print 'Install VPython ...'
    os.system(checked[2])
else:
    print 'Skip installing VPython'    
print

#Install ImageMagik
to_install = raw_input("Press Enter Key to Install ImageMagik ... (Enter or y as yes, others as No)")
if to_install =='' or to_install =='Y' or to_install =='y':
    print "....", 'Install ImageMagik ...'
    os.system(checked[4])
else:
    print 'Skip installing ImageMagik' 
print

# Create $HOME\.miicraft and $HOME\.miicraft\output
HOMEPATH = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']
if not os.path.isdir(HOMEPATH+"\\.miicraft"):
    os.mkdir(HOMEPATH+"\\.miicraft")
if not os.path.isdir(HOMEPATH+"\\.miicraft\\output"):    
    os.mkdir(HOMEPATH+"\\.miicraft\\output")

# Create C:\MiiCraft
print "....","Note: The MiiCraft is installed in c:\\MiiCraft\\ as default. You can move the directory to other place."    
MiiCraftPath = "c:\\MiiCraft"+MiiCraft_VER+"\\"
if not os.path.isdir(MiiCraftPath):
    print "....","Create ", MiiCraftPath
    os.mkdir(MiiCraftPath)    

# Copy files to C:\MiiCraft\        
to_install = raw_input("Press Enter Key to Copy files to C:\\MiiCraft\\"+MiiCraft_VER+"... (Enter or y as yes, others as No)")
if to_install =='' or to_install =='Y' or to_install =='y':        
    # Copy files to $HOMEPATH+""\\.miicraft\\" 
    os.system("copy *.py " +MiiCraftPath)
    os.system("copy *.ini "+MiiCraftPath)
    os.system("copy *.gif "+MiiCraftPath)
    os.system("copy *.png "+MiiCraftPath)
    
    os.system("mkdir "+MiiCraftPath+"\\sample")
    os.system("mkdir "+MiiCraftPath+"\\sample\\Eiffel_Tower")
    os.system("mkdir "+MiiCraftPath+"\\sample\\Hexball")
    os.system("copy sample\\*.* "              +MiiCraftPath+"\\sample\\")
    os.system("copy Sample\\Eiffel_Tower\\*.* "+MiiCraftPath+"\\sample\\Eiffel_Tower\\")
    os.system("copy Sample\\Hexball\\*.* "     +MiiCraftPath+"\\sample\\Hexball\\")
else:
    print 'Skip copying files to', MiiCraftPath 
print    

# Check if CorrectRGB_MASK.png exists in c:\miicraft
if not os.path.isfile("C:\\MiiCraft"+MiiCraft_VER+"\\CorrectRGB_MASK.png"):
    print "CorrectRGB_MASK.png is not in C:\\MiiCraft\\"+MiiCraft_VER+", please copy the correspond CorrectRGB_MASK.png to C:\\MiiCraft"+MiiCraft_VER+"\\"
    print 
    
# Install Skeinforge, unzip the skeinforge file to c:\miicraft\skeinforge\
to_install = raw_input("Press Enter Key to Install Skeinforge ... (Enter or y as yes, others as No)")
if to_install =='' or to_install =='Y' or to_install =='y': 
    CWD = os.getcwd() # Setup_CWD\Sources
    print "....","Change from "+CWD+" to "+CWD+MiiCraftPath+"\n"
    os.chdir(MiiCraftPath) 
    
    print "....",'unzip Skeinforge ...'
    dir = 'skeinforge'
    if not os.path.isdir(dir):
        print "....","Create ", dir
        os.mkdir(dir)  
    
    zfobj = zipfile.ZipFile(CWD+"\\"+checked[3])
    for name in zfobj.namelist():
        if name.endswith('/'):
            if not os.path.isdir(os.path.join(dir, name)):
                os.mkdir(os.path.join(dir, name))
        else:
            outfile = open(os.path.join(dir, name), 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()

    raw_input(".... Press Enter Key to bring the Skeinforge Window up, then close the Skeinforge Window. \n")
    
    run_skeinforge = sys.exec_prefix +"\\python.exe " + ".\\skeinforge\\skeinforge_application\\skeinforge.py"
    skeinforge_setting_path = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']+"\\.skeinforge"
    
    os.system(run_skeinforge)
    
    os.chdir(CWD) # return to Setup_CWD\Sources
    print "....","Change from "+MiiCraftPath+" to "+CWD+"\n"
else:
    print 'Skip installing skeinforge' 
print   

os.chdir(Setup_CWD)

print "MiiCraft is installed in", MiiCraftPath
print "Run", MiiCraftPath+"\\MiiCraftSuite_"+".py", "to start.\n"

raw_input("Press Enter Key to finish setup")


  
