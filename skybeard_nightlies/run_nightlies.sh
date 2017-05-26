if [ "$#" -ne 1 ]
then
    SKNLOC=$2
    if [ ! -d "$SKNLOC" ]
    then
        echo "ERROR: Directory '$2' does not exist!"
        exit 1
    fi
else
    SKNLOC=$PWD
fi

if [ ! -d "$1" ]
then
    echo "ERROR: Director '$1' does not exist!"
    exit 1
fi

echo "Making 'master' directory in $1 and cloning branch"

cd $1

git clone https://github.com/LanceMaverick/skybeard-2 --single-branch master

cd -

echo "Running tests on branch 'master'"

python $SKNLOC/run_nightly.py --branch master --location $1/master --out $1

echo "Making 'skybeard-2' directory in $1"

cd $1

git clone https://github.com/LanceMaverick/skybeard-2
cd $1/skybeard-2

git checkout skb-dev

cd -

python $SKNLOC/run_nightly.py --branch skb-dev --location $1/skybeard-2 --out $1

cd $1/skybeard-2

pr_array=($(git pull-request -r LanceMaverick/skybeard-2 | grep -E 'REQUEST' | awk -F ' ' '{print $2}'))

echo $pr_array

for i in "${pr_array[@]}"
    do
      echo "Checking Out Pull Request #$i"
      git pull-request -r LanceMaverick/skybeard-2 $i
      git branch
      echo "Leaving Directory"
      cd -
      python $SKNLOC/run_nightly.py --branch pull-request-$i --location $1/skybeard-2 --out $1
      cd $1/skybeard-2
    done

cd -
rm -rf $1/master
rm -rf $1/skybeard-2

echo "# Skybeard Nightly Tests" > header.md
DATE=`date +%Y-%m-%d`

markdown-pdf $1/test_summary*.md --out $1/TestSummary_$DATE.pdf 
rm $1/test_summary*.md
rm header.md
for i in $(ls $1/std_err*.md);
   do markdown-pdf $i;
   done
rm $1/std_err*.md

pdfunite $1/std_err*.pdf $1/ErrorLog_$DATE.pdf
rm $1/std_err*.pdf
