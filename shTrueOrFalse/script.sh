#!/usr/bin/env bash

url="http://127.0.0.1:8000/"

menu="
0. Exit
1. Play a game
2. Display scores
3. Reset scores
Enter an option:"

login(){
    # Description: Downloads ID_card file from api, uses that to create auth cookie
    curl -s -o ID_card.txt $url"download/file.txt"
    local username=$(cut ID_card.txt -d'"' -f4)
    local password=$(cut ID_card.txt -d'"' -f8)
    curl -s -c cookie.txt -u $username:$password $url"login"
}

stage1(){
    curl -s -o ID_card.txt $url"download/file.txt"
    cat ID_card.txt
}

stage2(){
    echo "Login message: $(login)"
}

stage3(){
    echo "Login message: $(login)"
    response=$(curl -s --cookie cookie.txt $url"game")
    echo "Response: $response"
}

stage4(){
    while true; do
        echo -e "$menu"
        read -r opt
        if [ $opt -eq 0 ]; then
            echo "See you later!"
            break
        elif [ $opt -eq 1 ]; then
            echo "Playing game"
        elif [ $opt -eq 2 ]; then
            echo "Displaying scores"
        elif [ $opt -eq 3 ]; then
            echo "Resetting scores"
        else
            echo "Invalid option!"
        fi
    done
}

stage5(){
    while true; do
        echo -e "$menu"
        read -r opt
        if [ $opt -eq 0 ]; then # -------------------- Exit
            echo "See you later!"
            break
        elif [ $opt -eq 1 ]; then # ------------------ Play game
            RANDOM=4096
            local correct=("Perfect!" "Awesome!" "You are a genius!" "Wow!" "Wonderful!")
            local correct_count=0

            echo "What is your name?"
            local usr_name="Kevin"
            read -r usr_name

            login

            while true; do
                local res=$(curl -s --cookie cookie.txt $url"game")
                local qst=$(echo "$res" | cut -d'"' -f4)
                local ans=$(echo "$res" | cut -d'"' -f8)
    
                echo -e "$qst"
                echo "True or False?"
                local usr_ans
                read -r usr_ans
                if [ $usr_ans = $ans ]; then   
                    echo "${correct[$((RANDOM % 5))]}"
                    (( correct_count += 1 ))
                else
                    echo "Wrong answer, sorry!"
                    echo "$usr_name you have $correct_count correct answer(s)."
                    echo "Your score is $(($correct_count*10)) points."
                    break
                fi
            done

        elif [ $opt -eq 2 ]; then # ------------------ Display scores
            echo "Displaying scores"
        
        elif [ $opt -eq 3 ]; then # ------------------ Reset scores
            echo "Resetting scores"
        
        else
            echo "Invalid option!"
        fi
    done
}

stage6(){
    while true; do
        echo -e "$menu"
        read -r opt

        if [ $opt -eq 0 ]; then # -------------------- Exit
            echo "See you later!"
            break

        elif [ $opt -eq 1 ]; then # ------------------ Play game
            RANDOM=4096
            local correct=("Perfect!" "Awesome!" "You are a genius!" "Wow!" "Wonderful!")
            local correct_count=0

            echo "What is your name?"
            local usr_name="Kevin"
            read -r usr_name

            login

            while true; do
                local res=$(curl -s --cookie cookie.txt $url"game")
                local qst=$(echo "$res" | cut -d'"' -f4)
                local ans=$(echo "$res" | cut -d'"' -f8)

                echo -e "$qst"
                echo "True or False?"
                local usr_ans
                read -r usr_ans
                if [ $usr_ans = $ans ]; then   
                    echo "${correct[$((RANDOM % 5))]}"
                    (( correct_count += 1 ))
                else
                    echo "Wrong answer, sorry!"
                    echo "$usr_name you have $correct_count correct answer(s)."
                    echo "Your score is $(($correct_count*10)) points."

                    # append to scores.txt, create file if not exists
                    echo "User: $usr_name, Score: $(($correct_count*10)), Date: $(date +'%F')" >> scores.txt
                    break
                fi
            done

        elif [ $opt -eq 2 ]; then # ------------------ Display scores
            if [ -e scores.txt ]; then
                echo "Player scores"
                cat scores.txt
            else
                echo "File not found or no scores in it!"
            fi

        elif [ $opt -eq 3 ]; then # ------------------ Reset scores
            if [ -e scores.txt ]; then
                rm scores.txt
                echo "File deleted successfully!"
            else
                echo "File not found or no scores in it!"
            fi

        else
            echo "Invalid option!"
        fi
    done
}

echo "Welcome to the True or False Game!"
stage6
