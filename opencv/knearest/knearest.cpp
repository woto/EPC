#include "ml.h"
#include "highgui.h"

int main( int argc, char** argv )
{
    CvScalar color=CV_RGB(180,120,0);
    const int K = 10;
    int i, j, k, accuracy;
    float response;
    int train_sample_count = 400;
    CvRNG rng_state = cvRNG(-1);
    CvMat* trainData = cvCreateMat( train_sample_count, 2, CV_32FC1 );
    CvMat* trainClasses = cvCreateMat( train_sample_count, 1, CV_32FC1 );
    IplImage* img = cvCreateImage( cvSize( 500, 500 ), 8, 3 );
    float _sample[2];
    CvMat sample = cvMat( 1, 2, CV_32FC1, _sample );
    cvZero( img );

    CvMat trainData1, trainData2, trainData3, trainClasses1, trainClasses2, trainClasses3;
	CvMat colData1x, colData1y, colData2x, colData2y, colData3x, colData3y;
    // form the training samples
    cvGetRows( trainData, &trainData1, 0, 100 );
	cvGetCol( &trainData1, &colData1x, 0);
	cvGetCol( &trainData1, &colData1y, 1);
    cvRandArr( &rng_state, &colData1x, CV_RAND_NORMAL, cvScalar(200), cvScalar(50) );
	cvRandArr( &rng_state, &colData1y, CV_RAND_NORMAL, cvScalar(200), cvScalar(50) );

    cvGetRows( trainData, &trainData2, 100, 200 );
    cvGetCol( &trainData2, &colData2x, 0);
	cvGetCol( &trainData2, &colData2y, 1);
    cvRandArr( &rng_state, &colData2x, CV_RAND_NORMAL, cvScalar(300), cvScalar(50) );
	cvRandArr( &rng_state, &colData2y, CV_RAND_NORMAL, cvScalar(300), cvScalar(50) );

    cvGetRows( trainData, &trainData3, 200, 300 );
	cvGetCol( &trainData3, &colData3x, 0);
	cvGetCol( &trainData3, &colData3y, 1);
    cvRandArr( &rng_state, &colData3x, CV_RAND_NORMAL, cvScalar(100), cvScalar(30) );
	cvRandArr( &rng_state, &colData3y, CV_RAND_NORMAL, cvScalar(400), cvScalar(30) );

    
    cvGetRows( trainClasses, &trainClasses1, 0, 100 );
    cvSet( &trainClasses1, cvScalar(1) );

    cvGetRows( trainClasses, &trainClasses2, 100, 200 );
    cvSet( &trainClasses2, cvScalar(2) );

    cvGetRows( trainClasses, &trainClasses3, 200, 300 );
    cvSet( &trainClasses3, cvScalar(3) );
    // learn classifier
    CvKNearest knn( trainData, trainClasses, 0, false, K );
    CvMat* nearests = cvCreateMat( 1, K, CV_32FC1);

    for( i = 0; i < img->height; i++ )
    {
        for( j = 0; j < img->width; j++ )
        {
            sample.data.fl[0] = (float)j;
            sample.data.fl[1] = (float)i;

            // estimates the response and get the neighbors' labels
            response = knn.find_nearest(&sample,K,0,0,nearests,0);

            // compute the number of neighbors representing the majority
            for( k = 0, accuracy = 0; k < K; k++ )
            {
                if( nearests->data.fl[k] == response)
                    accuracy++;
            }
            // highlight the pixel depending on the accuracy (or confidence)
		color=CV_RGB(180,120,0);
		if(response==1){
			if(accuracy>5)
				color=CV_RGB(180,0,0);	
			else		
				color=CV_RGB(180,100,100);
		}else if(response==2){
			if(accuracy>5)
				color=CV_RGB(0,180,0);
			else
				color=CV_RGB(100,180,100);
		}else if(response==3){
			if(accuracy>5)
				color=CV_RGB(0,0,180);
			else
				color=CV_RGB(100,100,180);
		}
		cvSet2D( img, i, j,color); 
        }
    }

    // display the original training samples
    for( i = 0; i < 100; i++ )
    {
        CvPoint pt;
        pt.x = cvRound(trainData1.data.fl[i*2]);
        pt.y = cvRound(trainData1.data.fl[i*2+1]);
        cvCircle( img, pt, 2, CV_RGB(255,0,0), CV_FILLED );
        pt.x = cvRound(trainData2.data.fl[i*2]);
        pt.y = cvRound(trainData2.data.fl[i*2+1]);
        cvCircle( img, pt, 2, CV_RGB(0,255,0), CV_FILLED );
	
        pt.x = cvRound(trainData3.data.fl[i*2]);
        pt.y = cvRound(trainData3.data.fl[i*2+1]);
        cvCircle( img, pt, 2, CV_RGB(0,0,255), CV_FILLED );
    }

    cvNamedWindow( "classifier result", 1 );
    cvShowImage( "classifier result", img );
    cvWaitKey(0);

    cvReleaseMat( &trainClasses );
    cvReleaseMat( &trainData );
    return 0;
}

