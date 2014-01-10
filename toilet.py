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

"""
from plugin import BasePlugin
import subprocess

import xhtml

class Plugin(BasePlugin):
    def init(self):
        self.api.add_event_handler('muc_say', self.setoilette)
        self.api.add_event_handler('conversation_say', self.setoilette)
        self.api.add_event_handler('private_say', self.setoilette)

    def nocommand(self, text):
        """ find if another command is insert (like -h)
        lstrip for remove left spaces
        """
        if text.lstrip().startswith('-'):
            return False
        return True

    def setoilette(self, msg, tab):
        """ split body, get html toilet result, remove title, convert to poezio style """
        msgsplit = xhtml.clean_text(msg['body']).split()
        # check if ok
        if len(msgsplit) > 2 and self.nocommand(msgsplit[0]) and self.nocommand(msgsplit[1]) and self.nocommand(' '.join(msgsplit[2:])):
            xhtml_result = None
            try:
            # -f == --font && -E == --export <format>
                process = subprocess.Popen(['toilet', '-E', 'html', '-f', msgsplit[0], '--filter', msgsplit[1], ' '.join(msgsplit[2:])], stdout=subprocess.PIPE)
                xhtml_result = process.communicate()[0].decode('utf-8')
            except:
                xhtml_result = None
            if xhtml_result:
                # remove title
                titlefind = xhtml_result.find('<title>')
                if titlefind:
                    xhtml_result = xhtml_result[:titlefind] + xhtml_result[xhtml_result.find('</title>')+8:]
                # convert to poezio color ## not work like wanted, color not show
                result = "\n" + xhtml.xhtml_to_poezio_colors(xhtml_result)
                msg['body'] = result
            else:
                msg['body'] = ' '.join(msgsplit[2:])
