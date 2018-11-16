import time
from basic_serial_instrument import BasicSerialInstrument

class SingleNeoPixel(BasicSerialInstrument):
    def __init__(self, *args, **kwargs):
        BasicSerialInstrument.__init__(self, *args, **kwargs)
        time.sleep(1)
        
    def set_rgb(self, r, g, b):
        """Set the RGB value of the NeoPixel, range 0-255.
        """
        self.query("set_rgb {} {} {}\n".format(r,g,b))

if __name__ == "__main__":
    np = SingleNeoPixel()
    np.set_rgb(0,0,0)
    for i in range(3):
        for j in range(255):
            col = [0,0,0]
            col[i] = 255-j
            col[(i+1) % 3] = j
            np.set_rgb(*col)
            time.sleep(0.01)


