all:tuto14.cpp shader.cpp camera.cpp data.cpp dnn_opencv.cpp
	g++ -g tuto14.cpp  shader.cpp camera.cpp data.cpp dnn_opencv.cpp -I./include -L./lib --std=c++11 -lglad -lglfw3 -lGL -lX11 -lpthread -lXrandr -lXi -ldl -o test `pkg-config opencv --cflags --libs`
