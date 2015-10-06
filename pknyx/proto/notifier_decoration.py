# -*- coding: utf-8 -*-

from pknyx.common.singleton import Singleton
from pknyx.services.logger import Logger


class Notifier(object):
    __metaclass__ = Singleton

    def __init__(self):
        super(Notifier, self).__init__()

        self._pendingFuncs = []
        self._datapointJobs = {}

    def _executeJob(self, method, event):
        try:
            method(event)
        except:
            Logger().exception("Notifier._executeJob()")

    def addDatapointJob(self, func, dp, condition="change", thread=False):
        Logger().debug("Notifier.addDatapointJob(): func=%s, dp=%s" % (repr(func), repr(dp)))

        if condition not in ("change", "always"):
            raise NotifierValueError("invalid condition (%s)" % repr(condition))

        self._pendingFuncs.append(("datapoint", func, (dp, condition, thread)))

    def datapoint(self, dp, *args, **kwargs):
        """ Decorator for addDatapointJob()
        """
        Logger().debug("Notifier.datapoint(): dp=%s, args=%s, kwargs=%s" % (repr(dp), repr(args), repr(kwargs)))

        def decorated(func):
            """ We don't wrap the decorated function!
            """
            Logger().debug("Notifier.datapoint():decorated(): func.__class__.__bases__=%s" % func.__class__.__bases__)

            self.addDatapointJob(func, dp, *args, **kwargs)

            return func

        return decorated

    def doRegisterJobs(self, obj):
        Logger().debug("Notifier.doRegisterJobs(): obj=%s" % repr(obj))

        for type_, func, args in self._pendingFuncs:
            Logger().debug("Notifier.doRegisterJobs(): type_=\"%s\", func=%s, args=%s" % (type_, func.func_name, repr(args)))
            method = getattr(obj, func.func_name, None)
            if method is not None:
                Logger().debug("Notifier.doRegisterJobs(): add method %s() of %s" % (method.im_func.func_name, method.im_self))
                if method.im_func is func:
                    if type_ == "datapoint":
                        dp, condition, thread = args
                        try:
                            self._datapointJobs[obj][dp].append((method, condition, thread))
                        except KeyError:
                            try:
                                self._datapointJobs[obj][dp] = [(method, condition, thread)]
                            except KeyError:
                                self._datapointJobs[obj] = {dp: [(method, condition, thread)]}
                        #print self._datapointJobs

    def datapointNotify(self, obj, dp, oldValue, newValue):
        Logger().debug("Notifier.datapointNotify(): obj=%s, dp=%s, oldValue=%s, newValue=%s" % (obj.name, dp, oldValue, newValue))

        if dp in self._datapointJobs[obj].keys():
            for method, condition, thread_ in self._datapointJobs[obj][dp]:
                if oldValue != newValue and condition == "change" or condition == "always":
                    try:
                        Logger().debug("Notifier.datapointNotify(): trigger method %s() of %s" % (method.im_func.func_name, method.im_self))
                        event = dict(name="datapoint", dp=dp, oldValue=oldValue, newValue=newValue, condition=condition, thread=thread_)

                        if thread_:
                            thread.start_new_thread(self._executeJob, (method, event))
                        else:
                            self._executeJob(method, event)
                    except:
                        Logger().exception("Notifier.datapointNotify()")

    def printJobs(self):
        """ Print registered jobs
        """


def main():
    Logger().setLevel('trace')

    notifier = Notifier()

    class Test1:
        def __init__(self, name):
            self.name = name

        @notifier.datapoint("toto")
        def test(self, event):
            Logger().info("Test.test(): name=%s, event=%s" % (self.name, event))

    class Test2:
        def __init__(self, name):
            self.name = name

        @notifier.datapoint("toto")
        def test(self, event):
            Logger().info("Test.test(): name=%s, event=%s" % (self.name, event))

    t1_1 = Test1("t1_1")
    t1_2 = Test1("t1_2")

    t2_1 = Test2("t2_1")
    t2_2 = Test2("t2_2")

    notifier.doRegisterJobs(t1_1)
    notifier.doRegisterJobs(t1_2)
    notifier.doRegisterJobs(t2_1)
    notifier.doRegisterJobs(t2_2)

    notifier.datapointNotify(t1_2, dp='toto', oldValue=0, newValue=1)


if __name__ == '__main__':
    main()
