/**
 * Contains declaration of Tokeniser class.
 */

#include "Tokeniser.h"
#include <stdexcept>

/**
 * Converts a string into a vector of tokens.
 *
 * \param[in]  inputString  The string to be converted. Can be a single line or a whole program.
 *
 * \return  A vector of tokens representing the given string.
 */
TokensVector
Tokeniser::ConvertStringToTokens(
    const std::string& inputString
)
{
    TokensVector tokens{};

    if ( !inputString.empty() )
    {
        // Convert each line in the string
        size_t currentIndex{ 0u };
        size_t newLinePos = inputString.find( "\n" );
        while ( std::string::npos != newLinePos )
        {
            std::string line = inputString.substr( currentIndex, newLinePos );
            ConvertSingleLineAndAppend( line, tokens );

            currentIndex = newLinePos;
            newLinePos = inputString.find( "\n", currentIndex );
        }

        // Convert final line
        std::string line = inputString.substr( currentIndex, std::string::npos );
        ConvertSingleLineAndAppend( line, tokens );
    }

    return tokens;
}

/**
 * Converts a single line string into a vector of tokens.
 *
 * \param[in]      inputString   The string to be converted, representing a single line of code.
 * \param[in/out]  tokensVector  Vector of tokens to append to.
 */
void
Tokeniser::ConvertSingleLineAndAppend(
    const std::string& inputString,
    TokensVector& tokensVector
)
{
    // If string is empty or commented out, i.e. begins with a //
    if ( inputString.empty() || std::strncmp( inputString.c_str(), "//", 2u ) )
    {
        return;
    }

    size_t currentIndex{ 0u };
    Token::Ptr nextToken;
    while ( nullptr != ( nextToken = GetNextToken( inputString, currentIndex ) ) )
    {
        tokensVector.push_back( nextToken );
    }

    // Check there are no non-whitespace characters left at the end of the line.
    for ( size_t index = currentIndex; index < inputString.size(); ++index )
    {
        if ( !IsWhitespace( inputString[index] ) )
        {
            throw std::invalid_argument( "Non-whitespace characters leftover at the end of line." );
        }
    }
}

/**
 * Gets the next token in a string, and updates current index.
 *
 * \param[in]      inputString   The string from which to get the token.
 * \param[in/out]  startIndex    The index of the beginning of the substring representing the next token.
 *
 * \return  The next token starting at index (the largest possible that matches a rule), or nullptr if there is
 *          no matching token to be found.
 */
Token::Ptr
Tokeniser::GetNextToken(
    const std::string& inputString,
    size_t& startIndex
)
{
    /**
     * Algorithm is as follows:
     *
     * Given a start pointer, create end pointer = start+1 (skipping any whitespace at the start).
     *
     * Increment end ptr until a valid substring (one that matches a token) is found. When this happens,
     * mark that a valid substring has been found and record the last valid end ptr. We can't assume exact matches
     * are actually the right token, due to possibilities like + and ++, or | and ||.
     *
     * Continue until we find whitespace or end of string. Note: if we stop when a token becomes invalid, we would miss
     * a potential scenario where e.g. name is valid, name_ is invalid, name_a is valid.
     * When this happens, create token for last valid substring, then update start ptr to last valid end ptr + 1.
     */

    // Skip past any whitespace at the start of the token string.
    while ( startIndex < inputString.size() && IsWhitespace( inputString[startIndex] ) )
    {
        ++startIndex;
    }

    size_t endIndex{ startIndex + 1u }; // End of current substring (exclusive)

    // Initialise the "latest saved" variables to invalid values.
    int lastValidEndIndex{ -1 };
    TokenType lastValidTokenType{ INVALID_TOKEN };

    // Loop until we hit the end of the string or a whitespace character
    while ( endIndex < inputString.size() && !IsWhitespace( inputString[endIndex] ) )
    {
        std::string currentSubstring = inputString.substr( startIndex, endIndex - startIndex );
        // If the current substring matches a token, record it as the latest valid end index.
        TokenType tokenType = GetTokenType( currentSubstring );
        if ( INVALID_TOKEN != tokenType )
        {
            lastValidEndIndex = endIndex;
            lastValidTokenType = tokenType;
        }

        ++endIndex;
    }

    // If no matching token is found, return nullptr.
    if ( 0u > lastValidEndIndex )
    {
        return nullptr;
    }

    // Create token from the latest matching substring.
    std::string validTokenString = inputString.substr( startIndex, lastValidEndIndex - startIndex );
    // TODO: add method for this

    startIndex = lastValidEndIndex;
}

/**
 * Queries if character is whitespace.
 *
 * \param[in]  character  The character being checked.
 *
 * \return  True if the character is whitespace, false otherwise.
 */
bool
Tokeniser::IsWhitespace(
    const char character
)
{
    return ' ' == character || '\t' == character || '\n' == character;
}

/**
 * Gets the token type of a string representing a token.
 *
 * \param[in]  tokenString  The string representing the token being queried.
 *
 * \return  The type of token belonging to the string (INVALID_TOKEN if the string does not represent a recognised
 *          token).
 */
TokenType
Tokeniser::GetTokenType(
    const std::string& tokenString
)
{
    return INVALID_TOKEN; // stub return, TODO: implement
}