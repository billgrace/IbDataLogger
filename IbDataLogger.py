#!/usr/local/bin/python3
import sys
import time
import datetime
import threading
import avro.datafile
import avro.schema
import avro.io
import tkinter
from enum import Enum
import numpy

import SharedVars
import IbDataLoggerEnums
import IbDataLoggerClasses
import IbDataLoggerStorage
import IbDataLoggerUtilities
import IbDataLoggerGui
import IbDataLoggerTws

def Main():
	IbDataLoggerStorage.ReadPreferencesFile()
	IbDataLoggerGui.PrepareGui()
	IbDataLoggerGui.RefreshGui()
	IbDataLoggerGui.GuiBackgroundManagementThread()
	SharedVars.GuiWindow.mainloop()
	SharedVars.BackgroundRunning = False

def StartTrackingTheMarket():
	# Prepare our infrastructure to log the market
	InitializeMonitorManagement()
	IbDataLoggerUtilities.GetTapAddress()
	IbDataLoggerUtilities.LogTradingDayStart()
	IbDataLoggerStorage.PrepareDiskStorage()
	IbDataLoggerUtilities.EstablishExpirationDates()
	SharedVars.BackgroundRunning = True
	StatusReportingThr = threading.Thread(target=StatusReportingThread).start()
	UnderlyingMonitorThr = threading.Thread(target=UnderlyingMonitorThread).start()
	UnderlyingLoggingThr = threading.Thread(target=UnderlyingLoggingThread).start()
	MonitorManagerThr = threading.Thread(target=MonitorManagerThread).start()
	SharedVars.StatusReportingIsActive = True
	IbDataLoggerTws.ConnectToTws()
	IbDataLoggerTws.SubscribeToUnderlying()
	SharedVars.UnderlyingMonitorReadingIsActive = True
	SharedVars.OptionMonitorReadingIsActive = True
	SharedVars.StorageIsActive = True

def StopTrackingTheMarket():
	# 1 - Set state machine to 'after trading'
	IbDataLoggerUtilities.LogTradingDayEnd()
	# 2 - Turn off thread activities
	SharedVars.StorageIsActive = False
	SharedVars.OptionMonitorReadingIsActive = False
	SharedVars.UnderlyingMonitorReadingIsActive = False
	SharedVars.StatusReportingIsActive = False
	# 2a - Wait for threads to register end of activity
	time.sleep(SharedVars.WaitForThreadsToWindUpInterval)
	# 3 - Signal threads to terminate
	SharedVars.BackgroundRunning = False

def StatusReportingThread():
	while SharedVars.BackgroundRunning:
		if SharedVars.StatusReportingIsActive:
			IbDataLoggerTws.GetIbDataTapStatus()
		time.sleep(SharedVars.StatusReportingInterval)

def UnderlyingMonitorThread():
	while SharedVars.BackgroundRunning:
		if SharedVars.UnderlyingMonitorReadingIsActive:
			IbDataLoggerTws.ReadUnderlyingMonitor()
		time.sleep(SharedVars.UnderlyingMonitorReadingInterval)

def UnderlyingLoggingThread():
	while SharedVars.BackgroundRunning:
		if SharedVars.UnderlyingMonitorReadingIsActive and SharedVars.StorageIsActive:
			IbDataLoggerStorage.LogUnderlyingData()
		time.sleep(SharedVars.StorageWriteInterval)

def OptionMonitorThread(MonitorIndex):
	MyMonitorIndex = MonitorIndex
	MySubscriptionId = SharedVars.ActiveOptionMonitors[MonitorIndex]['SubscriptionId']
	while SharedVars.BackgroundRunning:
		if SharedVars.OptionMonitorReadingIsActive:
			Success, NewMonitorData = IbDataLoggerTws.ReadMonitor(MySubscriptionId)
			if not Success:
				IbDataLoggerUtilities.LogError('problem reading option monitor ID: ' + str(MySubscriptionId))
			else:
				SharedVars.ActiveOptionMonitors[MyMonitorIndex] = NewMonitorData
		else:
			break
		time.sleep(SharedVars.OptionMonitorReadingInterval)

def OptionLoggingThread(MonitorIndex):
	MyMonitorIndex = MonitorIndex
	while SharedVars.BackgroundRunning:
		if SharedVars.OptionMonitorReadingIsActive and SharedVars.StorageIsActive:
			IbDataLoggerStorage.LogOptionData(MyMonitorIndex)
		# if not SharedVars.OptionMonitorReadingIsActive:
		# 	break
		time.sleep(SharedVars.StorageWriteInterval)

def InitializeMonitorManagement():
	SharedVars.HighestStrikePriceToBeMonitored = SharedVars.InitialHighestToBe
	SharedVars.LowestStrikePriceToBeMonitored = SharedVars.InitialLowestToBe
	SharedVars.HighestStrikePriceBeingMonitored = SharedVars.InitialHighestBeing
	SharedVars.LowestStrikePriceBeingMonitored = SharedVars.InitialLowestBeing

