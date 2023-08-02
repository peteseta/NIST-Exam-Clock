# NIST Exam Clock

This is designed to be a replacement for `exam_clock_8_main_mac_v3.app`, which was previously used to run all internal examinations at NIST.

While the app is packaged for distribution, this repository and all the source code has been made public to allow for community debugging and future maintainance/development

## Features
tbw

## On various design choices

The design philosophy is akin to that of a web frontend interfacing with a backend.
- The "frontend" are the UI components which are mostly defined as classes in helper files.
- These objects communicate with the "backend" (the main app class in /main.py) through callback functions
  - Data is not stored until it is passed to the backend. This way, the logic does not depend on any UI and works independantly, good for a critical task like this exam clock.
- The frontend objects don't work with each other, it's up to the backend to transfer data between components.

This design largely separates development of the UI vs. the underlying data structures, validation, and core functions.
  - This simplifies development and increases extendability.
  - The code is more readable and easier to understand.

### *Why isn't there a database function to insert preset IB subject + papers?*

A database would only make sense if it also contained each subject's paper details (reading time, duration) which in the proposed implementation it does not (it only contains a list of subjects and levels)
- Such a database would need to be updated each time the curriculum changes
  - This would either involve scraping (PDF/web) data or processing data from internal IBO documents which likely cannot be shared with me, may change in format, and is anyway outside the scope of the IA.
  - This exam clock should last well after I graduate, so should be no function which needs to be updated at each curriculum change.
- The existing clock is also used for SAT exams, where all the above reasons also apply.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details