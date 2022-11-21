#!/usr/bin/env bash

NOCOLOR='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
LIGHTGRAY='\033[0;37m'
DARKGRAY='\033[1;30m'
LIGHTRED='\033[1;31m'
LIGHTGREEN='\033[1;32m'
YELLOW='\033[1;33m'
LIGHTBLUE='\033[1;34m'
LIGHTPURPLE='\033[1;35m'
LIGHTCYAN='\033[1;36m'
WHITE='\033[1;37m'

PYTHON_SCRIPT=topy.py
TOP_FILE_DIR=top_files/
INPUT_FILE=test.in
SERVER1="35.165.134.136"
S1_TOPFILE="${TOP_FILE_DIR}server1.top"

SERVER2="13.57.50.95"
S2_TOPFILE="${TOP_FILE_DIR}server2.top"

SERVER3="35.90.154.134"
S3_TOPFILE="${TOP_FILE_DIR}server3.top"

SERVER4="18.217.37.142"
S4_TOPFILE="${TOP_FILE_DIR}server4.top"

echo "${WHITE}running checks"

# checks if python script exits
if [ -f "$PYTHON_SCRIPT" ]; then
        echo "${LIGHTGREEN}python script found."
else
        echo "${RED}failed to find python script '$PYTHON_SCRIPT'."
        exit 1
fi

# check if top. files exist
if [ -f "$S1_TOPFILE" ] && [ -f "$S2_TOPFILE" ] && [ -f "$S3_TOPFILE" ] && [ -f "$S4_TOPFILE" ]
then
        echo "${LIGHTGREEN}topology files found."
else
        echo "${RED}failed to find some topology files."
        exit 1
fi

# checks if test.in exits to delete
if [ -f "$INPUT_FILE" ]; then
        echo "${RED}'${INPUT_FILE}' found... deleting"
        rm "$INPUT_FILE"
fi

# function get externa ip using GET HTTP request
get_ext_ip(){
        curl -s http://whatismyip.akamai.com/
}

# getting external ip
ext_ip=$(get_ext_ip)

if [ "$ext_ip" = "$SERVER1" ]; then
        echo "${YELLOW}will run test as server 1 using ${ext_ip}"
        top_file=$S1_TOPFILE
elif [ $ext_ip = $SERVER2 ]; then
        echo "${YELLOW}will run test as server 2 using ${ext_ip}"
        top_file=$S2_TOPFILE
elif [ $ext_ip = $SERVER3 ]; then
        echo "${YELLOW}will run test as server 3 using ${ext_ip}"
        top_file=$S3_TOPFILE
elif [ $ext_ip = $SERVER4 ]; then
        echo "${YELLOW}will run test as server 4 using ${ext_ip}"
        top_file=$S4_TOPFILE
fi


echo "\n${WHITE}gennerating inputs"

server_cmd="server -t ${top_file} -i 30"
echo "${server_cmd}" >> $INPUT_FILE
echo "update" >> $INPUT_FILE
echo "display" >> $INPUT_FILE 
echo "exit" >> $INPUT_FILE
echo "${GREEN}test generated"
echo "${YELLOW}use 'python3 topy.py < test.in' to conduct test"
echo "\n${LIGHTCYAN}'${INPUT_FILE}' contents"
echo "${WHITE}---------------------------"
cat $INPUT_FILE

echo "${RED}not running on an defined AWS EC2 instance... exiting"
exit 1