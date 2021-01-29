#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR
echo "Doing"
nohup python2.6 site/server.py 2>&1 > /dev/null &


#disown
#disown
echo $! >./running.pid
echo "Done"