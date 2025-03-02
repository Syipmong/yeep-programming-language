# Yeep Programming Language

## Introduction

Yeep is a new programming language designed to be simple, efficient, and easy to learn. It aims to provide developers with a powerful toolset for building a wide range of applications, from web development to data analysis.

## Features

- **Simplicity**: Yeep's syntax is straightforward and easy to understand, making it accessible to beginners.
- **Efficiency**: The language is designed to be fast and efficient, allowing developers to write high-performance code.
- **Versatility**: Yeep can be used for various types of applications, including web development, data analysis, and more.

## Getting Started

To get started with Yeep, follow these steps:

1. **Installation**: Download and install the Yeep compiler from the official website.
2. **Hello World**: Create a new file with the `.yeep` extension and write your first "Hello, World!" program.
3. **Run**: Use the Yeep compiler to run your program and see the output.

## Interactive Session

Below is an example of an interactive session with the Yeep programming language:

```yeep
yeep > FUN add(a, b) -> a + b * 5
<function add>
yeep > add(4, 2)
14
yeep > VAR myFun = someFun(a) -> a
Invalid Syntax: Token cannot appear after previous tokens
File <stdin>, line 1

VAR myFun = someFun(a) -> a
                      ^^
yeep > VAR myFun = someFun(a) -> a + 2
Invalid Syntax: Token cannot appear after previous tokens
File <stdin>, line 1

VAR myFun = someFun(a) -> a + 2
                      ^^
yeep > FUN add(a) -> a
<function add>
yeep > VAR someFun = add
<function add>
yeep > someFun(5)
5
yeep > FUN (c, d) -> c + d
```

## Documentation

For more detailed information on how to use Yeep, please refer to the [official documentation]("")

## Contributing

We welcome contributions from the community. If you would like to contribute to Yeep, please read our [contributing guidelines]("")

## License

## Contact
