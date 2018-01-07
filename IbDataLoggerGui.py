import time
import datetime
import threading
import tkinter
import SharedVars
import IbDataLoggerEnums
import IbDataLoggerUtilities
import IbDataLoggerStorage
import IbDataLoggerTws
import IbDataLogger

def PrepareGui():
	GuiMainWindowLeft = 10
	GuiMainWindowTop = 10
	GuiMainWindowWidth = 1200
	GuiMainWindowHeight = 800
	GuiDayPanelTop = 0.00
	GuiDayPanelRight = 0.99
	GuiDayPanelBackground = '#fff'
	GuiIpPanelTop = 0.00
	GuiIpPanelBackground = '#8fd'
	GuiStatusPanelTop = 0.1
	GuiStatusPanelBackground = '#8df'
	GuiTwsPanelTop = 0.275
	GuiTwsPanelBackground = '#fc2'
	GuiMarketDataButtonsLeft = 0.25
	GuiUnderlyingPanelTop = 0.42
	GuiUnderlyingPanelBackground = '#fef'
	GuiOptionsPanelTop = 0.555
	GuiOptionsPanelBackground = '#fec'
	GuiStoragePanelTop = 0.78
	GuiStoragePanelBackground = '#ccf'
	GuiDebugPanelTop = 0.93
	GuiDebugPanelBackground = '#fec'

	# main window
	SharedVars.GuiWindow.geometry(str(GuiMainWindowWidth) + 'x' + str(GuiMainWindowHeight) + '+' + str(GuiMainWindowLeft) + '+' + str(GuiMainWindowTop))
	SharedVars.GuiWindow.configure(background='cyan')
	SharedVars.GuiWindow.resizable(True, True)

	# Appearance aids
	# GuiStatusPanelTopLine = tkinter.Canvas(SharedVars.GuiWindow, highlightthickness=0, bd=0, bg='#000', height=1, width=GuiMainWindowWidth).place(anchor='nw', relx=0.00, rely=GuiStatusPanelTop-0.005)
	GuiTwsPanelTopLine = tkinter.Canvas(SharedVars.GuiWindow, highlightthickness=0, bd=0, bg='#000', height=1, width=GuiMainWindowWidth).place(anchor='nw', relx=0.00, rely=GuiTwsPanelTop-0.005)
	GuiUnderlyingPanelTopLine = tkinter.Canvas(SharedVars.GuiWindow, highlightthickness=0, bd=0, bg='#000', height=1, width=GuiMainWindowWidth).place(anchor='nw', relx=0.00, rely=GuiUnderlyingPanelTop-0.005)
	GuiOptionsPanelTopLine = tkinter.Canvas(SharedVars.GuiWindow, highlightthickness=0, bd=0, bg='#000', height=1, width=GuiMainWindowWidth).place(anchor='nw', relx=0.00, rely=GuiOptionsPanelTop-0.005)
	GuiStoragePanelTopLine = tkinter.Canvas(SharedVars.GuiWindow, highlightthickness=0, bd=0, bg='#000', height=1, width=GuiMainWindowWidth).place(anchor='nw', relx=0.00, rely=GuiStoragePanelTop-0.005)
	GuiDebugPanelTopLine = tkinter.Canvas(SharedVars.GuiWindow, highlightthickness=0, bd=0, bg='#000', height=1, width=GuiMainWindowWidth).place(anchor='nw', relx=0.00, rely=GuiDebugPanelTop-0.005)

	# Day tracking
	SharedVars.GuiTodayTheDateIsDisplay.place(anchor='ne', relx=GuiDayPanelRight + 0.00, rely=GuiDayPanelTop + 0.00)
	SharedVars.GuiTodayIsATradingDayDisplay.place(anchor='ne', relx=GuiDayPanelRight + 0.00, rely=GuiDayPanelTop + 0.04)
	SharedVars.GuiCurrentTimeDisplay.place(anchor='ne', relx=GuiDayPanelRight + 0.00, rely=GuiDayPanelTop + 0.08)
	SharedVars.GuiDaySegmentDisplay.place(anchor='ne', relx=GuiDayPanelRight + 0.00, rely=GuiDayPanelTop + 0.12)
	SharedVars.GuiProgramStartDateTime.place(anchor='ne', relx=GuiDayPanelRight + 0.00, rely=GuiDayPanelTop + 0.16)
	# TCP/IP
	# -- Ip address selection
	GuiIbDataLinkIpAddressLabel = tkinter.Label(SharedVars.GuiWindow, text='IbDataTap IP address:', background=GuiIpPanelBackground).place(anchor='ne', relx=0.24, rely=GuiIpPanelTop + 0.00)
	SharedVars.GuiIbDataLinkIpAddressText.place(anchor='nw', relx=0.25, rely=GuiIpPanelTop + 0.00)
	SharedVars.GuiIbDataLinkIpAddressText.configure(background=GuiIpPanelBackground)
	# SharedVars.GuiIpModeRadioButtonLocal.place(anchor='nw', relx=0.40, rely=GuiIpPanelTop + 0.00)
	# SharedVars.GuiIpModeRadioButtonLocal.configure(background = GuiIpPanelBackground)
	# SharedVars.GuiIpModeRadioButtonDistant.place(anchor='nw', relx=0.55, rely=GuiIpPanelTop + 0.00)
	# SharedVars.GuiIpModeRadioButtonDistant.configure(background = GuiIpPanelBackground)
	# -- Ip port selection
	GuiIbDataLinkIpPortNumberLabel = tkinter.Label(SharedVars.GuiWindow, text='IbDataTap IP port number:', background=GuiIpPanelBackground).place(anchor='ne', relx=0.24, rely=GuiIpPanelTop + 0.05)
	SharedVars.GuiIbDataLinkIpPortNumberText.place(anchor='nw', relx=0.25, rely=GuiIpPanelTop + 0.05)
	SharedVars.GuiIbDataLinkIpPortNumberText.configure(background = GuiIpPanelBackground)
	# SharedVars.GuiIbDataLinkIpPortNumberIncrementButton.place(anchor='nw', relx=0.40, rely=GuiIpPanelTop + 0.045)
	# SharedVars.GuiIbDataLinkIpPortNumberIncrementButton.configure(background = GuiIpPanelBackground)
	# SharedVars.GuiIbDataLinkIpPortNumberDecrementButton.place(anchor='nw', relx=0.55, rely=GuiIpPanelTop + 0.045)
	# SharedVars.GuiIbDataLinkIpPortNumberDecrementButton.configure(background = GuiIpPanelBackground)

	# Status display
	SharedVars.GuiIbDataTapStatusText.place(anchor='nw', relx=0.02, rely=GuiStatusPanelTop + 0.00)
	SharedVars.GuiIbDataTapStatusText.configure(background = GuiStatusPanelBackground)
	# SharedVars.GuiIbDataTapStatusStartButton.place(anchor='nw', relx=0.85, rely=GuiStatusPanelTop + 0.02)
	# SharedVars.GuiIbDataTapStatusStartButton.configure(background = GuiStatusPanelBackground)
	# SharedVars.GuiIbDataTapStatusStopButton.place(anchor='nw', relx=0.85, rely=GuiStatusPanelTop + 0.07)
	# SharedVars.GuiIbDataTapStatusStopButton.configure(background = GuiStatusPanelBackground)
	
	# TWS link
	# -- market data timing
	GuiTwsStatusLabel = tkinter.Label(SharedVars.GuiWindow, text='TWS market data timing:', background=GuiTwsPanelBackground).place(anchor='ne', relx=0.24, rely=GuiTwsPanelTop + 0.00)
	# SharedVars.GuiTwsMarketTimingRadioButtonLive.place(anchor='nw', relx=GuiMarketDataButtonsLeft + 0.00, rely=GuiTwsPanelTop + 0.00)
	# SharedVars.GuiTwsMarketTimingRadioButtonLive.configure(background=GuiTwsPanelBackground)
	# # SharedVars.GuiTwsMarketTimingRadioButtonLive.select()
	# SharedVars.GuiTwsMarketTimingRadioButtonFrozen.place(anchor='nw', relx=GuiMarketDataButtonsLeft + 0.072, rely=GuiTwsPanelTop + 0.00)
	# SharedVars.GuiTwsMarketTimingRadioButtonFrozen.configure(background=GuiTwsPanelBackground)
	# # SharedVars.GuiTwsMarketTimingRadioButtonFrozen.deselect()
	# SharedVars.GuiTwsMarketTimingRadioButtonDelayed.place(anchor='nw', relx=GuiMarketDataButtonsLeft + 0.167, rely=GuiTwsPanelTop + 0.00)
	# SharedVars.GuiTwsMarketTimingRadioButtonDelayed.configure(background=GuiTwsPanelBackground)
	# # SharedVars.GuiTwsMarketTimingRadioButtonDelayed.deselect()
	# SharedVars.GuiTwsMarketTimingRadioButtonDelayedFrozen.place(anchor='nw', relx=GuiMarketDataButtonsLeft + 0.27, rely=GuiTwsPanelTop + 0.00)
	# SharedVars.GuiTwsMarketTimingRadioButtonDelayedFrozen.configure(background=GuiTwsPanelBackground)
	# SharedVars.GuiTwsMarketTimingRadioButtonDelayedFrozen.deselect()
	# # -- preferred client ID
	# GuiTwsPreferredClientIdLabel = tkinter.Label(SharedVars.GuiWindow, text='Preferred Client ID:', background=GuiTwsPanelBackground).place(anchor='ne', relx=0.24, rely=GuiTwsPanelTop + 0.05)
	# SharedVars.GuiTwsPreferredClientIdText.place(anchor='nw', relx=0.25, rely=GuiTwsPanelTop + 0.05)
	# SharedVars.GuiTwsPreferredClientIdText.configure(background=GuiTwsPanelBackground)
	# # -- connection port number
	# GuiTwsConnectionPortNumberLabel = tkinter.Label(SharedVars.GuiWindow, text='Connection port number:', background=GuiTwsPanelBackground).place(anchor='ne', relx=0.24, rely=GuiTwsPanelTop + 0.10)
	# SharedVars.GuiTwsConnectionPortNumberText.place(anchor='nw', relx=0.25, rely=GuiTwsPanelTop + 0.10)
	# SharedVars.GuiTwsConnectionPortNumberText.configure(background=GuiTwsPanelBackground)
	# # -- connect/disconnect buttons
	# SharedVars.GuiTwsConnectButton.place(anchor='nw', relx=0.85, rely=GuiTwsPanelTop + 0.02)
	# SharedVars.GuiTwsDisconnectButton.place(anchor='nw', relx=0.85, rely=GuiTwsPanelTop + 0.07)

	# Underlying
	# -- Define
	GuiUnderlyingSymbolLabel = tkinter.Label(SharedVars.GuiWindow, text='Underlying symbol:', background=GuiUnderlyingPanelBackground).place(anchor='ne', relx=0.24, rely=GuiUnderlyingPanelTop + 0.00)
	SharedVars.GuiUnderlyingSymbolText.place(anchor='nw', relx=0.25, rely=GuiUnderlyingPanelTop + 0.00)
	SharedVars.GuiUnderlyingSymbolText.configure(background=GuiUnderlyingPanelBackground)
	GuiUnderlyingSymbolTypeLabel = tkinter.Label(SharedVars.GuiWindow, text='Underlying symbol type:', background=GuiUnderlyingPanelBackground).place(anchor='ne', relx=0.24, rely=GuiUnderlyingPanelTop + 0.04)
	SharedVars.GuiUnderlyingSymbolTypeText.place(anchor='nw', relx=0.25, rely=GuiUnderlyingPanelTop + 0.04)
	SharedVars.GuiUnderlyingSymbolTypeText.configure(background=GuiUnderlyingPanelBackground)
	# -- Connect/Disconnect
	# SharedVars.GuiStartUnderlyingButton.place(anchor='nw', relx=0.85, rely=GuiUnderlyingPanelTop + 0.02)
	# SharedVars.GuiStopUnderlyingButton.place(anchor='nw', relx=0.85, rely=GuiUnderlyingPanelTop + 0.07)
	# -- Values
	SharedVars.GuiUnderlyingValuesDisplayText.place(anchor='nw', relx=0.01, rely=GuiUnderlyingPanelTop + 0.087)
	SharedVars.GuiUnderlyingValuesDisplayText.configure(background=GuiUnderlyingPanelBackground)

	# Options
	# -- Define
	GuiExpirationDateRangeLabel = tkinter.Label(SharedVars.GuiWindow, text='Expiration Date range:', background=GuiOptionsPanelBackground).place(anchor='ne', relx=0.14, rely=GuiOptionsPanelTop + 0.00)
	SharedVars.GuiExpirationDateRangeText.place(anchor='nw', relx=0.15, rely=GuiOptionsPanelTop + 0.00)
	GuiStrikePriceRangeLabel = tkinter.Label(SharedVars.GuiWindow, text='Strike Price range:', background=GuiOptionsPanelBackground).place(anchor='ne', relx=0.29, rely=GuiOptionsPanelTop + 0.00)
	SharedVars.GuiStrikePriceRangeText.place(anchor='nw', relx=0.30, rely=GuiOptionsPanelTop + 0.00)
	GuiExpirationDatesLabel = tkinter.Label(SharedVars.GuiWindow, text='Expiration dates:', background=GuiOptionsPanelBackground).place(anchor='ne', relx=0.14, rely=GuiOptionsPanelTop + 0.035)
	SharedVars.GuiExpirationDateListText.place(anchor='nw', relx=0.15, rely=GuiOptionsPanelTop + 0.035)

	# # -- Start/Stop monitoring
	# SharedVars.GuiStartOptionsButton.place(anchor='nw', relx=0.85, rely=GuiOptionsPanelTop + 0.02)
	# SharedVars.GuiStopOptionsButton.place(anchor='nw', relx=0.85, rely=GuiOptionsPanelTop + 0.07)
	# -- Values
	SharedVars.GuiOptionDisplayLabel1.place(anchor='nw', relx=0.01, rely=GuiOptionsPanelTop + 0.075)
	SharedVars.GuiOptionDisplayLabel2.place(anchor='nw', relx=0.01, rely=GuiOptionsPanelTop + 0.110)
	SharedVars.GuiOptionDisplayLabel3.place(anchor='nw', relx=0.01, rely=GuiOptionsPanelTop + 0.145)
	SharedVars.GuiOptionDisplayLabel4.place(anchor='nw', relx=0.01, rely=GuiOptionsPanelTop + 0.18)

	# Data storage
	# -- Define
	GuiStoragePathLabel = tkinter.Label(SharedVars.GuiWindow, text='Storage path:', background=GuiStoragePanelBackground).place(anchor='ne', relx=0.13, rely=GuiStoragePanelTop + 0.00)
	SharedVars.GuiStoragePathText.place(anchor='nw', relx=0.14, rely=GuiStoragePanelTop + 0.00)
	# -- Start/Stop data storage
	# SharedVars.GuiStartStorageButton.place(anchor='nw', relx=0.85, rely=GuiStoragePanelTop + 0.02)
	# SharedVars.GuiStopStorageButton.place(anchor='nw', relx=0.85, rely=GuiStoragePanelTop + 0.07)

	# Debug
	SharedVars.GuiMessageLabel.place(anchor='sw', relx=0.01,rely=0.99)
	SharedVars.GuiExitButton.place(anchor='se', relx=0.99, rely=0.99)
	SharedVars.GuiThreadCountLabel.place(anchor='se', relx=0.90, rely=0.99)
	SharedVars.GuiTest1Button.place(anchor='se', relx=0.30, rely=0.99)
	SharedVars.GuiTest1Button.configure(text='Start tracking')
	SharedVars.GuiTest2Button.place(anchor='se', relx=0.40, rely=0.99)
	SharedVars.GuiTest2Button.configure(text='Stop tracking')
	SharedVars.GuiTest3Button.place(anchor='se', relx=0.50, rely=0.99)
	SharedVars.GuiTest3Button.configure(text='Write test file')
	SharedVars.GuiTest4Button.place(anchor='se', relx=0.60, rely=0.99)
	SharedVars.GuiTest4Button.configure(text='Read Option')

