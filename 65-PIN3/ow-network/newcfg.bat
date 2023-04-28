netconvert --node-files ow.nod.xml --edge-files ow.edg.xml
randomTrips.py -n net.net.xml -e 100 -o output.trips.xml
duarouter -n net.net.xml --route-files output.trips.xml -o net.rou.xml --ignore-errors
@REM sumo -c net.sumo.cfg --netstate-dump sumoTrace.xml --netstate-dump.empty-edges false --summary summary.xml --output-prefix TIME