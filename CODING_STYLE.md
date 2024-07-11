# Introduction

The Flatlander project adheres to a set of coding style guidelines that prioritize readability, maintainability, and simplicity. These guidelines are designed to ensure that the codebase remains consistent, efficient, and easy to understand.

## Core Principles

1. **Declarative over Imperative**: Favor declarative code that focuses on what needs to be accomplished, rather than how it's accomplished. This leads to more concise, expressive, and composable code.
2. **Functional code is king**: Embrace functional programming principles to write pure functions, side effects only go to the TRUTH Object, and promote data immutability.
3. **Immutable code everywhere**: Strive to use immutable data structures and functions that preserve immutability. This ensures that code is more predictable, stable, and easier to reason about.
4. **The TRUTH object**: The TRUTH object is the single source of truth for the system. It's a singleton that contains all state and is responsible for updating and maintaining the system's state.

**Coding Conventions**

- **Indentation**: Use 4 spaces for indentation.
- **Line length**: Keep lines shorter than 80 characters.
- **Naming conventions**:
  - kabob-case-is-the-best-case
  - Use descriptive, kabob-case names for variables and functions.
  - Use PascalCase for class names.
- **Docstrings**: Use triple quotes for docstrings and include a brief description of the function or class.

**Best Practices**

- **Keep it simple**: Favor simple, elegant solutions over complex, convoluted ones.
- **Write tests**: Include comprehensive tests for all code changes to ensure correctness and prevent regressions.
- **Code reviews**: Perform regular code reviews to ensure that code meets the project's coding standards and best practices.

**Enforcement**

These coding style guidelines are enforced using a combination of linters, code formatters, and manual code reviews.

By following these guidelines, we can ensure that the Flatlander codebase remains a joy to work with and a testament to the power of clean, maintainable code.

Feel free to modify or add to this guide as needed!
