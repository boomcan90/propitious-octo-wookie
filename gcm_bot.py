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

from pubsub import pub

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

# iot_mahjong = 'fyygEukC5Hw:APA91bGyCm3e--AV1GMI0pmtBGjO3XiAjS8WqNW21TKVnGkLRAoJvzVskgX_4FM5JdaZYOG7Lmmg8lF8sII5lQcxetW2kvSLbwTvd18OgicF1zT6gFQ8YIwIwZy32VvTvwmcE3RLQWBe'
# iot_mahjong_s6 = 'c198uVK7Dgw:APA91bEvUwogy4q0Px33WfHpOPvOZe6U7uCML1hd1e7LDuBfoGC7zdErxWvBpld-FczRi8hFc4z5brY-WEIXXsXFiAgTQ9Ligyk_acrMfClitaq9mzyNqgW8RB2r76Tz8FjCZVYJbEhF'

iot_mahjong = 'esFRv1m7kuM:APA91bEulv8eXb6kalzNzz5BE6CbbyEhjahdJKEgI2FOePEUauOWBNKupQdJDKLT-PrUxZc4vi2KX6XWAzzKXn1tR_FEYHCCKvTFUyBhunISSATVw_ZZ9dEtqjXBkjkqdYr-1JvpIHJq'

iot_mahjong_s6 = 'eMHlZwX1uFE:APA91bHegAMIfFxsveZqUM04In2NYTxUeuvWS5_iD4IW9sgGVGU3airy-1t1iQny5iRMaPooEzZofEdsQOvDGseczSxf6gLVMvwM5k3dqi4XqjfIN6VhTsUb3RKaD7greAFimVcu43Jn'

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
        pub.sendMessage('clientMessageReceived', arg1=gcm, arg2="message received!")
        if gcm.get('message_type', False) in ('ack', 'receipt'):
            if gcm['message_type'] == 'ack':
                print u"GCM received successfully but handphone may not have gotten message yet."
            if gcm.get('message_type', False) == 'receipt':
                print gcm['data']['message_status']
                print u"GCM Receipt! Android handphone received the message!"
        if gcm.get('data', False) and gcm['data'].has_key('test'):
            print(u"has key teSt")
        if gcm.get('data', False) and gcm['data'].has_key('text'):
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
