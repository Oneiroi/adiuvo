#!/bin/bash

error(){
	echo $1;
	exit 1;
}
[[ -z "$1" ]] && error "I need something to pgrep for! usage $0 <str>"
pTot=0
pCnt=0
echo "--- Memory report for $1 ---"
pgrep $1 | while read pid;
do
	grep Private /proc/$pid/smaps | awk '{ print $2 }' | while read mem;
	do
		let pTot+=$mem
	done
	let pCnt+=1
done

echo "Pid count: $pCnt"
echo "Total Memory: $pTot kb"
