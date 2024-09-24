import sys
import json


def parse_json(path):
    with open(path) as file:
        return json.loads(file.read())


def set_compiler_flags(config, results):
    results.append(
        '1' if config["options"]["allow_change_level_at_runtime"] else '0'
    )
    results.append(
        config["options"]["minimum_level_logged"]
    )
    return


def return_values_to_cmake(results):
    print(';'.join(map(str, results)))
    exit(0)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        results = []

        config_file_path = sys.argv[1]
        config = parse_json(config_file_path)

        set_compiler_flags(config, results)

        return_values_to_cmake(results)
    exit(-1)
