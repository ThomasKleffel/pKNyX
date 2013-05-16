# -*- coding: utf-8 -*-

""" Python KNX framework.

License
=======

 - B{pKNyX} (U{http://www.pknyx.org}) is Copyright:
  - (C) 2013 Frédéric Mantegazza

Licensed under the EUPL, Version 1.1 or - as soon they will be approved by
the European Commission - subsequent versions of the EUPL (the "Licence");
You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:

 - U{http://ec.europa.eu/idabc/eupl}

Unless required by applicable law or agreed to in writing, software distributed
under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.

See the Licence for the specific language governing permissions and limitations
under the Licence.

Module purpose
==============

Helper functions

Implements
==========

 - reprStr
 - prettyFormat
 - isOdd
 - hmsToS
 - hmsToS
 - hmsAsStrToS
 - sToHms
 - sToHmsAsStr

Documentation
=============

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

from pprint import PrettyPrinter

from pknyx.common import config


def reprStr(obj):
    """ Return a simple name for the object instance.

    <function myFunc at 0x405b1a3c>                                                     -> myFunc
    <class 'module1.module2.MyClass'>                                                   -> myClass
    <class 'module1.module2.MyClass' at 0x408cd3ec>                                     -> MyClass
    <unbound method MyClass.myMethod>                                                   -> myMethod
    <bound method MyClass.myMethod of <module1.module2.MyClass instance at 0x40585e0c>> -> myMethod
    <module1.module2.MyClass instance at 0x40585e2c>                                    -> MyClass at 0x40585e2c
    <module1.module2.MyClass object at 0x40585e2c>                                      -> MyClass at 0x40585e2c
    """
    reprObj = repr(obj)
    reprObj = reprObj.replace("'", "")
    reprObj = reprObj.replace("<", "")
    reprObj = reprObj.replace(">", "")

    if reprObj.find("class") != -1:
        fields = reprObj.split()
        strValue = fields[1].split('.')[-1]

    elif reprObj.find("unbound method") != -1:
        fields = reprObj.split()
        strValue = fields[2].split('.')[-1]

    elif reprObj.find("bound method") != -1:
        fields = reprObj.split()
        strValue = fields[2].split('.')[-1]

    elif reprObj.find("function") != -1:
        fields = reprObj.split()
        strValue = fields[1]

    elif reprObj.find("instance") != -1:
        fields = reprObj.split()
        strValue = "%s at %s" % (fields[0].split('.')[-1], fields[-1])

    elif reprObj.find("object") != -1:
        fields = reprObj.split()
        strValue = "%s at %s" % (fields[0].split('.')[-1], fields[-1])

    else:
        strValue = reprObj

    #reprList = strValue.split()
    #for iPos in xrange(len(reprList)):

        ## Default repr for classes
        #if reprList[iPos] == "<class":
            #strValue = reprList[iPos+1].split(".")[-1][:-2]
            #break

        ## Default repr for methods
        #elif reprList[iPos] == "method":
            #strValue = reprList[iPos+1]
            #break

        ## Default repr for instances
        #elif reprList[iPos] == "object" or reprList[iPos] == "instance":
            #strValue = reprList[iPos-1].split(".")[-1]+" at "+reprList[iPos+2].split(">")[0]
            #break

    return strValue

def prettyFormat(value):
    """ Pretty format a value.

    @param value: value to pretty format
    @type value: python object

    @return: the value pretty formated
    @rtype: str
    """
    pp = PrettyPrinter()
    prettyStr = pp.pformat(value)

    return prettyStr

def isOdd(value):
    """ Test if value is odd.

    @param value: value to test
    @type value: int
    """
    return int(value / 2.) != value / 2.

def hmsToS(h, m, s):
    """ Convert hours, minutes, seconds to seconds.

    @param h: hours
    @type h: int

    @param m: minutes
    @type m: int

    @param s: seconds
    @type s: int

    @return: seconds
    @rtype: int
    """
    return (h * 60 + m) * 60 + s

def hmsAsStrToS(hhmmss):
    """ Convert hh:mm:ss to seconds.

    @param hhmmss: hours, minutes and seconds
    @type hhmmss: str

    @return: seconds
    @rtype: int
    """
    hhmmss = hhmmss.split(':')
    h = int(hhmmss[0])
    m = int(hhmmss[1])
    s = int(hhmmss[2])
    return hmsToS(h, m, s)

def sToHms(s):
    """ Convert seconds to hours, minutes, seconds.

    @param s: seconds
    @type s: int

    @return: hours, minutes, seconds
    @rtype: tuple of int
    """
    if s < 0:
        s = 0
    h = int(s / 3600)
    m = int((s - h * 3600) / 60)
    s -= (h * 3600 + m * 60)
    return h, m, s

def sToHmsAsStr(s):
    """ Convert seconds to hh:mm:ss.

    @param s: seconds
    @type s: int

    @return: hours, minutes, seconds
    @rtype: str
    """
    return "%02d:%02d:%02d" % sToHms(s)
