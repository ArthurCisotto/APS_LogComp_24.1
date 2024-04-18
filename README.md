# APS_LogComp_24.1

### Introdução à Linguagem de Programação Yarn

**Yarn** é uma linguagem de programação que surgiu da minha paixão pelo crochê em união com os estudos em linguagens formais e lógica da computação. O objetivo era simples: transformar as receitas de crochê, que normalmente seguimos manualmente, em programas que podemos codificar, visualizar e ajustar com facilidade.

### Motivação
Ao aprender sobre linguagens formais, percebi que os padrões de crochê têm muito em comum com a programação: ambos seguem regras precisas e podem ser descritos através de loops, condições e sequências de comandos. Criar a Yarn foi minha maneira de unir esses dois mundos, tornando o crochê mais acessível e inovador através de uma abordagem programática.

### Usos e Capacidades da Yarn

- **Definir Configurações Iniciais**: Os usuários podem especificar características iniciais como a cor do fio e o tamanho da agulha, estabelecendo o contexto para os projetos de crochê.
  
- **Executar Comandos de Crochê**: Comandos específicos para criar correntes, realizar diferentes tipos de pontos (como ponto baixo, ponto alto e mais), mudar a cor do fio, e outras ações fundamentais para construir um projeto de crochê.

- **Utilizar Estruturas de Controle**:
  - **Loops**: Para repetir sequências de pontos, facilitando a criação de padrões complexos sem a necessidade de reescrever os comandos várias vezes.
  - **Condicionais**: Para introduzir mudanças no padrão baseando-se em condições específicas, como alterações na cor do fio após certas linhas, permitindo a personalização avançada dos projetos.

- **Definir e Reutilizar Funções**: Os usuários podem encapsular padrões de crochê em funções, que podem ser reutilizadas ao longo de diferentes projetos, promovendo a modularidade e reusabilidade.

- **Comentar o Código**: Assim como em outras linguagens de programação, Yarn suporta a adição de comentários para explicar partes do código, facilitando a compreensão e manutenção dos padrões.

### EBNF para Yarn

```ebnf
program = { setup_block | command | loop | conditional | function_def | comment } ;

setup_block = "setup", "{", setup_commands, "}" ;
setup_commands = { yarn_command | hook_command } ;
yarn_command = "yarnColor", "=", string_literal ;
hook_command = "hookSize", "=", number ;

command = ( chain | stitch | change_yarn | skip_chain | repeat_command ) ";" ;
chain = "chain", "(", number, ")" ;
skip_chain = "skipChain", "(", number, ")" ;
stitch = ( single_crochet | double_crochet | treble_crochet | slip_stitch ), "(", number, ")" ;
single_crochet = "singleCrochet" ;
double_crochet = "doubleCrochet" ;
treble_crochet = "trebleCrochet" ;
slip_stitch = "slipStitch" ;
change_yarn = "changeYarn", "(", string_literal, ")" ;

loop = "repeat", number, "times", "{", { command }, "}" ;
conditional = "if", condition, "{", { command }, "}" ;
condition = expression ;
expression = simple_expression [ relational_op simple_expression ] ;
simple_expression = term { add_op term } ;
term = number | "row" ;
relational_op = "==" | "!=" | "<" | ">" | "<=" | ">=" ;
add_op = "+" | "-" | "%" ;

function_def = "function", identifier, "()", "{", { command }, "}" ;
repeat_command = "repeat", number, "times", "{", { command }, "}" ;

comment = "//", { all_characters } ;

identifier = letter, { letter | digit | "_" } ;
number = digit, { digit } ;
string_literal = '"', { all_characters - '"' }, '"' ;
letter = "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" ;
digit = "0" | "1" | ... | "9" ;
all_characters = letter | digit | symbol | whitespace ;
symbol = "<" | ">" | "=" | "+" | "-" | "(" | ")" | "{" | "}" | ";" | "," | "." ;
whitespace = " " | tab | newline ;
```

### Exemplo de Receita do Cachecol em Yarn

```yarn
// Setup inicial do projeto de cachecol
setup {
  yarnColor = "gray";  // Define a cor do fio como cinza
  hookSize = 10;       // Define o tamanho da agulha para fio super bulky
}

// Cria a linha de base do cachecol
function foundationRow() {
  chain(11);  // Cria 11 correntes para a linha de base
}

// Primeira linha após a linha de base
function firstRow() {
  skipChain(1);  // Pula a primeira corrente
  repeat 10 times {
    singleCrochet(1);  // Faz um ponto baixo em cada corrente restante
  }
}

// Linhas subsequentes
function standardRow() {
  chain(1);  // Faz 1 corrente e vira o trabalho
  repeat 10 times {
    singleCrochet(1);  // Faz um ponto baixo em cada ponto abaixo
  }
}

// Construção do cachecol
foundationRow();  // Executa a linha de fundação
firstRow();       // Executa a primeira linha de ponto baixo

// Repete a linha padrão do cachecol para as linhas 2 até 101
repeat 100 times {
  standardRow();
}

// Finalizando o cachecol
// Finalize o cachecol cortando o fio e escondendo as pontas soltas com uma agulha.
```
