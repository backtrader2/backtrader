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

import backtrader as bt

__all__ = ['KeltnerChannel']

class KeltnerChannel(bt.Indicator):
    '''
    Keltner channel is a technical analysis indicator showing a central moving average line
    plus channel lines at a distance above and below.
    The indicator is named after Chester W. Keltner (1909–1998)
    who described it in his 1960 book How To Make Money in Commodities.
    This name was applied by those who heard about it from him,
    but Keltner called it the ten-day moving average trading rule
    and indeed made no claim to any originality for the idea.

    Formula:
      - midband = SimpleMovingAverage((high+low+close)/3, period)
      - topband = midband + devfactor * SimpleMovingAverage((high - low)/2, period)
      - botband = midband - devfactor * SimpleMovingAverage((high - low)/2, period)

    See:
      - https://en.wikipedia.org/wiki/Keltner_channel
    Parameters :
    period : moving average period
    devfactor : deviation factor
    movav : moving average type. ex : backtrader.indicators.MovAv.SMA, MovAv.EMA, MovAv.DEMA, MovAv.HMA etc. See mabase.py
    '''

    lines = ('mid', 'top', 'bot',)
    params = (('period', 10), ('devfactor', 2.0), ('movav', bt.ind.MovAv.Simple),)

    plotinfo = dict(subplot=False)
    plotlines = dict(
        mid=dict(ls='--'),
        top=dict(_samecolor=True),
        bot=dict(_samecolor=True),
    )

    def _plotlabel(self):
        plabels = [self.p.period, self.p.devfactor]
        plabels += [self.p.movav] * self.p.notdefault('movav')
        return plabels

    def __init__(self):
        self.lines.mid = ma = self.p.movav((self.data.high + self.data.low + self.data.close)/3 , period=self.p.period)
        deviation = self.p.devfactor * self.p.movav((self.data.high - self.data.low)/2, period=self.p.period)
        self.lines.top = ma + deviation
        self.lines.bot = ma - deviation

        super(KeltnerChannel, self).__init__()