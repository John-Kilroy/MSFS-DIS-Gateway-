#include "Base64Encoder.h"

static const std::string base64_chars =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789+/";

std::string Base64Encoder::encode(const std::vector<uint8_t>& bytes) {
    std::string ret;
    int val = 0, valb = -6;
    for (uint8_t c : bytes) {
        val = (val << 8) + c;
        valb += 8;
        while (valb >= 0) {
            ret.push_back(base64_chars[(val >> valb) & 0x3F]);
            valb -= 6;
        }
    }
    if (valb > -6) {
        ret.push_back(base64_chars[((val << 8) >> (valb + 8)) & 0x3F]);
    }
    while (ret.size() % 4) {
        ret.push_back('=');
    }
    return ret;
}
