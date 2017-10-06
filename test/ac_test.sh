#!/bin/sh

test_dir=`dirname $0`
script_dir=$test_dir/..

tc_counter=1

run_tc()
{
    prog=$1
    inp=$2
    out=$3

    echo -n "RUN TC$tc_counter... "
    $script_dir/$prog $test_dir/$inp 2>/dev/null | diff -u - $test_dir/$out >/dev/null
    if [ $? -eq 0 ]; then
        echo "OK"
    else
        echo "NOK"
    fi
    tc_counter=`expr $tc_counter + 1`
}

run_test_suite()
{
    run_tc "poker_stats.py -p HubertusB -v -f UTG -d" test_input02.txt test_output02.txt
    run_tc "poker_stats.py -p HubertusB -v -f MP -d" test_input03.txt test_output03.txt
    run_tc "poker_stats.py -p HubertusB -v -f CO -d" test_input04.txt test_output04.txt
    run_tc "poker_stats.py -p HubertusB -v -f BTN -d" test_input05.txt test_output05.txt
    run_tc "poker_stats.py -p HubertusB -v -f SB -d" test_input06.txt test_output06.txt
    run_tc "poker_stats.py -p HubertusB -v -f BB -d" test_input07.txt test_output07.txt
}

run_test_suite
