import sys
import subprocess
from requests import post
import json
import time
import datetime
import math
import SharedVars
import IbDataLoggerEnums
import IbDataLoggerClasses

def RebootMyself():
	subprocess.call('sudo reboot', shell = True)

def DelayMinutes(NumberOfMinutes):
	time.sleep(NumberOfMinutes * 60)

def LogTradingDayStart():
	logEntryJsonObject = {'logged_by_type':'logger', 'logged_by_name':SharedVars.MyLoggerName, 'log_entry':'Started tracking the market'}
	p = post('http://' + SharedVars.DistantBeaconUrl + '/beacon/OperatingLog.php', data = {'operating_log_json':json.dumps(logEntryJsonObject)})
	p = post('http://' + SharedVars.LocalBeaconUrl + '/beacon/OperatingLog.php', data = {'operating_log_json':json.dumps(logEntryJsonObject)})

def LogTradingDayEnd():
	logEntryJsonObject = {'logged_by_type':'logger', 'logged_by_name':SharedVars.MyLoggerName, 'log_entry':'Finished tracking the market'}
	p = post('http://' + SharedVars.DistantBeaconUrl + '/beacon/OperatingLog.php', data = {'operating_log_json':json.dumps(logEntryJsonObject)})
	p = post('http://' + SharedVars.LocalBeaconUrl + '/beacon/OperatingLog.php', data = {'operating_log_json':json.dumps(logEntryJsonObject)})

def GetBeaconUrl():
	if SharedVars.TargetTapIsLocal:
		return SharedVars.LocalBeaconUrl
	else:
		return SharedVars.DistantBeaconUrl

def GetTapAddress():
	GetTapAddressJsonObject = {'target_tap_name':SharedVars.TargetTapName}
	p = post('http://' + GetBeaconUrl() + '/beacon/TapNameToAddress.php', data = {'tap_name_to_address_json':json.dumps(GetTapAddressJsonObject)})
	ResponseString = p.text
	if ResponseString[0:9] == 'Address: ':
		AddressJson = ResponseString[9:]
		AddressObject = json.loads(AddressJson)
		SharedVars.IbDataLinkIpAddress = AddressObject['targetIpAddress']
		SharedVars.IbDataLinkIpPortNumber = AddressObject['targetPortNumber']
		SharedVars.IbDataLinkIpLastUpdatedAt = AddressObject['lastBeaconTimeStamp']
	elif ResponseString[0:5] == 'Error':
		print('Error trying to get IbDataLink IP address: ' + ResponseString[8:])
	else:
		print('Unknown response trying to get IbDataLink address: ' + str(ResponseString))

def GetExpirationDaysFromSymbolMonth(SymbolDateString):
	GetDaysQueryJsonObject = {'symbol_date_string':SymbolDateString}
	p = post('http://' + GetBeaconUrl() + '/beacon/MarketDates.php', data = {'market_date_query_json':json.dumps(GetDaysQueryJsonObject)})
	ResponseString = p.text
	print(ResponseString)
	if ResponseString[0:7] == 'Dates: ':
		DatesJson = ResponseString[7:]
		FullDateString = json.loads(DatesJson)
		CommaDelimitedDateString = FullDateString['listOfDates']
		ArrayOfDates = CommaDelimitedDateString.split(',')
		return ArrayOfDates
	elif ResponseString[0:5] == 'Error':
		print('Error trying to get expiration days (' + SymbolDateString + '): ' + ResponseString[8:])
		return [0,]
	else:
		print('Unknown response trying to get expiration days (' + SymbolDateString + '): ' + str(ResponseString))
		return [0,]

def YearMonthString(year, month):
	YearString = format(year, '4d')
	MonthString = format(month, '02d')
	return YearString + '-' + MonthString

def IsItATradingDay(year, month, day):
	# (We get the list of trading days using the same mechanism that is used to get the list of a month's
	#  expiration dates by setting the symbol to "Trading")
	TodayYearMonthString = YearMonthString(year, month)
	TradingDaySymbolDateString = 'Trading-' + TodayYearMonthString
	ThisMonthsTradingDays = GetExpirationDaysFromSymbolMonth(TradingDaySymbolDateString)
	if str(day) in ThisMonthsTradingDays:
		return True
	else:
		return False

