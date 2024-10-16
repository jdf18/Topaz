import sys
import json
import yaml


def parse_json(path):
    with open(path) as file:
        return json.loads(file.read())


def parse_format(format_string):
    # PATH, FILE, FUNC, LINE, TIME, CODE
    form = ''
    args = []
    i = 0

    while i < len(format_string):
        if format_string[i] == '%':
            i += 1
            assert i+3 < len(format_string)
            form += '%s'
            test_string = format_string[i:i+4]
            if test_string in ["PATH", "FILE", "FUNC", "LINE", "TIME", "CODE"]:
                args.append({
                                "PATH": "path",
                                "FILE": "file",
                                "FUNC": "func",
                                "LINE": "line",
                                "TIME": "time_str",
                                "CODE": "code"
                            }[test_string])
                i += 4
            else:
                raise AssertionError(test_string)
        else:
            form += format_string[i]
            i += 1

    return args, form


def generate_printf_code(format_string: str, time_format: str):
    args, form = parse_format(format_string)
    arg_code = ''.join([', '+x for x in args])

    setup_code = ''

    if "time_str" in args:
        setup_code += strings["time_setup_code"].format(time_format=time_format)
    if "file" in args:
        setup_code += strings["file_setup_code"]

    with open("logging_printf.c", 'w') as file:
        file.write(strings["logging_printf"].format(setup_code=setup_code, form=form, arg_code=arg_code))


def generate_header(levels: dict, src_file_dir):
    with open(src_file_dir+"/src/topaz.h.txt", 'r') as file:
        topaz_core = file.read()

    log_nos = '\n'.join([strings["template_log_level_macro"].format(name=k, value=v) for k, v in levels.items()])
    log_methods = '\n'.join([strings["template_log_macro"].format(name=k) for k in levels.keys()])

    file_contents = '\n'.join([strings["topaz_header_start"], log_nos, log_methods, strings["topaz_header_end"]])

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

        with open(src_file_dir+"/src/generation_strings.yaml", 'r') as file:
            strings: dict[str] = yaml.safe_load(file)
        del file

        config = parse_json(config_file_path)

        generate_printf_code(config['formatting']['message'], config['formatting']['time'])

        generate_header(config['levels'], src_file_dir)
        generate_lut(config['levels'], src_file_dir)

