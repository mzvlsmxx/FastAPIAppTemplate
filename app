#!/bin/env bash

menu() {
    local CONFIG_FILE="batch-config.ini"
    local COMPOSE_FILE_PATH
    local APP_CONTAINER_NAME APP_SERVICE_NAME APP_LOG_PATH
    local REDIS_SERVICE_NAME
    local BROKER_CONTAINER_NAME BROKER_SERVICE_NAME BROKER_HOST BROKER_PORT
    local BROKER_DEPS_CONTAINER_NAME BROKER_DEPS_SERVICE_NAME
    local MYSQL_CONTAINER_NAME MYSQL_SERVICE_NAME MYSQL_HOST MYSQL_PORT MYSQL_USER choice

    if [[ ! -f "$CONFIG_FILE" ]]; then
        cat > "$CONFIG_FILE"  << 'ENDCFG'
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

    # 4. Menu Loop
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
        # ... (rest of menu UI)
        echo "+--------------------------------------< 0. Exit >-------------------------------------+"
        
        read -p "Choice (0-28) >> " choice

        case $choice in
            1) docker compose -f "$COMPOSE_FILE_PATH" up -d --build && docker image prune -f ;;
            2) docker compose -f "$COMPOSE_FILE_PATH" up -d ;;
            3) docker compose -f "$COMPOSE_FILE_PATH" start ;;
            4) docker compose -f "$COMPOSE_FILE_PATH" stop ;;
            5) docker compose -f "$COMPOSE_FILE_PATH" down ;;
            6) echo "--- APP LOGS ---"; docker logs "$APP_CONTAINER_NAME"
               read -p "Next..."
               echo "--- MYSQL LOGS ---"; docker logs "$MYSQL_CONTAINER_NAME"
               ;;
            14) docker exec -it "$APP_CONTAINER_NAME" sh ;;
            20) docker exec -it "$MYSQL_CONTAINER_NAME" mysql -h "$MYSQL_HOST" -u "$MYSQL_USER" -p ;;
            0) break ;;
            *) echo "Invalid option" ;;
        esac
        read -p "Press any key to continue..."
    done
}

menu
