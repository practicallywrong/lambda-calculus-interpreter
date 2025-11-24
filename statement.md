## Problem Statement

This project demonstrates how even simple Turing-complete systems, such as the λ-calculus, can perform any computation. By building a minimal λ-calculus interpreter with macro support, users can write and execute programs to explore fundamental concepts like recursion, functional abstraction, and computational universality. The goal is to show that complex computations can emerge from simple, minimal primitives.

## Scope of the Project

We will build an interpreter for λ-calculus (using a stricter grammar) with support for macros.

## Target Users

This project is aimed at individuals who want to understand and experiment with λ-calculus to implement algorithms and computational models.

## High-Level Features

* **Lambda Calculus Parsing**: Supports variables, abstractions (`λx. …`), and applications `(f x)`.
* **Macro Expansion**: Define reusable lambda expressions in a configuration file.
* **Expression Normalization**: Reduces lambda expressions using beta-reduction.
* **α-Conversion Support**: Avoids variable capture during substitution.
* **Debugging Support**: Optional step-by-step token parsing and reduction for easier debugging.
