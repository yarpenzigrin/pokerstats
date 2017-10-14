#!/bin/sh

test_dir=`dirname $0`
script_dir=$test_dir/../..

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
    run_tc "poker_stats.py --filter name=HubertusB;voluntary=only dump_ps --sort" test_input01.txt test_output01.txt
    run_tc "poker_stats.py --filter name=HubertusB;voluntary=only dump_ps" test_input02.txt test_output02.txt
    run_tc "poker_stats.py --filter name=HubertusB dump_ps --sort" test_input03.txt test_output03.txt
    run_tc "poker_stats.py --filter name=HubertusB dump_ps " test_input04.txt test_output04.txt

    run_tc "poker_stats.py --filter name=HubertusB;position=SB;voluntary=only dump_ps --sort" test_input01.txt test_output05.txt
    run_tc "poker_stats.py --filter name=HubertusB;position=SB;voluntary=only dump_ps" test_input02.txt test_output06.txt
    run_tc "poker_stats.py --filter name=HubertusB;position=SB dump_ps --sort" test_input03.txt test_output07.txt
    run_tc "poker_stats.py --filter name=HubertusB;position=SB dump_ps" test_input04.txt test_output08.txt

    run_tc "poker_stats.py --filter name=HubertusB;position=BB;voluntary=only dump_ps --sort" test_input02.txt test_output09.txt
    run_tc "poker_stats.py --filter name=HubertusB;position=BB;voluntary=only dump_ps" test_input02.txt test_output10.txt
    run_tc "poker_stats.py --filter name=HubertusB;position=BB dump_ps --sort" test_input03.txt test_output11.txt
    run_tc "poker_stats.py --filter name=HubertusB;position=BB dump_ps" test_input04.txt test_output12.txt

    # temporary AT for reporting until we have UTs
    run_tc "poker_stats.py --filter name=HubertusB report" test_input_merged.txt test_output13.txt
    run_tc "poker_stats.py --filter name=HubertusB;voluntary=only report" test_input_merged.txt test_output14.txt
    run_tc "poker_stats.py --filter name=HubertusB;voluntary=forced report" test_input_merged.txt test_output15.txt
    run_tc "poker_stats.py --filter name=HubertusB;voluntary=only;flop_players=2 report" test_input_merged.txt test_output16.txt
}

run_test_suite
