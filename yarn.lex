%{
#include <stdio.h>
#include <stdlib.h>
#include "yarn.tab.h"
%}

%%

"setup"                 { return SETUP; }
"{"                     { return LBRACE; }
"}"                     { return RBRACE; }
"var"                   { return VAR; }
"="                     { return EQUALS; }
"("                     { return LPAREN; }
")"                     { return RPAREN; }
";"                     { return SEMICOLON; }
"repeat"                { return REPEAT; }
"from"                  { return FROM; }
"to"                    { return TO; }
"function"              { return FUNCTION; }
","                     { return COMMA; }
"if"                    { return IF; }
"else"                  { return ELSE; }
"//"                    { return COMMENT; }
"yarnColor"             { return CHAIN; }
"hookSize"              { return SKIPCHAIN; }
"chain"                 { return CHAIN; }
"skipChain"             { return SKIPCHAIN; }
"singleCrochet"         { return SINGLECROCHET; }
"doubleCrochet"         { return DOUBLECROCHET; }
"trebleCrochet"         { return TREBLECROCHET; }
"slipStitch"            { return SLIPSTITCH; }
"changeYarn"            { return CHANGECOLOR; }
"=="                    { return EQ; }
"!="                    { return NEQ; }
"<"                     { return LT; }
"<="                    { return LTE; }
">"                     { return GT; }
">="                    { return GTE; }
"+"                     { return '+'; }
"-"                     { return '-'; }
"*"                     { return '*'; }
"/"                     { return '/'; }
"%"                     { return '%'; }

[a-zA-Z][a-zA-Z0-9_]*   { yylval.str = strdup(yytext); return IDENTIFIER; }

[0-9]+                  { yylval.num = atoi(yytext); return NUMBER; }

\"([^"]|\\.)*\"         { yylval.str = strdup(yytext); return STRING; }

[ \t\n]+                ; // Ignorar espaços em branco e tabulações

"//".*    ; // Ignora comentários

.                       { return yytext[0]; } // Caracteres não reconhecidos

%%

int yywrap() {
    return 1;
}
