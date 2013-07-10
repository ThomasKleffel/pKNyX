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

One of the nice feature of B{pKNyX} is to be able to register some L{FunctionalBlock<pknyx.core.functionalBlock>}
sub-classes methods to have them executed at specific times. For that, B{pKNyX} uses the nice third-party module
U{APScheduler<http://pythonhosted.org/APScheduler>}.

The idea is to use the decorators syntax to register these methods:

class MyBlock(FunctionalBlock):

    @scheduler.every(minutes=5)
    def update(self):
        # do anything needed to update

Unfortunally, a decorator can only wraps a function. But what we want is to register an instance method! How can it be
done, as we didn't instanciated the class yet?

Luckily, such classes are not directly instanciated by the user, but through the L{ETS<pknyx.core.ets>} register()
method. So, here is how this registration is done.

Instead of directly using the APScheduler, the Scheduler class below provides the decorators we need (every(), in this
example), and maintains a list of names of the decorated functions, in _pendingFuncs.

Then, when a new instance of the FunctionalBlock sub-class is created, in ets.register(), we call the
Scheduler.doRegisterJobs() method which tried to retreive the bounded method matching one of the decorated functions.
If found, the method is registered in L{APScheduler<apscheduler.scheduler>}.

Scheduler also adds a listener to be notified when a decorated method call fails to be run, so we can log it.

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id: template.py 130 2013-07-02 08:58:54Z fma $"

import traceback

import apscheduler.scheduler

from pknyx.common.exception import PKNyXValueError
from pknyx.services.loggingServices import Logger, LEVELS

scheduler = None


class SchedulerValueError(PKNyXValueError):
    """
    """


class Scheduler_(object):
    """ Scheduler class
    """
    def __init__(self):
        """

        raise SchedulerValueError:
        """
        super(Scheduler_, self).__init__()

        self._pendingFuncs = []

        self._apscheduler = apscheduler.scheduler.Scheduler()
        self._apscheduler.add_listener(self._listener, mask=(apscheduler.scheduler.EVENT_JOB_ERROR|apscheduler.scheduler.EVENT_JOB_MISSED))

    def _listener(self, event):
        """ APScheduler listener.

        This listener is called by L{APScheduler<apscheduler.scheduler>} when executing jobs.

        It can be setup so only errors are triggered.
        """
        Logger().debug("Scheduler._listener(): event=%s" % repr(event))

        if event.exception:
            message = "\n" + "".join(traceback.format_tb(event.traceback)) + str(event.exception)
            Logger().log(LEVELS['exception'], message)

    @property
    def apscheduler(self):
        return self._apscheduler

    def addEveryJob(self, func, **kwargs):
        """ Add a job which has to be called 'every xxx'

        @param func: job to register
        @type func: callable
        """
        Logger().debug("Scheduler.addEveryJob(): func=%s" % repr(func))
        self._pendingFuncs.append(("every", func, kwargs))

    def every(self, **kwargs):
        """ Decorator for addEveryJob()
        """
        Logger().debug("Scheduler.every(): kwargs=%s" % repr(kwargs))

        def decorated(func):
            """ We don't wrap the decorated function!
            """
            self.addEveryJob(func, **kwargs)

            return func

        return decorated

    def addAtJob(self, func, **kwargs):
        """ Add a job which has to be called 'at xxx'

        @param func: job to register
        @type func: callable
        """
        Logger().debug("Scheduler.addAtJob(): func=%s" % repr(func))
        self._pendingFuncs.append(("at", func, kwargs))

    def at(self, **kwargs):
        """ Decorator for addAtJob()
        """
        Logger().debug("Scheduler.at(): kwargs=%s" % repr(kwargs))

        def decorated(func):
            """ We don't wrap the decorated function!
            """
            self.addAtJob(func, **kwargs)

            return func

        return decorated

    def addCronJob(self, func, **kwargs):
        """ Add a job which has to be called with cron

        @param func: job to register
        @type func: callable
        """
        Logger().debug("Scheduler.addCronJob(): func=%s" % repr(func))
        self._pendingFuncs.append(("cron", func, kwargs))

    def cron(self, **kwargs):
        """ Decorator for addCronJob()
        """
        Logger().debug("Scheduler.cron(): kwargs=%s" % repr(kwargs))

        def decorated(func):
            """ We don't wrap the decorated function!
            """
            self.addCronJob(func, **kwargs)

            return func

        return decorated

    def doRegisterJobs(self, obj):
        """ Really register jobs.

        @param obj: instance for which a method may have been pre-registered
        @type obj:
        """
        Logger().debug("Scheduler.doRegisterJobs(): obj=%s" % repr(obj))

        for type_, func, kwargs in self._pendingFuncs:
            Logger().debug("Scheduler.doRegisterJobs(): type_=\"%s\", func=%s, kwargs=%s" % (type_, func.func_name, repr(kwargs)))
            try:
                method = getattr(obj, func.func_name)
                Logger().debug("Scheduler.doRegisterJobs(): method=%s" % repr(method))
                if method.im_func is func:
                    if type_ == 'every':
                        self._apscheduler.add_interval_job(method, **kwargs)
                    elif type_ == 'at':
                        self._apscheduler.add_date_job(method, **kwargs)
                    elif type_ == 'cron':
                        self._apscheduler.add_cron_job(method, **kwargs)
            except AttributeError:
                Logger().exception("Scheduler.doRegisterJobs()", debug=True)

    def printJobs(self):
        """ Print pending jobs
        """
        self._apscheduler.print_jobs()

    def start(self):
        """ Start the scheduler
        """
        self._apscheduler.start()

    def shutdown(self):
        """ Sshutdown the scheduler
        """
        self._apscheduler.shutdown()


# Scheduler factory
def Scheduler():
    global scheduler
    if scheduler is None:
        scheduler = Scheduler_()

    return scheduler


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
