# Program scheduling
The IbDataLogger.py program is meant to be automatically started each day. Here in the Pacific time zone, the markets operate from 6:30 AM until 1:00 PM.<p>
The Interactive Brokers TWS application is automatically launched each day at 6:00 AM and shuts itself down each night.
The IbDataLink/IbDataTap code is automatically launched at 6:05 AM and shuts itself down each afternoon.
The IbDataLogger.py program is launched each day at 6:30 AM and shuts itself down each afternoon.
# Preferences
A file in the execution directory named Preferences.cfg contains keyword = value lines to provide editable over-rides of some items that othersise take the default values written into the python code.
# Strike prices, expiration dates and trading days
## Strike prices
Strike prices of interest are calculated by the program at $5 increments. The current underlying price is taken as a center point and a parameter named "StrikePriceRange" indicates how many strike prices above (and below) the underlying will be monitored and logged.<p>
For example, with an underlying at 2,462.13 and a StrikePriceRange of 3, the strike prices being monitored would be:
2450, 2455, 2460, 2465, 2470 and 2475.<p>
At the beginning of each day, the number of strike prices being monitored will be two times the value of StrikePriceRange.
As the underlying moves up and down, additional strike prices will be added to the list of those being monitored so as to maintain the configured StrikePriceRange. HOWEVER, already-active strike prices that fall outside that range as the underlying moves away from them will NOT be dropped! So the overall range of strike prices will tend to grow through the day as the underlying moves up and down.
## Expiration dates
A parameter named "ExpirationDateRange" indicates how many expiration dates will be monitored and logged.<p>
Rather than venturing into a potentially complicated algorithmic method of figuring out valid expiration dates, the python code relies on a pre-existing text file listing them. This file is named ExpirationDates.dat and is also in the execution directory.<p>
Each line in this file contains a date formatted as YYYY-MM-DD such as '2019-08-14' to represent August 14, 2019.<p>
There is one date per line in this text file and those dates are in chronological order.<p>
The python code picks out a working list of expiration dates by scanning this file until it finds a date that is not already past and takes that date as its first expiration date to be monitored. It then picks up however many of the immediately following dates are needed to make up a list containing ExpirationDateRange expiration dates.<p>
 _NOTA BENE !!!_ While the programming staff is wildly enthusiastic --bordering on ecstatic-- about the simplicity of this system to determine valid expiration dates, it DOES fall to the ongoing maintenance crew to be sure that this file is kept up to date. CBOE doesn't appear to publish its calendar very far in advance (it's now September 2017 and I can't find their 2018 calendar yet....) so perhaps a scheduled once-each-first-of-the-month duty will be needed to fire up TOS and check the chains available and use that to update the ExprationDates.dat file.
## trading days
Yep, you guessed it! "TradingDates.dat" is just like "ExpirationDates.dat" and tells the python code which dates warrant monitoring and logging because the markets are open and active.<p>
If this file is not found, the python code will treat every day as a trading day - probably doing no harm beyond wasting storage space.<p>
If this file IS found, the python code will treat a date as a trading day if it is found in the file.
# Data Storage
## Storage rate
A parameter named StorageRecordWriteInterval (seconds as a float) indicates how often each monitor's current data should be written to storage.<p>
Note that this is distinct from the rate at which monitors are updated from IbDataTap/IbDataLink (parameters UnderlyingMonitorReadingInterval and OptionMonitorReadingInterval) as well as from the rate at which the python visible GUI screen window is updated (GuiRefreshInterval... WHICH IS IN MILLISECONDS!!) and the rate at which the IbDataLink status is fetched (StatusReportingInterval).<p>
Also, keep in mind that none of these configurable intervals hold any sway over how frequently TWS deigns to update IbDataTap about any of the ongoing market data values.
## Storage location
### Storage root path
A data storage root path is configured in a parameter named StoragePath. It defaults to the directory where the python script resides (NOT the directory from which it is being executed should they be different). This can be set to any absolute directory location by editing the corresponding entry in the Preferences.cfg file.
### Daily path
Each time the python code is run, it creates a new directory under the data storage root path and names that sub-directory YYYY-MM-DD as in '2019-08-14'.<p>
All of the day's data is stored in this sub-directory.
## File names
In each daily sub-directory, individual files are created for 1) the underlying and 2) each option being tracked.<p>
The file name for the underlying is (symbol) + '-Underlying' as in 'SPX-Underlying'.<p>
The file name for each option is (symbol) + (Expiration date) + (Strike price) + (Contract right) as in 'SPX-2019-08-14-2465-PUT'.
## File content
All data is stored as plain text.<p>
Each entry in each file is a single line of text and has two parts.<p>
The first part is the time at which the line was written to storage as hour, minute, second, milliseconds (hour in 24-hour format) such as: '09-23-47-528' meaning 47.528 seconds after 9:23AM.<p>
The second part is a string representation of the Avro-serialized byte stream received over TCP for a MonitorData class object holding the present values associated with the particular item (the underlying or an option).<p>
These two parts on each line are separated by three dashes to aid in later parsing.

# IbDataLogger
