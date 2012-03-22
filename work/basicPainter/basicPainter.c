#ifdef _CH_
#pragma package <opencv>
#endif

#ifndef _EiC
#include "cv.h"
#include "highgui.h"
#include <stdio.h>
#include <ctype.h>
#endif

IplImage* imagen;
IplImage* imgColor;
int red,green,blue;
IplImage* screenBuffer;
int drawing;
int r,last_x, last_y;

void draw(int x,int y){
	//Draw a circle where is the mouse
	cvCircle(imagen, cvPoint(x,y), r, CV_RGB(red,green,blue), -1, CV_AA, 0);
	//Get clean copy of image
	screenBuffer=cvCloneImage(imagen);
	cvShowImage( "Demo", screenBuffer );
}

void drawCursor(int x, int y){
	//Get clean copy of image
	screenBuffer=cvCloneImage(imagen);
	//Draw a circle where is the mouse
	cvCircle(screenBuffer, cvPoint(x,y), r, CV_RGB(0,0,0), 1, CV_AA, 0);
}

void changeColor(int pos){
	cvSet(imgColor, CV_RGB(red,green,blue),NULL);
}

/*************************
* Mouse CallBack
* event: 
*	#define CV_EVENT_MOUSEMOVE      0
*	#define CV_EVENT_LBUTTONDOWN    1
*	#define CV_EVENT_RBUTTONDOWN    2
*	#define CV_EVENT_MBUTTONDOWN    3
*	#define CV_EVENT_LBUTTONUP      4
*	#define CV_EVENT_RBUTTONUP      5
*	#define CV_EVENT_MBUTTONUP      6
*	#define CV_EVENT_LBUTTONDBLCLK  7
*	#define CV_EVENT_RBUTTONDBLCLK  8
*	#define CV_EVENT_MBUTTONDBLCLK  9
*
* x, y: mouse position
*
* flag:
*	#define CV_EVENT_FLAG_LBUTTON   1
*	#define CV_EVENT_FLAG_RBUTTON   2
*	#define CV_EVENT_FLAG_MBUTTON   4
*	#define CV_EVENT_FLAG_CTRLKEY   8
*	#define CV_EVENT_FLAG_SHIFTKEY  16
*	#define CV_EVENT_FLAG_ALTKEY    32
*
**************************/

void on_mouse( int event, int x, int y, int flags, void* param )
{
	last_x=x;
	last_y=y;
	drawCursor(x,y);
    //Select mouse Event
	if(event==CV_EVENT_LBUTTONDOWN)
        {
			drawing=1;
			draw(x,y);
		}
    else if(event==CV_EVENT_LBUTTONUP)
		{
			//drawing=!drawing;
			drawing=0;
		}
	else if(event == CV_EVENT_MOUSEMOVE  &&  flags & CV_EVENT_FLAG_LBUTTON)
		{
			if(drawing)
				draw(x,y);
		}
}



int main( int argc, char** argv )
{
    printf( "Mouse Event and drawing sample\n"
		"Hot keys: \n"
	"\tr - reset image\n"
	"\t+ - cursor radio ++\n"
	"\t- - cursor radio --\n"
	"\ts - Save image as out.png\n"
        "\tESC - quit the program\n"
        "\tDavid Millan Escriva | Damiles\n");
	drawing=0;
	r=10;
	last_x=last_y=red=green=blue=0;
	//Create image
	imagen=cvCreateImage(cvSize(240,240),IPL_DEPTH_8U,3);
	imgColor=cvCreateImage(cvSize(1,1),IPL_DEPTH_8U,3);
	//Set data of image to white
	cvSet(imagen, CV_RGB(255,255,255),NULL);
	cvSet(imgColor, CV_RGB(red,green,blue),NULL);
	//Image we show user with cursor and other artefacts we need
	screenBuffer=cvCloneImage(imagen);
	
	//Create window
    	cvNamedWindow( "Demo", 0 );
	cvNamedWindow( "ColorSelector",0);
	//Create track Bar
	cvCreateTrackbar("Red","ColorSelector", &red,255,&changeColor);
	cvCreateTrackbar("Green","ColorSelector", &green,255,&changeColor);
	cvCreateTrackbar("Blue","ColorSelector", &blue,255,&changeColor);

	cvResizeWindow("Demo", 240,240);
	cvResizeWindow("ColorSelector", 240,240);
	//Create mouse CallBack
	cvSetMouseCallback("Demo",&on_mouse, 0 );

	//Main Loop
    for(;;)
    {
		int c;

        cvShowImage( "Demo", screenBuffer );
        cvShowImage( "ColorSelector", imgColor);
        c = cvWaitKey(10);
        if( (char) c == 27 )
            break;
	if( (char) c== '+' ){
		r++;
		drawCursor(last_x,last_y);
	}
	if( ((char)c== '-') && (r>1) ){
		r--;
		drawCursor(last_x,last_y);
	}
	if( (char)c== 'r'){
		cvSet(imagen, cvRealScalar(255),NULL);
		drawCursor(last_x,last_y);
	}
	if( (char)c== 's'){
		cvSaveImage("out.png", imagen);
	}
		
    }

    cvDestroyWindow("Demo");

    return 0;
}

#ifdef _EiC
main(1,"mouseEvent.c");
#endif
