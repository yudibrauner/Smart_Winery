# This class represents a container of wine

import datetime
import random
import tkinter as tk
import matplotlib
matplotlib.use("TKAgg")
import pylab
import os
import time
import threading
import multiprocessing
import tkinter.messagebox
import helpFunctions

import matplotlib.animation as animation
import tkinter.scrolledtext as ScrolledText
import matplotlib.pyplot as plt

from data_generator import *
from sensors import *
from tkinter import *
from tkinter.filedialog import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from logger import *
from tkinter.font import Font
from decider import *

# vars:

NO_DETAILS = "N/A"
SENSORS_INTERVAL = 1
NUM_OF_SENSORS = 6
DEFAULT_TEMPERATURE = 0

# images:
EMPTY_IMAGE = "images/container.png"
FULL_IMAGE = "images/containerAct.png"
EMPTY_CONT_IMAGE = "images/emptyCont.png"
FULL_CONT_IMAGE = "images/fullCont.png"
FINISH_CONT_IMAGE = "images/finishCont.png"
END_PROCESS_IMAGE = "images/EndProcess.png"
SETTINGS_IMAGE = "images/settings.png"
COOLER_IMAGE = "images/cooler.png"
PUMP_IMAGE = "images/stir.png"
SENSE_IMAGE = "images/sense.png"
CONTAINER_IMAGE = "images/new_container.png"

#programs:
SLOW_LIST = ('data\Tannins_slow.txt', 'data\Color_slow.txt', 'data\Density_slow.txt', 'data\Cool_slow.txt', 'data\Temperature_slow.txt', 'data\Pump_slow.txt')
NORMAL_LIST = ('data\Tannins_normal.txt', 'data\Color_normal.txt', 'data\Density_normal.txt', 'data\Cool_normal.txt', 'data\Temperature_normal.txt', 'data\Pump_normal.txt')
FAST_LIST = ('data\Tannins_fast.txt', 'data\Color_fast.txt', 'data\Density_fast.txt', 'data\Cool_fast.txt', 'data\Temperature_fast.txt', 'data\Pump_fast.txt')
PROGRAMS = {'Slow': SLOW_LIST, 'Normal': NORMAL_LIST, 'Fast': FAST_LIST, 'Create a new ferm.': 'new'}
LOGTYPES = {'Short log': 'short', 'Long log': 'long', 'Both': 'both'}

# rates:
COLOR_QUALITY = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5}
COLOR_POWER = {'2': 2, '4': 4, '6': 6, '8': 8, '10': 10}
SMELL_OZ = {'2': 2, '4': 4, '6': 6, '7': 7, '8': 8}
SMELL_SOURCE = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6}
SMELL_QUALITY = {'8': 8, '10': 10, '12': 12, '14': 14, '16': 16}
TASTE_OZ = {'2': 2, '4': 4, '6': 6, '7': 7, '8': 8}
TASTE_SOURCE = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6}
TASTE_QUALITY = {'10': 10, '13': 13, '16': 16, '19': 19, '22': 22}
TASTE_SHIUR = {'4': 4, '5': 5, '6': 6, '7': 7, '8': 8}
GENERAL_RATE = {'7': 7, '8': 8, '9': 9, '10': 10, '11': 11}

# arrays:
SENSORS = ('Tannins', 'Color', 'Density', 'Cool')
SENSOR_NAMES = ["tannins", "color", "density", "temperature"]
COUNTER_NAMES = ['cool', 'pump']
ALL_ATTR_NAMES = ['tannins', 'color', 'density', 'temperature', 'cool', 'pump']
HEIGHTS = ['top', 'mid', 'bot']
# plt.style.use('fivethirtyeight')

# colors:
BACKGROUND = '#37474f'
CONT_NAME_BG = '#78909C'
ATTRS_BG = '#E0E0E0'
EXPECTEDLINECOLOR = '#00A3E0'
OBSERVEDLINECOLOR = '#183A54'
REALDATALINECOLOR = '#D3D3D3'
FONTITLECOLOR = '#FFD966'

