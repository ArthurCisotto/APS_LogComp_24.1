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

%token <str> STRING IDENTIFIER YARNCOLOR HOOKSIZE
%token <num> NUMBER
%token SETUP LBRACE RBRACE VAR EQUALS LPAREN RPAREN SEMICOLON REPEAT FROM TO FUNCTION COMMA IF ELSE NEWLINE COMMENT END_OF_FILE
%token EQ NEQ LT GT LTE GTE CHAIN SKIPCHAIN SINGLECROCHET DOUBLECROCHET TREBLECROCHET SLIPSTITCH CHANGECOLOR
%type <str> string_literal
%type <num> expression relational_expr additive_expr multiplicative_expr unary_expr primary_expr number

%left '+' '-'
%left '*' '/' '%'
%nonassoc LPAREN RPAREN EQ NEQ LT GT LTE GTE

%%
program: setup_block statement_list END_OF_FILE
        { printf("Completed parsing program.\n");
            return 0;
        }
        ;

setup_block: SETUP LBRACE optional_newlines setup_commands optional_newlines RBRACE SEMICOLON
           { printf("Setup block parsed.\n"); }
           ;

optional_newlines:
          /* empty */
        | optional_newlines NEWLINE
        ;

setup_commands: /* empty */
              | setup_commands yarn_command optional_newlines
              | setup_commands hook_command optional_newlines
              ;

yarn_command: YARNCOLOR EQUALS string_literal SEMICOLON
             { printf("Parsed yarn command.\n"); }
             ;

hook_command: HOOKSIZE EQUALS number SEMICOLON
             { printf("Parsed hook command.\n"); }
             ;

statement_list: /* empty */
              | statement_list statement
              | statement_list statement NEWLINE
              ;

statement: function_def
         | variable_decl
         | loop
         | conditional
         | command
         | assignment_statement
         | function_call
         | comment
         | NEWLINE
         ;

assignment_statement: IDENTIFIER EQUALS expression SEMICOLON
                      { printf("Parsed assignment statement.\n"); }
                      ;

variable_decl: VAR IDENTIFIER EQUALS expression SEMICOLON
              { printf("Parsed variable declaration.\n"); }
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
      { printf("Parsed chain command.\n"); }
      ;

skip_chain: SKIPCHAIN LPAREN number RPAREN
           { printf("Parsed skip chain command.\n"); }
           ;

single_crochet: SINGLECROCHET LPAREN number RPAREN
               { printf("Parsed single crochet command.\n"); }
               ;

double_crochet: DOUBLECROCHET LPAREN number RPAREN
               { printf("Parsed double crochet command.\n"); }
               ;

treble_crochet: TREBLECROCHET LPAREN number RPAREN
               { printf("Parsed treble crochet command.\n"); }
               ;

slip_stitch: SLIPSTITCH LPAREN number RPAREN
            { printf("Parsed slip stitch command.\n"); }
            ;

change_yarn: CHANGECOLOR LPAREN string_literal RPAREN
            { printf("Parsed change yarn command.\n"); }
            ;

loop: REPEAT IDENTIFIER FROM number TO number LBRACE statement_list RBRACE
     { printf("Parsed loop structure.\n"); }
     ;

conditional: IF condition LBRACE statement_list RBRACE
            | IF condition LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE
            { printf("Parsed conditional structure.\n"); }
            ;

condition: expression
          { printf("Parsed condition.\n"); }
          ;

expression: relational_expr
           { printf("Parsed expression.\n"); }
           ;

relational_expr: additive_expr
               | additive_expr relational_op additive_expr
               { printf("Parsed relational expression.\n"); }
               ;

additive_expr: multiplicative_expr
             | additive_expr '+' multiplicative_expr
             | additive_expr '-' multiplicative_expr
             { printf("Parsed additive expression.\n"); }
             ;

multiplicative_expr: unary_expr
                    | multiplicative_expr '*' unary_expr
                    | multiplicative_expr '/' unary_expr
                    | multiplicative_expr '%' unary_expr
                    { printf("Parsed multiplicative expression.\n"); }
                    ;

unary_expr: primary_expr
          | '+' primary_expr
          | '-' primary_expr
          { printf("Parsed unary expression.\n"); }
          ;

primary_expr: number
            | IDENTIFIER
            | LPAREN expression RPAREN
            { printf("Parsed primary expression.\n"); }
            ;

relational_op: EQ | NEQ | LT | GT | LTE | GTE
              ;

number: NUMBER
       { printf("Parsed number.\n"); }
       ;

string_literal: STRING
               { printf("Parsed string literal.\n"); }
               ;

function_def: FUNCTION IDENTIFIER LPAREN param_list RPAREN LBRACE statement_list RBRACE
            { printf("Parsed function definition.\n"); }
            ;

function_call: IDENTIFIER LPAREN opt_arguments RPAREN SEMICOLON
              { printf("Parsed function call.\n"); }
              ;

opt_arguments: /* empty */
             | expression_list
             ;

expression_list: expression
               | expression_list COMMA expression
               { printf("Parsed expression list.\n"); }
               ;

param_list: IDENTIFIER
          | param_list COMMA IDENTIFIER
          { printf("Parsed parameter list.\n"); }
          ;

comment: COMMENT { /* Ignore comment */ }
       ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro sintático: %s\n", s);
}

int main() {
    int result = yyparse();  // Chama yyparse uma vez e guarda o resultado.
    printf("yyparse() returned %d\n", result);
    if (result == 0) {
        printf("Parsing completed successfully.\n");
        return 0;
    } else {
        printf("Parsing failed.\n");
        return 1;
    }
}
