# bim
A custom interpreted programming language built from scrath with python!

## Features
- Full lexer-parser-interpreter pipeline
- Syntax combines best of javascript and python
- All core data types (numbers, string, booleans, arrays)
- Control flow statements (if, else if, else)
- Comes built with some core function and allows for user defined functions
- Error handling provides detailed error reports

## How it works:
### Lexer:
The lexer is the component that reads the code
- Tokenizes source code into symbols
- deals with operators, keywords, symbols, etc
- Strings are also processed here including escape sequences

### Parser
The parser is the component that builds the code
- Build the Abstract Syntax Tree (AST) using tokens provided from the lexer
- Operator precedence is determined here allowing for chained 

### Interpreter 
The interpreter is the component that executes the code
- Executes the nodes in the AST from token
- Variable scoping and function call stacks are managed here
- Exceptions (like break/continue statements) are also managed here

## Installation
Make sure you have python installed. 
Then run:
```bash
git clone https://github.com/jashith1/bim/
cd bim
pip install .
```

## Usage
The syntax for bim is inspired by javascript and python.\
Variables:
```js
// Dynamic typing
my_str = "hello"
my_num = 21
my_bool = true
```

Arrays:
```js
my_arr = [0, 1, 2, 3]
my_arr.push(4)
last = my_arr.pop()
length = my_arr.length()
```

Conditional Statements:
```js
score = 87
if(score >= 90){
    print("A!")
} else if(score >= 80){
    print("B!")
} else if(score >= 70){
    print("C!")
} else{
    print("F")
}
```

Loops:
```js
nums = [73, 46, 21]
for(num in nums){
    print(num)
}

i = 0
while(i < 10){
    print(i)
    i = i + 1
    
    if(i == 7){
        break
    }
}

for(i in range(10)){
    if(i == 3){
        continue
    }
    print(i)
}
```

In-built functions:
```js
print(my_str, "world")
len(my_str)
abs(-21)
upper(my_str)
lower("WORLD")
min(2, 5)
max(2, 5)
```

Custom function:
```js 
function add(a, b){
    return a + b
}

my_sum = add(5, 6)
print(my_sum)
```