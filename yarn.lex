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

<INITIAL>[a-zA-Z][a-zA-Z0-9_]* {
                            yylval.str = strdup(yytext);
                            return IDENTIFIER;
                        }

<INITIAL>[0-9]+         {
                            yylval.num = atoi(yytext);
                            return NUMBER;
                        }

<INITIAL>"\""([^"]|\\.)*\""" {
                            yylval.str = strdup(yytext);
                            return STRING;
                        }

[ \t\n]                 ; // Ignorar espaços em branco e tabulações
.                       { return yytext[0]; } // Caracteres não reconhecidos

%%

int yywrap() {
    return 1;
}
