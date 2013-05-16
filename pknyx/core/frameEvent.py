# -*- coding: utf-8 -*-

""" Python KNX framework

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

Bus frame management

Implements
==========

 - B{FrameEvent}

Documentation
=============


Usage
=====


@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

from pknyx.common.loggingServices import Logger


class FrameEvent(object):
    """ Bus frame event handling
    """
    def __init__(self, source, frame):
        """ Create a FrameEvent object

        @param source:
        @type source:

        @param frame:
        @type frame:
        """
        super(FrameEvent, self).__init__()



#public class FrameEvent extends EventObject
#{
    #private static final long serialVersionUID = 1L;

    #private final CEMI c;
    #private final byte[] b;

    #/**
     #* Creates a new frame event for <code>frame</code>.
     #* <p>
     #*
     #* @param source the creator of this event
     #* @param frame cEMI frame
     #*/
    #public FrameEvent(final Object source, final CEMI frame)
    #{
        #super(source);
        #c = frame;
        #b = null;
    #}

    #/**
     #* Creates a new frame event for <code>frame</code>.
     #* <p>
     #*
     #* @param source the creator of this event
     #* @param frame EMI2 L-data frame
     #*/
    #public FrameEvent(final Object source, final byte[] frame)
    #{
        #super(source);
        #b = frame;
        #c = null;
    #}

    #/**
     #* Returns the cEMI frame, if supplied at event creation.
     #* <p>
     #*
     #* @return cEMI frame object, or <code>null</code>
     #*/
    #public final CEMI getFrame()
    #{
        #return CEMIFactory.copy(c);
    #}

    #/**
     #* Returns the frame as byte array, if supplied at event creation.
     #* <p>
     #*
     #* @return copy of frame as byte array, or <code>null</code>
     #*/
    #public final byte[] getFrameBytes()
    #{
        #return b != null ? (byte[]) b.clone() : null;
    #}
#}