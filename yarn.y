%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
extern int yylex();
void yyerror(const char *s);
%}

%union {
    char* str;
    int num;
}

%token <str> STRING IDENTIFIER
%token <num> NUMBER
%token SETUP LBRACE RBRACE VAR EQUALS LPAREN RPAREN SEMICOLON REPEAT FROM TO FUNCTION COMMA IF ELSE COMMENT
%token EQ NEQ LT GT LTE GTE
%type <str> condition expression primary_expr string_literal
%type <num> relational_expr additive_expr multiplicative_expr unary_expr param number
%left '+' '-'
%left '*' '/' '%'
%nonassoc LPAREN RPAREN EQ NEQ LT GT LTE GTE

%%

program: setup_block statement_list
       ;

setup_block: SETUP LBRACE setup_commands RBRACE
           ;

setup_commands: /* empty */
              | setup_commands yarn_command
              | setup_commands hook_command
              ;

yarn_command: IDENTIFIER EQUALS string_literal SEMICOLON
            ;

hook_command: IDENTIFIER EQUALS number SEMICOLON
            ;

statement_list: /* empty */
              | statement_list statement
              ;

statement: function_def
         | variable_decl
         | loop
         | conditional
         | command
         | comment
         ;

variable_decl: VAR IDENTIFIER EQUALS expression SEMICOLON
             ;

command: chain SEMICOLON
       | stitch SEMICOLON
       | change_yarn SEMICOLON
       | skip_chain SEMICOLON
       ;

chain: IDENTIFIER LPAREN number RPAREN
     ;

skip_chain: IDENTIFIER LPAREN number RPAREN
          ;

stitch: single_crochet
      | double_crochet
      | treble_crochet
      | slip_stitch
      ;

single_crochet: IDENTIFIER LPAREN number RPAREN
              ;

double_crochet: IDENTIFIER LPAREN number RPAREN
              ;

treble_crochet: IDENTIFIER LPAREN number RPAREN
              ;

slip_stitch: IDENTIFIER LPAREN number RPAREN
            ;

change_yarn: IDENTIFIER LPAREN string_literal RPAREN
           ;

loop: REPEAT IDENTIFIER FROM number TO number LBRACE statement_list RBRACE
    ;

conditional: IF condition LBRACE statement_list RBRACE
            | IF condition LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE
            ;

condition: expression
         ;

expression: relational_expr
          ;

relational_expr: additive_expr
               | additive_expr relational_op additive_expr
               ;

additive_expr: multiplicative_expr
             | additive_expr '+' multiplicative_expr
             | additive_expr '-' multiplicative_expr
             ;

multiplicative_expr: unary_expr
                    | multiplicative_expr '*' unary_expr
                    | multiplicative_expr '/' unary_expr
                    | multiplicative_expr '%' unary_expr
                    ;

unary_expr: primary_expr
          | '+' primary_expr
          | '-' primary_expr
          ;

primary_expr: number
            | IDENTIFIER
            | LPAREN expression RPAREN
            ;

relational_op: "==" | "!=" | "<" | ">" | "<=" | ">="
             ;

number: NUMBER
      ;

string_literal: STRING
              ;

comment: COMMENT { /* Ignore comment */ }
       ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro sintático: %s\n", s);
}

int main() {
    yyparse();
    return 0;
}