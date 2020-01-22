#include <cmath>
#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include "enable_test_visibility.h"

#include "core_vector3.h"
#include "data_image.h"
#include "logic_insolation.h"

float round(float _Number, unsigned int _DecimalPlace)
{
    return int(_Number*pow(10, _DecimalPlace))/pow(10, _DecimalPlace);
}

// -----------------------------------------------------------------------------
// Test data was created with the help of https://www.geogebra.org/3d?lang=de
// -----------------------------------------------------------------------------
TEST(CInsolation, CalculateLineHeightTest1)
{
    // given
    Core::CVector3<Core::F32> Point1(0.0f, 0.0f, 0.0f);
    Core::CVector3<Core::F32> Point2(5.0f, 5.0f, 3.0f);
    Core::F32 X = 3.0f;
    Core::F32 Y = 3.0f;
    Core::F32 ExpectedHeight = 1.8f;
    
    // when
    Core::F32 ActualHeight = Logic::CInsolation::CalculateLineHeight(Point1, Point2, X, Y);
    ActualHeight = round(ActualHeight, 2);
    
    // then
    ASSERT_FLOAT_EQ(ExpectedHeight, ActualHeight);
}

TEST(CInsolation, CalculateLineHeightTest2)
{
    // given
    Core::CVector3<Core::F32> Point1(-4.15845f, -2.84944f, -1.26391f);
    Core::CVector3<Core::F32> Point2(7.20618f, 2.30449f, 2.61415f);
    Core::F32 X = 1.1f;
    Core::F32 Y = -0.47f;
    Core::F32 ExpectedHeight = 0.53f;
    
    // when
    Core::F32 ActualHeight = Logic::CInsolation::CalculateLineHeight(Point1, Point2, X, Y);
    ActualHeight = round(ActualHeight, 2);
    
    // then
    ASSERT_FLOAT_EQ(ExpectedHeight, ActualHeight);
}

TEST(CInsolation, CalculateLineHeightTest3)
{
    // given
    Core::CVector3<Core::F32> Point1(4.58584f, -4.76206f, -2.19952f);
    Core::CVector3<Core::F32> Point2(-6.50204f, 5.6101f, 1.0f);
    Core::F32 X = -8.75f;
    Core::F32 Y = 7.71f;
    Core::F32 ExpectedHeight = 1.64f;
    
    // when
    Core::F32 ActualHeight = Logic::CInsolation::CalculateLineHeight(Point1, Point2, X, Y);
    ActualHeight = round(ActualHeight, 2);
    
    // then
    ASSERT_FLOAT_EQ(ExpectedHeight, ActualHeight);
}

// This tests what happens when two points have the same x value.
TEST(CInsolation, CalculateLineHeightSameX)
{
    // given
    Core::CVector3<Core::F32> Point1(5.f, 5.f, 5.f);
    Core::CVector3<Core::F32> Point2(5.f, 2.f, 3.f);
    Core::F32 X = 5.f;
    Core::F32 Y = 3.5f;
    Core::F32 ExpectedHeight = 4.f;
    
    // when
    Core::F32 ActualHeight = Logic::CInsolation::CalculateLineHeight(Point1, Point2, X, Y);
    ActualHeight = round(ActualHeight, 2);
    
    // then
    ASSERT_FLOAT_EQ(ExpectedHeight, ActualHeight);
}

// This tests what happens when two points have the same y value.
TEST(CInsolation, CalculateLineHeightSameY)
{
    // given
    Core::CVector3<Core::F32> Point1(5.f, 5.f, 5.f);
    Core::CVector3<Core::F32> Point2(1.f, 5.f, 3.f);
    Core::F32 X = 3.f;
    Core::F32 Y = 5.f;
    Core::F32 ExpectedHeight = 4.f;
    
    // when
    Core::F32 ActualHeight = Logic::CInsolation::CalculateLineHeight(Point1, Point2, X, Y);
    ActualHeight = round(ActualHeight, 2);
    
    // then
    ASSERT_FLOAT_EQ(ExpectedHeight, ActualHeight);
}

// This tests what happens when two points have the same x and y value.
TEST(CInsolation, CalculateLineHeightSameXandY)
{
    // given
    Core::CVector3<Core::F32> Point1(5.f, 5.f, 5.f);
    Core::CVector3<Core::F32> SunPosition(5.f, 5.f, 3.f);
    Core::F32 X = 5.f;
    Core::F32 Y = 5.f;
    Core::F32 ExpectedHeight = 5.f;
    
    // when
    Core::F32 ActualHeight = Logic::CInsolation::CalculateLineHeight(Point1, SunPosition, X, Y);
    ActualHeight = round(ActualHeight, 2);
    
    // then
    ASSERT_FLOAT_EQ(ExpectedHeight, ActualHeight);
}

// -----------------------------------------------------------------------------
// This test should result in a completely dark image because the heights of
// the height-map are all higher than the height of the sun position.
// This test depends on the conversion of the height-map-value to the actual
// height.
// -----------------------------------------------------------------------------
TEST(CInsolation, CalculateInsolationDarkImage)
{
    // given
    Data::CImage InputImage(Core::UWord(125));
    Core::CVector3<Core::F32> Sun(3.0f, 3.0f, 10.0f);
    
    Data::CImage ExpectedImage(Core::UWord(0x0000));  // completely dark

    // when
    auto *pActualImage = Logic::CInsolation::CalculateInsolation(InputImage, Sun);

    // then
    ASSERT_EQ(ExpectedImage, *pActualImage);
}

// -----------------------------------------------------------------------------
// This test should result in a completely white image because the heights of
// the height-map are all lower than the height of the sun position.
// This test depends on the conversion of the height-map-value to the actual
// height.
// -----------------------------------------------------------------------------
TEST(CInsolation, CalculateInsolationWhiteImage)
{
    // given
    Data::CImage InputImage(Core::UWord(125));
    Core::CVector3<Core::F32> Sun(3.0f, 3.0f, 200.0f);
    
    Data::CImage ExpectedImage(Core::UWord(0xFFFF));  // completely white
    
    // when
    auto *pActualImage = Logic::CInsolation::CalculateInsolation(InputImage, Sun);
    
    // then
    ASSERT_EQ(ExpectedImage, *pActualImage);
}