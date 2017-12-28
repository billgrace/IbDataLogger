import SharedVars
import IbDataLoggerEnums
import IbDataLoggerUtilities
import IbDataLoggerGui
import os, sys
import datetime
import threading
import io
import json
import avro.datafile
import avro.schema
import avro.io

def	PrepareDiskStorage():
	DailyPath = format(datetime.date.today().year, '04') + '-' + format(datetime.date.today().month, '02') + '-' + format(datetime.date.today().day, '02')
	SharedVars.StoragePath = SharedVars.StorageRootPath + '/' + DailyPath
	try:
		os.makedirs(SharedVars.StoragePath, exist_ok=True)
	except OSError:
		IbDataLoggerUtilities.LogError('Unable to create storage directory: ' + SharedVars.StoragePath + ', exception: ' + str(OSError))

def ReadPreferencesFile():
	try:
		PreferenceFile = open('Preferences.cfg', 'r')
		LineNumber = 0
		for Line in PreferenceFile:
			LineNumber += 1
			if Line[0] == '#':
				continue
			try:
				UnstrippedKeyWord, UnstrippedKeyValue = Line.split('=')
				KeyWord = UnstrippedKeyWord.strip()
				KeyValue = UnstrippedKeyValue.strip()
				if(KeyWord == 'StorageRootPath'):
					SharedVars.StorageRootPath = KeyValue
					print('SharedVars.StorageRootPath: ' + str(SharedVars.StorageRootPath))
				elif(KeyWord == 'MyLoggerName'):
					SharedVars.MyLoggerName = KeyValue
					# print('SharedVars.MyLoggerName: ' + str(SharedVars.MyLoggerName))
				elif(KeyWord == 'TargetTapName'):
					SharedVars.TargetTapName = KeyValue
					# print('SharedVars.TargetTapName: ' + str(SharedVars.TargetTapName))
				elif(KeyWord == 'DistantBeaconUrl'):
					SharedVars.DistantBeaconUrl = KeyValue
					# print('SharedVars.DistantBeaconUrl: ' + str(SharedVars.DistantBeaconUrl))
				elif(KeyWord == 'LocalBeaconUrl'):
					SharedVars.LocalBeaconUrl = KeyValue
					# print('SharedVars.LocalBeaconUrl: ' + str(SharedVars.LocalBeaconUrl))
				elif(KeyWord == 'TargetTapIsLocal'):
					SharedVars.TargetTapIsLocal = KeyValue
					# print('SharedVars.TargetTapIsLocal: ' + str(SharedVars.TargetTapIsLocal))
				elif(KeyWord == 'StatusReportingInterval'):
					SharedVars.StatusReportingInterval = float(KeyValue)
					# print('SharedVars.StatusReportingInterval: ' + str(SharedVars.StatusReportingInterval))
				elif(KeyWord == 'UnderlyingMonitorReadingInterval'):
					SharedVars.UnderlyingMonitorReadingInterval = float(KeyValue)
					# print('SharedVars.UnderlyingMonitorReadingInterval: ' + str(SharedVars.UnderlyingMonitorReadingInterval))
				elif(KeyWord == 'UnderlyingSymbol'):
					SharedVars.UnderlyingSymbol = KeyValue
					# print('SharedVars.UnderlyingSymbol: ' + str(SharedVars.UnderlyingSymbol))
				elif(KeyWord == 'UnderlyingSymbolType'):
					SharedVars.UnderlyingSymbolType = KeyValue
					# print('SharedVars.UnderlyingSymbolType: ' + str(SharedVars.UnderlyingSymbolType))
				elif(KeyWord == 'StrikePriceStep'):
					SharedVars.StrikePriceStep = float(KeyValue)
					# print('SharedVars.StrikePriceStep: ' + str(SharedVars.StrikePriceStep))
				elif(KeyWord == 'StrikePriceRange'):
					SharedVars.StrikePriceRange = int(KeyValue)
					# print('SharedVars.StrikePriceRange: ' + str(SharedVars.StrikePriceRange))
				elif(KeyWord == 'ExpirationDateRange'):
					SharedVars.ExpirationDateRange = int(KeyValue)
					# print('SharedVars.ExpirationDateRange: ' + str(SharedVars.ExpirationDateRange))
				elif(KeyWord == 'ContractMonitorReadingInterval'):
					SharedVars.ContractMonitorReadingInterval = float(KeyValue)
					# print('SharedVars.ContractMonitorReadingInterval: ' + str(SharedVars.ContractMonitorReadingInterval))
				elif(KeyWord == 'StorageWriteInterval'):
					SharedVars.StorageWriteInterval = float(KeyValue)
					# print('SharedVars.StorageWriteInterval: ' + str(SharedVars.StorageWriteInterval))
				elif(KeyWord == 'GuiBackgroundManagementInterval'):
					SharedVars.GuiBackgroundManagementInterval = KeyValue
					# print('SharedVars.GuiBackgroundManagementInterval: ' + str(SharedVars.GuiBackgroundManagementInterval))
				elif(KeyWord == 'GuiRefreshInterval'):
					SharedVars.GuiRefreshInterval = KeyValue
					# print('SharedVars.GuiRefreshInterval: ' + str(SharedVars.GuiRefreshInterval))
				elif(KeyWord == 'TradingDayStartTime'):
					StartTimeComponents = KeyValue.split(':')
					SharedVars.TradingDayStartTimeHour = int(StartTimeComponents[0])
					SharedVars.TradingDayStartTimeMinute = int(StartTimeComponents[1])
					# print('SharedVars.TradingDayStartTimeHour:Minute- {0:02d}:{1:02d}'.format(SharedVars.TradingDayStartTimeHour, SharedVars.TradingDayStartTimeMinute))
				elif(KeyWord == 'TradingDayEndTime'):
					EndTimeComponents = KeyValue.split(':')
					SharedVars.TradingDayEndTimeHour = int(EndTimeComponents[0])
					SharedVars.TradingDayEndTimeMinute = int(EndTimeComponents[1])
					# print('SharedVars.TradingDayEndTimeHour:Minute- {0:02d}:{1:02d}'.format(SharedVars.TradingDayEndTimeHour, SharedVars.TradingDayEndTimeMinute))
				else:
					IbDataLoggerUtilities.LogError('unrecognized preference.cfg KeyWord: ' + KeyWord + ' on line #' + str(LineNumber))
			except Exception as e:
				IbDataLoggerUtilities.LogError('problem parsing preference.cfg line #' + str(LineNumber) + ': ' + Line + ', exception: ' + str(e))
	except Exception as e:
		IbDataLoggerUtilities.LogError('unable to open Preferences.cfg - ' + str(e))

