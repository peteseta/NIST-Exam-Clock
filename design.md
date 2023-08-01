The design philosophy is akin to that of a web frontend interfacing with a backend.
- The "frontend" are the UI components which are mostly defined as classes in helper files.
- These objects communicate with the "backend" (the main app class in /main.py) through callback functions
  - Data is not stored until it is passed to the backend. This way, the logic does not depend on any UI and works independantly, good for a critical task like this exam clock.
- The frontend objects don't work with each other, it's up to the backend to transfer data between components.

- This largely separates development of the UI vs. the underlying data structures, validation, and core functions.
  - This simplifies development and increases extendability.
  - The code is more readable and easier to understand.