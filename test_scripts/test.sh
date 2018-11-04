#!/bin/bash

# To use this:
# ./test.sh <remote server #> <port #> <resource name> <rate limit in thousands of bytes>

# You can add or remove these if you want to test more or fewer threads.

wget remote0$1.cs.binghamton.edu:$2/$3 --limit-rate=$4k &
wget remote0$1.cs.binghamton.edu:$2/$3 --limit-rate=$4k &
wget remote0$1.cs.binghamton.edu:$2/$3 --limit-rate=$4k &
wget remote0$1.cs.binghamton.edu:$2/$3 --limit-rate=$4k &
wget remote0$1.cs.binghamton.edu:$2/$3 --limit-rate=$4k &
wget remote0$1.cs.binghamton.edu:$2/$3 --limit-rate=$4k &
wget remote0$1.cs.binghamton.edu:$2/$3 --limit-rate=$4k &
wget remote0$1.cs.binghamton.edu:$2/$3 --limit-rate=$4k
