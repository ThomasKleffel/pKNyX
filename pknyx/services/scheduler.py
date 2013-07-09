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

Scheduler management

Implements
==========

 - B{Scheduler}
 - B{SchedulerValueError}

Documentation
=============

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id: template.py 130 2013-07-02 08:58:54Z fma $"

import apscheduler.scheduler
#from apscheduler.scheduler import Scheduler as APScheduler

from pknyx.common.exception import PKNyXValueError
from pknyx.logging.loggingServices import Logger

scheduler = None


class SchedulerValueError(PKNyXValueError):
    """
    """


class SchedulerObject(object):
    """ Scheduler class

    This class is based on the excellent U{APScheduler<http://pythonhosted.org/APScheduler>}.
    We only add a few shortcuts for better named decorators.

    It can't work on class methods! So, we just store the methods and we will need to register it in the scheduler
    for each instance created. This will have to be done in ETS.weave(). Scheduler needs to be a Borg...
    """
    def __init__(self):
        """

        @param xxx:
        @type xxx:

        raise SchedulerValueError:
        """
        super(SchedulerObject, self).__init__()

        self._pendingJobs = []

        self._scheduler = apscheduler.scheduler.Scheduler()
        self._scheduler.add_listener(self._listener, mask=(apscheduler.scheduler.EVENT_JOB_ERROR|apscheduler.scheduler.EVENT_JOB_MISSED))

    def _listener(self, event):
        """
        """
        import traceback
        import logging
        Logger().debug("Scheduler._listener(): event=%s" % repr(event))
        if event.exception:
            message = "".join(traceback.format_tb(event.traceback)) + str(event.exception)
            Logger().log(logging.EXCEPTION, message)

    def every(self, **kwargs):
        """ Decorator version of :meth:`add_interval_job`.

        This decorator does not wrap its host function.
        Unscheduling decorated functions is possible by passing the ``job``
        attribute of the scheduled function to :meth:`unschedule_job`.
        """
        Logger().debug("SchedulerObject.every(): kwargs=%s" % repr(kwargs))
        def inner(func):
            Logger().debug("SchedulerObject.every().inner(): func=%s" % repr(func))
            self._pendingJobs.append(("every", func, kwargs))
            return func
        return inner

    def registerJobs(self, obj):
        """ Really register jobs.
        """
        Logger().debug("SchedulerObject.registerJobs(): obj=%s" % repr(obj))
        for type_, func, kwargs in self._pendingJobs:
            Logger().debug("SchedulerObject.registerJobs(): type_=\"%s\", func=%s, kwargs=%s" % (type_, func.func_name, repr(kwargs)))
            try:
                method = getattr(obj, func.func_name)
                Logger().debug("SchedulerObject.registerJobs(): method=%s" % repr(method))
                if method.im_func is func:
                    if type_ == 'every':
                        self._scheduler.add_interval_job(method, **kwargs)
                    elif type_ == 'at':
                        self._scheduler.add_date_job(method, **kwargs)
                    elif type_ == 'cron':
                        self._scheduler.add_cron_job(method, **kwargs)
            except AttributeError:
                Logger().exception("SchedulerObject.registerJobs()", debug=True)

    def printJobs(self):
        """
        """
        self._scheduler.print_jobs()

    def start(self):
        """
        """
        self._scheduler.start()


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class SchedulerTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()


# Scheduler factory
def Scheduler():
    global scheduler
    if scheduler is None:
        scheduler = SchedulerObject()

    return scheduler
