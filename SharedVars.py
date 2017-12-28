#Global variables shared among modules
import sys
import os
import time
import datetime
import tkinter
import avro.schema
import IbDataLoggerEnums
import IbDataLoggerClasses
import IbDataLoggerGui

# Program control
ProgramBeganTime = datetime.datetime.now()
CurrentDaySegment = IbDataLoggerEnums.DaySegment['NotSpecified']
TodayDayOfTheMonth = 0
GuiBackgroundManagementInterval = 1000
StatusReportingInterval = 0.3
UnderlyingMonitorReadingInterval = 1.0
OptionMonitorReadingInterval = 0.5
StorageWriteInterval = 1.0
WaitForThreadsToWindUpInterval = max(StatusReportingInterval,
										UnderlyingMonitorReadingInterval,
										OptionMonitorReadingInterval,
										StorageWriteInterval)
PauseBetweenOptionsBeingCancelled = 1.0
BackgroundRunning = False

# Day segment state machine
DaySegmentStateMachineSpinner = '-'
TodayIsATradingDay = False
TradingDayStartTimeHour = 6
TradingDayStartTimeMinute = 29
TradingDayEndTimeHour = 13
TradingDayEndTimeMinute = 0
RebootMyselfTimeHour = 14
RebootMyselfTimeMinute = 30

# TWS connection parameters
TwsPreferredClientId = 1
TwsConnectionPortNumber = 7496
TwsMarketDataTiming = IbDataLoggerEnums.MarketDataTimingType['Live']

# IP Connection
MyLoggerName = 'Default logger name'
DistantBeaconUrl = 'billgrace.com'
LocalBeaconUrl = 'IbDataTap.local'
TargetTapName = 'Default tap name'
TargetTapIsLocal = True
SocketTimeout = 1.0
IbDataTapStatus = IbDataLoggerClasses.StatusReportClass()
IbDataLinkIpMode = IbDataLoggerEnums.IpMode['Local']
StatusReportingIsActive = False
StatusSpinner = '-'
IbDataLinkIpAddress = '127.0.0.1'
IbDataLinkIpPortNumber = 56789
IbDataLinkIpLastUpdatedAt = 'I dunno'

# Underlying
UnderlyingMonitorReadingIsActive = False
UnderlyingSpinner = '-'
UnderlyingSymbol = 'SPX'
UnderlyingSymbolType = 'IND'
UnderlyingSubscriptionId = 0
UnderlyingMonitorData = IbDataLoggerClasses.MonitorDataClass()

#Option management
OptionManagementRefreshInterval = 1.0
StrikePriceStep = 5.0
StrikePriceRange = 1
ExpirationDateRange = 1
InitialHighestToBe = 1.0
InitialLowestToBe = 99999.0
InitialHighestBeing = -1.0
InitialLowestBeing = 99999.0
HighestStrikePriceToBeMonitored = InitialLowestToBe
LowestStrikePriceToBeMonitored = InitialLowestToBe
HighestStrikePriceBeingMonitored = InitialHighestBeing
LowestStrikePriceBeingMonitored = InitialLowestBeing
ExpirationDates = []
ActiveOptionMonitors = []
MonitorsToBeStarted = []

# Options
OptionMonitorReadingIsActive = False
OptionMonitorSpinner = '-'

# Data Storage
StorageRootPath = os.path.dirname(__file__)
StoragePath = ''
StorageIsActive = False

# Debug

# GUI main window
GuiRefreshInterval = 300
GuiWindow = tkinter.Tk()
GuiThreadCountLabel = tkinter.Label(GuiWindow, text='Thread count:')

# GUI day tracking
GuiTodayTheDateIsDisplay = tkinter.Label(GuiWindow, text='Today is Dayname Month Day, Year')
GuiTodayIsATradingDayDisplay = tkinter.Label(GuiWindow, text='Today IS/IS NOT a trading day')
GuiCurrentTimeDisplay = tkinter.Label(GuiWindow, text='The time is HH:MM:SS')
GuiDaySegmentDisplay = tkinter.Label(GuiWindow, text='We are not yet processing the state machine')
GuiProgramStartDateTime = tkinter.Label(GuiWindow, text='This program began running Month day, year @ HH:MM:SS')

