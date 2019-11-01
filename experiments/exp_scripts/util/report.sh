#! /bin/bash
DIR_SCRIPTS="Desktop/DisasterSimulator/experiments/temp/reports"

printf "Memory;CPU\n" >> $DIR_SCRIPTS/report_$1_$2.csv
end=$((SECONDS+3600))
while [ $SECONDS -lt $end ]; do
MEMORY=$(free -m | awk 'NR==2{printf "%.2f%%;", $3*100/$2 }')
CPU=$(grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage "%"}')
echo "$MEMORY$DISK$CPU" >> $DIR_SCRIPTS/report_$1_$2.csv
sleep 0.01
done