def LogTestFile():
	FileName = SharedVars.UnderlyingSymbol + '-TestFile'
	try:
		FilePathName = SharedVars.StoragePath + '/' + FileName
		print('Test file path: ' + FilePathName)
		File = open(FilePathName, 'a+')
		File.write('This is a line of text in the test file.\n')
		File.close()
	except Exception as e:
		IbDataLoggerUtilities.LogError('Exception in LogTestFile: ' + str(e))

def LogUnderlyingData():
	FileName = SharedVars.UnderlyingSymbol + '-Underlying'
	LogAMonitor(FileName, SharedVars.UnderlyingMonitorData)

def LogOptionData(ActiveMonitorListIndex):
	UnderlyingSymbol = SharedVars.UnderlyingSymbol
	SubscriptionId = SharedVars.ActiveOptionMonitors[ActiveMonitorListIndex]['SubscriptionId']
	ExpirationDate = SharedVars.ActiveOptionMonitors[ActiveMonitorListIndex]['ExpirationDate']
	StrikePrice = int(SharedVars.ActiveOptionMonitors[ActiveMonitorListIndex]['StrikePrice'])
	ContractRight = SharedVars.ActiveOptionMonitors[ActiveMonitorListIndex]['ContractRight']
	FileName = '{0}-{1:4d}-{2:02d}-{3:02d}-{4}-{5}'.format(UnderlyingSymbol,
															ExpirationDate['year'], ExpirationDate['month'], ExpirationDate['day'],
															StrikePrice, ContractRight)
	LogAMonitor(FileName, SharedVars.ActiveOptionMonitors[ActiveMonitorListIndex])

def LogAMonitor(FileName, MonitorData):
	LogAMonitorThr = threading.Thread(target=LogAMonitorThread, args=(FileName, MonitorData)).start()

def LogAMonitorThread(FileName, MonitorData):
	Time = datetime.datetime.now()
	TimeString = '{0:02d}-{1:02d}-{2:02d}-{3:03d}'.format(Time.hour, Time.minute, Time.second, int(Time.microsecond/1000))

	AvroSerializationBuffer = io.BytesIO()
	ByteBuffer = bytes()
	try:
		writer = avro.datafile.DataFileWriter(AvroSerializationBuffer, avro.io.DatumWriter(), SharedVars.MonitorDataReaderSchema)
		writer.append(MonitorData)
		writer.flush()
		AvroSerializationBuffer.seek(0)
		ByteBuffer = AvroSerializationBuffer.getvalue()
		MonitorDataString = str(ByteBuffer)
		AvroSerializationBuffer.close()
	except Exception as e:
		AvroSerializationBuffer.close()
		IbDataLoggerUtilities.LogError('Exception in LogAMonitor/Avro: ' + str(e))
	try:
		File = open(SharedVars.StoragePath + '/' + FileName, 'a+')
		File.write(TimeString + '---' + MonitorDataString + '\n')
		File.close()
	except Exception as e:
		IbDataLoggerUtilities.LogError('Exception in LogAMonitor/File: ' + str(e))