# # TCP/IP
# def GuiIpModeRadioButtonSet(Mode):
# 	SharedVars.IpMode = Mode
# 	if Mode == IbDataLoggerEnums.IpMode['Local']:
# 		SharedVars.IbDataLinkIpAddress = SharedVars.IbDataLinkLocalIpAddress
# 		SharedVars.GuiIpModeRadioButtonLocal.select()
# 		SharedVars.GuiIpModeRadioButtonDistant.deselect()
# 	elif Mode == IbDataLoggerEnums.IpMode['Distant']:
# 		SharedVars.IbDataLinkIpAddress = SharedVars.IbDataLinkDistantIpAddress
# 		SharedVars.GuiIpModeRadioButtonLocal.deselect()
# 		SharedVars.GuiIpModeRadioButtonDistant.select()
# 	else:
# 		IbDataLoggerUtilities.LogError('Unknown selector in GuiIpModeRadioButtonSet: ' + str(Mode))


# def GuiIpModeRadioButtonLocal_Clicked():
# 	GuiIpModeRadioButtonSet(IbDataLoggerEnums.IpMode['Local'])

# def GuiIpModeRadioButtonDistant_Clicked():
# 	GuiIpModeRadioButtonSet(IbDataLoggerEnums.IpMode['Distant'])

