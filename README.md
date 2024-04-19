# APS_LogComp_24.1

### Introdução à Linguagem de Programação Yarn

**Yarn** é uma linguagem de programação que surgiu da minha paixão pelo crochê em união com os estudos em linguagens formais e lógica da computação. O objetivo era simples: transformar as receitas de crochê, que normalmente seguimos manualmente, em programas que podemos codificar, visualizar e ajustar com facilidade.

### Motivação
Ao aprender sobre linguagens formais, percebi que os padrões de crochê têm muito em comum com a programação: ambos seguem regras precisas e podem ser descritos através de loops, condições e sequências de comandos. Criar a Yarn foi minha maneira de unir esses dois mundos.

### Usos e Capacidades da Yarn

- **Definir Configurações Iniciais**: Os usuários podem especificar características iniciais como a cor do fio e o tamanho da agulha, estabelecendo o contexto para os projetos de crochê.
  
- **Executar Comandos de Crochê**: Comandos específicos para criar correntes, realizar diferentes tipos de pontos (como ponto baixo, ponto alto e mais), mudar a cor do fio, e outras ações fundamentais para construir um projeto de crochê.

- **Utilizar Estruturas de Controle**:
  - **Loops**: Para repetir sequências de pontos, facilitando a criação de padrões complexos sem a necessidade de reescrever os comandos várias vezes.
  - **Condicionais**: Para introduzir mudanças no padrão baseando-se em condições específicas, como alterações na cor do fio após certas carreiras, permitindo a personalização avançada dos projetos.

- **Definir e Reutilizar Funções**: Os usuários podem encapsular padrões de crochê em funções, que podem ser reutilizadas ao longo de diferentes projetos, promovendo a modularidade e reusabilidade.

- **Comentar o Código**: Assim como em outras linguagens de programação, Yarn suporta a adição de comentários para explicar partes do código, facilitando a compreensão e manutenção dos padrões.

### EBNF para Yarn

```ebnf
program = setup_block, { statement } ;

setup_block = "setup", "{", setup_commands, "}" ;
setup_commands = { yarn_command | hook_command } ;
yarn_command = "yarnColor", "=", string_literal ;
hook_command = "hookSize", "=", number ;

statement = function_def | variable_decl | loop | conditional | command | comment ;

variable_decl = "var", identifier, "=", expression, ";" ;

command = ( chain | stitch | change_yarn | skip_chain ), ";" ;
chain = "chain", "(", number, ")" ;
skip_chain = "skipChain", "(", number, ")" ;
stitch = single_crochet | double_crochet | treble_crochet | slip_stitch ;
single_crochet = "singleCrochet", "(", number, ")" ;
double_crochet = "doubleCrochet", "(", number, ")" ;
treble_crochet = "trebleCrochet", "(", number, ")" ;
slip_stitch = "slipStitch", "(", number, ")" ;
change_yarn = "changeYarn", "(", string_literal, ")" ;

loop = "repeat", identifier, "from", number, "to", number, "{", { statement }, "}" ;

conditional = "if", condition, "{", { statement }, "}", [ "else", "{", { statement }, "}" ] ;

condition = expression ;
expression = relational_expr ;
relational_expr = additive_expr [ relational_op additive_expr ] ;
additive_expr = multiplicative_expr { add_op multiplicative_expr } ;
multiplicative_expr = unary_expr { mul_op unary_expr } ;
unary_expr = ["+" | "-"], primary_expr ;
primary_expr = number | identifier | "(", expression, ")" ;

relational_op = "==" | "!=" | "<" | ">" | "<=" | ">=" ;
add_op = "+" | "-" ;
mul_op = "*" | "/" | "%" ;

function_def = "function", identifier, "(", [ param_list ], ")", "{", { statement }, "}" ;
param_list = param { ",", param } ;
param = identifier ;

comment = "//", { all_characters } ;

identifier = letter, { letter | digit | "_" } ;
number = digit, { digit } ;
string_literal = '"', { all_characters - '"' }, '"' ;
letter = "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" ;
digit = "0" | "1" | ... | "9" ;
all_characters = letter | digit | symbol | whitespace ;
symbol = "<" | ">" | "=" | "+" | "-" | "*" | "/" | "%" | "(" | ")" | "{" | "}" | ";" | "," | "." ;
whitespace = " " | tab | newline ;
```

### Exemplo de Receita do Cachecol em Yarn

```yarn
// Setup inicial do projeto de cachecol
setup {
  yarnColor = "gray";  // Define a cor inicial do fio como cinza
  hookSize = 10;       // Define o tamanho da agulha para 10mm
};

var currentRow = 1;  // Inicializa a variável de controle de carreira

// Cria a carreira de base do cachecol
function foundationRow() {
  chain(11);  // Cria 11 correntes para a carreira de base
};

// Primeira carreira após a carreira de base
function firstRow() {
  skipChain(1);  // Pula a primeira corrente
  repeat 10 times {
    singleCrochet(1);  // Faz um ponto baixo em cada corrente restante
  }
};

// carreiras subsequentes com controle explícito de cor
function standardRow() {
  if (currentRow % 2 == 0) {
    changeYarn("white");  // Muda a cor do fio para branco nas carreiras pares
  } else {
    changeYarn("gray");   // Retorna para a cor cinza nas carreiras ímpares
  }
  chain(1);  // Faz 1 corrente e vira o trabalho
  repeat 10 times {
    singleCrochet(1);  // Faz um ponto baixo em cada ponto abaixo
  }
};

// Construção do cachecol
foundationRow();  // Executa a carreira de fundação
firstRow();       // Executa a primeira carreira de ponto baixo
currentRow = 2;   // Atualiza a variável de carreira

// Repete a carreira padrão do cachecol para as carreiras 2 até 101
repeat currentRow from 2 to 101 {
  standardRow();  // Aplica a função de carreira padrão
  currentRow = currentRow + 1;  // Incrementa o número da carreira
}

// Finalizando o cachecol
// Finalize o cachecol cortando o fio e escondendo as pontas soltas com uma agulha de lã.
```
