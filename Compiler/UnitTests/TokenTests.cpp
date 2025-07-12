#include <boost/test/unit_test.hpp>
#include "Token.h"

BOOST_AUTO_TEST_SUITE( TokenEqualityOperatorTests )

BOOST_AUTO_TEST_CASE( EqualTokens )
{
    TokenType tokenType{ IDENTIFIER };
    std::string tokenStringValue = "hello";

    // Create 2 tokens using the same initialising values
    TokenValue::Ptr tokenValue1 = std::make_shared<TokenValue>( tokenStringValue );
    Token::Ptr token1 = std::make_shared<Token>( tokenType, tokenValue1 );

    TokenValue::Ptr tokenValue2 = std::make_shared<TokenValue>( tokenStringValue );
    Token::Ptr token2 = std::make_shared<Token>( tokenType, tokenValue2 );

    BOOST_CHECK( *token1.get() == *token2.get() );
}

BOOST_AUTO_TEST_CASE( EqualTokensUnusedValue )
{
    TokenType tokenType{ IF };

    // Create 2 tokens using the same types and empty values
    Token::Ptr token1 = std::make_shared<Token>( tokenType, std::make_shared<TokenValue>() );
    Token::Ptr token2 = std::make_shared<Token>( tokenType, std::make_shared<TokenValue>() );

    BOOST_CHECK( *token1.get() == *token2.get() );
}

BOOST_AUTO_TEST_CASE( UnequalValues )
{
    TokenType tokenType{ IDENTIFIER };

    // Create 2 tokens using the unequal values
    TokenValue::Ptr tokenValue1 = std::make_shared<TokenValue>( "hello");
    Token::Ptr token1 = std::make_shared<Token>( tokenType, tokenValue1 );

    TokenValue::Ptr tokenValue2 = std::make_shared<TokenValue>( "goodbye" );
    Token::Ptr token2 = std::make_shared<Token>( tokenType, tokenValue2 );

    BOOST_CHECK_EQUAL( false, *token1.get() == *token2.get() );
}

// If token values are unequal but value type is unused, they should still pass the equality check.
BOOST_AUTO_TEST_CASE( UnequalValuesButUnused )
{
    TokenType tokenType{ FOR };

    // Create 2 tokens using unequal values but value types unused.
    TokenValue::Ptr tokenValue1 = std::make_shared<TokenValue>();
    tokenValue1->m_valueType = UNUSED;
    tokenValue1->m_value.numericValue = 0x00;
    Token::Ptr token1 = std::make_shared<Token>( tokenType, tokenValue1 );

    TokenValue::Ptr tokenValue2 = std::make_shared<TokenValue>();
    tokenValue2->m_valueType = UNUSED;
    tokenValue2->m_value.numericValue = 0xFF;
    Token::Ptr token2 = std::make_shared<Token>( tokenType, tokenValue2 );

    BOOST_CHECK( *token1.get() == *token2.get() );
}

BOOST_AUTO_TEST_CASE( UnequalValueTypes )
{
    TokenType tokenType{ FOR };

    // Create 2 tokens using unequal value types
    TokenValue::Ptr tokenValue1 = std::make_shared<TokenValue>();
    tokenValue1->m_valueType = NUMERIC;
    Token::Ptr token1 = std::make_shared<Token>( tokenType, tokenValue1 );

    TokenValue::Ptr tokenValue2 = std::make_shared<TokenValue>();
    tokenValue2->m_valueType = STRING;
    Token::Ptr token2 = std::make_shared<Token>( tokenType, tokenValue2 );

    BOOST_CHECK_EQUAL( false, *token1.get() == *token2.get() );
}

BOOST_AUTO_TEST_CASE( UnequalTokenTypes )
{
    // Create 2 tokens using unequal token types
    Token::Ptr token1 = std::make_shared<Token>( IF, std::make_shared<TokenValue>() );

    Token::Ptr token2 = std::make_shared<Token>( FOR, std::make_shared<TokenValue>() );

    BOOST_CHECK_EQUAL( false, *token1.get() == *token2.get() );
}

BOOST_AUTO_TEST_SUITE_END() // TokenEqualityOperatorTests