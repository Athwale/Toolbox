#!/bin/bash

. $(find . -name crema-common-lib.sh)

# CONFIG ##############################
OUTPUT='./Dump'
TOOL="$(find_upgrade_tool)"
#######################################

if ! test -e "$TOOL"; then
    echo "Error: upgrade_tool not present in $TOOL"
    echo "https://wiki.radxa.com/Rock/flash_the_image"
    exit 1
fi

show_info "Reboot to Loader mode"
adb reboot loader
show_info "Wait 15s"
sleep 15

show_info "Dumping Firmware:"
chmod u+x "$TOOL"
show_info "Test connection:"
$TOOL td &>/dev/null

if ! [ $? -eq 0 ]; then
    show_err "Error: No connection, is the device in loader mode? (adb reboot loader)"
    exit 1
else
    show_ok " Connection OK"
fi 

mkdir -p "$OUTPUT"
show_info "Saving device info in $OUTPUT/device_info.txt"
show_ok "Capability:" > "$OUTPUT/device_info.txt"
$TOOL rcb >> "$OUTPUT/device_info.txt"
show_ok "Flash ID:" >> "$OUTPUT/device_info.txt"
$TOOL rid >> "$OUTPUT/device_info.txt"
show_ok "Flash info:" >> "$OUTPUT/device_info.txt"
$TOOL rfi >> "$OUTPUT/device_info.txt"
show_ok "Chip info:" >> "$OUTPUT/device_info.txt"
$TOOL rci >> "$OUTPUT/device_info.txt"
show_ok "Secure mode:" >> "$OUTPUT/device_info.txt"
$TOOL rsm >> "$OUTPUT/device_info.txt"
show_ok "Partitions:" >> "$OUTPUT/device_info.txt"
$TOOL pl >> "$OUTPUT/device_info.txt"
sed -i -e 's/\r$//' "$OUTPUT/device_info.txt"

show_info "Partition list: (in $OUTPUT/partition_list.txt)"
$TOOL pl | grep "^[0-9][0-9]  0x" | awk '{ print $2" "$3" "$4 }' > "$OUTPUT/partition_list.txt"
sed -i -e 's/\r$//' "$OUTPUT/partition_list.txt"
cat "$OUTPUT/partition_list.txt"

echo; show_info "Downloading paritions into $OUTPUT/Images"
mkdir -p "$OUTPUT/Images"

cat "$OUTPUT/partition_list.txt" | while read line; do
    show_info " Partition: $line"
    NAME=$(echo "$line" | awk '{ print $3}')
    START=$(echo "$line" | awk '{ print $1}')
    LEN=$(echo "$line" | awk '{ print $2}')
    if [ "$NAME" == 'userdata' ]; then
        show_warn "\n#### SKIPPING USERDATA #### (Image too large)\n"
        continue
    fi
    $TOOL rl "$START" "$LEN" "$OUTPUT/Images/$NAME.img"
    if [ $? -eq 0 ]; then
        show_ok " OK"
    else
        show_err " Error: $NAME"
    fi 
    echo
done

show_ok "Download finished, reboot"
$TOOL rd
show_ok "Finished"

ding
