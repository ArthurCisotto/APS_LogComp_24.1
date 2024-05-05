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
%token EQ NEQ LT GT LTE GTE CHAIN SKIPCHAIN SINGLECROCHET DOUBLECROCHET TREBLECROCHET SLIPSTITCH CHANGECOLOR
%type <str> condition expression primary_expr string_literal
%type <num> relational_expr additive_expr multiplicative_expr unary_expr number
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

yarn_command: "yarnColor" EQUALS string_literal SEMICOLON
            ;

hook_command: "hookSize" EQUALS number SEMICOLON
            ;

statement_list: /* empty */
              | statement_list statement
              ;

statement: function_def
         | variable_decl
         | loop
         | conditional
         | command
         | assignment_statement
         | function_call
         | comment
         ;

variable_decl: VAR IDENTIFIER EQUALS expression SEMICOLON
             ;

command: chain SEMICOLON
       | skip_chain SEMICOLON
       | single_crochet SEMICOLON
       | double_crochet SEMICOLON
       | treble_crochet SEMICOLON
       | slip_stitch SEMICOLON
       | change_yarn SEMICOLON
       ;

chain: CHAIN LPAREN number RPAREN
     ;

skip_chain: SKIPCHAIN LPAREN number RPAREN
          ;

single_crochet: SINGLECROCHET LPAREN number RPAREN
              ;

double_crochet: DOUBLECROCHET LPAREN number RPAREN
              ;

treble_crochet: TREBLECROCHET LPAREN number RPAREN
              ;

slip_stitch: SLIPSTITCH LPAREN number RPAREN
            ;

change_yarn: CHANGECOLOR LPAREN string_literal RPAREN
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

relational_op: EQ | NEQ | LT | GT | LTE | GTE
             ;

number: NUMBER
      ;

string_literal: STRING
              ;

param: IDENTIFIER
     ;

function_def: FUNCTION IDENTIFIER LPAREN param_list RPAREN LBRACE statement_list RBRACE
            ;

function_call: IDENTIFIER LPAREN opt_arguments RPAREN SEMICOLON
             ;

opt_arguments: /* empty */
             | expression_list
             ;

expression_list: expression
               | expression_list COMMA expression
               ;

param_list: param
          | param_list COMMA param
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
