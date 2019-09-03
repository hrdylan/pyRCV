#bin/bash
python ../ParseVotes.py temp/sample_election.csv temp/parsed_elections
OIFS="$IFS"
IFS=$'\n'
echo `ls ` 
for file in `ls temp/parsed_elections`  
do
  echo "file = $file"
  python ../pyRCV.py temp/parsed_elections/$file temp/results/$file-results.csv
done
IFS="$OIFS"