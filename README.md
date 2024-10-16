# Topaz Logging Library

Topaz is a simple logging library written in C, providing logs with metadata such as timestamps, log levels, file names, and line numbers. 
The library is built to do as much at compile time as possible and will probably be horrific to actually  use.

This project is just me experimenting, wanting to write a basic logging library.
It is most definitely not code that should be reused anywhere remotely important as there will be many bugs and inefficiencies as well as its non-standard build process.


## Features
- **Customisable log messages**: Logs can be formatted with timestamps, log levels, file names, function names, and line numbers for extra context when debugging.
- **Configurable Log Levels**: Supports DEBUG, INFO, WARN, ERROR, and FATAL log levels by default but more can be added.
- **Simple Integration**: Can be added to any CMake project via add_subdirectory() or as a Git submodule.

## Prerequisites

Before using the Topaz library, ensure you have the following installed:

1. CMake: Version 3.10 or higher is required to build the project.
   - You can download CMake from [cmake.org](cmake.org).
2. Python: This project requires Python 3.x to run scripts for generating the source files.
   - You can download Python from [python.org](https://www.python.org/downloads/).
   - Ensure Python is added to your system's PATH. 
3. A C Compiler: You will need a C compiler (such as GCC, Clang, or MSVC) to build the library.

## Installation

You can add Topaz to your project either by cloning it into your repository or adding it as a Git submodule.

### Option 1: Add as a Git Submodule (recommended)

Add Topaz as a submodule to your project:

```bash
git submodule add https://github.com/yourusername/Topaz.git lib/Topaz
```
Initialize the submodule:

```bash
git submodule update --init --recursive
```

In your CMakeLists.txt, add it as a subdirectory and link against your target:

```cmake
add_subdirectory(lib/Topaz)
target_link_libraries(your_target PRIVATE Topaz)
```

Then follow the configuration instructions and the project **should** build. 

### Option 2: Clone the Repository

Clone the repository into your project:
```bash
git clone https://github.com/jdf18/Topaz.git lib/Topaz
```

In your CMakeLists.txt, include Topaz as a subdirectory:

```cmake
add_subdirectory(lib/Topaz)
target_link_libraries(your_target PRIVATE Topaz)
```

Then follow the configuration instructions and the project **should** build.

## Configuration

Topaz currently requires a JSON configuration file to control the logging formats, names for log levels, along with other options.
This configuration file should be provided at configuration time* and the absolute path can be specified with a CMake flag. 
The default path is set to `${CMAKE_SOURCE_DIR}/logging_conf.json`.

*If the logging configuration file is changed, the cmake command should be rerun to ensure any changes take place.  

```cmake
set(TOPAZ_CONFIG_FILE ${CMAKE_CURRENT_SOURCE_DIR}/logging_config.json)
```

### JSON Configuration File

The JSON file should be structured like the following file: (see [default](https://github.com/jdf18/Topaz/blob/main/default_conf.json))

```json
{
  "version": "1.0.0",

  "formatting": {
    "message": "%CODE: %FILE [%LINE] - %TIME: ",
    "time": "%H.%M.%S"
  },

  "levels": {
    "DEBUG": 10,
    "INFO": 20,
    "WARN": 30,
    "ERROR": 40
  },

  "options": {
    "allow_change_level_at_runtime": true,
    "minimum_level_logged": 10
  }
}
```

- `version`: The version of the configuration file.
- `formatting`:
  - `message`: Defines the format of the log message. It supports the variables `%TIME`, `%CODE`, `%FUNC`, `%FILE`, `%PATH`, and `%LINE`.
  - `time`: The format for the timestamps in the log output. This uses date-time format specifiers found [here](https://en.cppreference.com/w/c/chrono/strftime).
- `levels`: Defines numeric values for each named log level. These are also what are used to compare against `minimum_level_logged` 
- `options`:
  - `allow_change_level_at_runtime`: If true, this allows the function `set_application_logging_level()` to be used to change what is printed to the console at runtime.
  - `minimum_level_logged`: Any log statements which have a level lower than this value will not be printed to the console.

For any log statements with a level below `minimum_level_logged`, the C preprocessor will remove the log statement and replace it with nothing so even if `set_application_logging_level()` is used, these statements will not be shown.
Instead, what you can do is use `LOG_LEVEL_STR("DEBUG", TOPAZ_DEBUG, ...)` or `LOG_LEVEL(log_level, ...)`.

## Usage

Include the topaz.h header in your source files where logging is required:

```c
#include "topaz.h"
```

Use the default logging macros to log messages at different levels. Example usage:

```c
LOG_INFO("Application started");
LOG_DEBUG("User ID: %d", user_id);
LOG_WARN("Low memory detected");
LOG_ERROR("Failed to connect to database");
LOG_FATAL("Unexpected system shutdown");
```

## License

Topaz is licensed under the GNU LGPLv3 license. See the [LICENSE](https://github.com/jdf18/Topaz/blob/main/LICENSE) file for more details.
