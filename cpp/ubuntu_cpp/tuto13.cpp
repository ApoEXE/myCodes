#include <iostream>
#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include "Config.h"
#include "data.h"


float lastX = SCR_WIDTH / 2.0f;
float lastY = SCR_HEIGHT / 2.0f;
float _xoffset =0.0;
bool firstMouse = true;
float _yoffset =0.0;
double yoffset_scroll= 0.0;
bool scroll_cb = false;
bool mouse_cb = false;



void framebuffer_size_callback(GLFWwindow *window, int width, int height) 
{
    // make sure the viewport matches the new window dimensions; note that width and
    // height will be significantly larger than specified on retina displays.
    glViewport(0, 0, width, height);
}

// glfw: whenever the mouse moves, this callback is called
// -------------------------------------------------------
void mouse_callback(GLFWwindow *window, double xpos, double ypos) 
{
    if (firstMouse)
    {
        lastX = xpos;
        lastY = ypos;
        firstMouse = false;
    }

    _xoffset = xpos - lastX;
    _yoffset = lastY - ypos; // reversed since y-coordinates go from bottom to top

    lastX = xpos;
    lastY = ypos;
    mouse_cb = true;
}

// glfw: whenever the mouse scroll wheel scrolls, this callback is called
// ----------------------------------------------------------------------
void scroll_callback(GLFWwindow *window, double xoffset, double yoffset) 
{
    scroll_cb = true;
    yoffset_scroll = yoffset;
}
void inputCallbacks(GLFWwindow *window){

    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);
    glfwSetCursorPosCallback(window, mouse_callback);
    glfwSetScrollCallback(window, scroll_callback);
    
}
int main()
{   data dt;
    int rd = dt.init_GLFW_GLAD();
    printf("initialize good?: %d",rd);
    inputCallbacks(dt.window);
    dt.draw_loop();
    return rd;
}