# def GuiIbDataLinkIpPortNumberIncrementButton_Clicked():
# 	if SharedVars.IbDataLinkIpPortNumber == SharedVars.IbDataLinkIpPortNumberMax:
# 		SharedVars.IbDataLinkIpPortNumber = SharedVars.IbDataLinkIpPortNumberMin
# 	else:
# 		SharedVars.IbDataLinkIpPortNumber += 1

# def GuiIbDataLinkIpPortNumberDecrementButton_Clicked():
# 	if SharedVars.IbDataLinkIpPortNumber == SharedVars.IbDataLinkIpPortNumberMin:
# 		SharedVars.IbDataLinkIpPortNumber = SharedVars.IbDataLinkIpPortNumberMax
# 	else:
# 		SharedVars.IbDataLinkIpPortNumber -= 1

# # Status
# def GuiIbDataTapStatusStartButton_Clicked():
# 	SharedVars.StatusReportingIsActive = True

# def GuiIbDataTapStatusStopButton_Clicked():
# 	SharedVars.StatusReportingIsActive = False

# # TWS
# def GuiTwsMarketTimingRadioButtonSet(TimingType):
# 	SharedVars.TwsMarketDataTiming = TimingType
# 	if TimingType == IbDataLoggerEnums.MarketDataTimingType['Live']:
# 		SharedVars.GuiTwsMarketTimingRadioButtonLive.select()
# 		SharedVars.GuiTwsMarketTimingRadioButtonFrozen.deselect()
# 		SharedVars.GuiTwsMarketTimingRadioButtonDelayed.deselect()
# 		SharedVars.GuiTwsMarketTimingRadioButtonDelayedFrozen.deselect()
# 	elif TimingType == IbDataLoggerEnums.MarketDataTimingType['Frozen']:
# 		SharedVars.GuiTwsMarketTimingRadioButtonLive.deselect()
# 		SharedVars.GuiTwsMarketTimingRadioButtonFrozen.select()
# 		SharedVars.GuiTwsMarketTimingRadioButtonDelayed.deselect()
# 		SharedVars.GuiTwsMarketTimingRadioButtonDelayedFrozen.deselect()
# 	elif TimingType == IbDataLoggerEnums.MarketDataTimingType['Delayed']:
# 		SharedVars.GuiTwsMarketTimingRadioButtonLive.deselect()
# 		SharedVars.GuiTwsMarketTimingRadioButtonFrozen.deselect()
# 		SharedVars.GuiTwsMarketTimingRadioButtonDelayed.select()
# 		SharedVars.GuiTwsMarketTimingRadioButtonDelayedFrozen.deselect()
# 	elif TimingType == IbDataLoggerEnums.MarketDataTimingType['DelayedFrozen']:
# 		SharedVars.GuiTwsMarketTimingRadioButtonLive.deselect()
# 		SharedVars.GuiTwsMarketTimingRadioButtonFrozen.deselect()
# 		SharedVars.GuiTwsMarketTimingRadioButtonDelayed.deselect()
# 		SharedVars.GuiTwsMarketTimingRadioButtonDelayedFrozen.select()

