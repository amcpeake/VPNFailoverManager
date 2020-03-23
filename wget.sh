echo "$1", "$2", "$3"

#if [ "$1" = "get" ]
#then
#  curl -o /dev/null http://speedtest.wdc01.softlayer.com/downloads/test100.zip
#fi


if [ "$3" = "down" ]
then
    curl -o /tmp/test100.zip http://speedtest.wdc01.softlayer.com/downloads/test100.zip "$1" "$2"
else
    curl -T /tmp/test100.zip filebin.net "$1" "$2"
fi
