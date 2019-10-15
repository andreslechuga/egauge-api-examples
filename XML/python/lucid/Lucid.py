# Copyright (c) 2013 eGauge Systems LLC
# 	4730 Walnut St, Suite 110
# 	Boulder, CO 80301
# 	voice: 720-545-9767
# 	email: davidm@egauge.net
#
# All rights reserved.
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
import json
from datetime import datetime

def convert (dev_id, new_egauge_push_data, prev_egauge_push_data = None):
    res = {}
    res['datasource'] = "%s.%d" % (dev_id,
                                   new_egauge_push_data.config_serial_number)
    if prev_egauge_push_data == None \
            or (prev_egauge_push_data.config_serial_number
                != new_egauge_push_data.config_serial_number):
        catalog = []
        for regnum in range (len (new_egauge_push_data.regname)):
            meter = {}
            meter['meterId'] = regnum
            meter['meterName'] = new_egauge_push_data.regname[regnum]
            meter['meterUnits'] = 'Wh'
            catalog.append (meter)
        res['metercatalog'] = catalog
        prev_ts = None
        prev_row = None
    else:
        idx = len (prev_egauge_push_data.ts) - 1
        prev_ts = prev_egauge_push_data.ts[idx]
        prev_row = prev_egauge_push_data.row[idx]
        print "prev_ts = %s" % datetime.fromtimestamp (prev_ts).isoformat ()
        print "prev_row = %s" % prev_row

    readings = []

    for i in range (len (new_egauge_push_data.ts)):
        ts = new_egauge_push_data.ts[i]
        row = new_egauge_push_data.row[i]
        if prev_ts and prev_row:
            ts_str = datetime.fromtimestamp (ts).isoformat ()
            for regnum in range (len (new_egauge_push_data.row[i])):
                reading = {}
                if new_egauge_push_data.regtype[regnum] != 'P':
                    # for now, BuildingOS can only handle power/energy readings
                    continue
                val = (row[regnum] - prev_row[regnum])
                reading['timestamp'] = ts_str
                reading['local'] = False	# eGauge timestamps are UTC...
                reading['value'] = val / 3600.0	# convert to Wh
                reading['meterId'] = regnum
                readings.append (reading)
        prev_ts = ts
        prev_row = row

    res['readings'] = readings

    return json.dumps (res, sort_keys=True, indent=4, separators=(',', ': '))