def IsTodayATradingDay():
	ThisDay = datetime.date.today()
	SharedVars.TodayIsATradingDay = IsItATradingDay(ThisDay.year, ThisDay.month, ThisDay.day)
	return SharedVars.TodayIsATradingDay

def EstablishExpirationDates():
	# Get (from the beacon site) the list of expiration days for:
	#   this month
	#   next month
	#   the following month
	#  and make a list of all the resulting expiration date structures.
	# Scan the list and take the needed number of them that aren't earlier than today
	#  and put these on the working list.
	# clear our list of expiration dates
	SharedVars.ExpirationDates.clear()
	# get an 'expiration date' equal to today
	Today = IbDataLoggerClasses.ExpirationDateClass()
	Today['year'] = datetime.date.today().year
	Today['month'] = datetime.date.today().month
	Today['day'] = datetime.date.today().day
	# Make symbol_date strings for this month, next month and the following month
	ThisMonthYearNumber = datetime.date.today().year
	ThisMonthMonthNumber = datetime.date.today().month
	if ThisMonthMonthNumber == 12:
		NextMonthYearNumber = ThisMonthYearNumber + 1
		NextMonthMonthNumber = 1
	else:
		NextMonthYearNumber = ThisMonthYearNumber
		NextMonthMonthNumber = ThisMonthMonthNumber + 1
	if NextMonthMonthNumber == 12:
		FollowingMonthYearNumber = NextMonthYearNumber + 1
		FollowingMonthMonthNumber = 1
	else:
		FollowingMonthYearNumber = NextMonthYearNumber
		FollowingMonthMonthNumber = NextMonthMonthNumber + 1
	ThisMonthSymbolDateString = SharedVars.UnderlyingSymbol + '-' + YearMonthString(ThisMonthYearNumber, ThisMonthMonthNumber)
	NextMonthSymbolDateString = SharedVars.UnderlyingSymbol + '-' + YearMonthString(NextMonthYearNumber, NextMonthMonthNumber)
	FollowingMonthSymbolDateString = SharedVars.UnderlyingSymbol + '-' + YearMonthString(FollowingMonthYearNumber, FollowingMonthMonthNumber)
	ThisMonthExpirationDays = GetExpirationDaysFromSymbolMonth(ThisMonthSymbolDateString)
	if ThisMonthExpirationDays[0] == 0:
		print('Got a zero day for this month expiration days')
		return
	else:
		# Traverse the list of expiration dates we got for this month
		for day in ThisMonthExpirationDays:
			# Make an expiration date for this day
			NewExpirationDate = IbDataLoggerClasses.ExpirationDateClass()
			NewExpirationDate['year'] = ThisMonthYearNumber
			NewExpirationDate['month'] = ThisMonthMonthNumber
			NewExpirationDate['day'] = int(day)
			if CompareExpirationDates(Today, NewExpirationDate) == -1:
				#Today is later than this expiration date, so skip it
				continue
			# Today is not later than this expiration date so add it to the list
			SharedVars.ExpirationDates.append(NewExpirationDate)
			# If the list is now long enough, we're done
			if len(SharedVars.ExpirationDates) >= SharedVars.ExpirationDateRange:
				break
	# OK, we've traversed the expiration dates for this month. Did we get enough of them?
	if len(SharedVars.ExpirationDates) >= SharedVars.ExpirationDateRange:
		return
	# We still need more expiration dates....
	NextMonthExpirationDays = GetExpirationDaysFromSymbolMonth(NextMonthSymbolDateString)
	if NextMonthExpirationDays[0] == 0:
		print('Got a zero day for this month expiration days')
		return
	else:
		# Traverse the list of expiration dates we got for this month
		for day in NextMonthExpirationDays:
			# Make an expiration date for this day
			NewExpirationDate = IbDataLoggerClasses.ExpirationDateClass()
			NewExpirationDate['year'] = NextMonthYearNumber
			NewExpirationDate['month'] = NextMonthMonthNumber
			NewExpirationDate['day'] = int(day)
			if CompareExpirationDates(Today, NewExpirationDate) == -1:
				#Today is later than this expiration date, so skip it
				continue
			# Today is not later than this expiration date so add it to the list
			SharedVars.ExpirationDates.append(NewExpirationDate)
			# If the list is now long enough, we're done
			if len(SharedVars.ExpirationDates) >= SharedVars.ExpirationDateRange:
				break
	# OK, we've traversed the expiration dates for this month. Did we get enough of them?
	if len(SharedVars.ExpirationDates) >= SharedVars.ExpirationDateRange:
		return
	# We STILL need more expiration dates....
	FollowingMonthExpirationDays = GetExpirationDaysFromSymbolMonth(FollowingMonthSymbolDateString)
	if FollowingMonthExpirationDays[0] == 0:
		print('Got a zero day for this month expiration days')
		return
	else:
		# Traverse the list of expiration dates we got for this month
		for day in FollowingMonthExpirationDays:
			# Make an expiration date for this day
			NewExpirationDate = IbDataLoggerClasses.ExpirationDateClass()
			NewExpirationDate['year'] = FollowingMonthYearNumber
			NewExpirationDate['month'] = FollowingMonthMonthNumber
			NewExpirationDate['day'] = int(day)
			if CompareExpirationDates(Today, NewExpirationDate) == -1:
				#Today is later than this expiration date, so skip it
				continue
			# Today is not later than this expiration date so add it to the list
			SharedVars.ExpirationDates.append(NewExpirationDate)
			# If the list is now long enough, we're done
			if len(SharedVars.ExpirationDates) >= SharedVars.ExpirationDateRange:
				break
	# OK, we've traversed the expiration dates for this month. Did we get enough of them?
	if len(SharedVars.ExpirationDates) >= SharedVars.ExpirationDateRange:
		return
	# !!!! I give up !!!! MAYBE we'll want to support expiration dates more than 2 months ahead....someday...
	print('Unable to obtain enough expiration dates in this, next and following months.....')

