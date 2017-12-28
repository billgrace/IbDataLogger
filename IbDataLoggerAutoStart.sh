#!/bin/bash
echo "2 minute delay to give this Mac Mini system time to start up and settle down"
for i in {120..01}
do
	echo -n "$i"
	sleep 1
done
echo "Delay complete - now launching IbDataLogger.py"
cd /Users/billgrace/Documents-Macmini-Local/IbDataLogger
python3 /Users/billgrace/Documents-Macmini-Local/IbDataLogger/IbDataLogger.py
