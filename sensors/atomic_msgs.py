#
# atomic_msgs.py - Send data to the cogserver/atomspace.
#
# Copyright (C) 2015,2016,2017  Linas Vepstas
# Copyright (C) 2016,2017  Hanson Robotics
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License v3 as
# published by the Free Software Foundation and including the exceptions
# at http://opencog.org/wiki/Licenses
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, write to:
# Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from netcat import netcat


# The code here is a quick, cheap hack to place information into the
# cogserver atomspace. It opens a socket to the cogserver, and sends
# scheme snippets across.  These areu usually some Atomese.
#
class AtomicMsgs:

    def __init__(self):
        self.hostname = "localhost"
        self.port = 17001
        self.OCTOMAP_NAME = "faces"
        self.SPATIAL_RESOLUTION = "0.1"
        self.TIME_RESOLUTION = "10"
        self.TIME_UNITS = "100"

    # --------------------------------------------------------
    # Wholeshow control -- Start and stop openpsi
    # XXX Not functional
    def wholeshow_stop(self):
        netcat(self.hostname, self.port, "(disable-all-demos)")
        netcat(self.hostname, self.port, "(halt)")

    def wholeshow_start(self):
        netcat(self.hostname, self.port, "(enable-all-demos)")
        netcat(self.hostname, self.port, '(run)')

    # Face postions in the space-server
    def perceived_face(self, faceid, xx, yy, zz):
        face = '(perceived-face ' + str(faceid) + ' ' + str(xx) + ' ' + ' ' + str(yy) + ' ' + str(zz) + ')' + "\n"
        netcat(self.hostname, self.port, face)

    def perceived_emotion(self, faceid, emotiontype, strength):
        # (perceived-face-happy "UUID" happy 0.4)
        face = '(perceived-emotion ' + str(faceid) + ' ' + str(emotiontype) + ' ' + str(strength) + ')' + "\n"
        netcat(self.hostname, self.port, face)

    # --------------------------------------------------------
    # Speech-to-text stuff
    def perceived_sentence(self, stt):
        spoke = "(ghost \"" + stt + "\")\n"
        netcat(self.hostname, self.port, spoke)

    def perceived_word(self, stt):
        spoke = "(perceived-word \"" + stt + "\")\n"
        netcat(self.hostname, self.port, spoke)

    # Affect in speech
    # Indicate that the robot heard freindly speech
    def affect_happy(self):
        netcat(self.hostname, self.port, "(State chat-affect chat-happy)")

    # Indicate that the robot heard negative speech
    def affect_negative(self):
        netcat(self.hostname, self.port, "(State chat-affect chat-negative)")

    # --------------------------------------------------------
    # Text-to-speech stuff
    # Let atomspace know that vocalization has started or ended.
    def vocalization_started(self):
        netcat(self.hostname, self.port, "(State chat-state chat-start)")

    def vocalization_ended(self):
        netcat(self.hostname, self.port, "(State chat-state chat-stop)")

    # --------------------------------------------------------
    # Sound localization -- send 3D xyz coordinate of sound source
    def update_sound(self, x, y, z):
        snd = "(map-sound " + str(x) + " " + str(y) + " " + str(z) + ")\n"
        netcat(self.hostname, self.port, snd)

    def audio_energy(self, decibel):
        # A StateLink is used because evaluation of psi-rules should
        # only depend on the most recent value.
        deci = '(StateLink (AnchorNode "Decibel value") ' + \
               ' (NumberNode ' + str(decibel) + '))\n'
        netcat(self.hostname, self.port, deci)

    # Louds bands, explosions, hand-claps, shouts.
    def audio_bang(self, decibel):
        loud = '(StateLink (AnchorNode "Sudden sound change value")' + \
               ' (NumberNode ' + str(decibel) + '))\n'
        netcat(self.hostname, self.port, loud)

    # saliency location
    # Degree of the salient point
    def saliency(self, x, y, z, deg):
        sal = '(StateLink (AnchorNode "Salient location")' + \
              '(List (NumberNode ' + str(x) + ')' + \
              '  (NumberNode ' + str(y) + ')' + \
              '  (NumberNode ' + str(z) + ')))\n' + \
              '(StateLink (AnchorNode "Salient degree")' + \
              '  (NumberNode ' + str(deg) + '))\n'
        netcat(self.hostname, self.port, sal)

    # room luminance <=25 - dark, <=40 - normal, >40 - bright
    def room_brightness(self, bright):
        room = '(StateLink (AnchorNode "luminance")' + \
               ' (NumberNode ' + str(bright) + '))\n'
        netcat(self.hostname, self.port, room)

    # --------------------------------------------------------
    # Generic
    def evaluate_scm(self, scm_string):
        netcat(self.hostname, self.port, scm_string)
