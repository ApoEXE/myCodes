#ifndef SHADER_H
#define SHADER_H
//#include <GL/glew.h>
#include <glad/glad.h> // include glad to get all the required OpenGL headers
#include <glm/glm.hpp>
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>

class Shader
{
public:
    // the program ID
    Shader(std::string filepath);
    unsigned int ID;
    void use();
    // utility uniform functions
    void setBool(const std::string &name, bool value) const;
    void setInt(const std::string &name, int value) const;
    void setFloat(const std::string &name, float value) const;

private:
    struct ShaderProgramSource
    {
        std::string VertexSource;
        std::string FragmentSource;
        std::string GeometrySource;
    };
    unsigned int CreateShader(const std::string &vertexShader, const std::string &fragmentShader);
    unsigned int CompileShader(unsigned int type, const std::string &source);
    ShaderProgramSource ParseShaders(const std::string &filepath);

public:
// activate the shader
    // ------------------------------------------------------------------------
    void use_program() ;
    // utility uniform functions
    // ------------------------------------------------------------------------
    void setBool(const std::string &name, bool value) ;
    // ------------------------------------------------------------------------
    void setInt(const std::string &name, int value);
    // ------------------------------------------------------------------------
    void setFloat(const std::string &name, float value);
    // ------------------------------------------------------------------------
    void setVec2(const std::string &name, const glm::vec2 &value) ;
    void setVec2(const std::string &name, float x, float y);
    // ------------------------------------------------------------------------
    void setVec3(const std::string &name, const glm::vec3 &value) ;
    void setVec3(const std::string &name, float x, float y, float z) ;
    // ------------------------------------------------------------------------
    void setVec4(const std::string &name, const glm::vec4 &value);
    void setVec4(const std::string &name, float x, float y, float z, float w) ;
    // ------------------------------------------------------------------------
    void setMat2(const std::string &name, const glm::mat2 &mat);
    // ------------------------------------------------------------------------
    void setMat3(const std::string &name, const glm::mat3 &mat);
    // ------------------------------------------------------------------------
    void setMat4(const std::string &name, const glm::mat4 &mat);
};

// use/activate the shader

#endif