class Container:
    def __init__(self, _id, _place, root, interval, externalDB):
        self.id = _id            # number of container in winery
        self.frame = root
        self.specFrame = LabelFrame(self.frame, bg=BACKGROUND, width=139, height=116)
        self.tasks = list()
        self.listsAndDicts = {'sensorNames': SENSOR_NAMES, 'counterNames': COUNTER_NAMES, 'heights': HEIGHTS, 'attrNames': ALL_ATTR_NAMES}
        self.coolCounterGlobal, self.coolCounter = 0, 0
        self.pumpCounterGlobal, self.pumpCounter = 0, 0
        self.newImage = PhotoImage(file=EMPTY_CONT_IMAGE)
        self.interval = interval
        self.animationInterval = interval * 1000
        self.initStringVars()
        self.buttonFunction = self.addCont
        self.isFull = False
        self.place = _place
        self.initNones()
        self.initLabels()
        self.initGraphs()
        self.initParams()
        self.frame.grid(row=0, column=0, columnspan=2)
        self.showingLog = self.shortLogger
        self.containerDB = []
        self.exDB = externalDB
        self.endDateTime = ''

    def initStringVars(self):
        self.temperature = StringVar()
        self.cool = StringVar()
        self.tannins = StringVar()
        self.color = StringVar()
        self.density = StringVar()
        self.realCool = StringVar()
        self.realTemperature = StringVar()
        self.realTannins = StringVar()
        self.realColor = StringVar()
        self.realDensity = StringVar()
        self.initDictVars()
        self.name = StringVar()
        self.program = StringVar()
        self.logTypes = StringVar()
        self.time = StringVar()
        self.date = StringVar()
        self.numOfCools = 0
        self.numOfRegulations = 0
        self.numOfSensors = NUM_OF_SENSORS
        self.sensorsInterval = SENSORS_INTERVAL
        self.topColor = StringVar()
        self.howersFromStart = StringVar()

    def initDictVars(self):
        # te1 = StringVar(value=NO_DETAILS)
        # te2 = StringVar(value=NO_DETAILS)
        # te3 = StringVar(value=NO_DETAILS)
        # ta1 = StringVar(value=NO_DETAILS)
        # ta2 = StringVar(value=NO_DETAILS)
        # ta3 = StringVar(value=NO_DETAILS)
        # d1 = StringVar(value=NO_DETAILS)
        # d2 = StringVar(value=NO_DETAILS)
        # d3 = StringVar(value=NO_DETAILS)
        # c1 = StringVar(value=NO_DETAILS)
        # c2 = StringVar(value=NO_DETAILS)
        # c3 = StringVar(value=NO_DETAILS)
        # cool = StringVar(value=NO_DETAILS)
        # pump = StringVar(value=NO_DETAILS)
        # dictTemerature = {'top': te1,'mid': te2, 'bot': te3}
        # dictTannins = {'top': ta1,'mid': ta2, 'bot': ta3}
        # dictColor = {'top': c1,'mid': c2, 'bot': c3}
        # dictDensity = {'top': d1,'mid': d2, 'bot': d3}
        # dictCool = {'center': cool}
        # dictPump = {'center': pump}
        self.senseDictParams = {}
        self.realDictParams = {}
        self.expectedDictParams = {}
        for sensorName in SENSOR_NAMES:
            self.senseDictParams[sensorName] = {}
            self.realDictParams[sensorName] = {}
            self.expectedDictParams[sensorName] = StringVar(value=NO_DETAILS)
            for height in HEIGHTS:
                self.senseDictParams[sensorName][height] = StringVar(value=NO_DETAILS)
                self.realDictParams[sensorName][height] = StringVar(value=NO_DETAILS)
        for counterName in COUNTER_NAMES:
            self.senseDictParams[counterName] = StringVar(value=NO_DETAILS)
            self.realDictParams[counterName] = StringVar(value=NO_DETAILS)
            self.expectedDictParams[counterName] = StringVar(value=NO_DETAILS)
        # self.senseDictParams = {'density': dictDensity, 'color': dictColor, 'tannins': dictTannins,
        #                    'temperature': dictTemerature, 'cool': dictCool, 'pump': dictPump}
        # self.realDictParams = {'density': dictDensity, 'color': dictColor, 'tannins': dictTannins,
        #                        'temperature': dictTemerature, 'cool': dictCool, 'pump': dictPump}

    def initNones(self):
        self.image = None
        self.photo = None
        self.end_process_photo = None
        self.dynamic_data = None
        self.wine_data = None
        self.sensors_data = None
        self.generator = None
        self.logger = None
        self.logger_name = None
        self.shortLogger = None
        self.shortLogger_name = None
        self.generator_thread = None
        self.decider = None
        self.text_handler = None
        # self.st = ScrolledText.ScrolledText(wrap=tk.WORD, width=45, height=20)
        # self.st.configure(font='TkFixedFont')
        # self.st.grid(column=0, row=1, sticky='w', columnspan=10)
        self.rootCont = None

    def initLabels(self):
        self.densityLabel = None
        self.idLabel = None
        self.nameLabel = None
        self.densityValLabel = None
        self.tanninsValLabel = None
        self.colorValLabel = None
        self.coolValLabel = None
        self.expectedDensityLabel = None
        self.expectedTanninsLabel = None
        self.expectedColorLabel = None
        self.expectedCoolLabel = None

    def initGraphs(self):
        self.graph_plot = Figure(figsize=(4, 8), dpi=70)
        self.sub_plot_221 = self.graph_plot.add_subplot(411)
        self.sub_plot_222 = self.graph_plot.add_subplot(412)
        self.sub_plot_223 = self.graph_plot.add_subplot(413)
        self.sub_plot_224 = self.graph_plot.add_subplot(414)
        self.sub_plot_221.title.set_text('Tannins')
        self.sub_plot_222.set_title('Color')
        self.sub_plot_223.set_title('Density')
        self.sub_plot_224.set_title('Cool')
        self.data_221 = None
        self.data_222 = None
        self.data_223 = None
        self.data_224 = None
        self.ani221 = None
        self.ani222 = None
        self.ani223 = None
        self.ani224 = None
        self.data_221_new = None

    def setImage(self):
        self.photo = PhotoImage(file=self.image)
        # contButton = Button(self.frame, height=44, width=52, image=self.photo, relief=FLAT, background=BACKGROUND, command=self.buttonFunction)
        # contButton.place(x=self.place[0], y=self.place[1])
        newContButton = Button(self.specFrame, height=106, width=129, image=self.photo, relief=FLAT, background=BACKGROUND, command=self.buttonFunction)
        self.specFrame.place(x=self.place[0], y=self.place[1])
        newContButton.place(x=0, y=0)

    def startLabels(self):
        nameFont = Font(family="Times New Roman", size=13, weight='bold')
        labelFont = Font(family="Times New Roman", size=6)
        # self.idLabel = Label(self.specFrame, text=str(self.id) + ': ', background=BACKGROUND)
        # self.idLabel.place(x=self.place[0] + 10, y=self.place[1] - 30)
        self.nameLabel = Label(self.specFrame, textvariable=str(self.name), font=nameFont, background=CONT_NAME_BG)
        self.nameLabel.place(x=70 - 10*len(self.name.get())/2, y=83)
        self.coolValLabel = Label(self.specFrame, textvariable=str(self.senseDictParams['cool']), background=ATTRS_BG, font=labelFont)
        # self.coolValLabel = Label(self.specFrame, textvariable=str(self.realCool), background=ATTRS_BG, font=labelFont)
        self.coolValLabel.place(x=75, y=23)
        self.densityValLabel = Label(self.specFrame, textvariable=str(self.getSenseAttr('density', 'top')), background=ATTRS_BG, font=labelFont)
        # self.densityValLabel = Label(self.specFrame, textvariable=str(self.realDensity), background=ATTRS_BG, font=labelFont)
        self.densityValLabel.place(x=75, y=60)
        self.tanninsValLabel = Label(self.specFrame, textvariable=str(self.getSenseAttr('tannins', 'top')), background=ATTRS_BG, font=labelFont)
        # self.tanninsValLabel = Label(self.specFrame, textvariable=str(self.realTannins), background=ATTRS_BG, font=labelFont)
        self.tanninsValLabel.place(x=75, y=48)
        self.colorValLabel = Label(self.specFrame, textvariable=str(self.getSenseAttr('color', 'top')), background=ATTRS_BG, font=labelFont)
        # self.colorValLabel = Label(self.specFrame, textvariable=str(self.realColor), background=ATTRS_BG, font=labelFont)
        self.colorValLabel.place(x=75, y=35)
        self.end_process_photo = PhotoImage(file=END_PROCESS_IMAGE)
        self.settingPhoto = PhotoImage(file=SETTINGS_IMAGE)
        self.coolPhoto = PhotoImage(file=COOLER_IMAGE)
        self.pumpPhoto = PhotoImage(file=PUMP_IMAGE)
        self.sensePhoto = PhotoImage(file=SENSE_IMAGE)
        self.containerPhoto = PhotoImage(file=CONTAINER_IMAGE)

    def initParams(self):
        self.cool.set(NO_DETAILS)                # generator data
        self.tannins.set(NO_DETAILS)             # generator data
        self.color.set(NO_DETAILS)               # generator data
        self.density.set(NO_DETAILS)             # generator data
        self.temperature.set(NO_DETAILS)         # generator data
        self.realTemperature.set(NO_DETAILS)     # sensor data
        self.realCool.set("0")                   # sensor data
        self.realTannins.set(NO_DETAILS)         # sensor data
        self.realColor.set(NO_DETAILS)           # sensor data
        self.realDensity.set(NO_DETAILS)         # sensor data
        self.name.set(NO_DETAILS)
        self.time.set(NO_DETAILS)
        self.date.set(NO_DETAILS)
        self.logTypes.set('Short log')
        self.program.set('No Program')
        self.image = EMPTY_CONT_IMAGE
        self.setImage()
        self.howersFromStart.set('0')

    def fillContainer(self):
        #self.updateParams()
        self.isFull = True
        self.image = FULL_CONT_IMAGE
        self.buttonFunction = self.showDetails
        self.setImage()
        self.startLabels()

    def addDetails(self, rootCont, nameEntry, numSensorsEntry, intervalSensorsEntry):
        name = nameEntry.get()
        numSensors = numSensorsEntry#.get()
        intervalSensors = intervalSensorsEntry#.get()
        program = self.program.get()
        if program == 'Create a new ferm.':
            self.createNewProg()
        elif program == 'No Program':
            self.mesBox("Please choose a program.", "")
        elif name == "":
            self.mesBox("Please enter the wine's name.", "")
        else:
            if numSensors == "":
                numSensors = NUM_OF_SENSORS
            if intervalSensors == "":
                intervalSensors = SENSORS_INTERVAL
            self.numOfSensors = int(numSensors)
            self.sensorsInterval = int(intervalSensors)
            self.name.set(name)
            # Configure logger
            self.logger_name = str(self.name.get()) + '_' + str(self.id)
            self.shortLogger_name = 'S_' + str(self.name.get()) + '_' + str(self.id)
            self.startDateTime = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
            # Add the handler to logger
            self.setup_logger(str(self.logger_name), 'logs/longLogs/' + str(self.logger_name) + '.log')
            self.logger = logging.getLogger(self.logger_name)
            # self.logger = logging.getLogger(self.logger_name)
            # logging.basicConfig(filename='logs/longLogs/' + self.logger_name + '.log',
            #                     level=logging.INFO,
            #                     format='%(asctime)s - %(levelname)s - %(message)s')
            self.logger.info('-> container added')

            # Add the handler to logger
            self.setup_logger(str(self.shortLogger_name), 'logs/shortLogs/' + str(self.shortLogger_name) + '.log')
            self.shortLogger = logging.getLogger(self.shortLogger_name)            # self.shortLogger = logging.getLogger(self.shortLogger_name)
            # logging.basicConfig(filename='logs/shortLogs/' + self.shortLogger_name + '.log',
            #                     level=logging.INFO,
            #                     format='%(asctime)s - %(levelname)s - %(message)s')
            self.shortLogger.info('-> container added')
            self.fillContainer()
            self.buttonFunction = self.showDetails
            self.data_221 = PROGRAMS[program][0]
            self.data_222 = PROGRAMS[program][1]
            self.data_223 = PROGRAMS[program][2]
            self.data_224 = PROGRAMS[program][3]
            self.dynamic_data = 'data/dynamic_data/'
            self.wine_data = self.dynamic_data + 'generator/' + str(self.id) + '_' + str(self.name.get())
            self.sensors_data = self.dynamic_data + 'sensors/' + str(self.id) + '_' + str(self.name.get())
            self.generator = DataGenerator(self, self.wine_data, self.program.get(), PROGRAMS[self.program.get()], self.interval, self.logger)
            self.generator_thread = threading.Thread(target=self.generator.start_generating, daemon=True)
            self.generator_thread.start()
            self.sensors = Sensors(self, self.logger)#, self.generator, self.sensors_data)
            rootCont.destroy()

    def createNewProg(self):
        self.mesBox('TODO IT', '')

    def addCont(self):
        self.rootCont = Toplevel()
        self.rootCont.wm_title("Adding container " + str(self.id))
        contFrame = Frame(self.rootCont, width=270, height=450)
        contFrame.pack()

        Label(contFrame, text='Name (wine type): ').place(x=40, y=20)
        nameEntry = Entry(contFrame)
        nameEntry.place(x=40, y=50)

        Label(contFrame, text='Fermentation Program: ').place(x=40, y=80)
        programEntry = OptionMenu(contFrame, self.program, *PROGRAMS.keys())
        programEntry.place(x=40, y=100)

        # Label(contFrame, text='Number of sensors in cluster:').place(x=40, y=140)
        # numSensorsEntry = Entry(contFrame)
        # numSensorsEntry.place(x=40, y=170)
        # numSensorsEntry.insert(0, str(NUM_OF_SENSORS))
        #
        # Label(contFrame, text='Sensors reading interval [sec]:').place(x=40, y=200)
        # intervalSensorsEntry = Entry(contFrame)
        # intervalSensorsEntry.place(x=40, y=230)
        # intervalSensorsEntry.insert(0, '5')
        numOfSensors = NUM_OF_SENSORS
        intervalSensors = SENSORS_INTERVAL
        insertButton = Button(contFrame, text='Start Fermentation', command=lambda: self.addDetails(self.rootCont, nameEntry, numOfSensors, intervalSensors))
        insertButton.place(x=40, y=400)

    def fermIsFinished(self):
        self.image = FINISH_CONT_IMAGE
        self.endDateTime = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
        self.setImage()
        self.tannins.set(NO_DETAILS)
        self.cool.set(NO_DETAILS)
        self.density.set(NO_DETAILS)
        self.color.set(NO_DETAILS)
        self.temperature.set(NO_DETAILS)
        self.initDictVars()
        # helpFunctions.sendMail(self.name.get() + " in container " + str(self.id) + " is finished")

    def clearAllVariables(self, rootCont):
        new_container = Container(self.id, self.place, self.frame, self.interval, self.exDB)
        # TODO: add this new container to allContainers from main and remove previous container from there.
        # swapNewForOldContainer(self.id, new_container)
        self.cool.set(None)
        self.tannins.set(None)
        self.color.set(None)
        self.density.set(None)
        self.temperature.set(None)
        self.realTemperature.set(None)
        self.realCool.set(None)
        self.realTannins.set(None)
        self.realColor.set(None)
        self.realDensity.set(None)
        self.initDictVars()
        self.time.set(None)
        self.date.set(None)
        # TODO: what are these things?
        # self.idLabel.place_forget()
        # self.nameLabel.place_forget()
        # self.coolValLabel.place_forget()
        # self.tanninsValLabel.place_forget()
        # self.colorValLabel.place_forget()
        # self.densityValLabel.place_forget()
        self.logger = None
        self.generator.stay_alive = False
        rootCont.destroy()

    def settingsProcess(self, rootCont):
        rootCont = Tk()
        # self.rootCont = Toplevel()
        # self.rootCont.wm_title("Settings")
        settingsFrame = Frame(rootCont, width=270, height=300)
        settingsFrame.pack()
        Label(settingsFrame, text='Set sensors reading interval [sec]:').place(x=40, y=20)
        intervalSensorsEntry = Entry(settingsFrame)
        intervalSensorsEntry.place(x=40, y=50)
        intervalSensorsEntry.insert(0, str(self.sensorsInterval))
    # TODO: we need to see the name of the chosen log
        Label(settingsFrame, text='Log Type: ').place(x=40, y=80)
        logTypeEntry = OptionMenu(settingsFrame, self.logTypes, *LOGTYPES.keys())
        logTypeEntry.place(x=40, y=100)

        openLogButton = Button(settingsFrame, text='Open this log file',
                              command=lambda: self.openLog())
        openLogButton.place(x=40, y=150)

        insertButton = Button(settingsFrame, text='Set', command=lambda: self.changeDetails(rootCont, intervalSensorsEntry))
        insertButton.place(x=40, y=250)

    def openLog(self):
        logType = self.logTypes.get()
        if logType == 'Short log':
            os.startfile('logs/shortLogs/' + str(self.shortLogger_name) + '.log', 'open')
        #TODO

    def changeDetails(self, rootCont, intervalSensorsEntry):
        intervalSensors = intervalSensorsEntry.get()
        logEntry = self.logTypes.get()
        if str(logEntry) == 'Short log':
            self.logger.removeHandler(self.text_handler)
            self.shortLogger.addHandler(self.text_handler)
        elif str(logEntry) == 'Long log':
            self.logger.addHandler(self.text_handler)
            self.shortLogger.removeHandler(self.text_handler)
        elif str(logEntry) == 'Both':
            self.logger.addHandler(self.text_handler)
            self.shortLogger.addHandler(self.text_handler)

        if intervalSensors != '':
            self.sensorsInterval = int(intervalSensors)
            self.sensors.setSensorsInterval()
            self.shortLogger.info('Sensors Interval Changed to ' + str(self.sensorsInterval))
            rootCont.destroy()
        else:
            msgBox = messagebox.showwarning(title='Interval Missing', message='Please add interval')

    def endProcess(self, rootCont):
        msgBox = messagebox.askyesno('End Process ' + str(self.id) + ': ' + str(self.name.get()), 'Are you sure you want to end this process?', master=rootCont)
        if msgBox:
            self.logger.info('-> End of Process')
            self.logger.handlers = []
            self.generator.updateLogger(self.logger)

            self.rootCont = Toplevel()
            self.rootCont.wm_title("Rate The Wine")
            rateFrame = Frame(self.rootCont, width=600, height=500)
            rateFrame.pack()
            self.initRates()

            showFrame = LabelFrame(self.rootCont, width=500, height=80, text="Appearance")
            showFrame.place(x=20, y=20)
            Label(showFrame, text='Color quality').place(x=10, y=10)
            CQEntry = OptionMenu(showFrame, self.rates[0], *COLOR_QUALITY.keys())
            CQEntry.place(x=100, y=10)
            Label(showFrame, text='Color strength').place(x=260, y=10)
            CPEntry = OptionMenu(showFrame, self.rates[1], *COLOR_POWER.keys())
            CPEntry.place(x=350, y=10)
            smellFrame = LabelFrame(self.rootCont, width=500, height=80, text="Fragrance")
            smellFrame.place(x=20, y=120)
            Label(smellFrame, text='Centralization').place(x=10, y=10)
            SOEntry = OptionMenu(smellFrame, self.rates[2], *SMELL_OZ.keys())
            SOEntry.place(x=60, y=10)
            Label(smellFrame, text='Originality').place(x=150, y=10)
            SSEntry = OptionMenu(smellFrame, self.rates[3], *SMELL_SOURCE.keys())
            SSEntry.place(x=200, y=10)
            Label(smellFrame, text='Quality').place(x=290, y=10)
            SQEntry = OptionMenu(smellFrame, self.rates[4], *SMELL_QUALITY.keys())
            SQEntry.place(x=340, y=10)

            tasteFrame = LabelFrame(self.rootCont, width=500, height=80, text="Flavor")
            tasteFrame.place(x=20, y=220)
            Label(tasteFrame, text='Centralization').place(x=20, y=3)
            TOEntry = OptionMenu(tasteFrame, self.rates[5], *TASTE_OZ.keys())
            TOEntry.place(x=20, y=25)
            Label(tasteFrame, text='Originality').place(x=120, y=3)
            TSEntry = OptionMenu(tasteFrame, self.rates[6], *TASTE_SOURCE.keys())
            TSEntry.place(x=120, y=25)
            Label(tasteFrame, text='Quality').place(x=220, y=3)
            TQEntry = OptionMenu(tasteFrame, self.rates[7], *TASTE_QUALITY.keys())
            TQEntry.place(x=220, y=25)
            Label(tasteFrame, text='Residual').place(x=320, y=3)
            THEntry = OptionMenu(tasteFrame, self.rates[8], *TASTE_SHIUR.keys())
            THEntry.place(x=320, y=25)

            generalFrame = LabelFrame(self.rootCont, width=500, height=80, text="General Evaluation")
            generalFrame.place(x=20, y=320)
            Label(generalFrame, text='General ranking').place(x=20, y=20)
            GEntry = OptionMenu(generalFrame, self.rates[9], *GENERAL_RATE.keys())
            GEntry.place(x=100, y=20)
            Label(generalFrame, text='Notes:').place(x=200, y=20)
            scoreEntry = Entry(generalFrame)
            scoreEntry.place(x=300, y=20)

            Label(rateFrame, text='Vintner:').place(x=20, y=420)
            nameEntry = Entry(rateFrame)
            nameEntry.place(x=80, y=420)
            if self.endDateTime == '':
                self.endDateTime = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
            def isFullFields(self):
                for rate in self.rates:
                    if rate.get() == 'No Rate':
                        return False
                return True

            def calculateScore(self):
                sum = 0
                for rate in self.rates:
                    sum += int(rate.get())
                return sum

            def addToDataBase(rootCont):
                if nameEntry.get() and isFullFields(self):
                    calc = calculateScore(self)
                    line_to_DB = {"Container id": self.id, "Fermentation": self.program.get(),
                                  "Wine name": self.name.get(), "Mistakes": 0, "Score": calc,
                                  "Start": self.startDateTime, "End": self.endDateTime,
                                  "C: Quality": int(self.rates[0].get()), "C: Strength": int(self.rates[1].get()),
                                  "S: Centralization": int(self.rates[2].get()), "S: Originality": int(self.rates[3].get()), "S: Quality": int(self.rates[4].get()),
                                  "T: Centralization": int(self.rates[5].get()), "T: Originality": int(self.rates[6].get()),
                                  "T: Quality": int(self.rates[7].get()), "T: Residual": int(self.rates[8].get()),
                                  "General ranking": int(self.rates[9].get()), "Note": scoreEntry.get(), "Vintner": nameEntry.get()
                                  }
                    # print('Adding score and process to DB: ' + str(calc) + ' + ' + str(self.generator.file))
                    self.exDB['general'].append(line_to_DB)
                    new_dict = {'id': self.id, 'name': self.name.get(), 'log': self.containerDB}
                    self.exDB['containers'].append(new_dict)
                    rootCont.destroy()
                    self.id = NO_DETAILS
                    self.name.set(None)
                else:
                    self.mesBox('You did not fill all the fields', 'Try Again')
            saveButton = Button(rateFrame, text='Save', command=lambda: addToDataBase(self.rootCont))
            saveButton.place(x=200, y=450)
            dontSaveButton = Button(rateFrame, text='Don\'t Save', command=self.rootCont.destroy)
            dontSaveButton.place(x=300, y=450)
            self.clearAllVariables(rootCont)

    def initRates(self):
        self.rates = []
        for i in range(0, 10):
            self.rates.append(StringVar())
            self.rates[i].set('No Rate')
            self.rates[i].set('5')

    def showDetails(self):
        self.rootCont = Toplevel()
        self.rootCont.wm_title("Container " + str(self.id) + ': ' + str(self.name.get()))
        # FRAMES:
        contFrameMain = Frame(self.rootCont, width=1400, height=730, bg='#37474f')
        contFrameMain.pack()
        titleFont = Font(family="Times New Roman", size=30)
        Label(contFrameMain, text=self.name.get(), background=BACKGROUND, font=titleFont, fg=FONTITLECOLOR).place(x=630, y=10)
        subTitleFont = Font(family="Times New Roman", size=15)
        Label(contFrameMain, text=self.program.get(), background=BACKGROUND, font=subTitleFont, fg=FONTITLECOLOR).place(x=650, y=60)

        containerImageLabel = Label(contFrameMain, width=500, height=555, image=self.containerPhoto, background=None)
        containerImageLabel.place(x=470, y=110)
        bigLabelsFont = Font(family="Times New Roman", size=14, weight='bold')
        top_up = 120
        top_under = 155
        mid_up = 250
        mid_under = 285
        bot_up = 390
        bot_under = 425
        left = 110
        right = 390
        under_line = 470
        # TODO: they disapear, maybe as a result of the posting on a label and not on a frame?
        self.color_top_label = Label(containerImageLabel, textvariable=str(self.senseDictParams['color']['top']), font=bigLabelsFont, fg='black')
        self.color_top_label.place(x=left, y=top_under)
        self.color_mid_label = Label(containerImageLabel, textvariable=str(self.senseDictParams['color']['mid']), font=bigLabelsFont, fg='black')
        self.color_mid_label.place(x=left, y=mid_under)
        self.color_bot_label = Label(containerImageLabel, textvariable=str(self.senseDictParams['color']['bot']), font=bigLabelsFont, fg='black')
        self.color_bot_label.place(x=left, y=bot_under)
        self.density_top_label = Label(containerImageLabel, textvariable=str(self.senseDictParams['density']['top']), font=bigLabelsFont, fg='black')
        self.density_top_label.place(x=left, y=top_up)
        self.density_mid_label = Label(containerImageLabel, textvariable=str(self.senseDictParams['density']['mid']), font=bigLabelsFont, fg='black')
        self.density_mid_label.place(x=left, y=mid_up)
        self.density_bot_label = Label(containerImageLabel, textvariable=str(self.senseDictParams['density']['bot']), font=bigLabelsFont, fg='black')
        self.density_bot_label.place(x=left, y=bot_up)
        self.temperature_top_label = Label(containerImageLabel, textvariable=str(self.senseDictParams['temperature']['top']), font=bigLabelsFont, fg='black')
        self.temperature_top_label.place(x=right, y=top_up)
        self.temperature_mid_label = Label(containerImageLabel, textvariable=str(self.senseDictParams['temperature']['mid']), font=bigLabelsFont, fg='black')
        self.temperature_mid_label.place(x=right, y=mid_up)
        self.temperature_bot_label = Label(containerImageLabel, textvariable=str(self.senseDictParams['temperature']['bot']), font=bigLabelsFont, fg='black')
        self.temperature_bot_label.place(x=right, y=bot_up)
        self.tannins_top_label = Label(containerImageLabel, textvariable=str(self.senseDictParams['tannins']['top']), font=bigLabelsFont, fg='black')
        self.tannins_top_label.place(x=right, y=top_under)
        self.tannins_mid_label = Label(containerImageLabel, textvariable=str(self.senseDictParams['tannins']['mid']), font=bigLabelsFont, fg='black')
        self.tannins_mid_label.place(x=right, y=mid_under)
        self.tannins_bot_label = Label(containerImageLabel, textvariable=str(self.senseDictParams['tannins']['bot']), font=bigLabelsFont, fg='black')
        self.tannins_bot_label.place(x=right, y=bot_under)
        self.cool_label = Label(containerImageLabel, textvariable=str(self.senseDictParams['cool']), font=bigLabelsFont, fg='black')
        self.cool_label.place(x=right, y=under_line)
        self.pump_label = Label(containerImageLabel, textvariable=str(self.senseDictParams['pump']), font=bigLabelsFont, fg='black')
        self.pump_label.place(x=left, y=under_line)

        # Graphs frame
        contFrameGraphs = Frame(contFrameMain, width=700, height=535)
        contFrameGraphs.place(x=1000, y=110)

        upContFrameLog = Frame(contFrameMain, width=385, height=300, background=CONT_NAME_BG)
        upContFrameLog.place(x=60, y=350)
        labelsFont = Font(family="Times New Roman", size=20)
        Label(upContFrameLog, text='Process Log', background=CONT_NAME_BG, font=labelsFont, fg='black').place(x=130, y=7)
        contFrameLog = Frame(upContFrameLog, width=385, height=250)
        contFrameLog.pack(fill='both', expand='yes')

        # Add text widget to display logging info
        self.st = ScrolledText.ScrolledText(contFrameLog, wrap=tk.WORD, width=45, height=20)
        self.st.configure(font='TkFixedFont')
        self.st.grid(column=0, row=1, sticky='w', columnspan=10)

        # Create textLogger
        self.text_handler = TextHandler(self.st)
        #self.logger.addHandler(self.text_handler)
        self.shortLogger.addHandler(self.text_handler)

        upContFrameDetails = Frame(contFrameMain, width=270, height=220, background=CONT_NAME_BG)
        upContFrameDetails.place(x=175, y=110)
        Label(upContFrameDetails, textvariable=str(self.time), background=CONT_NAME_BG, font=labelsFont, fg='black').place(x=10, y=5)
        Label(upContFrameDetails, textvariable=str(self.date), background=CONT_NAME_BG, font=labelsFont, fg='black').place(x=150, y=5)
        contFrameExpectedDetails = Frame(upContFrameDetails, width=270, height=180)
        contFrameExpectedDetails.place(x=0, y=40)

        Label(contFrameExpectedDetails, text='Density:').place(x=5, y=10)
        self.expectedDensityLabel = Label(contFrameExpectedDetails, textvariable=str(self.getExpectedAttr('density')))
        self.expectedDensityLabel.place(x=80, y=10)
        Label(contFrameExpectedDetails, text='Tannins:').place(x=5, y=35)
        self.expectedTanninsLabel = Label(contFrameExpectedDetails, textvariable=str(self.getExpectedAttr('tannins')))
        self.expectedTanninsLabel.place(x=80, y=35)
        Label(contFrameExpectedDetails, text='Color:').place(x=5, y=60)
        self.expectedColorLabel = Label(contFrameExpectedDetails, textvariable=str(self.getExpectedAttr('color')))
        self.expectedColorLabel.place(x=80, y=60)
        Label(contFrameExpectedDetails, text='Temperature:').place(x=5, y=85)
        self.expectedTemperatureLabel = Label(contFrameExpectedDetails, textvariable=str(self.getExpectedAttr('temperature')))
        self.expectedTemperatureLabel.place(x=80, y=85)
        Label(contFrameExpectedDetails, text='Cool acts:').place(x=5, y=110)
        self.expectedCoolLabel = Label(contFrameExpectedDetails, textvariable=str(self.getExpectedAttr('cool')))
        self.expectedCoolLabel.place(x=80, y=110)
        Label(contFrameExpectedDetails, text='Pump acts:').place(x=5, y=135)
        self.expectedPumpLabel = Label(contFrameExpectedDetails, textvariable=str(self.getExpectedAttr('pump')))
        self.expectedPumpLabel.place(x=80, y=135)
        Label(contFrameExpectedDetails, text='Howers left:').place(x=5, y=160)
        self.expectedPumpLabel = Label(contFrameExpectedDetails, textvariable=str(self.howersFromStart))
        self.expectedPumpLabel.place(x=80, y=160)

        Button(contFrameMain, image=self.end_process_photo, command=lambda: self.endProcess(self.rootCont)).place(x=63, y=110)
        Button(contFrameMain, image=self.settingPhoto, command=lambda: self.settingsProcess(self.rootCont)).place(x=63, y=210)
        Button(contFrameMain, image=self.sensePhoto, command=lambda: self.sensors.readData()).place(x=120, y=210)
        Button(contFrameMain, image=self.coolPhoto, command=self.coolIt).place(x=63, y=280)
        Button(contFrameMain, image=self.pumpPhoto, command=self.pumpIt).place(x=120, y=280)

        canvas = FigureCanvasTkAgg(self.graph_plot, contFrameGraphs)
        canvas.get_tk_widget().pack(side=tk.LEFT, expand=True)
        self.ani221 = animation.FuncAnimation(self.graph_plot, self.animate, fargs=(self.sub_plot_221, self.data_221, 1), interval=self.animationInterval)
        self.ani222 = animation.FuncAnimation(self.graph_plot, self.animate, fargs=(self.sub_plot_222, self.data_222, 2), interval=self.animationInterval)
        self.ani223 = animation.FuncAnimation(self.graph_plot, self.animate, fargs=(self.sub_plot_223, self.data_223, 3), interval=self.animationInterval)
        self.ani224 = animation.FuncAnimation(self.graph_plot, self.animate, fargs=(self.sub_plot_224, self.data_224, 4), interval=self.animationInterval)

        def onExit():
            self.logger.removeHandler(self.text_handler)
            self.rootCont.destroy()
        self.rootCont.protocol('WM_DELETE_WINDOW', onExit)  # root is your root window

        self.rootCont.bind('<Escape>', lambda e: onExit())       # you can press escape to exit this frame

    def animate(self, i, sub_plot, data, sensor_type_index):         # sensor_type_index=index for parsing from generated data
        pullData = open(data, 'r').read()
        dataList = pullData.split('\n')
        xList = []
        yList = []
        for eachLine in dataList:
            if len(eachLine) > 1:
                x, y = eachLine.split(' ')
                xList.append(float(x))
                yList.append(float(y))

        pullDynamicData = open(self.sensors_data, 'r').read()
        dynamicdataList = pullDynamicData.split('\n')
        xdynList = []
        ydynList = []
        for eachLine in dynamicdataList:
            if len(eachLine) > 1:
                parts = eachLine.split(' ')
                xdynList.append(float(parts[0]))
                ydynList.append(float(parts[sensor_type_index]))

        pullDynamicRealData = open(self.wine_data, 'r').read()
        dynamicRealdataList = pullDynamicRealData.split('\n')
        xdynRealList = []
        ydynRealList = []
        for eachLine in dynamicRealdataList:
            if len(eachLine) > 1:
                parts = eachLine.split(' ')
                xdynRealList.append(float(parts[0]))
                ydynRealList.append(float(parts[sensor_type_index]))

        sub_plot.clear()
        sub_plot.set_title(SENSORS[sensor_type_index-1])
        self.graph_plot.subplots_adjust(hspace=.5)
        sub_plot.plot(xList, yList, EXPECTEDLINECOLOR)#, label='Expected')
        sub_plot.plot(xdynList, ydynList, OBSERVEDLINECOLOR)#, label='Observed')
        sub_plot.plot(xdynRealList, ydynRealList, REALDATALINECOLOR)
        sub_plot.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=5)

