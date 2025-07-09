#include <boost/test/unit_test.hpp>
#include "Tokeniser.h"

BOOST_AUTO_TEST_SUITE( TokeniserTests )

/**
 * Tests that when ConvertStringToTokens() is called with an empty string, it returns an empty vector of tokens.
 */
BOOST_AUTO_TEST_CASE( ConvertStringToTokens_EmptyString )
{
    Tokeniser::Ptr tokeniser = std::make_shared<Tokeniser>();
    std::vector<Token> outputVector = tokeniser->ConvertStringToTokens( "" );

    BOOST_CHECK( outputVector.empty() );
}

BOOST_AUTO_TEST_SUITE_END() // TokeniserTests