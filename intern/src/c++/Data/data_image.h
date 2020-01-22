#pragma once

#include "core_constants.h"
#include "core_defines.h"
#include "core_types.h"

namespace Data
{
    class CImage 
    {
        PUBLIC
            explicit CImage(Core::UWord _FillColor);

        PUBLIC
            Core::UWord GetPixel(unsigned int _X, unsigned int _Y)  const;
            void SetPixel(unsigned int _X, unsigned int _Y, Core::UWord _Color);
        
        PUBLIC
            bool operator == (const CImage& _rImage) const;
        
        PRIVATE
            Core::UWord m_Image[Core::IMAGE_SIZE * Core::IMAGE_SIZE];
    };

}