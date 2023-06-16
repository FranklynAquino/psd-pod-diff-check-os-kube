#!/bin/sh

#get date
date=`date +%Y%m%d`
#echo ${date}_resultspy.csv
#exit

#Run python open search query
echo "Running python query"
#Orig
#python3 run.py $1 | sort -n > ${date}_resultspy.csv

#Updated to consider balance pods
python3 run.py $1 | sort -n | grep binance > ${date}_resultspy.csv
countpy=`wc -l ${date}_resultspy.csv`
echo "Found $countpy pods\n"

#Run kubectl command to list pods
echo "Running kubectl command"
#Orig
#kubectl get pod -o=custom-columns=NAME:.metadata.name --all-namespaces | grep binance  | egrep -v "balance|overflow" | sort -n > ${date}_resultskube.csv
#Updated to consider balance pods
kubectx atlas-aps1-prod-1
kubectl get pod -o=custom-columns=NAME:.metadata.name --all-namespaces | grep binance  | egrep -v "overflow" | sort -n > ${date}_resultskube.csv
countkube=`wc -l ${date}_resultskube.csv`
echo "Found $countkube pods\n"

#Compare lists of pods
echo "Comparing files"
numDiffs=`diff -w ${date}_resultspy.csv ${date}_resultskube.csv | grep -v - | wc -l`
echo "Differences: $numDiffs"

#[ $numDiffs -eq 0 ] && echo "Both pod lists match!" || echo "Pods only in open search will begin with a '<' character \nPods only in kubernetes will begin with a '>' character"

if [ $numDiffs -eq 0 ]
then
    echo "Both pod lists match!" 
else
    echo "\nPods only in open search will begin with a '<' character \nPods only in k8s will begin with a '>' character"
    diff -w ${date}_resultspy.csv ${date}_resultskube.csv
fi

    
