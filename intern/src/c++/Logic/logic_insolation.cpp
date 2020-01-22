#include <algorithm>
#include <functional>
#include <vector>

#include "core_constants.h"
#include "core_vector3.h"
#include "data_image.h"
#include "logic_insolation.h"

namespace Logic
{
    ////////////////////////////////////////////////////////////////////////////////
    /// \fn Data::CImage* CInsolation::CalculateInsolation(Data::CImage* _pImage, Core::CVector3<Core::F32> &_rSun)
    ///
    /// \brief This method calculates for every pixel if it receives direct sun light.
    ///
    /// It iterates through all pixels and compares the height of the map with the the height of the sun beam. The sun beam
    /// is a line whose equation will be calculated for every pixel. The BRESENHAM algorithm is the basis for this function.
    ///
    /// \param _pImage The height map image which contains the height information.
    /// \param _rSun Vector of the sun position.
    /// \return An image with black and white pixels. If a pixel is white it means that it receives direct sunlight.
    ////////////////////////////////////////////////////////////////////////////////
    Data::CImage *CInsolation::CalculateInsolation(Data::CImage &_rImage, Core::CVector3<Core::F32> &_rSun)
    {
        auto x1 = (Core::UInt) _rSun[0];
        auto y1 = (Core::UInt) _rSun[1];
        auto z1 = (Core::UInt) _rSun[2];
        
        assert(x1 < Core::IMAGE_SIZE && y1 < Core::IMAGE_SIZE && "Sun position is beyond the image size!");
        
        auto pImage = new Data::CImage(0xFFFF);  ///< New Image that will be initialized in white.
        
        for (Core::UInt x = 0; x < Core::IMAGE_SIZE; x++)
        {
            for (Core::UInt y = 0; y < Core::IMAGE_SIZE; y++)
            {
                Core::UInt x0 = x;
                Core::UInt y0 = y;
                auto z0 = (Core::UInt) _rImage.GetPixel(x0, y0);
                Core::CVector3<Core::F32> Point(x0, y0, z0);
                
                int dx = x1 - x0, sx = x0 < x1 ? 1 : -1;
                int dy = -(y1 - y0), sy = y0 < y1 ? 1 : -1;
                int err = dx + dy, e2;
                
                while (x0 <= x1 && y0 <= y1)
                {
                    e2 = 2 * err;
                    
                    if (e2 > dy)
                    {
                        err += dy;
                        x0 += sx;
                    }
                    
                    if (e2 < dx)
                    {
                        err += dx;
                        y0 += sy;
                    }
                    
                    Core::F32 TerrainHeight = _rImage.GetPixel(x0, y0) * Core::HEIGHT_CONVERSION;
                    Core::F32 LineHeight = CalculateLineHeight(Point, _rSun, (Core::F32) x0, (Core::F32) y0);
                    
                    if (TerrainHeight >= LineHeight)
                    {
                        pImage->SetPixel(x, y, 0x0000);  // something blocks the light from the sun for that pixel
                        break;
                    }
                    
                    if (x0 == x1 && y0 == y1)
                        break;
                }
            }
        }
        return pImage;
    }
    
    ////////////////////////////////////////////////////////////////////////////////
    /// \fn CalculateLineHeight(Core::CVector3<Core::F32> &_rHeightmapPosition,
    ///                         Core::CVector3<Core::F32> &_rSun,
    ///                         Core::F32 _X, Core::F32 _Y)
    ///
    /// \brief Calculates the height of a point on a 3d line for a given x and y value.
    ///
    /// Based on two points, the sun position and a position on the height-map, the 3D-line-equation will be calculated.
    /// with this equation the height or z-value of a point on this line can be calculated. Some special conditions have
    /// to be considered. E.g. when both points share the same x-value.
    ///
    /// \param _rHeightmapPosition Vector of the position on the height-map.
    /// \param _rSun Vector of the position of the sun.
    /// \param _X X-Coordinate of the point.
    /// \param _Y Y-Coordinate of the point.
    /// \return Returns the height or z-value of the given point.
    ////////////////////////////////////////////////////////////////////////////////
    Core::F32 CInsolation::CalculateLineHeight(Core::CVector3<Core::F32> &_rHeightmapPosition,
                                               Core::CVector3<Core::F32> &_rSun,
                                               Core::F32 _X, Core::F32 _Y)
    {
        Core::CVector3<Core::F32> Direction = _rSun - _rHeightmapPosition;
        Core::F32 LineFactor = 0;
        
        if (Direction[0] != 0 && _rHeightmapPosition[0] != _X)
        {
            LineFactor = (_X - _rHeightmapPosition[0]) / Direction[0];
        }
        else if (Direction[1] != 0 && _rHeightmapPosition[1] != _Y)
        {
            LineFactor = (_Y - _rHeightmapPosition[1]) / Direction[1];
        }
        else
        {
            if (_rSun[2] > _rHeightmapPosition[2])
                return _rSun[2];
            else
                return _rHeightmapPosition[2];
        }
        
        return LineFactor * Direction[2] + _rHeightmapPosition[2];
    }
    
    
    
    // TEMPLATE
    ////////////////////////////////////////////////////////////////////////////////
    /// \fn function-signature.
    ///
    /// \brief <short-description>.
    ///
    /// <long-description>.
    ///
    /// \param <parameter-name> <parameter-description>.
    /// \return <return-description>.
    ////////////////////////////////////////////////////////////////////////////////
}