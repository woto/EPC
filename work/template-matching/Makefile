#
# Replace OPENCV_DIR with your OpenCV base directory
# 
OPENCV_DIR	= C:\OpenCV
OBJS		= template_match.o
CC			= gcc
DEBUG		= -g
CFLAGS		= -c -I"$(OPENCV_DIR)\cvaux\include" \
				 -I"$(OPENCV_DIR)\ml\include" \
				 -I"$(OPENCV_DIR)\cv\include" \
				 -I"$(OPENCV_DIR)\cxcore\include" \
				 -I"$(OPENCV_DIR)\otherlibs\_graphics\include" \
				 -I"$(OPENCV_DIR)\otherlibs\cvcam\include" \
				 -I"$(OPENCV_DIR)\otherlibs\highgui"
LFLAGS		= -L"$(OPENCV_DIR)\lib" -lcxcore -lcv -lcvaux -lhighgui -lml -lcvcam

all: $(OBJS)
	$(CC) $(OBJS) $(LFLAGS) -o template_match

template_match.o: template_match.c
	$(CC) $(CFLAGS) template_match.c

clean:
	del *.o
