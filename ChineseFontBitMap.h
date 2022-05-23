#include <Arduino.h>
#include "SimpleMap.h"

class ChineseFontBitMap {
  public:
    ChineseFontBitMap();
    ~ChineseFontBitMap();
    uint8_t* get_map(String character);
    // get one character pixel width
    int get_pixel_len();
    // get one character byte len
    int get_byte_len();
  private:
    SimpleMap<String, int> *_font_map;
};
