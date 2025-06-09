#!/bin/bash

# Usage check
if [ $# -lt 2 ]; then
    echo "Usage: $0 <protocol> <number_of_players>"
    echo "Example: $0 atlas 10"
    exit 1
fi

# Get the protocol and number of players from the arguments
PROTOCOL="$1" 
PLAYER_ID=$2

READY_CHECK_PROGRAM="wise_ready"
MAIN_PROGRAM="wise"
READ_PROGRAM="wise_read"
SLEEP_SECONDS=10

> "ready_output.txt"
> "wise_output.log"
> "output.log"

for ((i=0; i<PLAYER_ID; i++)); do
    > "wise_output"$i".log"
    > "Persistence/Transactions-P"$i".data"
done

# Launch clients
for ((i=0; i<PLAYER_ID; i++)); do
    xterm -hold -e "python3 ExternalIO/wise_client.py $i; tail -f wise_output.log" &
done

# Loop for 5 rounds
for round_no in {1..5}; do
    echo "Starting round $round_no"

    ./compile.py $READY_CHECK_PROGRAM $PLAYER_ID $round_no

    while true; do
        PLAYERS=$PLAYER_ID Scripts/${PROTOCOL}.sh ${READY_CHECK_PROGRAM}-${PLAYER_ID}-$round_no | tee ready_output.txt

        if grep -q "All players ready: 1" ready_output.txt; then
            echo "All players are ready!"
            break
        else
            echo "Not all players ready yet. Sleeping for $SLEEP_SECONDS seconds..."
            sleep $SLEEP_SECONDS
        fi
    done

    echo "Running main program: $MAIN_PROGRAM (Round $round_no)"
    ./compile.py $MAIN_PROGRAM $PLAYER_ID $round_no

    PLAYERS=$PLAYER_ID Scripts/${PROTOCOL}.sh ${MAIN_PROGRAM}-${PLAYER_ID}-$round_no | tee -a output.log
    grep "Winner" output.log >> wise_output.log

    for ((i=0; i<PLAYER_ID; i++)); do    
        > "wise_output$i.log"
        ./compile.py $READ_PROGRAM $PLAYER_ID $round_no $i
        sed_range='2,5p'
        PLAYERS=$PLAYER_ID Scripts/${PROTOCOL}.sh ${READ_PROGRAM}-${PLAYER_ID}-$round_no-$i | sed -n "$sed_range" | tee -a wise_output$i.log
    done

done
