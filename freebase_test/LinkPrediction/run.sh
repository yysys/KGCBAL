#/bin/bash

for((i=1;i<=4;i++));
do
python3 linkpredhit.py $($i * 5 + 70) 500 RootedPageRank
done