# def GuiTwsMarketTimingRadioButtonLive_Clicked():
# 	GuiTwsMarketTimingRadioButtonSet(IbDataLoggerEnums.MarketDataTimingType['Live'])

# def GuiTwsMarketTimingRadioButtonFrozen_Clicked():
# 	GuiTwsMarketTimingRadioButtonSet(IbDataLoggerEnums.MarketDataTimingType['Frozen'])

# def GuiTwsMarketTimingRadioButtonDelayed_Clicked():
# 	GuiTwsMarketTimingRadioButtonSet(IbDataLoggerEnums.MarketDataTimingType['Delayed'])

# def GuiTwsMarketTimingRadioButtonDelayedFrozen_Clicked():
# 	GuiTwsMarketTimingRadioButtonSet(IbDataLoggerEnums.MarketDataTimingType['DelayedFrozen'])

# def GuiTwsConnectButton_Clicked():
# 	IbDataLoggerTws.ConnectToTws()

# def GuiTwsDisconnectButton_Clicked():
# 	IbDataLoggerTws.DisconnectFromTws()

# # Underlying
# def GuiStartUnderlyingButton_Clicked():
# 	IbDataLoggerTws.SubscribeToUnderlying()

# def GuiStopUnderlyingButton_Clicked():
# 	IbDataLoggerTws.UnsubscribeFromUnderlying()

