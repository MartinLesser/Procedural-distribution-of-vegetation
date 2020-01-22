#pragma once

#include <QObject>
#include <string>

#include "core_defines.h"

namespace Data
{
    class CImage;
}

namespace Logic
{
    class CImageLoader : public QObject
    {
        Q_OBJECT
        
        PUBLIC
            Q_INVOKABLE static Data::CImage* LoadImage(const char& _rPath);
    };
}