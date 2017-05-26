# Skybeard Nightlies
To test compatibility of changes/updates made in merge request branches, Skybeard includes an application for checking the changes against the master branch. The script produces tables in PDF form which show the results of running the tests contained within Skybeard Core and any beard plugins which have been installed. To run the nightlies simply run the bash executable `run_nightlies.sh` specifying the location in which you want the test information to be placed and, if needed, the location of the nightlies scripts.
```
mkdir testing
bash ./run_nightlies.sh testing [location of skybeard_nightlies folder]
```
