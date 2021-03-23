#include <iostream>
#include "Config.h"
#include "callbacks.h"
#include "data.h"

float lastX = SCR_WIDTH / 2.0f;
float lastY = SCR_HEIGHT / 2.0f;
float _xoffset =0.0;
bool firstMouse = true;
float _yoffset =0.0;
double yoffset_scroll= 0.0;
bool scroll_cb = false;
bool mouse_cb = false;

int main()
{   data dt;
    int rd = dt.init_GLFW_GLAD();
    printf("%s \n",exec("glxinfo | grep \"OpenGL version\"").c_str());
    inputCallbacks(dt.window);
    dt.draw_loop();
    return rd;
}
