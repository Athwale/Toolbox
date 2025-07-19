#!/bin/bash
BLUE="\033[1;34m"
RED="\033[1;31m"
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
SPECIAL="\033[5m\033[3;31m\033[1;107m"
ENDC="\033[0m"

function show_info() {
    echo $2 -e "${BLUE}{ INFO    } $1 ${ENDC}" >&2
}

function show_err() {
    echo -e "${RED}{ ERROR   } $1 ${ENDC}" >&2
}

function show_warn() {
    echo -e "${YELLOW}{ WARNING } $1 ${ENDC}" >&2
}

function show_warn_special() {
    echo -e "${SPECIAL}{ WARNING } $1 ${ENDC}" >&2
}

function show_ok() {
    echo -e "${GREEN}{ OK      } $1 ${ENDC}" >&2
}

function find_upgrade_tool() {
    UT=$(find . -name 'upgrade_tool' | head -n 1)
    if test -e "$UT"; then
        "$UT" td | grep -q 'Program Log will save'
        if [ $? -eq 0 ]; then
            echo "$UT"
            return
        fi
    fi
    echo ""
}










