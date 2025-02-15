#!/bin/bash

gh repo list LineageOS --limit 4000 | while read -r repo _; do
    if [ $(echo "$repo" | grep "android_device") ]; then
        echo "Selecting $repo"
        gh repo clone "$repo" "$repo"
    fi
done
