import SharedVars
import time
import threading
import IbDataLogger
import IbDataLoggerClasses
import IbDataLoggerUtilities
import IbDataLoggerDataComm

import json

def GetIbDataTapStatus():
	SharedVars.StatusSpinner = IbDataLoggerUtilities.NextSpinner(SharedVars.StatusSpinner)
	Success, IncomingAvro = IbDataLoggerDataComm.TcpExchange(b'', 'StatusControl', 'ReadStatus', 'StatusControl', 'ReadStatus')
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to tcpexchange in GetIbDataTapStatus()')
		return
	Success, status = IbDataLoggerDataComm.DeserializeObject(IncomingAvro)
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to deserialize in GetIbDataTapStatus()')
		return
	SharedVars.IbDataTapStatus = status

def SubscribeToUnderlying():
	StartUnderlyingMonitorRequest = IbDataLoggerClasses.StartUnderlyingMonitorRequestClass()
	StartUnderlyingMonitorRequest['Symbol'] = SharedVars.UnderlyingSymbol
	StartUnderlyingMonitorRequest['SymbolType'] = SharedVars.UnderlyingSymbolType
	Success, SerializedBuffer = IbDataLoggerDataComm.SerializeObject(StartUnderlyingMonitorRequest, SharedVars.StartUnderlyingMonitorRequestWriterSchema)
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to serialize in SubscribeToUnderlying()')
		return
	PacketDataBuffer = SerializedBuffer
	Success, IncomingAvro = IbDataLoggerDataComm.TcpExchange(PacketDataBuffer, 'Monitor', 'StartUnderlying', 'StatusControl', 'CommandAcknowledge')
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to tcpexchange in SubscribeToUnderlying()')
		return
	Success, Acknowledgement = IbDataLoggerDataComm.DeserializeObject(IncomingAvro)
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to deserialize in SubscribeToUnderlying()')
		return
	SharedVars.UnderlyingSubscriptionId = Acknowledgement['SubscriptionId']

def UnsubscribeFromUnderlying():
	CancelMonitor(SharedVars.UnderlyingSubscriptionId)
	SharedVars.UnderlyingMonitorReadingIsActive = False

def ReadUnderlyingMonitor():
	SharedVars.UnderlyingSpinner = IbDataLoggerUtilities.NextSpinner(SharedVars.UnderlyingSpinner)
	Success, MonitorData = ReadMonitor(SharedVars.UnderlyingSubscriptionId)
	if Success:
		SharedVars.UnderlyingMonitorData = MonitorData

def SubscribeToOption(Symbol, ExpirationDate, ContractRight, StrikePrice):
	StartContractMonitorRequest = IbDataLoggerClasses.StartContractMonitorRequestClass()
	StartContractMonitorRequest['Symbol'] = Symbol
	StartContractMonitorRequest['ExpirationDate'] = ExpirationDate
	StartContractMonitorRequest['ContractRight'] = ContractRight
	StartContractMonitorRequest['StrikePrice'] = StrikePrice
	Success, SerializedBuffer = IbDataLoggerDataComm.SerializeObject(StartContractMonitorRequest, SharedVars.StartContractMonitorRequestWriterSchema)
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to serialize in SubscribeToOption()')
		return False, 0
	PacketDataBuffer = SerializedBuffer
	Success, IncomingAvro = IbDataLoggerDataComm.TcpExchange(PacketDataBuffer, 'Monitor', 'StartOption', 'StatusControl', 'CommandAcknowledge')
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to tcpexchange in SubscribeToOption()')
		return False, 0
	Success, Acknowledgement = IbDataLoggerDataComm.DeserializeObject(IncomingAvro)
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to deserialize in SubscribeToOption()')
		return False, 0
	NewOptionMonitor = IbDataLoggerClasses.MonitorDataClass()
	NewOptionMonitor['SubscriptionId'] = Acknowledgement['SubscriptionId']
	return True, NewOptionMonitor

def StartOptionMonitor(Symbol, ExpirationDate, ContractRight, StrikePrice):
	 Success, OptionMonitorData = SubscribeToOption(Symbol, ExpirationDate, ContractRight, StrikePrice)
	 if not Success:
	 	IbDataLoggerUtilities.LogError('In StartOptionMonitor(), unable to subscribe to: ' + Symbol + str(ExpirationDate) + ContractRight + str(StrikePrice))
	 	return
	 OptionMonitorData['Symbol'] = Symbol
	 OptionMonitorData['ExpirationDate'] = ExpirationDate
	 OptionMonitorData['ContractRight'] = ContractRight
	 OptionMonitorData['StrikePrice'] = StrikePrice
	 SharedVars.ActiveOptionMonitors.append(OptionMonitorData)
	 NewOptionMonitorListIndex = len(SharedVars.ActiveOptionMonitors)-1
	 OptionMonitorThr = threading.Thread(target=IbDataLogger.OptionMonitorThread, args=(NewOptionMonitorListIndex,)).start()
	 OptionLoggingThr = threading.Thread(target=IbDataLogger.OptionLoggingThread, args=(NewOptionMonitorListIndex,)).start()

