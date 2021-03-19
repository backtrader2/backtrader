#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015-2020 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import os

import testcommon

import backtrader as bt
import backtrader.indicators as btind
import pandas as pd

datafiles = ['orcl-2003-2005.txt', 'yhoo-2003-2005.txt']

chkvals = [
    ['0.124001', '1.682931', '0.146236'],
]

chkmin = 10
chkind = btind.OLS_BetaN
#chkargs = dict()

DATAFEED = bt.feeds.BacktraderCSVData
FROMDATE = datetime.datetime(2003, 1, 1)
TODATE = datetime.datetime(2005, 12, 31)

def getdata(datafile, fromdate=FROMDATE, todate=TODATE):
    modpath = os.path.dirname(os.path.abspath(__file__))
    dataspath = '../datas'
    datapath = os.path.join(modpath, dataspath, datafile)
    data = DATAFEED(
        dataname=datapath,
        fromdate=fromdate,
        todate=todate)

    return data

class TS2(testcommon.TestStrategy):
    def __init__(self):
        ind0 = self.data0.close
        ind1 = self.data1.close
        self.p.inddata = [ind0, ind1]
        self.ind = btind.OLS_BetaN(*self.p.inddata )

def test_run(main=False):
    datas = [getdata(i) for i in datafiles]
    testcommon.runtest(datas,
                       TS2,
                       main=main,
                       plot=main,
                       chkind=chkind,
                       chkmin=chkmin,
                       chkvals=chkvals)


if __name__ == '__main__':
    test_run(main=True)
