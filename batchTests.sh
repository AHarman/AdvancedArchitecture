#!/bin/sh

echo "Grouping 1"
python programs/gentests.py -r 16 -i 64 -g 1
echo 1
python simulator.py -f out.txt -a -e 1
echo 2
python simulator.py -f out.txt -a -e 2
echo 4
python simulator.py -f out.txt -a -e 4
echo 8
python simulator.py -f out.txt -a -e 8
echo 16
python simulator.py -f out.txt -a -e 16

echo "Grouping 2"
python programs/gentests.py -r 16 -i 64 -g 2
echo 1
python simulator.py -f out.txt -a -e 1
echo 2
python simulator.py -f out.txt -a -e 2
echo 4
python simulator.py -f out.txt -a -e 4
echo 8
python simulator.py -f out.txt -a -e 8
echo 16
python simulator.py -f out.txt -a -e 16

echo "Grouping 4"
python programs/gentests.py -r 16 -i 64 -g 4
echo 1
python simulator.py -f out.txt -a -e 1
echo 2
python simulator.py -f out.txt -a -e 2
echo 4
python simulator.py -f out.txt -a -e 4
echo 8
python simulator.py -f out.txt -a -e 8
echo 16
python simulator.py -f out.txt -a -e 16

echo "Grouping 8"
python programs/gentests.py -r 16 -i 64 -g 8
echo 1
python simulator.py -f out.txt -a -e 1
echo 2
python simulator.py -f out.txt -a -e 2
echo 4
python simulator.py -f out.txt -a -e 4
echo 8
python simulator.py -f out.txt -a -e 8
echo 16
python simulator.py -f out.txt -a -e 16

echo "Grouping 16"
python programs/gentests.py -r 16 -i 64 -g 16
echo 1
python simulator.py -f out.txt -a -e 1
echo 2
python simulator.py -f out.txt -a -e 2
echo 4
python simulator.py -f out.txt -a -e 4
echo 8
python simulator.py -f out.txt -a -e 8
echo 16
python simulator.py -f out.txt -a -e 16

echo "Grouping 32"
python programs/gentests.py -r 16 -i 64 -g 32
echo 1
python simulator.py -f out.txt -a -e 1
echo 2
python simulator.py -f out.txt -a -e 2
echo 4
python simulator.py -f out.txt -a -e 4
echo 8
python simulator.py -f out.txt -a -e 8
echo 16
python simulator.py -f out.txt -a -e 16

git checkout superscalar-ooo

echo "Grouping 1"
python programs/gentests.py -r 16 -i 64 -g 1
echo 1
python simulator.py -f out.txt -a -e 1
echo 2
python simulator.py -f out.txt -a -e 2
echo 4
python simulator.py -f out.txt -a -e 4
echo 8
python simulator.py -f out.txt -a -e 8
echo 16
python simulator.py -f out.txt -a -e 16

echo "Grouping 2"
python programs/gentests.py -r 16 -i 64 -g 2
echo 1
python simulator.py -f out.txt -a -e 1
echo 2
python simulator.py -f out.txt -a -e 2
echo 4
python simulator.py -f out.txt -a -e 4
echo 8
python simulator.py -f out.txt -a -e 8
echo 16
python simulator.py -f out.txt -a -e 16

echo "Grouping 4"
python programs/gentests.py -r 16 -i 64 -g 4
echo 1
python simulator.py -f out.txt -a -e 1
echo 2
python simulator.py -f out.txt -a -e 2
echo 4
python simulator.py -f out.txt -a -e 4
echo 8
python simulator.py -f out.txt -a -e 8
echo 16
python simulator.py -f out.txt -a -e 16

echo "Grouping 8"
python programs/gentests.py -r 16 -i 64 -g 8
echo 1
python simulator.py -f out.txt -a -e 1
echo 2
python simulator.py -f out.txt -a -e 2
echo 4
python simulator.py -f out.txt -a -e 4
echo 8
python simulator.py -f out.txt -a -e 8
echo 16
python simulator.py -f out.txt -a -e 16

echo "Grouping 16"
python programs/gentests.py -r 16 -i 64 -g 16
echo 1
python simulator.py -f out.txt -a -e 1
echo 2
python simulator.py -f out.txt -a -e 2
echo 4
python simulator.py -f out.txt -a -e 4
echo 8
python simulator.py -f out.txt -a -e 8
echo 16
python simulator.py -f out.txt -a -e 16

echo "Grouping 32"
python programs/gentests.py -r 16 -i 64 -g 32
echo 1
python simulator.py -f out.txt -a -e 1
echo 2
python simulator.py -f out.txt -a -e 2
echo 4
python simulator.py -f out.txt -a -e 4
echo 8
python simulator.py -f out.txt -a -e 8
echo 16
python simulator.py -f out.txt -a -e 16

