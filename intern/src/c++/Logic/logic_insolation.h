#pragma once

#include <QObject>

#include "core_types.h"
#include "core_defines.h"

namespace Core
{
    template<typename T>
    class CVector3;
}

namespace Data
{
    class CImage;
}

namespace Logic
{
    class CInsolation : public QObject
    {
        Q_OBJECT
        
        PUBLIC
            explicit CInsolation (QObject* parent = 0) : QObject(parent) {}
            Q_INVOKABLE static int test() { return 5; }
            Q_INVOKABLE static Data::CImage *CalculateInsolation(Data::CImage& _rImage, Core::CVector3<Core::F32>&
                    _rSun);
        
        PRIVATE
            static Core::F32
            CalculateLineHeight(Core::CVector3<Core::F32>& _rPoint1, Core::CVector3<Core::F32>& _rPoint2,
                                Core::F32 _X, Core::F32 _Y);
    };
}