TemplateMatching 1.0
--------------------
Author:  Nashruddin Amin <me@nashruddin.com>
Website: http://www.nashruddin.com

Requirements
------------
1. C compiler. I recommend gcc. For windows platform it is available at
   http://www.mingw.org
2. OpenCV, freely available at http://www.sourceforge.net/projects/opencvlibrary

Compile
-------
1. Extract the package to any directory

2. Open Makefile and change the line
        
   OPENCV_DIR = C:\OpenCV
   
   to the directory where you install OpenCV.

3. Open a console and go to the directory where you extracted the package. Type:
   
   make

   to compile. And type:
   
   template_matching <reference image> <template image>
   
   to run the program.
   
Contact
-------
Please send comments and bug reports to me@nashruddin.com.
