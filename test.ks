echo

#$$ if: secure - test 1
CONDITION secure IS TURNED ON
#$$ else:
CONDITION secure TURNED OFF
#$$ fi
#$$ if: secure - test 2
CONDITION secure IS TURNED ON
#$$ else:
CONDITION secure TURNED OFF
#$$ fi

echo

#$$ if: test - test test
CONDITION test IS TURNED ON
#$$ else:
CONDITION test IS TURNED OFF
#$$ fi

#$$ if: secure - comment for a condition
CONDITION secure IS TURNED ON
#$$ else:
CONDITION secure TURNED OFF
#$$ fi