def CompareExpirationDates(Date1, Date2):
	# If other Date1 is later, return -1; if equal; return 0, if earlier, return 1
	try:
		if Date1['year'] > Date2['year']:
			return -1
		if Date1['year'] < Date2['year']:
			return 1
		if Date1['month'] > Date2['month']:
			return -1
		if Date1['month'] < Date2['month']:
			return 1
		if Date1['day'] > Date2['day']:
			return -1
		if Date1['day'] < Date2['day']:
			return 1
		return 0
	except Exception as e:
		LogError('problem comparing expiration dates - ' + str(e))
		# print('Date1: ' + str(Date1) + ', Date2: ' + str(Date2))

def NearestStrikePriceBelowUnderlying():
	# divide underlying by StrikePriceStep, take only the integer part of the result & multiply it by StrikePriceStep
	working = (SharedVars.UnderlyingMonitorData['Last']['Price'] / SharedVars.StrikePriceStep)
	working = math.floor(working)
	return working * SharedVars.StrikePriceStep

def NearestStrikePriceAboveUnderlying():
	return NearestStrikePriceBelowUnderlying() + SharedVars.StrikePriceStep

def NextSpinner(Spinner):
	if '-' == Spinner:
		return '/'
	if '/' == Spinner:
		return'|'
	if '|' == Spinner:
		return '\\'
	else:
		return '-'

def LogError(message):
	ErrorTimeStamp = datetime.datetime.now()
	ErrorTimeString = '{0:%A} {0:%B} {0:%d}, {0:%Y} @ {0:%I:%M%p} '.format(ErrorTimeStamp)
	FormattedErrorString = ErrorTimeString + message
	SharedVars.GuiMessageLabel.config(text=FormattedErrorString)
	print(FormattedErrorString)
