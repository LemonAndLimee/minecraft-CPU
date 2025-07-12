/**
 * Contains declaration of lexical Token class.
 */

#pragma once

#include "TokenTypes.h"
#include <stdint.h>
#include <memory>

using namespace TokenTypes;

// Max length that a string value held by the token can be.
constexpr size_t g_tokenStrValueMaxLen{ 32u };

enum TokenValueType
{
    UNUSED, // The token value is not holding anything
    NUMERIC,
    STRING
};

/**
 * Optional value stored by a token - can be numeric or a string.
 */
struct TokenValue
{
    using Ptr = std::shared_ptr<TokenValue>;

    TokenValueType m_valueType = UNUSED; // The type of value being stored
    union Value
    {
        uint8_t numericValue;
        char    stringValue[g_tokenStrValueMaxLen];
    } m_value;

    TokenValue()
    {
        m_valueType = UNUSED;
        m_value.numericValue = 0;
    };

    TokenValue( uint8_t numericValue )
    {
        m_valueType = NUMERIC;
        m_value.numericValue = numericValue;
    };

    TokenValue( std::string stringValue )
    {
        m_valueType = STRING;
        if ( stringValue.length() > g_tokenStrValueMaxLen )
        {
            printf( "Warning: Token value string %s exceeds max character length.\n", stringValue.c_str() );
        }
        strcpy_s( m_value.stringValue, g_tokenStrValueMaxLen, stringValue.c_str() );
    };

    bool
    operator==( const TokenValue& comparisonValue ) const
    {
        if ( m_valueType != comparisonValue.m_valueType )
        {
            return false;
        }

        switch ( m_valueType )
        {
        case NUMERIC:
            return comparisonValue.m_value.numericValue == m_value.numericValue;
        case STRING:
            return strcmp( comparisonValue.m_value.stringValue, m_value.stringValue ) == 0;
        default:
            // If type is unused or unknown, ignore value
            return true;
        }
    }
};

/**
 * Token base class - handles non-complex cases.
 */
class Token
{
public:
    using Ptr = std::shared_ptr<Token>;

    Token( TokenType type, TokenValue::Ptr value );

    TokenType m_type;

    // Contains token value - e.g. if type is identifier, this would contain the variable name.
    // If the token represents a constant literal number, this would contain the number.
    TokenValue::Ptr m_value;

    bool
    operator==( const Token& comparisonToken ) const
    {
        return comparisonToken.m_type == m_type && *comparisonToken.m_value.get() == *m_value.get();
    }
};