def MonitorManagerThread():
	while SharedVars.BackgroundRunning:
		# The instantiation of the underlying data class sets the price to zero so we test for > 0.01 as an indicator that initial data has been
		# - received from the underlying IB subscription. Until we have an initial underlying price, we don't want to turn loose the automatic
		# - process to determine desired options and subscribe to them.
		if SharedVars.UnderlyingMonitorReadingIsActive and (SharedVars.UnderlyingMonitorData['Last']['Price'] > 0.01):
			# Establish the high and low strike prices of interest
			SharedVars.HighestStrikePriceToBeMonitored = max(SharedVars.HighestStrikePriceToBeMonitored, (IbDataLoggerUtilities.NearestStrikePriceAboveUnderlying() + (SharedVars.StrikePriceStep * SharedVars.StrikePriceRange)))
			SharedVars.LowestStrikePriceToBeMonitored = min(SharedVars.LowestStrikePriceToBeMonitored, (IbDataLoggerUtilities.NearestStrikePriceBelowUnderlying() - (SharedVars.StrikePriceStep * SharedVars.StrikePriceRange)))
			# Queue for starting any strike prices of interest which haven't already been queued and started
			# - The first time through, we have to start up all the strike prices from lowest to highest, then we just
			# - - check to see if the highest became higher or the lowest became lower.
			# - We identify "first time through" as "highest-being-monitored" being its initial value of -1.0
			if SharedVars.HighestStrikePriceBeingMonitored < 0:
				# This is the first time we're adding items to the "option-monitor-to-be-launched" queue
				CurrentStrikePrice = SharedVars.LowestStrikePriceToBeMonitored
				while CurrentStrikePrice <= SharedVars.HighestStrikePriceToBeMonitored:
					QueueStrikePrice(CurrentStrikePrice)
					CurrentStrikePrice += SharedVars.StrikePriceStep
			else:
				# Once the initial strike price range is started up, we expand it as needed to keep the extremities at the
				# - desired distance from the underlying as it moves through the day.
				while SharedVars.HighestStrikePriceToBeMonitored > SharedVars.HighestStrikePriceBeingMonitored:
					NextHigherStrikeToBeMonitored =	SharedVars.HighestStrikePriceBeingMonitored + SharedVars.StrikePriceStep
					QueueStrikePrice(NextHigherStrikeToBeMonitored)
					SharedVars.HighestStrikePriceBeingMonitored = NextHigherStrikeToBeMonitored
				while SharedVars.LowestStrikePriceToBeMonitored < SharedVars.LowestStrikePriceBeingMonitored:
					NextLowerStrikeToBeMonitored = SharedVars.LowestStrikePriceBeingMonitored - SharedVars.StrikePriceStep
					QueueStrikePrice(NextLowerStrikeToBeMonitored)
					SharedVars.LowestStrikePriceBeingMonitored = NextLowerStrikeToBeMonitored
			# Each time through the thread, start one queued item until the queue is empty
			if len(SharedVars.MonitorsToBeStarted) > 0:
				MonitorToStart = SharedVars.MonitorsToBeStarted.pop(0)
				IbDataLoggerTws.StartOptionMonitor(SharedVars.UnderlyingSymbol, MonitorToStart['ExpirationDate'], MonitorToStart['ContractRight'], MonitorToStart['StrikePrice'])
		time.sleep(SharedVars.OptionManagementRefreshInterval)
	# Process end-of-tracking now that threads have been signalled to terminate
	# ... First, traverse list of active monitors and end one of them each time through the loop
	# ......(i.e. back out of the monitor list by reversing the process of building the list)
	while len(SharedVars.ActiveOptionMonitors) > 0:
		# - unsubscribe the monitor from IbDataTap and TWS
		IbDataLoggerTws.CancelMonitor(SharedVars.ActiveOptionMonitors[0]['SubscriptionId'])
		# - remove it from the list of active monitors
		del SharedVars.ActiveOptionMonitors[0]
		time.sleep(SharedVars.OptionManagementRefreshInterval)
	# ... Second, unsubscribe from the underlying
	IbDataLoggerTws.UnsubscribeFromUnderlying()
	# ... Last, after some delay to allow completion of all the unscubscribing above, disconnect from TWS
	time.sleep(10 * SharedVars.OptionManagementRefreshInterval)
	IbDataLoggerTws.DisconnectFromTws()

def QueueStrikePrice(StrikePrice):
	# Update the limit markers
	if StrikePrice > SharedVars.HighestStrikePriceBeingMonitored:
		SharedVars.HighestStrikePriceBeingMonitored = StrikePrice
	if StrikePrice < SharedVars.LowestStrikePriceBeingMonitored:
		SharedVars.LowestStrikePriceBeingMonitored = StrikePrice
	# Queue the full set of monitors to cover the strike price being added
	for ExpirationDate in SharedVars.ExpirationDates:
		NewMonitorPut = IbDataLoggerClasses.QueuedMonitorToStartClass()
		NewMonitorCall = IbDataLoggerClasses.QueuedMonitorToStartClass()
		NewMonitorPut['StrikePrice'] = StrikePrice
		NewMonitorPut['ContractRight'] = 'PUT'
		NewMonitorPut['ExpirationDate'] = ExpirationDate
		SharedVars.MonitorsToBeStarted.append(NewMonitorPut)
		NewMonitorCall['StrikePrice'] = StrikePrice
		NewMonitorCall['ContractRight'] = 'CALL'
		NewMonitorCall['ExpirationDate'] = ExpirationDate
		SharedVars.MonitorsToBeStarted.append(NewMonitorCall)

# def EndProgramThread():
# 	while SharedVars.BackgroundRunning:
# 		if datetime.datetime.now() > SharedVars.TimeToEndBackground:
# 			SharedVars.BackgroundRunning = False
# 		time.sleep(SharedVars.CheckForEndOfProgramInterval)

if __name__ == '__main__':
	Main()
