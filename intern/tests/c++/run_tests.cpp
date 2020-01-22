#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include <stdio.h>

int main(int argc, char** argv)
{
    testing::InitGoogleTest(&argc, argv);
    auto result = RUN_ALL_TESTS();
    printf("%d", result);
}
