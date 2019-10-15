#!/bin/sh
f=/tmp/push-data.txt
t=$(tempfile)
dt=$(date)
cat >$t
sz=$(cat $t | wc -c)
echo "$dt $sz bytes $REQUEST_URI from $REMOTE_ADDR" >> $f
echo "-----" >> $f
zcat $t >> $f
echo "-----" >> $f
echo "Content-type: text/html"
echo "Cache-Control: no-cache"
echo ""
echo "Thank You!"
rm -f $t
exit 0
