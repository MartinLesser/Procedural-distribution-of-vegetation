#include <iostream>

#include "extern/inc/CImg.h"
#include "data_image.h"
#include "logic_image_loader.h"

namespace Logic
{
    Q_INVOKABLE Data::CImage* CImageLoader::LoadImage(const char& _rPath)
    {
        auto pImage = new Data::CImage(0);
        cimg_library::CImg<float> image(_rPath);
        cimg_library::CImgDisplay main_disp(image);
        float pixvalR = image(10,10,0,0); // read red val at coord 10,10
        float pixvalG = image(10,10,0,1); // read green val at coord 10,10
        float pixvalB = image(10,10,0,2); // read blue val at coord 10,10
        std::cout << "R = " << pixvalR << ", G = " << pixvalG << ", B = " << pixvalB;
        std::cout << _rPath << std::endl;
        
        return pImage;
    }
}