#DB parts
    #in the end of the fermentation we will have a "matrix" of all the ferm, and we'll be able to add it to DB
    def add2matrix(self):
        if self.get_SenseAttr('temperature', 'bot') == 'N/A':
            return
        dateTime = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
        vector = {"howers from start": float(self.howersFromStart.get()),
                  "expected tannins": float(self.get_ExpectedAttr('tannins')), "expected color": float(self.get_ExpectedAttr('color')),
                  "expected temperature": float(self.get_ExpectedAttr('temperature')),"expected density": float(self.get_ExpectedAttr('density')),
                  "expected cool acts": float(self.get_ExpectedAttr('cool')),"expected pump acts": float(self.get_ExpectedAttr('pump')),
                  "top tannins sensor": float(self.get_SenseAttr('tannins', 'top')),"middle tannins sensor": float(self.get_SenseAttr('tannins', 'mid')),
                  "bottom tannins sensor": float(self.get_SenseAttr('tannins', 'bot')),"top color sensor": float(self.get_SenseAttr('color', 'top')),
                  "middle color sensor": float(self.get_SenseAttr('color', 'mid')),"bottom color sensor": float(self.get_SenseAttr('color', 'bot')),
                  "top temperature sensor": float(self.get_SenseAttr('temperature', 'top')),"middle temperature sensor": float(self.get_SenseAttr('temperature', 'mid')),
                  "bottom temperature sensor": float(self.get_SenseAttr('temperature', 'bot')),"top density sensor": float(self.get_SenseAttr('density', 'top')),
                  "middle density sensor": float(self.get_SenseAttr('density', 'mid')),"bottom density sensor": float(self.get_SenseAttr('density', 'bot')),
                  "cool acts": float(self.get_CounterAttr('cool')),"pump acts": float(self.get_CounterAttr('pump')),
                  "date": dateTime.split(' ')[0], "time": dateTime.split(' ')[1]}

        # print(vector)
        self.containerDB.append(vector)

    # SETTERS:
    def setInterval(self, interval):
        self.interval = interval

    # old functions:
    def setTannins(self, tannin):
        self.tannins.set(tannin)

    def setTemperature(self, temp):
        self.temperature.set(temp)

    def setColor(self, color):
        self.color.set(color)

    def setDensity(self, density):
        self.density.set(density)

    def setCool(self, cool):
        self.cool.set(cool)

    def setRealTemperature(self, temp):
        self.realTemperature.set(temp)

    def setRealTannins(self, tannin):
        self.realTannins.set(tannin)

    def setRealColor(self, color):
        self.realColor.set(color)

    def setRealDensity(self, density):
        self.realDensity.set(density)

    def setRealCool(self, cool):
        self.realCool.set(cool)

    def setRealValue(self, nameOfAttr, value):
        if nameOfAttr == "density":
            self.setRealDensity(value)
        elif nameOfAttr == "color":
            self.setRealColor(value)
        elif nameOfAttr == "tannins":
            self.setRealTannins(value)
        elif nameOfAttr == "cool":
            self.setRealCool(value)
        elif nameOfAttr == "temperature":
            self.setRealTemperature(value)