# # Options
# def GuiStartOptionsButton_Clicked():
# 	IbDataLoggerTws.StartOptionMonitor('SPX', SharedVars.ExpirationDates[0], 'PUT', IbDataLoggerUtilities.NearestStrikePriceAboveUnderlying())
# 	SharedVars.OptionMonitorReadingIsActive = True

# def GuiStopOptionsButton_Clicked():
# 	# Tell the option reading and logging threads to quit
# 	SharedVars.OptionMonitorReadingIsActive = False
# 	# Give the option reading and logging threads time to cycle and quit
# 	time.sleep(2 * SharedVars.OptionMonitorReadingInterval)
# 	time.sleep(2 * SharedVars.StorageWriteInterval)
# 	# Unsubscribe from the option monitors at the IbDataTap end
# 	for monitor in SharedVars.ActiveOptionMonitors:
# 		IbDataLoggerTws.CancelMonitor(monitor['SubscriptionId'])
# 	# Empty the list of active monitors
# 	SharedVars.ActiveOptionMonitors.clear()

# # Storage
# def GuiStartStorageButton_Clicked():
# 	SharedVars.StorageIsActive = True

# def GuiStopStorageButton_Clicked():
# 	SharedVars.StorageIsActive = False

# Debug
def GuiTest1Button_Clicked():
	a=1
	# # Sub/Unsub UL
	# if SharedVars.GuiTest1Button['text'] == 'Sub UL':
	# 	SharedVars.GuiTest1Button.config(text='Unsub UL')
	# 	IbDataLoggerTws.SubscribeToUnderlying()
	# else:
	# 	SharedVars.GuiTest1Button.config(text='Sub UL')
	# 	IbDataLoggerTws.UnsubscribeFromUnderlying()

	# Start Tracking the market
	print('Test1 button clicked')
	if SharedVars.CurrentDaySegment == IbDataLoggerEnums.DaySegment['TradingTime']:
		# Wha??? we're already tracking so it makes no sense to start tracking....
		IbDataLoggerUtilities.LogError('Already tracking!!')
	else:
		# Mimic what the state machine does
		SharedVars.CurrentDaySegment = IbDataLoggerEnums.DaySegment['TradingTime']
		IbDataLogger.StartTrackingTheMarket()

def GuiTest2Button_Clicked():
	a=1
	# # Read UL
	# IbDataLoggerTws.ReadUnderlyingMonitor()

	# Stop tracking the market
	print('Test2 button clicked')
	if SharedVars.CurrentDaySegment != IbDataLoggerEnums.DaySegment['TradingTime']:
		# Wha??? we're not already tracking so it makes no sense to stop tracking....
		IbDataLoggerUtilities.LogError('Not already tracking!!')
	else:
		# Mimic what the state machine does
		SharedVars.CurrentDaySegment = IbDataLoggerEnums.DaySegment['WaitingForTomorrow']
		IbDataLogger.StopTrackingTheMarket()

