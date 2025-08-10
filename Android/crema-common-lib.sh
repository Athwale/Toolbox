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

function verify_adb() {
    adb devices -l | grep -qw 'device'
    if [ $? -eq 0 ]; then
        show_ok "Device found"
    else
        show_info "Restart adb server"
        adb kill-server
        adb start-server
        sleep 1
        adb devices -l | grep -qw 'device'
        if [ $? -eq 0 ]; then
            show_ok "ADB device found"
        else
            show_err "No device"
            exit 1
        fi
    fi
}

function ding() {
    if which paplay &>/dev/null; then
        S=$(find . -name ding.wav)
        paplay "$S"
    fi
}







