#!/bin/sh

print_result()
{
    if [ $2 -eq 0 ]; then
        echo TC$1 PASSED
    else
        echo TC$1 FAILED
    fi
}

./poker_stats.py -p HubertusB -v -f UTG -d ./test/test_sample2.txt 2> /dev/null | diff -u - ./test/test_result2.txt > /dev/null
print_result 2 $?
./poker_stats.py -p HubertusB -v -f MP -d ./test/test_sample3.txt 2> /dev/null | diff -u - ./test/test_result3.txt > /dev/null
print_result 3 $?
./poker_stats.py -p HubertusB -v -f CO -d ./test/test_sample4.txt 2> /dev/null | diff -u - ./test/test_result4.txt > /dev/null
print_result 4 $?
./poker_stats.py -p HubertusB -v -f BTN -d ./test/test_sample5.txt 2> /dev/null | diff -u - ./test/test_result5.txt > /dev/null
print_result 5 $?
./poker_stats.py -p HubertusB -v -f SB -d ./test/test_sample6.txt 2> /dev/null | diff -u - ./test/test_result6.txt > /dev/null
print_result 6 $?
./poker_stats.py -p HubertusB -v -f BB -d ./test/test_sample7.txt 2> /dev/null | diff -u - ./test/test_result7.txt > /dev/null
print_result 7 $?