def GuiTest3Button_Clicked():
	a=1
	# # Sub/Unsub Option
	# if SharedVars.GuiTest3Button['text'] == 'Sub Option':
	# 	SharedVars.GuiTest3Button.config(text='Unsub Option')
	# 	Success, NewOptionMonitor = IbDataLoggerTws.SubscribeToOption('SPX', SharedVars.ExpirationDates[0], 'PUT', IbDataLoggerUtilities.NearestStrikePriceAboveUnderlying())
	# 	if Success:
	# 		if len(SharedVars.ActiveOptionMonitors) == 0:
	# 			SharedVars.ActiveOptionMonitors.append(NewOptionMonitor)
	# 		else:
	# 			SharedVars.ActiveOptionMonitors[0] = NewOptionMonitor
	# 	else:
	# 		IbDataLoggerUtilities.LogError('Failed to subscribe to option')
	# else:
	# 	SharedVars.GuiTest3Button.config(text='Sub Option')
	# 	CancelMonitor(SharedVars.ActiveOptionMonitors[0]['SubscriptionId'])
	IbDataLoggerStorage.PrepareDiskStorage()
	IbDataLoggerStorage.LogTestFile()

def GuiTest4Button_Clicked():
	a=1
	# Read Option
	MySubscriptionId = SharedVars.ActiveOptionMonitors[0]['SubscriptionId']
	Success, NewMonitorData = IbDataLoggerTws.ReadMonitor(MySubscriptionId)
	if not Success:
		IbDataLoggerUtilities.LogError('problem reading option monitor ID: ' + str(MySubscriptionId))
	else:
		SharedVars.ActiveOptionMonitors[0] = NewMonitorData

def GuiStopAllButton_Clicked():
	a=1

