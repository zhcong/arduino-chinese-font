#include <ChineseFontBitMap.h>
#include <font_bitmap.h>

ChineseFontBitMap::ChineseFontBitMap() {
  _font_map = new SimpleMap<String, int>([](String & a, String & b) -> int {  if (a == b) return 0;  else if (a > b) return 1;  else return -1; });
  _bitmap_mapping_init(_font_map);
}

ChineseFontBitMap::~ChineseFontBitMap() {
  delete _font_map;
}

uint8_t* ChineseFontBitMap::get_map(String character) {
  return (uint8_t*)FONT_BITMAP[_font_map->get(character)];
}

int ChineseFontBitMap::get_pixel_len() {
  return _PIXEL_LEN;
}

int ChineseFontBitMap::get_byte_len() {
  return _BYTE_LEN;
}
