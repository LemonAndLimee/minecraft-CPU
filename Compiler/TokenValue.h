/**
 * Contains declaration of data types used to define optional token value.
 */

#pragma once

// Max length that a string value held by the token can be.
constexpr size_t g_tokenStrValueMaxLen{ 32u };

enum TokenValueType // The type of value being stored
{
    UNUSED, // The token value is not holding anything
    NUMERIC,
    STRING,
    DTYPE // Data type
};

enum DataType // Supported data types
{
    DT_BYTE
};

/**
 * Optional value stored by a token - can be numeric or a string.
 */
struct TokenValue
{
    using Ptr = std::shared_ptr<TokenValue>;

    TokenValue()
    {
        m_value.numericValue = 0;
    }
    TokenValue( uint8_t numericValue )
    : m_valueType( NUMERIC )
    {
        m_value.numericValue = numericValue;
    };
    TokenValue( std::string stringValue )
    : m_valueType( STRING )
    {
        if ( stringValue.length() > g_tokenStrValueMaxLen )
        {
            printf( "Warning: Token value string %s exceeds max character length.\n", stringValue.c_str() );
        }
        strcpy_s( m_value.stringValue, g_tokenStrValueMaxLen, stringValue.c_str() );
    };
    TokenValue( DataType dataTypeValue )
    : m_valueType( TokenValueType::DTYPE )
    {
        m_value.dataTypeValue = dataTypeValue;
    };

    bool operator==( const TokenValue& comparisonValue ) const
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

    TokenValueType m_valueType = UNUSED;

    union Value
    {
        uint8_t  numericValue;
        char     stringValue[g_tokenStrValueMaxLen];
        DataType dataTypeValue;
    } m_value;
};
