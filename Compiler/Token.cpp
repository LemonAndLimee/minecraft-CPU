/**
 * Definition of lexical Token class.
 */

#include "Token.h"

Token::Token( TokenType type )
: Token( type, std::make_shared< TokenValue >() )
{
}

Token::Token( TokenType type, TokenValue::Ptr value )
: m_type( type ),
  m_value( value )
{
}