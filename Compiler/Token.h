/**
 * Contains declaration of lexical Token class.
 */

#pragma once

#include "TokenTypes.h"
#include <stdint.h>

using namespace TokenTypes;

// Max length that a string value held by the token can be.
constexpr size_t g_tokenStrValueMaxLen{ 32u };

/**
 * Optional value stored by a token - can be numeric or a string.
 */
union TokenValue
{
    uint8_t numericValue;
    char    stringValue[g_tokenStrValueMaxLen];
};

/**
 * Token base class - handles non-complex cases.
 */
class Token
{
public:
    Token( TokenType type, TokenValue value );

protected:
    TokenType m_type;

    // Contains token value - e.g. if type is identifier, this would contain the variable name.
    // If the token represents a constant literal number, this would contain the number.
    TokenValue m_value;
};