# GUI IP link
# -- IP address
GuiIbDataLinkIpAddressText = tkinter.Text(GuiWindow, height=1, width=15)
# GuiIpModeRadioButtonLocal = tkinter.Radiobutton(GuiWindow, variable=IbDataLinkIpMode, value=IbDataLoggerEnums.IpMode['Local'], text='Local', command=IbDataLoggerGui.GuiIpModeRadioButtonLocal_Clicked)
# GuiIpModeRadioButtonDistant = tkinter.Radiobutton(GuiWindow, variable=IbDataLinkIpMode, value=IbDataLoggerEnums.IpMode['Distant'], text='Distant', command=IbDataLoggerGui.GuiIpModeRadioButtonDistant_Clicked)
# -- IP port number
GuiIbDataLinkIpPortNumberText = tkinter.Text(GuiWindow, height=1, width=5)
# GuiIbDataLinkIpPortNumberIncrementButton = tkinter.Button(GuiWindow, text='Next port number', command=IbDataLoggerGui.GuiIbDataLinkIpPortNumberIncrementButton_Clicked)
# GuiIbDataLinkIpPortNumberDecrementButton = tkinter.Button(GuiWindow, text='Previous port number', command=IbDataLoggerGui.GuiIbDataLinkIpPortNumberDecrementButton_Clicked)
# -- connection status reporting
GuiIbDataTapStatusText = tkinter.Text(GuiWindow, height=6, width=50)
# GuiIbDataTapStatusStartButton = tkinter.Button(GuiWindow, text='Start status', command=IbDataLoggerGui.GuiIbDataTapStatusStartButton_Clicked)
# GuiIbDataTapStatusStopButton = tkinter.Button(GuiWindow, text='Stop status', command=IbDataLoggerGui.GuiIbDataTapStatusStopButton_Clicked)

# GUI TWS link
# -- market data timing type
# GuiTwsMarketTimingRadioButtonLive = tkinter.Radiobutton(GuiWindow, variable=TwsMarketDataTiming, value=IbDataLoggerEnums.MarketDataTimingType['Live'], text='Live', command=IbDataLoggerGui.GuiTwsMarketTimingRadioButtonLive_Clicked)
# GuiTwsMarketTimingRadioButtonFrozen = tkinter.Radiobutton(GuiWindow, variable=TwsMarketDataTiming, value=IbDataLoggerEnums.MarketDataTimingType['Frozen'], text='Frozen', command=IbDataLoggerGui.GuiTwsMarketTimingRadioButtonFrozen_Clicked)
# GuiTwsMarketTimingRadioButtonDelayed = tkinter.Radiobutton(GuiWindow, variable=TwsMarketDataTiming, value=IbDataLoggerEnums.MarketDataTimingType['Delayed'], text='Delayed', command=IbDataLoggerGui.GuiTwsMarketTimingRadioButtonDelayed_Clicked)
# GuiTwsMarketTimingRadioButtonDelayedFrozen = tkinter.Radiobutton(GuiWindow, variable=TwsMarketDataTiming, value=IbDataLoggerEnums.MarketDataTimingType['DelayedFrozen'], text='DelayedFrozen', command=IbDataLoggerGui.GuiTwsMarketTimingRadioButtonDelayedFrozen_Clicked)
# -- preferred client ID and connection port number
# GuiTwsPreferredClientIdText = tkinter.Text(GuiWindow, height=1, width = 5)
# GuiTwsConnectionPortNumberText = tkinter.Text(GuiWindow, height=1, width = 5)
# -- connect/disconnect
# GuiTwsConnectButton = tkinter.Button(GuiWindow, text='Connect to TWS', command=IbDataLoggerGui.GuiTwsConnectButton_Clicked)
# GuiTwsDisconnectButton = tkinter.Button(GuiWindow, text='Disconnect from TWS', command=IbDataLoggerGui.GuiTwsDisconnectButton_Clicked)

# GUI Underlying
# -- Define
GuiUnderlyingSymbolText = tkinter.Text(GuiWindow, height=1, width=10)
GuiUnderlyingSymbolTypeText = tkinter.Text(GuiWindow, height=1, width=10)
# -- Subscribe/Unsubscribe
# GuiStartUnderlyingButton = tkinter.Button(GuiWindow, text='Start underlying', command=IbDataLoggerGui.GuiStartUnderlyingButton_Clicked)
# GuiStopUnderlyingButton = tkinter.Button(GuiWindow, text='Stop underlying', command=IbDataLoggerGui.GuiStopUnderlyingButton_Clicked)
# -- Values
GuiUnderlyingValuesDisplayText = tkinter.Text(GuiWindow, height=1, width=110)

