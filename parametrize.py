#!/bin/python3
import sys
import re
from io import StringIO
from pathlib import Path


def process_conditions(input_file: Path, condition: str, active: bool) -> (list[str], StringIO):
    """
    Evaluate conditions in a file which are written like this:
    #$$ if: secure - test 1
      COMMAND 1
    #$$ else:
      COMMAND 2
    #$$ fi
    :param input_file: Source file.
    :param condition: Condition name to evaluate.
    :param active: Condition state. 1 if: branch is used, 0 else: branch is used.
    :return: (list[condition comments], output)
    """
    if_stub: str = '#$$ if: '
    else_stub: str = '#$$ else:'
    fi_stub: str = '#$$ fi'

    output_io = StringIO()
    comments = []
    in_if: bool = False
    in_else: bool = False
    with open(input_file, 'r') as ks:
        for line in ks.readlines():
            # Condition is active:
            if active and in_else and line.startswith(fi_stub):
                in_else = False
                in_if = False
                continue
            elif active and in_else:
                continue
            if active and in_if and line.startswith(else_stub):
                in_if = False
                in_else = True
                continue
            elif active and in_if and line.startswith(fi_stub):
                in_if = False
                continue

            # Condition is not active:
            if not active and in_if and line.startswith(fi_stub):
                in_else = False
                in_if = False
                continue
            if not active and in_if and line.startswith(else_stub):
                in_if = False
                in_else = True
                continue
            elif not active and in_if:
                continue
            elif not active and in_else and line.startswith(fi_stub):
                in_else = False
                continue

            if not line.startswith(f'{if_stub}{condition} -'):
                # Other condition statements are just copied over.
                output_io.write(line)
            else:
                comment: str = line.split('-')[1].strip()
                comments.append(comment)
                in_if = True
    return comments, output_io


def validate(file: Path) -> (bool, int, str):
    """
    Check the syntax of if conditions in the file.
    :param file: Path to the file.
    :return: (True if ok, line number, error)
    """
    last_if = 0
    line_n = 0
    else_cnt = 0
    in_if_branch = False
    with open(file, 'r') as ks:
        for line in ks.readlines():
            line_n += 1
            if line.startswith('#$$'):
                if not re.search(r'^#\$\$ fi$|^#\$\$ else:$|^#\$\$ if: \w+ - [\w ]+$', line):
                    return False, line_n, 'Unrecognized keyword'
            if in_if_branch and line.startswith('#$$ if:'):
                return False, line_n, 'Stray if'
            elif line.startswith('#$$ if:'):
                in_if_branch = True
                last_if = line_n
            elif in_if_branch and line.startswith('#$$ else:'):
                else_cnt += 1
                if else_cnt > 1:
                    return False, line_n, 'Multiple else statements'
            elif in_if_branch and line.startswith('#$$ fi'):
                in_if_branch = False
                else_cnt = 0
            elif not in_if_branch and line.startswith('#$$ fi'):
                return False, line_n, 'Stray fi'
            elif not in_if_branch and line.startswith('#$$ else:'):
                return False, line_n, 'Stray else'
        if in_if_branch:
            return False, last_if, 'Stray if'
    return True, 0, ''


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Usage: parametrize.py input.ks output.ks condition 0/1')
        sys.exit(1)
    try:
        input_file: str = sys.argv[1]
        output_file: str = sys.argv[2]
        condition: str = sys.argv[3]
        state: bool = bool(int(sys.argv[4]))
        print(f'Processing file: {input_file}, condition: {condition}, state: {"ON" if state else "OFF"}')
        result, position, error = validate(Path(input_file))
        if result:
            print('If/else syntax OK')
            condition_comments, output = process_conditions(Path(input_file), condition, state)
            for n, c in enumerate(condition_comments):
                print(f'Evaluated {n}: {c}')
            print(f'File: {output_file} created. {len(condition_comments)} conditions evaluated')

            with open(Path(output_file), 'w') as o:
                o.write(output.getvalue())

        else:
            print(f'Condition syntax error on line: {position}, {error}')
            sys.exit(1)
    except IndexError as _:
        print('Command line arguments error')
        sys.exit(1)
