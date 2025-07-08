#pragma once

#include "TokenTypes.h"
#include <stdint.h>

using namespace TokenTypes;

class Token
{
public:
    Token() = default;

    // Max length that a string value held by the token can be
    static const size_t c_tokenStrValueMaxLen{32u};

protected:
    TokenType m_type;

    // Contains token value - e.g. if type is identifier, this would contain the variable name.
    // If the token represents a constant literal number, this would contain the number.
    union TokenValue
    {
        uint8_t numericValue;
        char    stringValue[Token::c_tokenStrValueMaxLen];
    } m_value;
};