NastyBoys Strategy
============================
to setup environment:
* spawn off a python2 virtualenv
* pip install stuff in the requirement
* init and update your gitsubmodule
* install pycurl
* (should you fancy for building your own bayesian classifier) download data from nltk

or you can do this:
> sh init.sh

then if you want to do bayesian classifier:
> python -m nltk.downloader all

Running the Nasty
----------------
Here's *a* method for selecting your symbols to trade:

First, get some market cap data for all symbols
(creates tick-cap-name and tick-cap files)

`./stock_set_update.sh`

Then, get a set of positions
(creates a file like 20131120_positions)

`python nasty.py False 2> /dev/null | sort > "\\`date +%Y%m%d\\`_positions"`

Then order these positions by market cap to prioritize your trades
(note, the join requires these files to be sorted on the join field)

`join -1 1 -2 1 20131120_positions tick-cap-name`




