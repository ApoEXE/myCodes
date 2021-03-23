/*
This short program shows how a live video stream from a web cam (or from a video file) can be rendered in OpenGL as a texture.
 The live video stream is captured using the Open Source Computer Vision library (OpenCV). 
 The program also shows how an OpenCV image can be converted into OpenGL texture. 
This code can be used as the first step in the development of an Augmented Reality application using OpenCV and OpenGL.
*/
#include <iostream>
#include <opencv2/highgui.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/core/cuda.hpp>
#include <opencv2/cudaimgproc.hpp>
#include <opencv2/cudawarping.hpp>
#include <opencv2/cudaarithm.hpp>
#include "Config.h"
#include "callbacks.h"
#include "data.h"

float lastX = SCR_WIDTH / 2.0f;
float lastY = SCR_HEIGHT / 2.0f;
float _xoffset = 0.0;
bool firstMouse = true;
float _yoffset = 0.0;
double yoffset_scroll = 0.0;
bool scroll_cb = false;
bool mouse_cb = false;

int main(int argc, char const *argv[])
{
    data dt;
    int rd = dt.init_GLFW_GLAD();
    printf("%s \n", exec("glxinfo | grep \"OpenGL version\"").c_str());
    inputCallbacks(dt.window);
    //opencv stuff
    cv::VideoCapture cap;

    if (argc > 1)
        cap.open(argv[1], cv::CAP_FFMPEG);
    else
    {
        cap.open(0, cv::CAP_V4L);
    }
    cv::Mat frame;
    while (cap.isOpened())
    {
        cap >> frame;
        cv::cuda::cvtColor(frame,frame,cv::COLOR_BGR2RGB);
        
        if (frame.empty())
        {
            break;
        }

        dt.draw_loop();
    }
    cap.release();
    return rd;
}
