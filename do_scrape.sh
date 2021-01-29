#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR
python2.6 site/do_scrape.py
curl http://localhost:8080/update