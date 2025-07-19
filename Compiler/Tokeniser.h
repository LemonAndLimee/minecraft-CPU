/**
 * Contains declaration of Tokeniser class.
 */

#pragma once

#include "Token.h"
#include <string>
#include <vector>
#include <memory>

using TokensVector = std::vector<Token::Ptr>;

// Class responsible for converting a string into a stream of tokens.
class Tokeniser
{
public:
    using Ptr = std::shared_ptr<Tokeniser>;
    Tokeniser() = default;

    TokensVector ConvertStringToTokens( const std::string& inputString );

    static TokenType GetTokenType( const std::string& tokenString );

    static bool IsWhitespace( const char character );

protected:
    void ConvertSingleLineAndAppend( const std::string& inputString, TokensVector& tokensVector );

    Token::Ptr GetNextToken( const std::string& inputString, size_t& startIndex );
};