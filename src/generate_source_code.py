import sys
import json


def parse_json(path):
    with open(path) as file:
        return json.loads(file.read())


# noinspection t
def generate_printf_code(format_string: str, time_format: str):
    # PATH, FILE, FUNC, LINE, TIME, CODE
    form = ''
    args = []
    i = 0

    while i < len(format_string):
        if format_string[i] != '%':
            form += format_string[i]
            i += 1
            continue
        else:
            i += 1
            assert i+3 < len(format_string)
            form += '%s'
            if format_string[i:i+4] == "PATH":
                args.append("path")
                i += 4
                continue
            if format_string[i:i+4] == "FILE":
                args.append("file")
                i += 4
                continue
            if format_string[i:i+4] == "FUNC":
                args.append("func")
                i += 4
                continue
            if format_string[i:i+4] == "LINE":
                args.append("line")
                i += 4
                continue
            if format_string[i:i+4] == "TIME":
                args.append("timeb")
                i += 4
                continue
            if format_string[i:i+4] == "CODE":
                args.append("code")
                i += 4
                continue
            print(format_string[i:i+4])
            raise AssertionError()

    arg_code = ''.join([', '+x for x in args])

    setup_code = ''

    is_time_required = ("timeb" in args)
    if is_time_required:
        setup_code += f'''
    char timeb[20];
    time_t now = time(NULL);
    struct tm *t = localtime(&now);
    strftime(timeb, sizeof(timeb), "{time_format}", t);
'''

    is_file_required = ("file" in args)
    if is_file_required:
        setup_code += '''
    char* last_slash = strrchr(path, '/');
    if (!last_slash) {
        last_slash = strrchr(path, '\\\\');
    }

    char* file = last_slash ? last_slash + 1 : path;
    '''

    with open("logging_printf.c", 'w') as file:
        file.write(f'''
#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <time.h>
#include "topaz.h"
            
void generated_print_strings(char* code, char* path, char* func, char* line) {{
{setup_code}
    printf("{form}"{arg_code});
}}
''')


def generate_header(levels: dict, src_file_dir):
    with open(src_file_dir+"/src/topaz.h.txt", 'r') as file:
        topaz_core = file.read()

    template_log_no = '''
#ifndef TOPAZ_{name}
#define TOPAZ_{name} {value}
#endif'''
    log_nos = '\n'.join([template_log_no.format(name=k, value=v) for k, v in levels.items()])

    template_log_method = '''
#if TOPAZ_{name} >= TOPAZ_MIN_LOGGING_LEVEL
#define LOG_{name}(...) LOG_LEVEL_STR("{name}", TOPAZ_{name},##__VA_ARGS__)
#else
#define LOG_{name}(...)
#endif'''
    log_methods = '\n'.join([template_log_method.format(name=k) for k in levels.keys()])

    file_contents = f'''
{topaz_core}

{log_nos}


{log_methods}

#endif //TOPAZ_TOPAZ_H
        '''
    with open("topaz.h", 'w') as file:
        file.write(file_contents)
    with open(src_file_dir+"/include/topaz.h", 'w') as file:
        file.write(file_contents)


def generate_lut(levels: dict, src_file_dir):
    max_index = max(levels.values()) + 1

    template_lut_row = '"{text}", '
    lut_rows = []
    for i in range(max_index):
        if i in levels.values():
            lut_rows.append(
                template_lut_row.format(
                    text=list(levels.keys())[list(levels.values()).index(i)]
                )
            )
        else:
            lut_rows.append(
                template_lut_row.format(
                    text='\\0'
                )
            )

    lut_contents = '\n'.join(lut_rows)

    file_contents = f'''
#ifndef TOPAZ_LEVELS_LUT_H
#define TOPAZ_LEVELS_LUT_H

#define TOPAZ_LUT_SIZE {max_index}

static const char* lut[] = {{
{lut_contents}
}};

#endif'''

    with open("levels_lut.h", 'w') as file:
        file.write(file_contents)
    with open(src_file_dir+"/src/levels_lut.h", 'w') as file:
        file.write(file_contents)


if __name__ == "__main__":
    if len(sys.argv) > 3:
        results = []

        config_file_path = sys.argv[1]
        gen_file_dir = sys.argv[2]
        src_file_dir = sys.argv[3]

        config = parse_json(config_file_path)

        generate_printf_code(config['formatting']['message'], config['formatting']['time'])

        generate_header(config['levels'], src_file_dir)
        generate_lut(config['levels'], src_file_dir)

