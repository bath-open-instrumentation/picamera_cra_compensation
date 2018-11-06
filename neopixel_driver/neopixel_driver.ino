// This code is mostly pinched from the "NeoPixel Ring simple sketch" (c) 2013 Shae Erisson, under GPLv3
// It's released under GPLv3

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

// This code is mostly pinched from the "NeoPixel Ring simple sketch" (c) 2013 Shae Erisson, under GPLv3
// It's released under GPLv3
#define PIN            6
#define NUMPIXELS      1
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

// We'll use this input buffer for serial comms
const int INPUT_BUFFER_LENGTH = 64;
char input_buffer[INPUT_BUFFER_LENGTH];


void setup() {
  Serial.begin(9600);
  pixels.begin(); // This initializes the NeoPixel library.
}

void rgb_cycle() {

  // For a set of NeoPixels the first NeoPixel is 0
  for(int i=0;i<3;i++){
    unsigned int colour[3] = {0,0,0};
    for(int j=0; j<256;j++){
      // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
      colour[i] = 255 - j;
      colour[(i+1) % 3] = j;
      pixels.setPixelColor(0, pixels.Color(colour[0],colour[1],colour[2])); // Moderately bright green color.
      delay(10); // Delay for a period of time (in milliseconds).
      pixels.show(); // This sends the updated pixel color to the hardware.
    }


  }
}

void static_colour(unsigned int r, unsigned int g, unsigned int b) {
  //pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
  pixels.setPixelColor(0, pixels.Color(r,g,b)); // Moderately bright green color.
  pixels.show(); // This sends the updated pixel color to the hardware.
  delay(10); // Delay for a period of time (in milliseconds).
}

void loop(){
  // The loop reads a command from the serial port and executes it.
  int received_bytes = Serial.readBytesUntil('\n',input_buffer,INPUT_BUFFER_LENGTH-1);
  if(received_bytes > 0){
    input_buffer[received_bytes] = '\0';
    String command = String(input_buffer);

    if(command.startsWith("set_rgb ")){ //set the colour of the LED
      int preceding_space = -1;
      unsigned int colour[3];
      for(int i=0;i<3;i++){ //read three integers and store in colour[]
        preceding_space = command.indexOf(' ',preceding_space+1);
        if(preceding_space<0){
          Serial.println(F("Error: command is set_rgb <int> <int> <int>"));
          break;
        }
        colour[i] = command.substring(preceding_space+1).toInt();
      }
      static_colour(colour[0],colour[1],colour[2]);
      Serial.println("done.");
      return;
    }
  }

}
