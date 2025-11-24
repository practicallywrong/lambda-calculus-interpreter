# λ-Calculus Interpreter

This project is a simple **λ-Calculus interpreter** with support for **macro definitions**. It parses lambda expressions, expands macros, and performs **beta-reduction** to normalize expressions.


## Features

* **Lambda calculus parsing**: Supports variables, abstractions (`λx. …`), and applications `(f x)`.
* **Macro expansion**: Define reusable lambda expressions in a configuration file.
* **Expression normalization**: Reduces lambda expressions using beta-reduction.
* Supports **α-conversion** to avoid variable capture during substitution.
* **Debugging support**: Step-by-step token parsing and reduction (optional, default off).


## Usage

Run the interpreter with a lambda calculus program and a macro file:

```bash
python app.py program.lc macros.cfg
```

## Defining Macros

Macros are defined in `macros.cfg` as `NAME = EXPRESSION`.
Example:

```
TWO = (λf.(λx.(f (f x))))
ADD = (λm.(λn.(λf.(λx.((m f) ((n f) x))))))
```

* Macro names must be valid variable names.
* Macros can reference other macros; the interpreter will expand.


## Notes

* The normalizer uses a **step limit** (100,000 by default) to prevent infinite reductions.
# lambda-calculus-interpreter