def RefreshGui():
	try:
		# Day tracking
		SharedVars.GuiTodayTheDateIsDisplay.configure(text='Today is {0}'.format(datetime.date.today().strftime("%A %B %d, %Y")))
		if SharedVars.TodayIsATradingDay:
			SharedVars.GuiTodayIsATradingDayDisplay.configure(text='It is a trading day')
		else:
			SharedVars.GuiTodayIsATradingDayDisplay.configure(text='It is not a trading day')
		CurrentTime = datetime.datetime.now()
		SharedVars.GuiCurrentTimeDisplay.configure(text='{3} The time is {0}:{1:02}:{2:02}'.format(CurrentTime.hour, CurrentTime.minute, CurrentTime.second, SharedVars.DaySegmentStateMachineSpinner))
		if SharedVars.CurrentDaySegment == IbDataLoggerEnums.DaySegment['NotSpecified']:
			SharedVars.GuiDaySegmentDisplay.configure(text='We have not yet started tracking this....')
		elif SharedVars.CurrentDaySegment == IbDataLoggerEnums.DaySegment['MorningBeforeTrading']:
			SharedVars.GuiDaySegmentDisplay.configure(text='We are waiting for the market to open')
		elif SharedVars.CurrentDaySegment == IbDataLoggerEnums.DaySegment['TradingTime']:
			SharedVars.GuiDaySegmentDisplay.configure(text='We are tracking the open market')
		elif SharedVars.CurrentDaySegment == IbDataLoggerEnums.DaySegment['WaitingForTomorrow']:
			SharedVars.GuiDaySegmentDisplay.configure(text='We are waiting for tomorrow to arrive')
		else:
			SharedVars.GuiDaySegmentDisplay.configure(text='We are lost...')
		SharedVars.GuiProgramStartDateTime.configure(text='This program began running {0:%A} {0:%B} {0:%d}, {0:%Y} @ {0:%I:%M%p}'.format(SharedVars.ProgramBeganTime))

		# TCP/IP
		SharedVars.GuiIbDataLinkIpAddressText.delete('1.0', 'end')
		SharedVars.GuiIbDataLinkIpAddressText.insert('end', SharedVars.IbDataLinkIpAddress)
		SharedVars.GuiIbDataLinkIpPortNumberText.delete('1.0', 'end')
		SharedVars.GuiIbDataLinkIpPortNumberText.insert('end', SharedVars.IbDataLinkIpPortNumber)

		# Status
		SharedVars.GuiIbDataTapStatusText.delete('1.0', 'end')
		SharedVars.GuiIbDataTapStatusText.insert('end', 'MarketDataType: ' + str(SharedVars.IbDataTapStatus['MarketDataType']) + '               - ' + SharedVars.StatusSpinner + ' -' +
										'\nTwsPreferredClientId: ' + str(SharedVars.IbDataTapStatus['TwsPreferredClientId']) +
										'\nTwsPortNumber: ' + str(SharedVars.IbDataTapStatus['TwsPortNumber']) +
										'\nIbDataTapConnectionStatus: ' + str(SharedVars.IbDataTapStatus['IbDataTapConnectionStatus']) +
										'\nNumberOfIdsOnMonitorList: ' + str(SharedVars.IbDataTapStatus['NumberOfIdsOnMonitorList']) +
										'\nDiagnosticInteger: ' + str(SharedVars.IbDataTapStatus['DiagnosticInteger'])
											+ '       Underlying ID: ' + str(SharedVars.UnderlyingSubscriptionId)
											)

		# Underlying
		if True:
		# if SharedVars.UnderlyingMonitorReadingIsActive:
			SharedVars.GuiUnderlyingSymbolText.delete('1.0', 'end')
			SharedVars.GuiUnderlyingSymbolText.insert('end', SharedVars.UnderlyingSymbol)
			SharedVars.GuiUnderlyingSymbolTypeText.delete('1.0', 'end')
			SharedVars.GuiUnderlyingSymbolTypeText.insert('end', SharedVars.UnderlyingSymbolType)
			SharedVars.GuiUnderlyingValuesDisplayText.delete('1.0', 'end')
			SharedVars.GuiUnderlyingValuesDisplayText.insert('end', 'Bid: $'  + str(SharedVars.UnderlyingMonitorData['Bid']['Price']) +
												', Ask: $' + str(SharedVars.UnderlyingMonitorData['Ask']['Price']) +
												', Last: $' + str(SharedVars.UnderlyingMonitorData['Last']['Price']) +
												', Open: $' + str(SharedVars.UnderlyingMonitorData['Open']) +
												', High: $' + str(SharedVars.UnderlyingMonitorData['High']) +
												', Low: $' + str(SharedVars.UnderlyingMonitorData['Low']) +
												', TWS#: ' + str(SharedVars.UnderlyingMonitorData['MonitorUpdateCount']) +
												' -' + SharedVars.UnderlyingSpinner + '-'
												 )

		# Options
		if True:
		# if SharedVars.OptionMonitorReadingIsActive:
			SharedVars.GuiExpirationDateRangeText.delete('1.0', 'end')
			SharedVars.GuiExpirationDateRangeText.insert('end', str(SharedVars.ExpirationDateRange))
			SharedVars.GuiStrikePriceRangeText.delete('1.0', 'end')
			SharedVars.GuiStrikePriceRangeText.insert('end', str(SharedVars.StrikePriceRange))
			SharedVars.GuiExpirationDateListText.delete('1.0', 'end')
			ExpirationDateListString = ''
			for ThisDate in SharedVars.ExpirationDates:
				if len(ExpirationDateListString) > 1:
					ExpirationDateListString = ExpirationDateListString + ', '
				ExpirationDateListString = ExpirationDateListString + str(ThisDate['year']) + '-' + str(ThisDate['month']) + '-' + str(ThisDate['day'])
			SharedVars.GuiExpirationDateListText.insert('end', ExpirationDateListString)
			SharedVars.GuiOptionDisplayLabel1.configure(text='Lowest strike price: ' + str(SharedVars.LowestStrikePriceBeingMonitored))
			SharedVars.GuiOptionDisplayLabel2.configure(text='Nearest strike below underlying: ' + str(IbDataLoggerUtilities.NearestStrikePriceBelowUnderlying()))
			SharedVars.GuiOptionDisplayLabel3.configure(text='Nearest strike above underlying: ' + str(IbDataLoggerUtilities.NearestStrikePriceAboveUnderlying()))
			SharedVars.GuiOptionDisplayLabel4.configure(text='Highest strike price: ' + str(SharedVars.HighestStrikePriceBeingMonitored))
			# SharedVars.GuiOptionDisplayLabel1.configure(text='First Expiration Date: ' + str(SharedVars.ExpirationDates[0]))
			if len(SharedVars.ActiveOptionMonitors) > 0:
				SharedVars.GuiOptionDisplayLabel2.configure(text='First active monitor. Strike: ' + str(SharedVars.ActiveOptionMonitors[0]['StrikePrice']) +
				', Bid: {0:.2f}'.format(SharedVars.ActiveOptionMonitors[0]['Bid']['Price']) +
				', Ask: {0:.2f}'.format(SharedVars.ActiveOptionMonitors[0]['Ask']['Price']) +
				', Last: {0:.2f}'.format(SharedVars.ActiveOptionMonitors[0]['Last']['Price'])
				)
			else:
				SharedVars.GuiOptionDisplayLabel2.configure(text='Nearest strike below underlying: ' + str(IbDataLoggerUtilities.NearestStrikePriceBelowUnderlying()))
			SharedVars.GuiOptionDisplayLabel3.configure(text='Nearest strike above underlying: ' + str(IbDataLoggerUtilities.NearestStrikePriceAboveUnderlying()))
			SharedVars.GuiOptionDisplayLabel4.configure(text='Highest strike price: ' + str(SharedVars.HighestStrikePriceBeingMonitored))

		# Storage
		SharedVars.GuiStoragePathText.delete('1.0', 'end')
		SharedVars.GuiStoragePathText.insert('end', str(SharedVars.StoragePath))

		# Debug
		SharedVars.GuiThreadCountLabel.configure(text='Thread count: ' + str(threading.active_count()) + ', Option monitor count: ' + str(len(SharedVars.ActiveOptionMonitors)))
	except Exception as e:
		IbDataLoggerUtilities.LogError('Exception in RefreshGui(): ' + str(e))

	# if datetime.datetime.now() > SharedVars.TimeToEndGui:
	# 	SharedVars.GuiWindow.destroy()
	# else:
	SharedVars.GuiWindow.after(SharedVars.GuiRefreshInterval, RefreshGui)

def GuiBackgroundManagementThread():
	SharedVars.DaySegmentStateMachineSpinner = IbDataLoggerUtilities.NextSpinner(SharedVars.DaySegmentStateMachineSpinner)
	ProcessDaySegmentStateMachine()
	SharedVars.GuiWindow.after(SharedVars.GuiBackgroundManagementInterval, GuiBackgroundManagementThread)

