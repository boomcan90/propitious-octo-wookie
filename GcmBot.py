"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2010  Nathanael C. Fritz
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

import sys
import json
import logging
import getpass
from optparse import OptionParser

import sleekxmpp
import xml
import xml.sax.saxutils
from sleekxmpp.xmlstream import ElementBase, register_stanza_plugin
from sleekxmpp.xmlstream.matcher import MatchXPath
from sleekxmpp.xmlstream.handler import Callback
import uuid

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


MODE = 1 # 0 - demo, 1 - iot_mahjong

SERVER = 'gcm.googleapis.com'
PORT = 5235
USERNAME = '849833088289@gcm.googleapis.com'
PASSWORD = 'AIzaSyAXy1plvmocySlJ87_8R0Gvrr-QA9bcpOo'

iot_mahjong = 'eBd2GDS1x5c:APA91bGWN57R-M7LWk-yNS-M77WDCyu_1_xNIiv2CwCbWa2KS7b6-CmL2ZcrjvI3n71606jHvnfglkaqkkXKh13NR3f4PH7-5rth8jPlc7yCCwhpP-0SnjpNP5Fix3F_IC28k-Wu6G6K'

iot_mahjong_s6 = 'cX42As8_naw:APA91bF9r_m2vMLD63WCyGP8q-dkt6WpWAhyqF2WwFoZINl8pe00rHGH9Z_Tt8bZYYdg_tLxT1FQ8pyOUoT5cl35UhQmAuONKf_kTNnMzr6WdhlQdokM8_1AYcrTNURalrt5j7XLiE2s'

demo_app = 'f3NRmGAh1uk:APA91bH0UDlsrdZHwntB_aAZmbgkHdDnTKHxlkhbvTr4Ask7M7TUlGgwRWTBw8xlSizF87u449vm8elgCMSWoxgbRswMJz8ompK8kXqcBQggb8ITJtijonyP4AGrKm4csIBTEkI3TPu4'

regid = demo_app

if (MODE == 1):
    USERNAME = '1047425879020@gcm.googleapis.com'
    PASSWORD = 'AIzaSyD2JGPOyHFwGGbfgCfKHyuU3JuhZ0GqRic'
    regid = iot_mahjong


#from sleekxmpp.plugins.xep_0199.ping import XEP_0199


#class XEP_0199_m(XEP_0199):
#    default_config = {
#        'keepalive': True,
#        'interval': 100,
#        'timeout': 10
#    }

#definition GCM  stanzas
class Gcm(ElementBase):
    namespace = 'google:mobile:data'
    name = 'gcm'
    plugin_attrib = 'gcm'
    interfaces = set('gcm')
    sub_interfaces = interfaces


class GcmMessage(ElementBase):
    namespace = ''
    name = 'message'
    interfaces = set('gcm')
    sub_interfaces = interfaces
    subitem = (Gcm,)


register_stanza_plugin(GcmMessage, Gcm)


class GcmBot(sleekxmpp.ClientXMPP):
    """
    A simple SleekXMPP bot that will echo messages it
    receives, along with a short thank you message.
    """

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.register_handler(
            Callback('GcmMessage', MatchXPath('{%s}message/{%s}gcm' % (self.default_ns, 'google:mobile:data')),
                     self.message_callback))
        self.add_event_handler("session_start", self.start)

        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        # self.add_event_handler("Message", self.message)

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        # self.send_presence()
        # self.get_roster()
        print "started"

    def message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Thanks for sending\n%(body)s" % msg).send()

    def send_gcm_message(self, message):
        msg = GcmMessage()
        msg['gcm'].xml.text = xml.sax.saxutils.escape(json.dumps(message, ensure_ascii=False))
        self.send(msg)

    # I could then access the JSON data using:

    def message_callback(self, message):
        gcm = json.loads(message.xml.find('{google:mobile:data}gcm').text)
        # print gcm
        if gcm.get('message_type', False) in ('ack', 'receipt'):
            if gcm['message_type'] == 'ack':
                print "########################################################"
                print u"GCM received successfully"
            if gcm.get('message_type', False) == 'receipt':
                print "########################################################"
                print gcm['data']['message_status']
                print u"GCM Receipt!"
        if gcm.get('data', False) and gcm['data'].has_key('test'):
            print "########################################################"
            print(u"has key teSt")
        if gcm.get('data', False) and gcm['data'].has_key('text'):
            print "########################################################"
            print gcm['data']['number']+"-"+gcm['data']['text']
            print(u"has key teXt")

    def startConnection(self, blocking=False):
    # Connect to the XMPP server and start processing XMPP stanzas.
    # if self.connect((self.clientServer, self.port), use_ssl=True):
        logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-8s %(message)s')
        print "starting xmpp bot"
        if self.connect(('gcm.googleapis.com', 5235), use_ssl=True):
            print "starting..."
            self.use_signals()
            self.process(block=blocking)
            print "started!!!"
        else:
            print('Unable to connect.')
        return self
