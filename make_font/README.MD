## make_font.py
使用命令示例
```shell
python make_font.py 思源雅黑.otf 常用汉字.txt 32 10
```
```shell
python make_font.py MiSans-Normal.ttf 常用汉字.txt 16 4
```
- 思源雅黑.otf ：字体文件
- 常用汉字.txt ：想要生成的字符列表
- 32：字体像素大小
- 10：有些字体会前几行留空，需要抬高像素

## 生成文件原理
python文件会生成`build`文件夹下的`font_bitmap.h`文件，该文件包含两部分，汉字像素的uint8_t数组和映射加载  
一旦arduino程序引用了这个头文件，会调用`_bitmap_mapping_init`完成映射，就可以通过汉字的`key`取到uint8_t数组的`value`
## 鸣谢
- 小米开源字体
- 思源雅黑开源