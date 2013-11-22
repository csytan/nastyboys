#!/bin/bash
#
# Description: Updates ticker/market_cap info from nasdaq site
#
# 3 ticker market_cap files are generated by this script:
# ndq-tick-cap:  from nasdaq
# nyse-tick-cap:  from nyse
# tick-cap:  consolidated ndq and nyse tickers/caps sorted by ticker
#
# Warning:  This is fairly brittle as it depends on an unchanging
# record format from www.nasdaq.com with 2 rows of header, a row
# of footer and comma delimd fields in specific order (ndq and nyse differ)

# get the list of nasdaq stocks
# OLD URL: wget -nv 'http://www.nasdaq.com/asp/symbols.asp?exchange=Q&start=0' -O tmp-ndq.csv 2>> $log
wget -nv 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download' -O tmp-ndq.csv 2>> error.log

# get the list of nyse stocks
# OLD URL: wget -nv 'http://www.nasdaq.com/asp/symbols.asp?exchange=N&start=0' -O tmp-nyse.csv 2>> $log
wget -nv 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download' -O tmp-nyse.csv 2>> error.log

# clean 'em up
# get num lines in each
ndq_ct=`awk 'BEGIN { RS = "\r\n"; ORS = "\r\n"; ct = 0; } { ct++ } END { print ct }' tmp-ndq.csv`
nyse_ct=`awk 'BEGIN { RS = "\r\n"; ORS = "\r\n"; ct = 0; } { ct++ } END { print ct }' tmp-nyse.csv`

echo "ndq lines: $ndq_ct" >> error.log
echo "nyse lines: $nyse_ct" >> error.log

# remove header and footer
awk "BEGIN { RS = \"\r\n\"; ORS = \"\r\n\"; } FNR > 2 && FNR < $ndq_ct { print }" tmp-ndq.csv > tmp-ndq-body.csv

awk "BEGIN { RS = \"\r\n\"; ORS = \"\r\n\"; } FNR > 2 && FNR < $nyse_ct { print }" tmp-nyse.csv > tmp-nyse-body.csv


# create file of ticker,mkt_cap
# market caps are in millions, rounds up to whole million
# 'puts' effectively removes \r from output
# Note: ndq market cap field is 4 and nyse mkt cap field is 2
#       the regex for splitting is kinda tricky for fields wrapped in parens
#       It appears that google segregates tickers for diff't share classes via
#       '.' rather than '/' or '^' as nasdaq does...output favors google
ruby -e '$stdin.each_line("\r\n") \
         { |line| $F = line.scan(/\"((?:[^"]|"!?=(?:,|\r))*)\"(?:,|\r)/).flatten; \
           sym = $F[0].sub(/[\/^]/, "."); \
           name = ""; \
           name = $F[1] if $F[1]; \
           cap = 0; \
           cap = $F[3].gsub(/\$|,/, "").to_i if $F[3]; \
           puts "#{sym} #{cap} \"#{name}\""; }' < tmp-ndq-body.csv > tmp-ndq-tick-cap

ruby -e '$stdin.each_line("\r\n") \
         { |line| $F = line.scan(/\"((?:[^"]|"!?=(?:,|\r))*)\"(?:,|\r)/).flatten; \
           sym = $F[0].sub(/[\/^]/, "."); \
           name = ""; \
           name = $F[1] if $F[1]; \
           cap = 0; \
           cap = $F[3].gsub(/\$|,/, "").to_i if $F[3]; \
           puts "#{sym} #{cap} \"#{name}\""; }' < tmp-nyse-body.csv > tmp-nyse-tick-cap

# create consolidated tick/cap file
# filter out any duplicated tick/caps (if tick appears twice with
# different cap, keep it)
# filter out any tickers that may look 'strange' to google
cat tmp-ndq-tick-cap tmp-nyse-tick-cap | sort | uniq  \
> tick-cap-name
cat tick-cap-name | cut -d ' ' -f 1,2 | \
grep -E '^[A-Z]+(\.[A-Z])? [0-9]+$' | sort -k 2nr > tick-cap

