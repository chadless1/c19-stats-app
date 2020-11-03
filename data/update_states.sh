#!/usr/bin/env bash

# update states csv file
# wget csv from git hub

wget https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv

yesterday=$(date +"%m.%d" -d yesterday)

mv us-states.csv us-states_$yesterday.csv













