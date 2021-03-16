#ifndef CONFIG_H
#define CONFIG_H
#include <glm/glm.hpp>
// settings
const unsigned int SCR_WIDTH = 1024;
const unsigned int SCR_HEIGHT = 768;

extern float lastX;

extern  float lastY;

extern bool firstMouse;

extern float _xoffset;

extern float _yoffset;

extern double yoffset_scroll;

extern bool scroll_cb;

extern bool mouse_cb;

#endif