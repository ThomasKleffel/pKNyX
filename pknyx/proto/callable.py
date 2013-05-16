# -*- coding: utf-8 -*-


class Foo(object):
    """
    """

    def __init__(self):
        """
        """

    def __call__(self, ga=None, id_=None):
        """
        """
        print ga, id_
        return self

    def test(self):
        """
        """
        print "test"


foo = Foo()

foo(ga=3).test()
