#!/bin/python3
import sys
import re
from pathlib import Path


def process_conditions(input_file: Path, output_file: Path, condition: str, active: bool) -> None:
    """
    Evaluate conditions in a file which are written like this:
    #$$ if: secure - test 1
      COMMAND 1
    #$$ else:
      COMMAND 2
    #$$ fi
    :param input_file: Source file.
    :param output_file: Output file.
    :param condition: Condition name to evaluate.
    :param active: Condition state. 1 if: branch is used, 0 else: branch is used.
    :return: None
    """
    if_stub: str = '#$$ if: '
    else_stub: str = '#$$ else:'
    fi_stub: str = '#$$ fi'

    blocks: int = 0
    in_if: bool = False
    in_else: bool = False
    with open(output_file, 'w') as output:
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

                if not line.startswith(f'{if_stub}{condition}'):
                    # Other condition statements are just copied over.
                    output.write(line)
                else:
                    comment: str = line.split('-')[1].strip()
                    blocks += 1
                    print(f'Condition {blocks}: {comment}')
                    in_if = True
    print(f'Evaluated: {blocks} conditions')


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
    processed_file = Path('./post.ks')

    if len(sys.argv) < 3:
        print('Usage: parametrize.py file.ks condition 0/1')
        sys.exit(1)
    try:
        state = bool(int(sys.argv[3]))
        print(f'Processing file: {sys.argv[1]}, condition: {sys.argv[2]}, state: {"ON" if state else "OFF"}')
        result, position, error = validate(Path(sys.argv[1]))
        if result:
            print('If statement syntax OK')
            process_conditions(Path(sys.argv[1]), processed_file, sys.argv[2], state)
            print(f'File: {processed_file} created')
        else:
            print(f'Condition syntax error on line: {position}, {error}')
            sys.exit(1)
    except IndexError as _:
        print('Command line arguments error')
        sys.exit(1)
