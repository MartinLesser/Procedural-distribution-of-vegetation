#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include "enable_test_visibility.h"

#include "core_vector3.h"
#include "data_image.h"

TEST(CImage, ConstructorShouldInitializeCorrectly)
{
    // given
    Core::UInt FillColor = 10;

    // when
    auto Image = Data::CImage(FillColor);

    // then
    ASSERT_EQ(Image.GetPixel(0, 0), FillColor);
    ASSERT_EQ(Image.GetPixel(1, 0), FillColor);
    ASSERT_EQ(Image.GetPixel(0, 1), FillColor);
    ASSERT_EQ(Image.GetPixel(1, 1), FillColor);
}