The design philosophy is akin to that of a web frontend interfacing with a backend.
- The "frontend" are the UI components which are mostly defined as classes in helper files.
- These objects communicate with the "backend" (the main app class in /main.py) through callback functions.
- The frontend objects don't work with each other, it's up to the backend to transfer data between components.

- This largely separates development of the UI vs. the underlying data structures, validation, and core functions.
  - This simplifies development and increases extendability.
  - The code is more readable and easier to understand.