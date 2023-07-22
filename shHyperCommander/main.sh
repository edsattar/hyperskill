#! /usr/bin/env bash

menu="
------------------------------
| Hyper Commander            |
| 0: Exit                    |
| 1: OS info                 |
| 2: User info               |
| 3: File and Dir operations |
| 4: Find Executables        |
------------------------------"

stage1(){
    while true; do
        echo -e "$menu"
        read -r opt
        if [ $opt -eq 0 ]; then
            echo "Farewell!"
            break
        elif [ $opt -eq 1 ]; then
            echo "Not implemented!"
        elif [ $opt -eq 2 ]; then
            echo "Not implemented!"
        elif [ $opt -eq 3 ]; then
            echo "Not implemented!"
        elif [ $opt -eq 4 ]; then
            echo "Not implemented!"
        else
            echo "Invalid option!"
        fi
    done
}

stage2(){
    while true; do
        echo -e "$menu"
        read -r opt
        if [ $opt -eq 0 ]; then
            echo "Farewell!"
            break
        elif [ $opt -eq 1 ]; then
            uname -no
        elif [ $opt -eq 2 ]; then
            whoami
        elif [ $opt -eq 3 ]; then
            echo "Not implemented!"
        elif [ $opt -eq 4 ]; then
            echo "Not implemented!"
        else
            echo "Invalid option!"
        fi
    done
}

echo "Hello $USER!"
stage2