#news, maybe to unite them:
    def setSenseValue(self, nameOfAttr, place, value):
        self.senseDictParams[nameOfAttr][place].set(value)

    def setRealValues(self, nameOfAttr, place, value):
        self.realDictParams[nameOfAttr][place].set(value)

    def setExpectedValue(self, nameOfAttr, value):
        self.expectedDictParams[nameOfAttr].set(value)

    def setDateTime(self, dateTime):
        self.date.set(dateTime.split(' ')[0])
        self.time.set(dateTime.split(' ')[1])

    def setNumber(self, num):
        self.id = num

    def setName(self, _name):
        self.name = _name

    def setCounter(self, counterName, value):
        self.senseDictParams[counterName].set(value)

#GETTERS:

    def getDefTemp(self):
        return DEFAULT_TEMPERATURE

    def attr(self, attrName):
        if attrName == "density":
            return self.density.get()
        elif attrName == "cool":
            return self.realCool.get()
        elif attrName == "color":
            return self.color.get()
        elif attrName == "tannins":
            return self.tannins.get()
        elif attrName == "temperature":
            return self.temperature.get()

# OTHER FUNCTIONS:

    def getRealAttr(self, name, place):
        if place == 0:
            return self.realDictParams[name].get()
        return self.realDictParams[name][place].get()

    def getSenseAttr(self, name, place):
        if place == 0:
            return self.senseDictParams[name]
        return self.senseDictParams[name][place]

    def get_SenseAttr(self, name, place):
        return self.getSenseAttr(name, place).get()

    def getCounterAttr(self, name):
        return self.senseDictParams[name]

    def get_CounterAttr(self, name):
        return self.getCounterAttr(name).get()

    def getExpectedAttr(self, name):
        return self.expectedDictParams[name]

    def get_ExpectedAttr(self, name):
        return self.getExpectedAttr(name).get()


