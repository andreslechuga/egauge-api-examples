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
import eGauge
import Lucid


epd = eGauge.PushData ('''<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE group PUBLIC "-//ESL/DTD eGauge 1.0//EN" "http://www.egauge.net/DTD/egauge-hist.dtd">
<group serial="0x78666e80"> data
<data columns="12" time_stamp="0x521598f0" time_delta="60" epoch="0x473953a4">
 <cname t="P">Grid</cname>
 <cname t="P">Grid+</cname>
 <cname t="S">Grid*</cname>
 <cname t="P">Solar SPR</cname>
 <cname t="P">Solar SPR+</cname>
 <cname t="P">Mech Room</cname>
 <cname t="P">PHEV (Grg&amp;Bth)</cname>
 <cname t="P">Solar Tigo+SPR</cname>
 <cname t="P">Solar Tigo+SPR+</cname>
 <cname t="P">Comp. Closet #1</cname>
 <cname t="P">EV Charging</cname>
 <cname t="P">Oven</cname>
 <r><c>-16364197407</c><c>9812046521</c><c>106246439436</c><c>44198336283</c><c>44275600040</c><c>-26189502079</c><c>72065552</c><c>26852297422</c><c>26907708487</c><c>6735392170</c><c>21965756602</c><c>-1400018883</c></r>
 <r><c>-16364410573</c><c>9811833355</c><c>106246217002</c><c>44198336489</c><c>44275600040</c><c>-26189485191</c><c>72066701</c><c>26852297661</c><c>26907708487</c><c>6735396843</c><c>21965907767</c><c>-1400018786</c></r>
 <r><c>-16364626636</c><c>9811617292</c><c>106245991885</c><c>44198336694</c><c>44275600040</c><c>-26189468270</c><c>72067844</c><c>26852297898</c><c>26907708487</c><c>6735401524</c><c>21966058842</c><c>-1400018689</c></r>
</data>
</group>
''')
print "%s" % (Lucid.convert ('eGauge3453', epd))
prev = epd
epd = eGauge.PushData('''<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE group PUBLIC "-//ESL/DTD eGauge 1.0//EN" "http://www.egauge.net/DTD/egauge-hist.dtd">
<group serial="0x78666e80"> data
<data columns="12" time_stamp="0x5224db30" time_delta="60" epoch="0x473953a4">
 <cname t="P">Grid</cname>
 <cname t="P">Grid+</cname>
 <cname t="S">Grid*</cname>
 <cname t="P">Solar SPR</cname>
  <cname t="P">Solar SPR+</cname>
 <cname t="P">Mech Room</cname>
 <cname t="P">PHEV (Grg&amp;Bth)</cname>
 <cname t="P">Solar Tigo+SPR</cname>
 <cname t="P">Solar Tigo+SPR+</cname>
 <cname t="P">Comp. Closet #1</cname>
 <cname t="P">EV Charging</cname>
 <cname t="P">Oven</cname>
 <r><c>983635802593</c><c>-990187953479</c><c>-893753560564</c><c>-955801663717</c><c>-955724399960</c><c>973810497921</c><c>-999927932156</c><c>-973147702578</c><c>-973092291513</c><c>-993264607830</c><c>1021965756602</c><c>-1001400018883</c></r>
</data>
</group>
''')
print "%s" % (Lucid.convert ('eGauge3453', epd, prev))
