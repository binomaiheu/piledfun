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
from luma.core.render import canvas
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, LCD_FONT

import numpy as np
from PIL import Image


def main(args):
    
    # intensity [0-15]
    # only have 10 kOhm resistor, so no high values here
    intensity = 2
    
    # create matrix device
    s = spi( port=0, device=0, gpio=noop())
    #d = max7219(s, cascaded=1, rotate=3 )    
    d = max7219(s, cascaded=1, rotate=0)    
    d.contrast( intensity * 16 )

    time.sleep(1)
    
    msg = "hallo, bino"
    
    happy_smiley=[
    [0,0,1,1,1,1,0,0],
    [0,1,0,0,0,0,1,0],
    [1,0,1,0,0,1,0,1],
    [1,0,0,0,0,0,0,1],
    [1,0,1,0,0,1,0,1],
    [1,0,0,1,1,0,0,1],
    [0,1,0,0,0,0,1,0],
    [0,0,1,1,1,1,0,0]]
    
    neutral_smiley=[
    [0,0,1,1,1,1,0,0],
    [0,1,0,0,0,0,1,0],
    [1,0,1,0,0,1,0,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1],
    [0,1,0,0,0,0,1,0],
    [0,0,1,1,1,1,0,0]]
    
    sad_smiley=[
    [0,0,1,1,1,1,0,0],
    [0,1,0,0,0,0,1,0],
    [1,0,1,0,0,1,0,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,1,1,0,0,1],
    [1,0,1,0,0,1,0,1],
    [0,1,0,0,0,0,1,0],
    [0,0,1,1,1,1,0,0]]
    
    happy_img = Image.fromarray(np.array(happy_smiley).astype('uint8')*255).convert(d.mode)
    neutral_img = Image.fromarray(np.array(neutral_smiley).astype('uint8')*255).convert(d.mode) 
    sad_img = Image.fromarray(np.array(sad_smiley).astype('uint8')*255).convert(d.mode)
    
    for k in range(20):
        d.display(happy_img)
        time.sleep(0.5)
        d.display(neutral_img)
        time.sleep(0.5)
        d.display(sad_img)
        time.sleep(0.5)
        d.display(neutral_img)
        time.sleep(0.5)
        
        
    #with canvas(d) as draw:
        #draw.rectangle(d.bounding_box, outline="white", fill="black")
        #time.sleep(1)
        #d.clear()
        
        #draw.point((1,0), fill="white")
        #time.sleep(1)
    
    
    #show_message( d, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.15 )

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
