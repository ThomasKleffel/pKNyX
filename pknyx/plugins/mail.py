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

Mail plugin

Implements
==========

 - B{Mail}

Documentation
=============

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2014 Frédéric Mantegazza
@license: GPL

@todo: rename to MailAlert (inheriting Alert)? Or use logging with email support?
"""

__revision__ = "$Id$"

import smtplib
import email.mime.text

from pknyx.common.exception import PKNyXValueError
from pknyx.services.logger import Logger


class MailValueError(PKNyXValueError):
    """
    """

class Mail(object):
    """ Mail class

    @ivar _:
    @type _:

    @todo:
    @todo:
    """
    def __init__(self, from_, to, subject, msg=""):
        """

        @param from_:
        @type from_:
        """
        super(Mail, self).__init__()

        # Create a text/plain message
        message = email.mime.text.MIMEText(msg)

        msg['Subject'] = subject
        msg['From'] = from_
        msg['To'] = to

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        s = smtplib.SMTP('localhost')
        s.sendmail(me, [you], msg.as_string())
        s.quit()
