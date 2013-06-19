# -*- coding: utf-8 -*-

""" Python KNX framework

License
=======

 - B{pKNyX} (U{http://www.pknyx.org}) is Copyright:
  - (C) 2013 Frédéric Mantegazza

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
or see:

 - U{http://www.gnu.org/licenses/gpl.html}

Module purpose
==============

Queue management

Implements
==========

 - B{PriorityQueue}
 - B{PriorityQueueValueError}

Documentation
=============

priorityDistribution meaning

Every array element correspondes to one of the priority steps (except the last step):
If element 0 is N, you get N times objects with priority 0 and 1 time objects with all lower priorities when calling
'remove'-method sequentially (if there are element with prioriy 0).

Value 0 blocks an priority step and values < 0 mean that first you get all objects with the corresponding priority.

Example

There are three priority steps. The priorityDistribution is {-1,3} and the following objects are in the queue:
3 objects w. priority 0, 5 with 1 and 2 with 2.
First you get all objects with priority 0, then 3 of the objects with priority 1, then one with pr. 2, then the
remaining 2 objects with pr. 1 and at last the remaining with pr. 2.

The size of this array must be smaller by one than the number of priority steps.

The array is be used internally (it is not cloned)

A queue inherits threading.Condition object, so can block/notify calling threads

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

import copy
import threading

from pknyx.common.exception import PKNyXValueError
from pknyx.common.loggingServices import Logger


class PriorityQueueValueError(PKNyXValueError):
    """
    """


class PriorityQueue(threading.Condition):
    """ PriorityQueue class

    @ivar _priorityDistribution: determines the handling of the different priorities
    @type _priorityDistribution: list/tuple of int
    """
    def __init__(self, prioritySteps, priorityDistribution):
        """ Create a new PriorityQueue

        @param prioritySteps: determines the number of priority steps the queue holds
        @type prioritySteps: int

        @param priorityDistribution: determines the handling of the different priorities
        @type priorityDistribution: list/tuple of int

        raise PriorityQueueValueError:
        """
        super(PriorityQueue, self).__init__()

        self._priorityDistribution = priorityDistribution

        if prioritySteps < 1:
            raise PriorityQueueValueError("there must be a least one priority step")

        if len(priorityDistribution) + 1 != noPrioritySteps:
            raise PriorityQueueValueError("size of array 'priorityDistribution' must be smaller by one than 'noPrioritySteps'")

        self._priorityDistribution = priorityDistribution

        self._count = copy.copy(priorityDistribution)
        self._queue = noPrioritySteps * [[]]


    def add(self, obj, priority):
        """ Add an element to the queue

        Add the given element to the queue according to the given priority, behind the last element with the same
        priority.

        @param obj: element to be inserted into the queue
        @type obj: any

        @param priority: priority value of the object to add
        @type priority: int
        """
        queue[priority].append(obj)

    def remove(self):
        """ Removes and returns the next element from this queue

        @return  The next element from this queue (None if queue is empty)
        """
        for i in range(len(queue) - 1):
            if count[i] == 0:
                count[i] = distr[i]
            elif queue[i].size() != 0:
                if count[i] > 0:
                    count[i] -= 1
                return queue[i].removeFirst()

        while i >= 0:
            if queue[i].size() != 0:
                return queue[i].removeFirst()
            i -= 1

        return None


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class PriorityQueueTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
