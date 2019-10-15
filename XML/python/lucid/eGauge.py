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
import sys, urllib2
from lxml import etree

class error (Exception):
    pass

class PushData:

    _tdesc = {
        "P": {
            "doc"	: "Power",
            "units"	: ["W",		"Ws"],
            "scale"	: 1,
            },
        "S": {
            "doc"	: "Apparent power",
            "units"	: ["VA",	"VAs"],
            "scale"	: 1,
            },
        "V": {
            "doc"	: "Voltage",
            "units"	: ["V",		"Vs"],
            "scale"	: 1e-3,
            },
        "I": {
            "doc"	: "Current",
            "units"	: ["A",		"As"],
            "scale"	: 1e-3,
            },
        "F": {
            "doc"	: "Frequency",
            "units"	: ["Hz",	"Hzs"],
            "scale"	: 1e-3,
            },
        "THD": {
            "doc"	: "Total Harmonic Distortion",
            "units"	: ["%",		"%s"],
            "scale"	: 1e-3,
            },
        "T": {
            "doc"	: "Temperature",
            "units"	: ["C",		"Cs"],
            "scale"	: 1e-3,
            },
        "Q": {
            "doc"	: "Mass flow-rate",
            "units"	: ["g/s",	"g"],
            "scale"	: 1e-3,
            },
        "v": {
            "doc"	: "Speed",
            "units"	: ["m/s",	"m"],
            "scale"	: 1e-3,
            },
        "R": {
            "doc"	: "Resistance",
            "units"	: ["Ohm",	"Ohm*s"],
            "scale"	: 1,
            },
        "Ee": {
            "doc"	: "Irradiance",
            "units"	: ["W/m^2",	"W/m^2*s"],
            "scale"	: 1,
            },
        "PQ": {
            "doc"	: "Reactive power",
            "units"	: ["VAr",	"VArh"],
            "scale"	: 1,
            },
        "$": {
            "doc"	: "Money",
            "units"	: ["$",		"$s"],
            "scale"	: 1,
            },
        "a": {
            "doc"	: "Angle",
            "units"	: ["DEG",		"DEGs"],
            "scale"	: 1,
            },
        "h": {
            "doc"	: "Humidity",
            "units"	: ["%",		"%s"],
            "scale"	: 1e-1,
            },
        "Qv": {
            "doc"	: "Volumetric flow-rate",
            "units"	: ["m^3/s",	"m^3"],
            "scale"	: 1e-9,
            },
        "Pa": {
            "doc"	: "Pressure",
            "units"	: ["Pa",	"Pa*s"],
            "scale"	: 1,
            }
        }


    def __init__ (self, xml_string):
        self.config_serial_number = None
        self.num_registers = 0
        self.regname = []
        self.regtype = []
        self.ts = []
        self.row = []

        xml = etree.fromstring (xml_string)
        if xml.tag != 'group':
            raise error, ('Expected <group> as the top element')
        self.config_serial_number = int (xml.attrib['serial'], 0)

        for data in xml:
            ts = None
            delta = None
            if data.tag != 'data':
                raise error, ('Expected <data> elements within <group>')

            if 'columns' in data.attrib:
                self.num_registers = int (data.attrib['columns'])
            if 'time_stamp' in data.attrib:
                ts = long (data.attrib['time_stamp'], 0)
            if 'time_delta' in data.attrib:
                delta = long (data.attrib['time_delta'], 0)
            if 'epoch' in data.attrib:
                self.epoch = int (data.attrib['epoch'], 0)

            if ts == None:
                raise error, ('<data> element is missing time_stamp attribute')
            if delta == None:
                raise error, ('<data> element is missing time_delta attribute')

            for el in data:
                if el.tag == 'r':
                    row = []
                    for c in el:
                        row.append (long (c.text))
                    self.ts.append (ts)
                    self.row.append (row)
                    ts -= delta
                elif el.tag == 'cname':
                    t = "P"
                    if 't' in el.attrib:
                        t = el.attrib['t']
                    self.regname.append (el.text)
                    self.regtype.append (t)
        return

    def __str__ (self):
        ret = ""
        ret += "serial # = %d, " % self.config_serial_number
        ret += "names = %s, " % self.regname
        ret += "types = %s, rows=[" % self.regtype
        for i in range (len (self.ts)):
            if i > 0:
                ret += ", "
            ret += "0x%08x, " % self.ts[i]
            ret += "%s" % self.row[i]
        ret += "]"
        return ret