# the counters functions:
    # This function gets the amount of the needed pumpings and pumps by them
    def checkPump(self, amount):
        for i in range(0, amount):
            self.pumpIt()
    # This function makes the attrs being the average of them
    def pumpIt(self):
        for sensorName in SENSOR_NAMES:
            avg = 0
            for height in HEIGHTS:
                avg = avg + float(self.getRealAttr(sensorName, height))
            avg = avg / 3
            if sensorName == 'color': # pumping raises the color
                avg += 0.5
            for height in HEIGHTS:
                self.setRealValues(sensorName, height, avg)
        self.pumpCounter = self.pumpCounter + 1
    # This cools until the top temp will be lower than the expected
    def checkCool(self):
        while float(self.getRealAttr('temperature', 'top')) > float(self.get_ExpectedAttr('temperature')):
            self.coolIt()
    # This cools the container in 0.1 degrees
    def coolIt(self):
        for height in HEIGHTS:
            new_temp = float(self.getRealAttr('temperature', height)) - 0.1
            self.setRealValues('temperature', height, new_temp)
        self.coolCounter = self.coolCounter + 1

    def setCoolSum(self):
        sum = self.coolCounter - self.coolCounterGlobal
        self.senseDictParams['cool'].set(sum)
        self.coolCounterGlobal = self.coolCounter

    def setPumpSum(self):
        sum = self.pumpCounter - self.pumpCounterGlobal
        self.senseDictParams['pump'].set(sum)
        self.pumpCounterGlobal = self.pumpCounter

# old functions of cooling and pumping:

    def checkTemp(self):
        while float(self.temperature.get()) > DEFAULT_TEMPERATURE:
            self.coolAct()
        self.realCool.set(self.cool.get())

    def coolAct(self):
        self.numOfCools += 1
        self.cool.set(int(self.cool.get()) + 1)
        self.temperature.set(round(float(self.temperature.get()) - 0.1, 2))
        #print(self.temperature.get())

    def regulate(self): #TODO : ask Shivi how the regulator affects the color, density...
        self.numOfRegulations += 1

    def mesBox(self, message, note):
        tkinter.messagebox.showinfo("Error", message + "\n" + note)

# TODO: how to use the static class? we may need to make it dynamic
    # def changeNote(self, message):
    #     self.frame.

    def setup_logger(self, logger_name, log_file, level=logging.INFO):
        l = logging.getLogger(logger_name)
        formatter = logging.Formatter('%(asctime)s : %(message)s')
        fileHandler = logging.FileHandler(log_file, mode='w')
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        l.setLevel(level)
        l.addHandler(fileHandler)
        l.addHandler(streamHandler)