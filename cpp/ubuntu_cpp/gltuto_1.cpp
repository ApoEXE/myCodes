//g++ gltuto_1.cpp  -lGL -lglfw3 -pthread -lX11 -ldl -lGLEW
// Include standard headers
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>
// Include GLEW. Always include it before gl.h and glfw3.h, since it's a bit magic.
#include <GL/glew.h>
// Include GLFW
#include <GLFW/glfw3.h>
// Include GLM for MATH
#include <glm/glm.hpp>
using namespace glm;

#include "common/shader.hpp"
// Open a window and create its OpenGL context
GLFWwindow *window; // (In the accompanying source code, this variable is global for simplicity)

static unsigned int CompileShader(unsigned int type, const std::string &source)
{
    unsigned int id = glCreateShader(type);
    const char *src = source.c_str();
    glShaderSource(id, 1, &src, nullptr);
    glCompileShader(id);
    //error handling
    int result;
    glGetShaderiv(id, GL_COMPILE_STATUS, &result);
    if (result == GL_FALSE)
    {
        int length;
        glGetShaderiv(id, GL_INFO_LOG_LENGTH, &length);
        char *message = (char *)alloca(length * sizeof(char));
        glGetShaderInfoLog(id, length, &length, message);

        std::cout << "ERRO to compile "<<(type == GL_VERTEX_SHADER ? "vertex": "fragment")<<" shaders" << std::endl;
        std::cout << message << std::endl;
        glDeleteShader(id);
        return 0;
    }
    return id;
}

static unsigned int CreateShader(const std::string &vertexShader, const std::string &fragmentShader)
{
    unsigned int program = glCreateProgram();
    unsigned int vs = CompileShader(GL_VERTEX_SHADER, vertexShader);
    unsigned int fs = CompileShader(GL_FRAGMENT_SHADER, fragmentShader);

    glAttachShader(program, vs);
    glAttachShader(program, fs);
    glLinkProgram(program);
    glValidateProgram(program);

    glDeleteShader(vs);
    glDeleteShader(fs);

    return program;
}

int principal_gl_inits_components()
{
    // Initialise GLFW
    glewExperimental = true; // Needed for core profile
    if (!glfwInit())
    {
        fprintf(stderr, "Failed to initialize GLFW\n");
        return -1;
    }
    glfwWindowHint(GLFW_SAMPLES, 4);               // 4x antialiasing
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3); // We want OpenGL 3.3
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);           // To make MacOS happy; should not be needed
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE); // We don't want the old OpenGL

    window = glfwCreateWindow(1024, 768, "Tutorial 01", NULL, NULL);
    if (window == NULL)
    {
        fprintf(stderr, "Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible. Try the 2.1 version of the tutorials.\n");
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(window); // Initialize GLEW
    glewExperimental = true;        // Needed in core profile
    if (glewInit() != GLEW_OK)
    {
        fprintf(stderr, "Failed to initialize GLEW\n");
        return -1;
    }
    // Ensure we can capture the escape key being pressed below
    glfwSetInputMode(window, GLFW_STICKY_KEYS, GL_TRUE);
    // Dark blue background
    glClearColor(0.0f, 0.0f, 0.4f, 0.0f);
}
void drawTriangle()
{

    GLuint VertexArrayID;
    glGenVertexArrays(1, &VertexArrayID);
    glBindVertexArray(VertexArrayID);
    printf("VertexArrayID: %d \n", VertexArrayID);
    // An array of 3 vectors which represents 3 vertices
    static const GLfloat position[] = {
        -1.0f,
        -1.0f,
        0.0f,
        1.0f,
        -1.0f,
        0.0f,
        0.0f,
        1.0f,
        0.0f,
    };
    //shader for working with vram and gpu functions
    //GLuint programID = LoadShaders("SimpleVertexShader.vertexshader", "SimpleFragmentShader.fragmentshader");

    // This will identify our vertex buffer
    GLuint vertexbuffer;
    // Generate 1 buffer, put the resulting identifier in vertexbuffer
    glGenBuffers(1, &vertexbuffer);
    // The following commands will talk about our 'vertexbuffer' buffer
    glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);
    // Give our vertices to OpenGL.
    glBufferData(GL_ARRAY_BUFFER, sizeof(position), position, GL_STATIC_DRAW);
    printf("vertexbuffer: %d \n", vertexbuffer);
    // 1st attribute buffer : vertices
    glEnableVertexAttribArray(0); //enable working with vertex 0
    glVertexAttribPointer(        //LAYOUT if is a X Y Z or X y or Polar ETC
        0,                        // attribute 0. No particular reason for 0, but must match the layout in the shader.
        3,                        // size
        GL_FLOAT,                 // type
        GL_FALSE,                 // normalized?
        sizeof(float) * 3,        // stride size of bytes in a vertex
        (void *)0                 // index of attr to workon
    );

    std::string vertexShader =
        "#version 330 core \n"
        "\n"
        "layout(location = 0) in vec4 position;\n"
        "\n"
        "void main() \n"
        "{\n"
        " gl_Position = position;\n"
        "}\n";
    std::string fragmentShader =
        "#version 330 core \n"
        "\n"
        "layout(location = 0) out vec4 color;\n"
        "\n"
        "void main() \n"
        "{\n"
        "  color = vec4(1.0,0.0,0.0,1.0);"
        "}\n";
    unsigned int shader = CreateShader(vertexShader,fragmentShader);
    glUseProgram(shader);
    do
    {
        // Clear the screen. It's not mentioned before Tutorial 02, but it can cause flickering, so it's there nonetheless.
        glClear(GL_COLOR_BUFFER_BIT);

        // Use our shader
        //glUseProgram(programID);

        // Draw the triangle !
        glDrawArrays(GL_TRIANGLES, 0, 3); // Starting from vertex 0; 3 vertices total -> 1 triangle
        //glDisableVertexAttribArray(0);

        // Swap buffers
        glfwSwapBuffers(window);
        glfwPollEvents();

    } // Check if the ESC key was pressed or the window was closed
    while (glfwGetKey(window, GLFW_KEY_ESCAPE) != GLFW_PRESS &&
           glfwWindowShouldClose(window) == 0);
    // Cleanup VBO
    glDeleteBuffers(1, &vertexbuffer);
    glDeleteVertexArrays(1, &VertexArrayID);
    //glDeleteProgram(programID);
    glDeleteProgram(shader);

    // Close OpenGL window and terminate GLFW
    glfwTerminate();
}

int main()
{
    principal_gl_inits_components();
    std::cout << glGetString(GL_VERSION) << std::endl;
    drawTriangle();
}
