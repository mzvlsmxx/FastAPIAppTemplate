
menu() {
    local CONFIG_FILE="batch-config.ini"
    local COMPOSE_FILE_PATH
    local APP_CONTAINER_NAME APP_SERVICE_NAME APP_LOG_PATH
    local REDIS_SERVICE_NAME
    local BROKER_CONTAINER_NAME BROKER_SERVICE_NAME BROKER_HOST BROKER_PORT
    local BROKER_DEPS_CONTAINER_NAME BROKER_DEPS_SERVICE_NAME
    local MYSQL_CONTAINER_NAME MYSQL_SERVICE_NAME MYSQL_HOST MYSQL_PORT MYSQL_USER choice

    if [[ ! -f "$CONFIG_FILE" ]]; then
        cat > "$CONFIG_FILE" << 'ENDCFG'
COMPOSE_FILE_PATH=
APP_CONTAINER_NAME=
APP_SERVICE_NAME=
APP_LOG_PATH=
REDIS_SERVICE_NAME=
BROKER_CONTAINER_NAME=
BROKER_SERVICE_NAME=
BROKER_DEPS_CONTAINER_NAME=
BROKER_DEPS_SERVICE_NAME=
BROKER_HOST=
BROKER_PORT=
MYSQL_CONTAINER_NAME=
MYSQL_SERVICE_NAME=
MYSQL_HOST=
MYSQL_PORT=
MYSQL_USER=
ENDCFG

        echo "Created new config file: $CONFIG_FILE"
        echo "Fulfill the config file with values, then restart the script."
        read -p "Press enter to exit..."
        return 1
    else
        while IFS='=' read -r key value; do
            [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue
            printf -v "$key" "%s" "$value"
        done < "$CONFIG_FILE"
    fi

    while true; do
        clear
        echo "+----------------------------+------< Whole System >------+----------------------------+"
        echo "| 1. Rebuild and Up detached | 4. Stop                    | 6. Show All Logs           |"
        echo "| 2. Up detached             | 5. Down                    |                            |"
        echo "| 3. Start                   |                            |                            |"
        echo "+----------------------------+-----------< App >----------+----------------------------+"
        echo "| 7. Rebuild and Up detached | 10. Stop                   | 12. Show Logs              |"
        echo "| 8. Up detached             | 11. Down                   | 13. Show App Logs          |"
        echo "| 9. Start                   |                            | 14. Enter Shell            |"
        echo "+----------------------------+--------< Database >--------+----------------------------+"
        echo "| 15. Up detached            | 17. Stop                   | 19. Show All Logs          |"
        echo "| 16. Start                  | 18. Down                   | 20. Enter MySQL Shell      |"
        echo "|                            |                            | 21. Enter Redis Shell      |"
        echo "+----------------------------+---------< Broker >---------+----------------------------+"
        echo "| 22. Up detached            | 24. Stop                   | 26. Show Logs              |"
        echo "| 23. Start                  | 25. Down                   | 27. Enter Shell            |"
        echo "+----------------------------+----------------------------+----------------------------+"
        echo "|                                                                                      |"
        echo "+-----------------------------------< 28. Status All >---------------------------------+"
        echo "|                                                                                      |"
        echo "+--------------------------------------< 0. Exit >-------------------------------------+"
        
        read -p "Choice (0-28) >> " choice

        clear

        case $choice in
            1) docker compose -f "$COMPOSE_FILE_PATH" up -d --build && docker image prune -f ;;
            2) docker compose -f "$COMPOSE_FILE_PATH" up -d ;;
            3) docker compose -f "$COMPOSE_FILE_PATH" start ;;
            4) docker compose -f "$COMPOSE_FILE_PATH" stop ;;
            5) docker compose -f "$COMPOSE_FILE_PATH" down ;;
            6) echo "< APP LOGS >" && docker logs "$APP_CONTAINER_NAME" && echo "< APP LOGS >"
               prompt_continue
               echo "< MYSQL LOGS >" && docker logs "$MYSQL_CONTAINER_NAME" && echo "< MYSQL LOGS >"
               prompt_continue
               echo "< REDIS LOGS >" && docker logs "$REDIS_CONTAINER_NAME" && echo "< REDIS LOGS >"
               prompt_continue
               echo "< BROKER LOGS >" && docker logs "$BROKER_CONTAINER_NAME" && echo "< BROKER LOGS >" ;;
            7) docker compose -f "$COMPOSE_FILE_PATH" up -d --no-deps --build "$APP_SERVICE_NAME" && docker image prune -f > /dev/null ;;
            8) docker compose -f "$COMPOSE_FILE_PATH" up -d ;;
            9) docker compose -f "$COMPOSE_FILE_PATH" start "$APP_SERVICE_NAME" ;;
            10) docker compose -f "$COMPOSE_FILE_PATH" stop "$APP_SERVICE_NAME" ;; 
            11) docker compose -f "$COMPOSE_FILE_PATH" down "$APP_SERVICE_NAME" ;;
            12) echo "< APP LOGS >" && docker logs "$APP_CONTAINER_NAME" && echo "< APP LOGS >" ;;
            13) echo "TODO show app internal logs";;
            14) docker exec -it "$APP_CONTAINER_NAME" sh ;;
            15) docker compose -f "$COMPOSE_FILE_PATH" up -d "$REDIS_SERVICE_NAME" "$MYSQL_SERVICE_NAME" ;;
            16) docker compose -f "$COMPOSE_FILE_PATH" start "$REDIS_SERVICE_NAME" "$MYSQL_SERVICE_NAME" ;;
            17) docker compose -f "$COMPOSE_FILE_PATH" stop "$REDIS_SERVICE_NAME" "$MYSQL_SERVICE_NAME" ;;
            18) docker compose -f "$COMPOSE_FILE_PATH" down "$REDIS_SERVICE_NAME" "$MYSQL_SERVICE_NAME" ;;
            19) echo "< MYSQL LOGS >" && docker logs "$MYSQL_CONTAINER_NAME" && echo "< MYSQL LOGS >"
                prompt_continue
                echo "< REDIS LOGS >" && docker logs "$REDIS_CONTAINER_NAME" && echo "< REDIS LOGS >" ;;
            20) docker exec -it "$MYSQL_CONTAINER_NAME" mysql -h "$MYSQL_HOST" -u "$MYSQL_USER" --port "$MYSQL_PORT" -p && break ;;
            21) docker exec -it "$REDIS_CONTAINER_NAME" redis-cli && break ;;
            22) docker compose -f "$COMPOSE_FILE_PATH" up -d "$BROKER_SERVICE_NAME" "$BROKER_DEPS_SERVICE_NAME" ;;
            23) docker compose -f "$COMPOSE_FILE_PATH" start "$BROKER_SERVICE_NAME" "$BROKER_DEPS_SERVICE_NAME" ;;
            24) docker compose -f "$COMPOSE_FILE_PATH" stop "$BROKER_SERVICE_NAME" "$BROKER_DEPS_SERVICE_NAME" ;;
            25) docker compose -f "$COMPOSE_FILE_PATH" down "$BROKER_SERVICE_NAME" "$BROKER_DEPS_SERVICE_NAME" ;;
            26) echo "< BROKER LOGS >" && docker logs "$BROKER_CONTAINER_NAME" && echo "< BROKER LOGS >" ;;
            27) docker exec -it "$BROKER_CONTAINER_NAME" /bin/bash && break ;;
            28) echo "< IMAGES >" && docker image ls && echo "< IMAGES >"
                prompt_continue
                echo "< CONTAINERS >" && docker ps -a && echo "< CONTAINERS >"
                prompt_continue
                echo "< NETWORKS >" && docker ps -a && echo "< NETWORKS >" ;;
            0) break ;;
            *) ;;
        esac
        read -p "Press any key to continue..."
    done
}

prompt_continue () {
    read -p "Press any key to continue..."
    clear
}

menu
