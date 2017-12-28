import SharedVars
import IbDataLoggerEnums

class ExpirationDateClass(dict):
	def __init__(self):
	# def __init__(self, *args, **kwargs):
		self['year'] = 1
		self['month'] = 1
		self['day'] = 2016

class QueuedMonitorToStartClass(dict):
	def __init__(self):
		ed = ExpirationDateClass()
		self['StrikePrice'] = 1234.0
		self['ContractRight'] = 'PUT'
		self['ExpirationDate'] = ed

class StartContractMonitorRequestClass(dict):
	def __init__(self):
	# def __init__(self, *args, **kwargs):
		ed = ExpirationDateClass()
		self['Symbol'] = ''
		self['ExpirationDate'] = ed
		self['ContractRight'] = ''
		self['StrikePrice'] = 1.0
		self['RequestedSubscriptionId'] = 0

class StartMonitorResultClass(dict):
	def __init__(self):
	# def __init__(self, *args, **kwargs):
		self['RequestSuccessCode'] = IbDataLoggerEnums.StartRequestResultReturnCode['NotSpecified'].name
		self['RequestErrorMessage'] = ''
		self['AssignedSubscriptionId'] = 0
		self['ThisIsTheUnderlying'] = False

class CancelMonitorRequestClass(dict):
	def __init__(self):
	# def __init__(self, *args, **kwargs):
		self['SubscriptionIdToCancel'] = 0

class CancelMonitorResultClass(dict):
	def __init__(self):
	# def __init__(self, *args, **kwargs):
		self['RequestSuccessCode'] = IbDataLoggerEnums.CancelRequestResultReturnCode['NotSpecified'].name
		self['SubscriptionId'] = 0

class ReadMonitorRequestClass(dict):
	def __init__(self):
	# def __init__(self, *args, **kwargs):
		self['SubscriptionIdToRead'] = 0
		self['SequenceNumber'] = 0

class OptionCompStructureClass(dict):
	def __init__(self):
	# def __init__(self, *args, **kwargs):
		self['Price'] = 0.0
		self['Size'] = 0
		self['ImpliedVolatility'] = 0.0
		self['Delta'] = 0.0
		self['Theta'] = 0.0
		self['Gamma'] = 0.0
		self['Vega'] = 0.0

class MonitorDataClass(dict):
	def __init__(self):
	# def __init__(self, *args, **kwargs):
		ed = ExpirationDateClass()
		aoc = OptionCompStructureClass()
		boc = OptionCompStructureClass()
		loc = OptionCompStructureClass()
		moc = OptionCompStructureClass()
		self['MonitorStatus'] = IbDataLoggerEnums.RequestedMonitorStatus['NotSpecified'].name
		self['RequestSuccessCode'] = IbDataLoggerEnums.ReadRequestResultReturnCode['NotSpecified'].name
		self['SequenceNumber'] = 0
		self['MonitorStartMilliseconds'] = 0
		self['MonitorLastUpdateMilliseconds'] = 0
		self['MonitorUpdateCount'] = 0
		self['Symbol'] = ''
		self['ExpirationDate'] = ed
		self['ContractRight'] = ''
		self['StrikePrice'] = 0.0
		self['SubscriptionId'] = 0
		self['Ask'] = aoc
		self['Bid'] = boc
		self['Last'] = loc
		self['Model'] = moc
		self['Volume'] = 0
		self['TimeStamp'] = ''
		self['Open'] = 0.0
		self['High'] = 0.0
		self['Low'] = 0.0
		self['Close'] = 0.0

class StartUnderlyingMonitorRequestClass(dict):
	def __init__(self):
	# def __init__(self, *args, **kwargs):
		self['Symbol'] = ''
		self['SymbolType'] = ''
		self['RequestedSubscriptionId'] = 0


class ControlCommandClass(dict):
	def __init__(self):
	# def __init__(self, *args, **kwargs):
		self['Command'] = IbDataLoggerEnums.CommandType['NotSpecified'].name
		self['IntegerParameter'] = 0
		self['IntegerParameter2'] = 0
		self['LongParameter'] = 0
		self['DoubleParameter'] =  0.0
		self['BoolParameter'] = False
		self['StringParameter'] = ''
		self['MarketDataType'] = IbDataLoggerEnums.MarketDataTimingType['NotSpecified'].name

class CommandAcknowledgementClass(dict):
	def __init__(self):
	# def __init__(self, *args, **kwargs):
		self['SubscriptionId'] = 0

class StatusReportClass(dict):
	def __init__(self):
	# def __init__(self, *args, **kwargs):
		self['MarketDataType'] = IbDataLoggerEnums.MarketDataTimingType['NotSpecified'].name
		self['TwsPreferredClientId'] = 0
		self['TwsPortNumber'] = 0
		self['IbDataTapConnectionStatus'] = IbDataLoggerEnums.ConnectionStatus['NotSpecified'].name
		self['NumberOfIdsOnMonitorList'] = 0
		self['DiagnosticInteger'] = 0