def ReadMonitor(IdToRead):
	ReadMonitorRequest = IbDataLoggerClasses.ReadMonitorRequestClass()
	ReadMonitorRequest['SubscriptionIdToRead'] = IdToRead
	Success, SerializedBuffer = IbDataLoggerDataComm.SerializeObject(ReadMonitorRequest, SharedVars.ReadMonitorRequestWriterSchema)
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to serialize in ReadMonitor(' + str(IdToRead) + ')')
		return False, 0
	PacketDataBuffer = SerializedBuffer

	Success, IncomingAvro = IbDataLoggerDataComm.TcpExchange(PacketDataBuffer, 'Monitor', 'ReadMonitor', 'Monitor', 'ReadMonitor')
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to tcpexchange in ReadMonitor(' + str(IdToRead) + ')')
		return False, 0
	Success, monitorData = IbDataLoggerDataComm.DeserializeObject(IncomingAvro)
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to deserialize in ReadMonitor(' + str(IdToRead) + ')')
		return False, 0
	return True, monitorData

def CancelMonitor(IdToCancel):
	CancelMonitorRequest = IbDataLoggerClasses.CancelMonitorRequestClass()
	CancelMonitorRequest['SubscriptionIdToCancel'] = IdToCancel
	Success, SerializedBuffer = IbDataLoggerDataComm.SerializeObject(CancelMonitorRequest, SharedVars.CancelMonitorRequestWriterSchema)
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to serialize in CancelMonitor()')
		return
	PacketDataBuffer = SerializedBuffer
	Success, IncomingAvro = IbDataLoggerDataComm.TcpExchange(PacketDataBuffer, 'Monitor', 'CancelMonitor', 'StatusControl', 'CommandAcknowledge')
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to tcpexchange in CancelMonitor()')
		return
	Success, acknowledgement = IbDataLoggerDataComm.DeserializeObject(IncomingAvro)
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to deserialize in CancelMonitor()')
		return

def ConnectToTws():
	#First send the currently configured connection parameters to IbDataLink
	SetConnectionParametersCommand = IbDataLoggerClasses.ControlCommandClass()
	SetConnectionParametersCommand['Command'] = 'SetConnectionParameters'
	SetConnectionParametersCommand['IntegerParameter'] = SharedVars.TwsPreferredClientId
	SetConnectionParametersCommand['IntegerParameter2'] = SharedVars.TwsConnectionPortNumber
	SetConnectionParametersCommand['MarketDataType'] = SharedVars.TwsMarketDataTiming.name
	Success, SerializedBuffer = IbDataLoggerDataComm.SerializeObject(SetConnectionParametersCommand, SharedVars.ControlCommandWriterSchema)
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to serialize in ConnectToTws()-1')
		return
	PacketDataBuffer = SerializedBuffer
	Success, IncomingAvro = IbDataLoggerDataComm.TcpExchange(PacketDataBuffer, 'StatusControl', 'ControlCommand', 'StatusControl', 'CommandAcknowledge')
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to tcpexchange in ConnectToTws()-1')
		return
	Success, acknowledgement = IbDataLoggerDataComm.DeserializeObject(IncomingAvro)
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to deserialize in ConnectToTws()-1')
		return
	ConnectToTwsCommand = IbDataLoggerClasses.ControlCommandClass()
	ConnectToTwsCommand['Command'] = 'ConnectToTws'
	Success, SerializedBuffer = IbDataLoggerDataComm.SerializeObject(ConnectToTwsCommand, SharedVars.ControlCommandWriterSchema)
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to serialize in ConnectToTws()-2')
		return
	PacketDataBuffer = SerializedBuffer
	Success, IncomingAvro = IbDataLoggerDataComm.TcpExchange(PacketDataBuffer, 'StatusControl', 'ControlCommand', 'StatusControl', 'CommandAcknowledge')
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to tcpexchange in ConnectToTws()-2')
		return
	Success, acknowledgement = IbDataLoggerDataComm.DeserializeObject(IncomingAvro)
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to deserialize in ConnectToTws()-2')
		return

def DisconnectFromTws():
	ConnectToTwsCommand = IbDataLoggerClasses.ControlCommandClass()
	ConnectToTwsCommand['Command'] = 'DisconnectFromTws'
	Success, SerializedBuffer = IbDataLoggerDataComm.SerializeObject(ConnectToTwsCommand, SharedVars.ControlCommandWriterSchema)
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to serialize in DisconnectFromTws()')
		return
	PacketDataBuffer = SerializedBuffer
	Success, IncomingAvro = IbDataLoggerDataComm.TcpExchange(PacketDataBuffer, 'StatusControl', 'ControlCommand', 'StatusControl', 'CommandAcknowledge')
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to tcpexchange in DisconnectFromTws()')
		return
	Success, acknowledgement = IbDataLoggerDataComm.DeserializeObject(IncomingAvro)
	if not Success:
		IbDataLoggerUtilities.LogError('Failed to deserialize in DisconnectFromTws()')
		return

