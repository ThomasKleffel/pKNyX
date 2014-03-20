# -*- coding: utf-8 -*-

""" Python KNX framework

License
=======

 - B{pKNyX} (U{http://www.pknyx.org}) is Copyright:
  - (C) 2013-2014 Frédéric Mantegazza

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

 - B{MUA}

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


class MUAValueError(PKNyXValueError):
    """
    """

class MUA(object):
    """ Mail User Agent class

    @ivar _smtp: SMTP server to use to send e-mails
    @type _smtp: str

    @ivar _subject: subject of e-mail
    @type _subject: str

    @ivar _to: recipient
    @type _to: str

    @ivar _from: sender
    @type _from: str
    """
    def __init__(self, smtp="localhost", subject=None, to=None, from_=None):
        """ create

        @param smtp: SMTP server
        @type smtp: str

        @param subject: subject of e-mail
        @type subject: str

        @param to: recipient
        @type to: str

        @param from_: sender
        @type from_: str
        """
        super(MUA, self).__init__()

        self._smtp = smtp

        self._subject = subject
        self._to = to
        self._from = from_

    def send(self, msg, subject=None, to=None, from_=None):
        """ Send an e-mail

        @param subject: subject of e-mail
        @type subject: str

        @param to: recipient
        @type to: str

        @param from_: sender
        @type from_: str
        """
        if subject is not None:
            self._subject = subject
        if to is not None:
            self._to = to
        if from_ is not None:
            self._from = from_

        if self._to is None:
            raise MUAValueError("subject must be specified, at least the first time")
        if self._to is None:
            raise MUAValueError("recipient must be specified, at least the first time")
        if self._from is None:
            raise MUAValueError("sender must be specified, at least the first time")

        # Create a text/plain message
        message = email.mime.text.MIMEText(msg)

        message['Subject'] = self._subject
        message['From'] = self._from
        message['To'] = self._to

        # Send the message via SMTP server, but don't include the envelope header
        smtp = smtplib.SMTP(self._smtp)
        smtp.sendmail(message['From'], [message['To']], message.as_string())
        smtp.quit()


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class MUATestCase(unittest.TestCase):

        def setUp(self):
            self.mua = MUA(smtp="localhost", subject="MUATestCase", to="pknyx@pknyx.org", from_="pknyx@pknyx.org")

        def tearDown(self):
            pass

        def test_send(self):
            self.mua.send("This is a test")
            mua = MUA("localhost")
            with self.assertRaises(MUAValueError):
                mua.send("Error")


    unittest.main()
