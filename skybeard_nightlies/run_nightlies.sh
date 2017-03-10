echo "Making 'master' directory in $1 and cloning branch"

cd $1

git clone https://github.com/LanceMaverick/skybeard-2 --single-branch master

cd -

echo "Running tests on branch 'master'"

python $1/run_nightly.py --branch master --location $1/master --out $1

echo "Making 'skb-dev' directory in $1 and cloning branch"

cd $1

git clone https://github.com/LanceMaverick/skybeard-2

git checkout skb-dev

cd -

python $1/run_nightly.py --branch skb-dev --location $1/skybeard-2 --out $1

cd $1/skybeard-2

pr_array=($(git pull-request -r LanceMaverick/skybeard-2 | sed -n 3p | grep -E -o '[[:digit:]]+'))

for i in "$pr_array":
    do
      git pull-request -r LanceMaverick/skybeard-2 -r $i
      git checkout pull-request-$i
      cd -
      python $1/run_nightly.py --branch pull-request-$i --location $1/skybeard-2 --out $1
    done

rm -rf master
rm -rf skybeard-2

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
