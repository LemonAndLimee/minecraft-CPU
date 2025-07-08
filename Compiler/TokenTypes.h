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

const std::unordered_map<TokenType, std::string> g_tokenTypesRegex {
    { DATA_TYPE, "byte" },
    { ASSIGN, "=" },
    { BYTE, "[0-9]+" },
    { IF, "if" },
    { ELSE, "else" },
    { WHILE, "while" },
    { FOR, "for" },
    { IDENTIFIER, "[a-zA-Z_][a-zA-Z_0-9]*" },
    { PLUS, "\\+" },
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
    { OR, "\\|" },
    { AND, "&" },
    { LSHIFT, "<<" },
    { RSHIFT, ">>" },
    { PAREN_OPEN, "\\(" },
    { PAREN_CLOSE, "\\)" },
    { BRACE_OPEN, "{" },
    { BRACE_CLOSE, "}" },
    { SEMICOLON, ";" },
};

}