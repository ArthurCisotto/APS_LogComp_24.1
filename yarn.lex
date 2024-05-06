%{
#include "yarn.tab.h"
%}

%%

"setup"                 { printf("Token: SETUP\n"); return SETUP; }
"{"                     { printf("Token: LBRACE\n"); return LBRACE; }
"}"                     { printf("Token: RBRACE\n"); return RBRACE; }
"var"                   { printf("Token: VAR\n"); return VAR; }
"="                     { printf("Token: EQUALS\n"); return EQUALS; }
"("                     { printf("Token: LPAREN\n"); return LPAREN; }
")"                     { printf("Token: RPAREN\n"); return RPAREN; }
";"                     { printf("Token: SEMICOLON\n"); return SEMICOLON; }
"repeat"                { printf("Token: REPEAT\n"); return REPEAT; }
"from"                  { printf("Token: FROM\n"); return FROM; }
"to"                    { printf("Token: TO\n"); return TO; }
"function"              { printf("Token: FUNCTION\n"); return FUNCTION; }
","                     { printf("Token: COMMA\n"); return COMMA; }
"if"                    { printf("Token: IF\n"); return IF; }
"else"                  { printf("Token: ELSE\n"); return ELSE; }
"//"                    { printf("Token: COMMENT\n"); return COMMENT; }
"yarnColor"             { printf("Token: YARNCOLOR\n"); return YARNCOLOR; }
"hookSize"              { printf("Token: HOOKSIZE\n"); return HOOKSIZE; }
"chain"                 { printf("Token: CHAIN\n"); return CHAIN; }
"skipChain"             { printf("Token: SKIPCHAIN\n"); return SKIPCHAIN; }
"singleCrochet"         { printf("Token: SINGLECROCHET\n"); return SINGLECROCHET; }
"doubleCrochet"         { printf("Token: DOUBLECROCHET\n"); return DOUBLECROCHET; }
"trebleCrochet"         { printf("Token: TREBLECROCHET\n"); return TREBLECROCHET; }
"slipStitch"            { printf("Token: SLIPSTITCH\n"); return SLIPSTITCH; }
"changeYarn"            { printf("Token: CHANGECOLOR\n"); return CHANGECOLOR; }
"=="                    { printf("Token: EQ\n"); return EQ; }
"!="                    { printf("Token: NEQ\n"); return NEQ; }
"<"                     { printf("Token: LT\n"); return LT; }
"<="                    { printf("Token: LTE\n"); return LTE; }
">"                     { printf("Token: GT\n"); return GT; }
">="                    { printf("Token: GTE\n"); return GTE; }
"+"                     { printf("Token: +\n"); return '+'; }
"-"                     { printf("Token: -\n"); return '-'; }
"*"                     { printf("Token: *\n"); return '*'; }
"/"                     { printf("Token: /\n"); return '/'; }
"%"                     { printf("Token: %\n"); return '%'; }
[a-zA-Z][a-zA-Z0-9_]*   { yylval.str = strdup(yytext); return IDENTIFIER; }
[0-9]+                  { yylval.num = atoi(yytext); return NUMBER; }
\"([^"]|\\.)*\"         { yylval.str = strdup(yytext); return STRING; }
[ \t\r]+                ; // Ignora espaços em branco, tabulações e retorno de carro
"\n"                    { printf("Token: NEWLINE\n"); return NEWLINE; } // Trata quebras de linha explicitamente
"//".*                  ; // Ignora comentários
.                       { return yytext[0]; } // Caracteres não reconhecidos
<<EOF>>                 { printf("Token: EOF\n"); return END_OF_FILE; }
%%
