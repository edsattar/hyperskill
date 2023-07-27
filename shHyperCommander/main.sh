#! /usr/bin/env bash

file_opt_menu(){
local menu="
---------------------------------------------------------------------
| 0 Back | 1 Delete | 2 Rename | 3 Make writable | 4 Make read-only |
---------------------------------------------------------------------"
    while true; do
        echo -e "$menu"
        local opt
        read -r opt
        if [ $opt = "0" ]; then # back
            break
        elif [ $opt = "1" ]; then # delete
            rm $1
            echo "$1 has been deleted."
            break

        elif [ $opt = "2" ]; then # rename
            echo "Enter the new file name:"
            local new_name
            read -r new_name
            mv $1 $new_name
            echo "$1 has been renamed as $new_name"
            break

        elif [ $opt = "3" ]; then # make writable
            chmod 666 $1
            echo "Permissions have been updated."
            ls -l $1
            break

        elif [ $opt = "4" ]; then # make read-only
            chmod 664 $1
            echo "Permissions have been updated."
            ls -l $1
            break
        fi
    done
}

list_dir_contents(){
    local arr=(*)
    for item in "${arr[@]}"; do
      if [[ -f "$item" ]]; then
        echo "F $item"
      elif [[ -d "$item" ]]; then
        echo "D $item"
      fi
    done
}

directory_menu(){
local menu="
---------------------------------------------------
| 0 Main menu | 'up' To parent | 'name' To select |
---------------------------------------------------"
    local opt
    while true; do
        echo -e "\nThe list of files and directories:"
        list_dir_contents
        echo -e "$menu"
        read -r opt
        if [ $opt = '0' ]; then # main menu
            break
        elif [ $opt = 'up' ]; then # up one dir
            cd ..
        else # file options
            if [ -f "$opt" ]; then
                file_opt_menu $opt
            elif [ -d "$opt" ]; then
                cd "$opt"
            else
                echo "Invalid input!"
            fi
        fi
    done
}

stage6(){
menu="
------------------------------
| Hyper Commander            |
| 0: Exit                    |
| 1: OS info                 |
| 2: User info               |
| 3: File and Dir operations |
| 4: Find Executables        |
------------------------------"

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
            directory_menu
        elif [ $opt -eq 4 ]; then # Find Executables
            local executable
            local exe_location
            echo "Enter an executable name:"
            read -r executable
            exe_location=$(which $executable)
            local exit_status=$?
            if [ $exit_status = 1 ]; then # not found
                echo "The executable with that name does not exist!"
            elif [ $exit_status = 0 ]; then # found
                echo "Located in: $exe_location"
                local args
                echo "Enter arguments:"
                read -r args
                $executable $args
            fi
        else
            echo "Invalid option!"
        fi
    done
}

echo "Hello $USER!"
stage6

