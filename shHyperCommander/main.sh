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

list_fldr(){
    local arr=(*)
    for item in "${arr[@]}"; do
      if [[ -f "$item" ]]; then
        echo "F $item"
      elif [[ -d "$item" ]]; then
        echo "D $item"
      fi
      # echo "do another thing"
    done
}


display_file_menu(){
local menu="
---------------------------------------------------
| 0 Main menu | 'up' To parent | 'name' To select |
---------------------------------------------------"
    local first=""
    local rest

    while true; do
        echo "The list of files and directories:"
        # find -type f -printf "F %f\n" -o -type d -printf "D %f\n" 
        list_fldr
        echo -e "$menu"
        # escape_char=$(printf "\u1b")
        # read -rsn1 first # get 1 character
        # if [[ $first == $(printf "\u1b") ]]; then
        #     read -rsn2 rest # read 2 more chars
        #     if [[ $rest == "[A" ]]; then
        #         echo "Not implemented!"
        #     else
        #         echo "Invalid input!"
        #     fi
        # elif [[ $first == '0' ]]; then 
        #     break
        read -r rest
        if [ $rest = '0' ]; then 
            break
        elif [ $rest = 'up' ]; then
            cd ..
        else
            # read -r rest
            local search_term="$first$rest"
            if [ -f "$search_term" ]; then
                echo "Not implemented!"
            elif [ -d "$search_term" ]; then
                cd "$search_term"
            else
                echo "Invalid input!"
            fi
        fi
    done
}

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

stage3(){
    while true; do
        echo -e "$menu"
        read -r opt
        if [ $opt -eq 0 ]; then # Exit
            echo "Farewell!"
            break
        elif [ $opt -eq 1 ]; then # OS info
            uname -no
        elif [ $opt -eq 2 ]; then # User info
            whoami
        elif [ $opt -eq 3 ]; then # File and Dir operations
            display_file_menu
        elif [ $opt -eq 4 ]; then # Find Executables
            echo "Not implemented!"
        else
            echo "Invalid option!"
        fi
    done
}

echo "Hello $USER!"
# stage3
# display_file_menu

