#!/bin/sh
cat >>/tmp/push-data.txt
echo "Content-type: text/html"
echo "Cache-Control: no-cache"
echo ""
echo "Thank You!"
set >>/tmp/push-data.txt
exit 0
