# Dashboard generator
This is a python script that builds up a runtime status of ECDC related servers. The status is presented as a html page updates itself periodically.
The graphical view is based on svg.

Server availability is based on **ping**, service availability on the presence of a listening **tcp port**. Finally for Event Formation Units (EFUs) the pipeline runtime is given by the result of the
**RUNTIMESTATS** command. Different statuses are presented with different colors which are explained in the legend.

The generator takes three optional commend line arguments

Option | Purpose
------------ | -------------
-d | debug print flag (default off)
-f | server file. The default is to use utgaard.csv
-r | minimum refresh interval in seconds (can be longer if checks take time)

### Starting the dashboard generator


To run the generator in the foreground

    > ./generate.py

for a 'daemon' like service

    > nohup ./generate.py &


### Starting a (python) webserver

The following command will start a webserver on port 8765 dthat serves
files in the current directory.

    > nohup  python -m SimpleHTTPServer 8765 &
