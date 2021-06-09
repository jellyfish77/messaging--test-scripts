#!/bin/bash
# Usage ./mqtt_load_test.sh [#clients] [#messages per client] [message size in bytes]

echo "Spawning $1 clients to publish $2 message(s) of size $3 byte(s) each"
message=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w $3 | head -n 1)
#for i in {0..$1}

time for (( i=1; i <= $1; i++ )); do
#do
  echo "python3 mqtt_publisher.py --broker 127.17.0.5 --port 1885 --clientid py-pub-$i --qos 1 --nummsgs $2 --topic test/topic2 --message..."
  
  python3 mqtt_publisher.py --broker 127.17.0.5 --port 1885 --clientid publisher-$i --qos 1 --nummsgs $2 --topic test/topic2 --message $message &> /dev/null &
done

printf "Messages published: %d\n" "$(($1 * $2))"
