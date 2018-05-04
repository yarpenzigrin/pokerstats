#!/bin/sh

test_dir=`dirname $0`
script_dir=$test_dir/../..

tc_counter=1
exit_code=0

run_tc()
{
    prog=$1
    inp=$2
    out=$3

    echo "RUN TC$tc_counter: ('$prog $test_dir/$inp' vs. '$test_dir/$out')"
    $prog $test_dir/$inp 2>/dev/null | diff -u - $test_dir/$out >/dev/null
    if [ $? -eq 0 ]; then
        echo "RUN TC$tc_counter: OK"
    else
        echo "RUN TC$tc_counter: NOK"
        exit_code=1
    fi
    tc_counter=`expr $tc_counter + 1`
}

run_test_suite()
{
    run_tc "python2.7 -m poker_stats --filter voluntary=forced dump_ps --sort HubertusB" test_input01.txt test_output01.txt
    run_tc "python2.7 -m poker_stats --filter position=BTN;3bet dump_ps HubertusB" test_input02.txt test_output02.txt
    run_tc "python2.7 -m poker_stats --filter voluntary=only;4bet dump_ps HubertusB" test_input03.txt test_output03.txt
    run_tc "python2.7 -m poker_stats --filter holding=AQs dump_ps HubertusB" test_input01.txt test_output08.txt
    run_tc "python2.7 -m poker_stats --filter holding=QAo dump_ps HubertusB" test_input01.txt test_output09.txt

    run_tc "python2.7 -m poker_stats report HubertusB" test_input_merged.txt test_output04.txt
    run_tc "python2.7 -m poker_stats blind_report HubertusB" test_input_merged.txt test_output05.txt
    run_tc "python2.7 -m poker_stats position_report HubertusB" test_input_merged.txt test_output06.txt
    run_tc "python2.7 -m poker_stats preflop_report HubertusB" test_input_merged.txt test_output07.txt
}

run_test_suite
exit $exit_code
