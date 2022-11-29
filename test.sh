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

TEST_DIR=test_files/
INPUT_FILE="${TEST_DIR}commands.in"
OUTPUT_FILE="${TEST_DIR}runtime.out"
ERROR_FILE="${TEST_DIR}runtime.err"

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
if [ -f "$S1_TOPFILE" ] && [ -f "$S2_TOPFILE" ] && [ -f "$S3_TOPFILE" ] && [ -f "$S4_TOPFILE" ]; then
	echo "${LIGHTGREEN}topology files found."
else
	echo "${RED}failed to find some topology files."
	exit 1
fi

if [ ! -d $TEST_DIR ]; then
	mkdir $TEST_DIR
fi

# checks if test.in exits to delete
if [ -f "$INPUT_FILE" ]; then
	echo "${RED}'${INPUT_FILE}' found... deleting"
	rm "$INPUT_FILE"
fi

# function get externa ip using GET HTTP request
get_ext_ip() {
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
else

	echo "${RED}not running on an defined AWS EC2 instance"

	echo "\n${YELLOW}do you wish to conintue using ${ext_ip}? [y/n]${WHITE}"
	flag=0
	while [ $flag -ge 0 ]; do

		read usr_input
		if [ ${usr_input:-1} = "n" ]; then
			exit 0
		elif [ ${usr_input:-1} = "y" ]; then
			flag=-1
		else
			echo "${RED}invalid option${WHITE}"
		fi
	done

	echo "\n${YELLOW}what topological file do you wish to use? [1-4]${WHITE}"
	flag=0
	while [ $flag -ge 0 ]; do

		read usr_input
		if [ ${usr_input:-1} -ge 1 ] && [ ${usr_input:-1} -le 4 ]; then
			echo "${YELLOW}will run test as server 4 using ${ext_ip}"
			top_file="${S1_TOPFILE%1.top}${usr_input:-1}.top"
			flag=-1
		else
			echo "${RED}invalid option${WHITE}"
		fi
	done
fi

echo "\n${WHITE}gennerating inputs"

server_cmd="server -t ${top_file} -i 30"
echo "${server_cmd}" >>$INPUT_FILE
echo "update 1 2 5" >>$INPUT_FILE
echo "update 1 3 4" >>$INPUT_FILE
echo "update 1 4 6" >>$INPUT_FILE
echo "display" >>$INPUT_FILE
echo "exit" >>$INPUT_FILE
echo "${GREEN}test generated"
echo "\n${LIGHTCYAN}'${INPUT_FILE}' contents"
echo "${WHITE}---------------------------"
cat $INPUT_FILE

echo "\n${YELLOW}do you wish to run test? [y/n]${WHITE}"
flag=0
while [ $flag -ge 0 ]; do

	read usr_input
	if [ ${usr_input:-1} = "n" ]; then
		echo "${YELLOW}use 'cat ${INPUT_FILE} | python3 ${PYTHON_SCRIPT} < test.in' to conduct test"
		exit 0
	elif [ ${usr_input:-1} = "y" ]; then
		echo "${GREEN}running test...${YELLOW}\n"
		flag=-1
	else
		echo "${RED}invalid option${WHITE}"
	fi
done

cat $INPUT_FILE | python3 -u $PYTHON_SCRIPT >${OUTPUT_FILE} 2>${ERROR_FILE}

if [ -s ${ERROR_FILE} ]; then
	echo "${RED} error have occured during execution"
	echo "${YELLOW} check ${ERROR_FILE}"
else
	rm $ERROR_FILE
fi

echo "${GREEN}test output located in ${OUTPUT_FILE}"

echo "${YELLOW}do you wish to see the output? [y/n]${WHITE}"
flag=0
while [ $flag -ge 0 ]; do

	read usr_input
	if [ ${usr_input:-1} = "n" ]; then
		exit 0
	elif [ ${usr_input:-1} = "y" ]; then
		cat ${OUTPUT_FILE}
		exit 0
	else
		echo "${RED}invalid option${WHITE}"
	fi
done
