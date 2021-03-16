#ifndef DATA_H
#define DATA_H
#include "Config.h"
#include <glad/glad.h>
#include <GLFW/glfw3.h>

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
#include "camera.h"
#include "shader.h"


class data : public Camera, public Shader
{
private:
    unsigned int VBO, VAO;
    unsigned int texture1, texture2;
    void setup_buffer();
    void processInput(GLFWwindow *window);

    // ---------------------------------------------------------------------------------------------

public:
    
    // timing
    float deltaTime = 0.0f; // time between current frame and last frame
    float lastFrame = 0.0f;

    // set up vertex data (and buffer(s)) and configure vertex attributes
    // ------------------------------------------------------------------
    GLFWwindow *window; //window component
    data(/* args */);
    ~data();
    int init_GLFW_GLAD();
    void draw_loop();
};

#endif