# GUI Options
# -- Define
GuiStrikePriceRangeText = tkinter.Text(GuiWindow, height=1, width = 3)
GuiExpirationDateRangeText = tkinter.Text(GuiWindow, height=1, width = 3)
GuiExpirationDateListText = tkinter.Text(GuiWindow, height=1, width=80)
# -- Start/Stop monitoring
# GuiStartOptionsButton = tkinter.Button(GuiWindow, text='Start Options', command=IbDataLoggerGui.GuiStartOptionsButton_Clicked)
# GuiStopOptionsButton = tkinter.Button(GuiWindow, text='Stop Options', command=IbDataLoggerGui.GuiStopOptionsButton_Clicked)
GuiOptionDisplayLabel1 = tkinter.Label(GuiWindow, text='Strike price furthest below the underlying .x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x')
GuiOptionDisplayLabel2 = tkinter.Label(GuiWindow, text='Strike price just below the underlying .x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x')
GuiOptionDisplayLabel3 = tkinter.Label(GuiWindow, text='Strike price judyst snove the underlying .x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x')
GuiOptionDisplayLabel4 = tkinter.Label(GuiWindow, text='Strike price furthest above the underlying .x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x')

# GUI Storage
# -- Define
GuiStoragePathText = tkinter.Text(GuiWindow, height=2, width=75)
# -- Start/Stop 
# GuiStartStorageButton = tkinter.Button(GuiWindow, text='Start Storage', command=IbDataLoggerGui.GuiStartStorageButton_Clicked)
# GuiStopStorageButton = tkinter.Button(GuiWindow, text='Stop Storage', command=IbDataLoggerGui.GuiStopStorageButton_Clicked)

# Debug
GuiMessageLabel = tkinter.Label(GuiWindow, text='Initial GuiMessageLabel text',
									fg='#055', bg='#8ff')
GuiExitButton = tkinter.Button(GuiWindow, text='Exit', command=IbDataLoggerGui.ExitGui)
GuiTest1Button = tkinter.Button(GuiWindow, text='Test1', command=IbDataLoggerGui.GuiTest1Button_Clicked)
GuiTest2Button = tkinter.Button(GuiWindow, text='Test2', command=IbDataLoggerGui.GuiTest2Button_Clicked)
GuiTest3Button = tkinter.Button(GuiWindow, text='Test3', command=IbDataLoggerGui.GuiTest3Button_Clicked)
GuiTest4Button = tkinter.Button(GuiWindow, text='Test4', command=IbDataLoggerGui.GuiTest4Button_Clicked)
GuiStopAllButton = tkinter.Button(GuiWindow, text='Stop All', command=IbDataLoggerGui.GuiStopAllButton_Clicked)

# Schemas
CancelMonitorRequestWriterSchema = avro.schema.Parse(open("schemas/CancelMonitorRequestWriterSchema.txt").read())
CancelMonitorResultReaderSchema = avro.schema.Parse(open("schemas/CancelMonitorResultReaderSchema.txt").read())
CommandAcknowledgementReaderSchema = avro.schema.Parse(open("schemas/CommandAcknowledgementReaderSchema.txt").read())
ControlCommandWriterSchema = avro.schema.Parse(open("schemas/ControlCommandWriterSchema.txt").read())
MonitorDataReaderSchema = avro.schema.Parse(open("schemas/MonitorDataReaderSchema.txt").read())
# MonitorDataWriterSchema = avro.schema.Parse(open("schemas/MonitorDataWriterSchema.txt").read())
ReadMonitorRequestWriterSchema = avro.schema.Parse(open("schemas/ReadMonitorRequestWriterSchema.txt").read())
StartContractMonitorRequestWriterSchema = avro.schema.Parse(open("schemas/StartContractMonitorRequestWriterSchema.txt").read())
StartCMonitorResultReaderSchema = avro.schema.Parse(open("schemas/StartMonitorResultReaderSchema.txt").read())
StartUnderlyingMonitorRequestWriterSchema = avro.schema.Parse(open("schemas/StartUnderlyingMonitorRequestWriterSchema.txt").read())
StatusReportReaderSchema = avro.schema.Parse(open("schemas/StatusReportReaderSchema.txt").read())
