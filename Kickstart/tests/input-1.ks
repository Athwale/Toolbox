#$$ if: test - test1
CONDITION test IS TURNED ON
#$$ else:
CONDITION test IS TURNED OFF
#$$ fi

#$$ if: test1 - test 1
CONDITION 1 test IS TURNED ON
#$$ else:
CONDITION 1 test IS TURNED OFF
#$$ fi

#$$ if: test - test2
CONDITION 1 test IS TURNED ON
#$$ else:
CONDITION 1 test IS TURNED OFF
#$$ fi