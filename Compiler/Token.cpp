/**
 * Definition of lexical Token class.
 */

#include "Token.h"

Token::Token( TokenType type, TokenValue value )
  : m_type( type ),
    m_value( value )
{
}