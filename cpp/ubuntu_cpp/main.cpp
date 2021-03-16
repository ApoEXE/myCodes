// http://www.codebind.com/linux-tutorials/install-opengl-ubuntu-linux/
//g++ main.cpp -o firstOpenGlApp -pthread -lglut -lGLU -lGL
#include <GL/glut.h>
#include<thread> 
#include <unistd.h>
#include <mutex>
int i=0;
std::mutex m;//you can use std::lock_guard if you want to be exception safe

void displayMe(void)
{
    glClear(GL_COLOR_BUFFER_BIT);
    glBegin(GL_POLYGON);
        glVertex3f(0.5, 0.0, 0.5);
        glVertex3f(0.5, 0.0, 0.0);
        glVertex3f(0.0, 0.5, 0.0);
        glVertex3f(0.0, 0.0, 0.5);
    glEnd();
    glFlush();
}
void do_work(int argc, char** argv){
    
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE);
    glutInitWindowSize(400, 300);
    glutInitWindowPosition(100, 100);
    glutCreateWindow("Hello world!");
    glutDisplayFunc(displayMe);
    glutMainLoop();
}
void resource(){
    m.lock();
    std::cout << i << " Hello Wife" << std::endl;
    i++;
    m.unlock();
}

int main(int argc, char** argv)
{
    printf("before GUI\n");
    //std::thread t1(do_work,argc,argv);
    std::thread man1(resource);
    std::thread man2(resource);
    std::thread man3(resource);
   // t1.join();//if i want to wait for thread to finish first
   man1.join();
   man2.join();
   man3.join();
    sleep(10);
    printf("after GUI");
    return 0;
}