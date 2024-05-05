%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
%}

%token SETUP LBRACE RBRACE VAR EQUALS LPAREN RPAREN SEMICOLON REPEAT FROM TO FUNCTION COMMA COMMENT
%token IDENTIFIER NUMBER STRING

%start program

%%

program: setup_block statement_list
       ;

setup_block: SETUP LBRACE setup_commands RBRACE
           ;

setup_commands: /* empty */
              | setup_commands yarn_command
              | setup_commands hook_command
              ;

yarn_command: IDENTIFIER EQUALS STRING SEMICOLON
            ;

hook_command: IDENTIFIER EQUALS NUMBER SEMICOLON
            ;

statement_list: /* empty */
              | statement_list statement
              ;

statement: function_def
         | variable_decl
         | loop
         | conditional
         | command
         | COMMENT
         ;

variable_decl: VAR IDENTIFIER EQUALS expression SEMICOLON
             ;

command: chain
       | stitch
       | change_yarn
       | skip_chain
       | SEMICOLON
       ;

chain: IDENTIFIER LPAREN NUMBER RPAREN SEMICOLON
     ;

stitch: IDENTIFIER LPAREN NUMBER RPAREN SEMICOLON
      ;

change_yarn: IDENTIFIER LPAREN STRING RPAREN SEMICOLON
           ;

skip_chain: IDENTIFIER LPAREN NUMBER RPAREN SEMICOLON
          ;

loop: REPEAT IDENTIFIER FROM NUMBER TO NUMBER LBRACE statement_list RBRACE
    ;

conditional: IF expression LBRACE statement_list RBRACE
            | IF expression LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE
            ;

function_def: FUNCTION IDENTIFIER LPAREN param_list RPAREN LBRACE statement_list RBRACE
            ;

param_list: /* empty */
          | param_list COMMA IDENTIFIER
          ;

expression: relational_expr
          ;

relational_expr: additive_expr
               | additive_expr EQUALS additive_expr
               ;

additive_expr: multiplicative_expr
             | multiplicative_expr '+' additive_expr
             | multiplicative_expr '-' additive_expr
             ;

multiplicative_expr: unary_expr
                    | unary_expr '*' multiplicative_expr
                    | unary_expr '/' multiplicative_expr
                    | unary_expr '%' multiplicative_expr
                    ;

unary_expr: primary_expr
          | '+' primary_expr
          | '-' primary_expr
          ;

primary_expr: NUMBER
            | IDENTIFIER
            | LPAREN expression RPAREN
            ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro sintático: %s\n", s);
}

int main() {
    yyparse();
    return 0;
}
