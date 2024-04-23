echo 'test' >> testfile
#$$ if: test - test test
#CONDITION test IS TURNED ON
sed -s
#$$ else:
if [ 1 -eq 1 ]; then
    echo 'yes'
fi
# TEST
CONDITION test IS TURNED OFF
#$$ fi
echo 'done'