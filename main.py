# -*- coding: utf-8 -*-
from container import *
from allContainers import *
from task import *
from winery import *

from tkinter import *
from tkinter.filedialog import *
import csv
import tkinter.messagebox
import os.path
import sqlite3
import time

#intialize items:

robArm = RoboticArm()



#functions:

def openFile():
    adress = askopenfilename()

def saveFile():
    adress = asksaveasfilename()

def mesBox():
    tkinter.messagebox.showinfo("About Us:", "Yehuda Brauner\nElyashiv Miller")

def printCont():
    containers.printFullList()

def refreshConts():
    for cont in containers.listOfContainers:
        print("work")
        subMenu3.add_command(label="print containers", command=printCont)


def print_menu():
    print('=====================')
    print('Menu:')
    print('q - quit')
    print('m - menu')
    print('p - print container list')
    print('1 - start container')
    print('2 - add task to container')
    print('3 - remove container')
    print('4 - move robotic arm')
    print('5 - set robotic arms home position')
    print('6 - start winery')
    print('=====================')


def addCont():
    # gets name and adds container
    num = input('container ID number in winery: ')
    # Todo: check if ID number is valid (from winery.allContainers)
    name = input('name (wine type): ')
    init_priority = input('initial priority: ')
    container = Container(name, num, init_priority)
    containers.addNewContainer(container)
    print('-> container added')


def addTaskToContainer():
    # gets num of container and adds a new task
    containers.printContainersList()
    num = input('container number in winery: ')
    Task.printAllTasks()
    tsk = input('input task: ')
    cont = containers.getContainer(num)
    cont.addTask(tsk)


def removeCont():
    # gets name and removes container
    name = input('name: ')
    success = containers.removeContainer(name)
    if success:
        print('-> container has been removed')


def moveRoboticArm():
    x, y, z = robArm.getPosition()
    print('current location:  X=' + str(x) + ' Y=' + str(y) + ' Z=' + str(z))
    dir = input('Direction? (N=north, E=east, S=south, W=west, U=up, D=down)')
    steps = input('Steps? ' + 'X:(0-' + str(robArm.xBoundaries-1) + ')' + ' Y:(0-' + str(robArm.yBoundaries-1) + ')' + ' Z:(0-' + str(robArm.zBoundaries-1) + ')')
    moved = robArm.move(dir, steps)
    x, y, z = robArm.getPosition()
    if moved:
        print('robot moved to:  X=' + str(x) + ' Y=' + str(y) + ' Z=' + str(z))
    else:
        print('-> out of bounds try again')
        moveRoboticArm()


def setHomePosition():
    x, y, z = robArm.getPosition()
    print('current location:  X=' + str(x) + ' Y=' + str(y) + ' Z=' + str(z))
    robArm.setHomePosition()
    print('-> setting home position to current location...')
    x, y, z = robArm.home.get()
    print('home position set to:  X=' + str(x) + ' Y=' + str(y) + ' Z=' + str(z))


def startWinery():
    winery = Winery()


def case(inp):
    if inp == 'm':
        print_menu()
    elif inp == 'p':
        containers.printFullList()
    elif inp == '1':
        addCont()
    elif inp == '2':
        addTaskToContainer()
    elif inp == '3':
        removeCont()
    elif inp == '4':
        moveRoboticArm()
    elif inp == '5':
        setHomePosition()
    elif inp == '6':
        startWinery()
    else:
        print('-> Wrong input try again')


# --------------------------------------------------------------------------------------------------------
containers = AllContainers()

# if __name__ == '__main__':
#     robArm = RoboticArm()
#     print_menu()
#     while True:
#         inp = input('Input: ')
#         if inp == 'q':
#             break
#         else:
#             case(inp)
#
#     containers.printFullList()






buttons = []


root = Tk()

topFrame = Frame(root, width=1000, height=500)
# bottomFrame = Frame()
topFrame.pack()
# bottomFrame.pack(side=BOTTOM)
global l1
l1=Label(root, text='winery app')
l1.pack()

menu=Menu(root)
root.config(menu=menu)

subMenu1 = Menu(menu)
menu.add_cascade(label="file", menu=subMenu1)
subMenu1.add_command(label="Open text", command=openFile)
subMenu1.add_command(label="Save as", command=saveFile)
subMenu1.add_separator()
subMenu1.add_command(label="XXXXXXXX")
subMenu1.add_command(label="exit", command=exit)

subMenu2 = Menu(menu)
menu.add_cascade(label="actions", menu=subMenu2)
subMenu2.add_command(label="print containers", command=printCont)
subMenu2.add_command(label="add container", command=addCont)
subMenu2.add_command(label="add task", command=addTaskToContainer)
subMenu2.add_command(label="remove container", command=removeCont)
subMenu2.add_command(label="move robotic hand", command=moveRoboticArm)
subMenu2.add_command(label="set home position", command=setHomePosition)
subMenu2.add_command(label="start winery", command=startWinery)

subMenu3=Menu(menu)
menu.add_cascade(label="containers", menu=subMenu3, command=refreshConts)
# here we need to add a button for every container


subMenu4=Menu(menu)
menu.add_cascade(label="help", menu=subMenu4)
subMenu4.add_command(label="About", command=mesBox)



# button1 = Button(topFrame, text='Open simulation', fg='blue')
# button2 = Button(topFrame, text='Close simulation', fg='blue')
# button3 = Button(topFrame, text='Button 3', fg='blue')
# button4 = Button(bottomFrame, text='Button 4', fg='red')

# button1.pack()
# button2.pack()
# button3.pack(side=LEFT)
# button4.pack()

root.mainloop()
