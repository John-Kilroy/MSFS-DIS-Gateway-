#pragma once

#include <string>
#include <vector>
#include <cstdint>

class Base64Encoder {
public:
    static std::string encode(const std::vector<uint8_t>& bytes);
};
