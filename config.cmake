function(topaz_conf_parse_file filepath)
    include(JSONParser.cmake) # https://github.com/sbellus/json-cmake
    file(READ ${filepath} topaz_config_file_contents)
    sbeParseJson(topaz_configuration topaz_config_file_contents)

    # Print the contents of the JSON config file
    foreach(var ${topaz_configuration})
        message(DEBUG "${var} = ${${var}}")
    endforeach()

    set(TOPAZ_CONFIG_VER ${topaz_configuration.version} PARENT_SCOPE)

    # * Set flags in both local and parent scope
    set(MINIMUM_LEVEL ${topaz_configuration.options.minimum_level_logged})
    set(MINIMUM_LEVEL ${topaz_configuration.options.minimum_level_logged} PARENT_SCOPE)
    set(RUNTIME_LEVEL_EVAL ${topaz_configuration.options.allow_change_level_at_runtime})
    set(RUNTIME_LEVEL_EVAL ${topaz_configuration.options.allow_change_level_at_runtime} PARENT_SCOPE)

    # Set the C macro directives
    add_definitions(-DTOPAZ_RUNTIME_LEVEL_CHANGE=${RUNTIME_LEVEL_EVAL})
    add_definitions(-DTOPAZ_MIN_LOGGING_LEVEL=${MINIMUM_LEVEL})

    # * Generate source files
    # Generate the custom print function in /gen/logging_printf.c and the levels macros
    add_custom_command(
        OUTPUT ${GENERATED_BINARY_DIR}/logging_printf.c ${GENERATED_BINARY_DIR}/topaz_levels.h
        DEPENDS ${filepath}
        COMMAND python3 ${CMAKE_CURRENT_SOURCE_DIR}/src/generate_source_code.py ${filepath} ${GENERATED_BINARY_DIR} ${CMAKE_CURRENT_SOURCE_DIR}
        WORKING_DIRECTORY ${GENERATED_BINARY_DIR}
        COMMENT "generating src/generated_printf_code.c"
    )

    sbeClearJson(topaz_configuration)
endfunction()