#pragma once

#include <unordered_map>
#include <string>

namespace TokenTypes
{

enum TokenType
{
    DATA_TYPE,
    ASSIGN,
    BYTE,
    IF,
    ELSE,
    WHILE,
    FOR,
    IDENTIFIER,
    PLUS,
    MINUS,
    MULTIPLY,
    DIVIDE,
    MOD,
    EXPONENT,
    EQ,  // ==
    NEQ, // !=
    LEQ, // <=
    GEQ, // >=
    LT,  // <
    GT,  // >
    NOT,
    OR,
    AND,
    LSHIFT,
    RSHIFT,
    PAREN_OPEN,
    PAREN_CLOSE,
    BRACE_OPEN,
    BRACE_CLOSE,
    SEMICOLON
};

// Contains the exact string matches (if they exist) of token types.
const std::unordered_map<TokenType, std::string> g_tokenTypesExactMatches {
    { DATA_TYPE, "byte" },
    { ASSIGN, "=" },
    // BYTE -> Non-exact match
    { IF, "if" },
    { ELSE, "else" },
    { WHILE, "while" },
    { FOR, "for" },
    // IDENTIFIER -> Non-exact match
    { PLUS, "+" },
    { MINUS, "-" },
    { MULTIPLY, "*" },
    { DIVIDE, "/" },
    { MOD, "%" },
    { EXPONENT, "^" },
    { EQ, "==" },
    { NEQ, "!=" },
    { LEQ, "<=" },
    { GEQ, ">=" },
    { LT, "<" },
    { GT, ">" },
    { NOT, "!" },
    { OR, "|" },
    { AND, "&" },
    { LSHIFT, "<<" },
    { RSHIFT, ">>" },
    { PAREN_OPEN, "(" },
    { PAREN_CLOSE, ")" },
    { BRACE_OPEN, "{" },
    { BRACE_CLOSE, "}" },
    { SEMICOLON, ";" },
};

}