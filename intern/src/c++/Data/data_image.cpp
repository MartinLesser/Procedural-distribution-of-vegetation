#include "data_image.h"

namespace Data
{
    CImage::CImage(Core::UWord _FillColor)
    {
        for (Core::UInt x = 0; x < Core::IMAGE_SIZE; x++) {
            for (Core::UInt y = 0; y < Core::IMAGE_SIZE; y++) {
                this->SetPixel(x, y, _FillColor);
            }
        }
    }

    Core::UWord CImage::GetPixel(unsigned int _X, unsigned int _Y) const
    {
        return this->m_Image[_X + _Y * Core::IMAGE_SIZE];
    }

    void CImage::SetPixel(unsigned int _X, unsigned int _Y, Core::UWord _Color)
    {
        this->m_Image[_X + _Y * Core::IMAGE_SIZE] =  _Color;
    }
    
    bool CImage::operator==(const CImage &_rImage) const
    {
        for (Core::UInt x = 0; x < Core::IMAGE_SIZE; x++) {
            for (Core::UInt y = 0; y < Core::IMAGE_SIZE; y++) {
                if (this->GetPixel(x, y) != _rImage.GetPixel(x, y))
                    return false;
            }
        }
        return true;
    }
}