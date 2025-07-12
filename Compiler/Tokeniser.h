/**
 * Contains declaration of Tokeniser class.
 */

#pragma once

#include "Token.h"
#include <string>
#include <vector>
#include <memory>

// Class responsible for converting a string into a stream of tokens.
class Tokeniser
{
public:
    using Ptr = std::shared_ptr<Tokeniser>;
    Tokeniser() = default;

    std::vector<Token::Ptr> ConvertStringToTokens( const std::string& inputString );

protected:
    std::vector<Token::Ptr> ConvertSingleLineToTokens( const std::string& inputString );
};