#!/bin/bash

# CONFIG ##############################
OUTPUT='../Dump'
TOOL='./Linux_Upgrade_Tool/upgrade_tool'
#######################################

if ! test -e "$TOOL"; then
    echo "Error: upgrade_tool not present in $(pwd)"
    echo "https://wiki.radxa.com/Rock/flash_the_image"
    exit 1
fi

echo "Reboot to Loader mode"
adb reboot loader
echo "Wait"
sleep 15

echo "Dumping Firmware:"
chmod u+x "$TOOL"
echo "Test connection:"
$TOOL td &>/dev/null

if ! [ $? -eq 0 ]; then
    echo "Error: No connection, is the device in loader mode? (adb reboot loader)"
    exit 1
else
    echo " Connection OK"
fi 

mkdir -p "$OUTPUT"
echo "Saving device info in $OUTPUT/device_info.txt"
echo "Capability:" > "$OUTPUT/device_info.txt"
$TOOL rcb >> "$OUTPUT/device_info.txt"
echo "Flash ID:" >> "$OUTPUT/device_info.txt"
$TOOL rid >> "$OUTPUT/device_info.txt"
echo "Flash info:" >> "$OUTPUT/device_info.txt"
$TOOL rfi >> "$OUTPUT/device_info.txt"
echo "Chip info:" >> "$OUTPUT/device_info.txt"
$TOOL rci >> "$OUTPUT/device_info.txt"
echo "Secure mode:" >> "$OUTPUT/device_info.txt"
$TOOL rsm >> "$OUTPUT/device_info.txt"
echo "Partitions:" >> "$OUTPUT/device_info.txt"
$TOOL pl >> "$OUTPUT/device_info.txt"
sed -i -e 's/\r$//' "$OUTPUT/device_info.txt"

echo "Partition list: (in $OUTPUT/partition_list.txt)"
$TOOL pl | grep "^[0-9][0-9]  0x" | awk '{ print $2" "$3" "$4 }' > "$OUTPUT/partition_list.txt"
sed -i -e 's/\r$//' "$OUTPUT/partition_list.txt"
cat "$OUTPUT/partition_list.txt"

echo; echo "Downloading paritions into $OUTPUT/Images"
mkdir -p "$OUTPUT/Images"

cat "$OUTPUT/partition_list.txt" | while read line; do
    echo " Partition: $line"
    NAME=$(echo "$line" | awk '{ print $3}')
    START=$(echo "$line" | awk '{ print $1}')
    LEN=$(echo "$line" | awk '{ print $2}')
    if [ "$NAME" == 'userdata' ]; then
        echo -e "\n#### SKIPPING USERDATA #### (Image too large)\n"
        continue
    fi
    $TOOL rl "$START" "$LEN" "$OUTPUT/Images/$NAME.img"
    if [ $? -eq 0 ]; then
        echo " OK"
    else
        echo " Error: $NAME"
    fi 
    echo
done

echo "Download finished, reboot"
$TOOL rd
echo "Finished"

