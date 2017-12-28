import SharedVars

from enum import Enum

class DaySegment(Enum):
	NotSpecified = 0
	MorningBeforeTrading = 1
	TradingTime = 2
	WaitingForTomorrow = 3

class IpMode(Enum):
	Local = 0
	Distant = 1

class SessionType(Enum):
	NotSpecified = 0
	StatusControl = 1
	Monitor = 2

class PacketTask(Enum):
	NotSpecified = 0
	ReadStatus = 1
	ControlCommand = 2
	CommandAcknowledge = 3
	StartUnderlying = 4
	StartOption = 5
	ReadMonitor = 6
	CancelMonitor = 7
	EndSession = 8

class OperatingModes(Enum):
	Development = 0
	Production = 1

class StartRequestResultReturnCode(Enum):
	NotSpecified = 0
	Success = 1
	IdAlreadyInUse = 2
	UnableToConnectToIB = 3

class CancelRequestResultReturnCode(Enum):
	NotSpecified = 0
	Success = 1
	IdNotFound = 2

class RequestedMonitorStatus(Enum):
	NotSpecified = 0
	Pending = 1
	Active = 2
	RejectedByIB = 3

class ReadRequestResultReturnCode(Enum):
	NotSpecified = 0
	Success = 1
	IdNotOnActiveList = 2

class CommandType(Enum):
	NotSpecified = 0
	SetConnectionParameters = 1
	ConnectToTws = 2
	DisconnectFromTws = 3

class MarketDataTimingType(Enum):
	NotSpecified = 0
	Live = 1
	Frozen = 2
	Delayed = 3
	DelayedFrozen = 4

class ConnectionStatus(Enum):
	NotSpecified = 0
	ConnectionAttemptFailed = 1
	Connected = 2
	ConnectionClosed = 3

