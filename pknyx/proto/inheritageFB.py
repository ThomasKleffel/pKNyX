import copy

from pknyx.common.utils import reprStr

class Datapoint(object):
    def __init__(self, fb, **kwargs):
        super(Datapoint, self).__init__()

        self.fb = fb
        self.kwargs = kwargs


class FunctionalBlock(object):
    def __new__(cls, *args, **kwargs):
        self = super(FunctionalBlock, cls).__new__(cls)
        print "FunctionalBlock.new()", cls.__dict__

        self.datapoints = {}
        classes = cls.__bases__ + (cls,)
        for cls in classes:
            for key, value in cls.__dict__.iteritems():
                if key.startswith("DP_"):
                    name = value['name']
                    if self.datapoints.has_key(name):
                        raise ValueError("duplicated Datapoint (%s)" % name)
                    self.datapoints[name] = Datapoint(self, **value)

        return self

    def __init__(self, name):
        super(FunctionalBlock, self).__init__()

        self._name = name

        # Call for additionnal user init
        self.init()

    def __repr__(self):
        return "<%s(name='%s')>" % (reprStr(self.__class__), self._name)

    def __str__(self):
        return "<%s('%s')>" % (reprStr(self.__class__), self._name)

    def init(self):
        """ Additionnal user init
        """
        pass

    @property
    def name(self):
        return self._name

    @property
    def dp(self):
        return self._datapoints


class FB(FunctionalBlock):
    DP_ = dict(name="cmd", access="output", dptId="1.001", default="Off")

    def init(self):
        print "init():", self.name, repr(self.datapoints)

class FB1(FB):
    pass

class FB2(FB):
    pass


def main():
    fb = FB("fb")
    print "main():", repr(fb)
    fb1 = FB1("fb1")
    print "main():", repr(fb1)
    fb2 = FB2("fb2")
    print "main():", repr(fb2)


if __name__ == "__main__":
    main()
