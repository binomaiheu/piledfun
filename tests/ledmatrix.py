#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ledmatrixpy
#  
#  Copyright 2019  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import time

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, LCD_FONT

import speech_recognition as sr
import sphinxbase
import pocketsphinx


def main(args):
    
    # intensity [0-15]
    # only have 10 kOhm resistor, so no high values here
    intensity = 2
    
    # create matrix device
    s = spi( port=0, device=0, gpio=noop())
    #d = max7219(s, cascaded=1, rotate=3 )
    d = max7219(s, cascaded=1 )
    d.contrast( intensity * 16 )

    time.sleep(1)
    
    # speech recognition
    WIT_AI_KEY='IVRCR4XCMWW343X2YIKHFDXMBBK7KMEM'
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Calibrating...")
        r.adjust_for_ambient_noise(source,duration=5)
        print("Say something...")
        audio = r.listen(source)
        
    msg = ""
    
    try:
        msg = r.recognize_witai( audio )
        print( "Wit.ai: " + msg )
    except sr.UnknownValueError:
        print("Wit.ai did not understand audio")
    except sr.RequestError as e:
        print("Wit.ai could not request results: {0}".format(e) )
        
    
    show_message( d, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.15 )

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
