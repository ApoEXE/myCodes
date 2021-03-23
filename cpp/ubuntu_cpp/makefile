all:tuto14.cpp shader.cpp camera.cpp data.cpp
	g++ -g tuto13.cpp  shader.cpp camera.cpp data.cpp -I./include -L./lib --std=c++11 -lglad -lglfw3 -lGL -lX11 -lpthread -lXrandr -lXi -ldl -o test `pkg-config opencv --cflags --libs`
#g++ main.cpp -o firstOpenGlApp -lglut -lGLU -lGL
#g++ gltuto_1.cpp  -lGL -lglfw3 -pthread -lX11 -ldl -lGLEW
#$(CXX) $(CXX_FLAGS) -I$(INCLUDE) -L$(LIB) $^ -o $@ (LIBRARIES)
#-lglfw3 -lGL -lX11 -lpthread -lXrandr -lXi -ldl
#g++ tuto7.cpp  -I./include -L./lib -lGLEW -lglfw3 -lGL -lX11 -lpthread -lXrandr -lXi -ldl