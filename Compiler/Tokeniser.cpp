/**
 * Contains declaration of Tokeniser class.
 */

#include "Tokeniser.h"

/**
 * Converts a string into a vector of tokens.
 *
 * \param[in]  inputString  The string to be converted. Can be a single line or a whole program.
 *
 * \return  A vector of tokens representing the given string.
 */
std::vector<Token>
Tokeniser::ConvertStringToTokens(
    const std::string& inputString
)
{
    std::vector<Token> tokens{};

    // If string is empty
    if ( inputString.empty() )
    {
        return tokens;
    }

    // Call ConvertSingleLineToTokens() for each line in inputString
}

/**
 * Converts a single line string into a vector of tokens.
 *
 * \param[in]  inputString  The string to be converted, representing a single line of code.
 *
 * \return  A vector of tokens representing the given string.
 */
std::vector<Token>
Tokeniser::ConvertSingleLineToTokens(
    const std::string& inputString
)
{
    std::vector<Token> tokens{};

    // If string is empty or commented out, i.e. begins with a //
    if ( inputString.empty() || std::strncmp( inputString.c_str(), "//", 2u ) )
    {
        return tokens;
    }

    // Else, convert...
}