def CompareHourMinute(Hour1, Minute1, Hour2, Minute2):
	# return 0 if HM1 == HM2, 1 if HM1 is later than HM2, -1 if HM1 is earlier than HM2
	if (Hour1 == Hour2) and (Minute1 == Minute2): return 0
	if Hour1 > Hour2: return 1
	if Hour1 < Hour2: return -1
	if Minute1 > Minute2: return 1
	return -1

def ProcessDaySegmentStateMachine():
	if SharedVars.CurrentDaySegment == IbDataLoggerEnums.DaySegment['NotSpecified']:
		# Just starting up - figure how to get to the appropriate state
		# First, save a copy of the current day-of-the-month so we can detect the transition into tomorrow when it comes
		CurrentTime = datetime.datetime.now()
		SharedVars.TodayDayOfTheMonth = CurrentTime.day
		# Then, decide where we have popped into existence on THIS day and initialize the state accordingly
		if not IbDataLoggerUtilities.IsTodayATradingDay():
			#  If it's not a trading day then we're just waiting for the day to end no matter what time it happens to be
			SharedVars.CurrentDaySegment = IbDataLoggerEnums.DaySegment['WaitingForTomorrow']
		else:
			# OK, this IS a trading day so what time of day is it?
			CurrentTimeOfDay = datetime.datetime.now()
			if -1 == CompareHourMinute(CurrentTimeOfDay.hour, CurrentTimeOfDay.minute, SharedVars.TradingDayStartTimeHour, SharedVars.TradingDayStartTimeMinute):
				# It's early and we're waiting for the market to open
				SharedVars.CurrentDaySegment = IbDataLoggerEnums.DaySegment['MorningBeforeTrading']
			elif 1 == CompareHourMinute(CurrentTimeOfDay.hour, CurrentTimeOfDay.minute, SharedVars.TradingDayEndTimeHour, SharedVars.TradingDayEndTimeMinute):
				# It's late, the market has closed and we're waiting for another day
				SharedVars.CurrentDaySegment = IbDataLoggerEnums.DaySegment['WaitingForTomorrow']
			else:
				# The market is open now so we start off active
				SharedVars.CurrentDaySegment = IbDataLoggerEnums.DaySegment['TradingTime']
				IbDataLogger.StartTrackingTheMarket()
	elif SharedVars.CurrentDaySegment == IbDataLoggerEnums.DaySegment['MorningBeforeTrading']:
		# It's the morning of a trading day and we're waiting for our starting time
		CurrentTimeOfDay = datetime.datetime.now()
		if 1 == CompareHourMinute(CurrentTimeOfDay.hour, CurrentTimeOfDay.minute, SharedVars.TradingDayStartTimeHour, SharedVars.TradingDayStartTimeMinute):
			SharedVars.CurrentDaySegment = IbDataLoggerEnums.DaySegment['TradingTime']
			IbDataLogger.StartTrackingTheMarket()
	elif SharedVars.CurrentDaySegment == IbDataLoggerEnums.DaySegment['TradingTime']:
		# It's a trading day and the market is open so we're waiting for our ending time
		CurrentTimeOfDay = datetime.datetime.now()
		if 1 == CompareHourMinute(CurrentTimeOfDay.hour, CurrentTimeOfDay.minute, SharedVars.TradingDayEndTimeHour, SharedVars.TradingDayEndTimeMinute):
			SharedVars.CurrentDaySegment = IbDataLoggerEnums.DaySegment['WaitingForTomorrow']
			IbDataLogger.StopTrackingTheMarket()
	elif SharedVars.CurrentDaySegment == IbDataLoggerEnums.DaySegment['WaitingForTomorrow']:
		# It's either not a trading day or the market has already closed so we're just waiting for tomorrow to come along
		#  ... Add-a-bandaid December 19, 2017: reboot every day since I can't figure out what's getting clogged up and
		#  ...  preventing proper data capture when we run for longer than a day.
		CurrentTimeOfDay = datetime.datetime.now()
		if 1 == CompareHourMinute(CurrentTimeOfDay.hour, CurrentTimeOfDay.minute, SharedVars.RebootMyselfTimeHour, SharedVars.RebootMyselfTimeMinute):
		# ... well, the 'boot myself' process below doesn't seem to work so let's just exit this
		# ...  python script and try to get the Automator to do a scheduled restart after that.
			ExitGui()
		# 	IbDataLoggerUtilities.RebootMyself()
		# We recognize the transition through midnight by the numerical day of the month changing
		CurrentTime = datetime.datetime.now()
		if SharedVars.TodayDayOfTheMonth != CurrentTime.day:
			# OK, we've just moved to another day
			SharedVars.TodayDayOfTheMonth = CurrentTime.day
			if IbDataLoggerUtilities.IsTodayATradingDay():
				SharedVars.CurrentDaySegment = IbDataLoggerEnums.DaySegment['MorningBeforeTrading']
			else:
				SharedVars.CurrentDaySegment = IbDataLoggerEnums.DaySegment['WaitingForTomorrow']

def ExitGui():
	# global BackgroundRunning
	SharedVars.BackgroundRunning = False
	SharedVars.GuiWindow.destroy()

