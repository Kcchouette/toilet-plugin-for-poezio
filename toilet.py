"""
This plugin uses toilet to transform every message into an ascii-art
message.

Installation
------------
You only have to load the plugin (and have :file:`toilet` installed, of course).
::

    /load toilet


Usage
-----

Say something in a Chat tab, with an arg1 and arg2 `<font> <filter> <message>`

.. note:: Can create fun things when used with :ref:`The rainbow plugin <rainbow-plugin>`.

"""
from plugin import BasePlugin
import subprocess

class Plugin(BasePlugin):
    def init(self):
        self.api.add_event_handler('muc_say', self.setoilette)
        self.api.add_event_handler('conversation_say', self.setoilette)
        self.api.add_event_handler('private_say', self.setoilette)

    def setoilette(self, msg, tab):
        msgsplit = msg['body'].split()
        if len(msgsplit) > 2:
            process = subprocess.Popen(['toilet', '-f', msgsplit[0], '--filter', msgsplit[1], ' '.join(msgsplit[2:])], stdout=subprocess.PIPE)
            result = process.communicate()[0].decode('utf-8')
            msg['body'] = result
