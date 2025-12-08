@echo off
setlocal

set "CONFIG_FILE=batch-config.ini"
if not exist "%CONFIG_FILE%" (
    echo COMPOSE_FILE_PATH=>>batch-config.ini
    echo APP_CONTAINER_NAME=>>batch-config.ini
    echo APP_SERVICE_NAME=>>batch-config.ini
    echo APP_LOG_PATH=>>batch-config.ini
    echo REDIS_SERVICE_NAME=>>batch-config.ini
    echo BROKER_CONTAINER_NAME=>>batch-config.ini
    echo BROKER_SERVICE_NAME=>>batch-config.ini
    echo BROKER_DEPS_CONTAINER_NAME=>>batch-config.ini
    echo BROKER_DEPS_SERVICE_NAME=>>batch-config.ini
    echo BROKER_HOST=>>batch-config.ini
    echo BROKER_PORT=>>batch-config.ini
    echo MYSQL_CONTAINER_NAME=>>batch-config.ini
    echo MYSQL_SERVICE_NAME=>>batch-config.ini
    echo MYSQL_HOST=>>batch-config.ini
    echo MYSQL_PORT=>>batch-config.ini
    echo MYSQL_USER=>>batch-config.ini
    echo Created new config file: batch-config.ini
    echo Fullfill the config file with values for the correct script execution
    pause
    exit /b
) else (
    for /f "tokens=1* delims==" %%a in ('findstr /v /b /c:"#" /c:" " "%CONFIG_FILE%"') do (
        set "%%a=%%b"
    )
)

:menu
echo.
echo +----------------------------+------^< Whole System ^>------+----------------------------+
echo ^| 1. Rebuild and Up detached ^| 4. Stop                    ^| 6. Show All Logs           ^|
echo ^| 2. Up detached             ^| 5. Down                    ^|                            ^|
echo ^| 3. ^Start                   ^|                            ^|                            ^|
echo +----------------------------+-----------^< App ^>----------+----------------------------+
echo ^| 7. Rebuild and Up detached ^| 10. Stop                   ^| 12. Show Logs              ^|
echo ^| 8. Up detached             ^| 11. Down                   ^| 13. Show App Logs          ^|
echo ^| 9. ^Start                   ^|                            ^| 14. Enter Shell            ^|
echo +----------------------------+--------^< Database ^>--------+----------------------------+
echo ^| 15. Up detached            ^| 17. Stop                   ^| 19. Show All Logs          ^|
echo ^| 16. ^Start                  ^| 18. Down                   ^| 20. Enter MySQL Shell      ^|
echo ^|                            ^|                            ^| 21. Enter Redis Shell      ^|
echo +----------------------------+---------^< Broker ^>---------+----------------------------+
echo ^| 22. Up detached            ^| 24. Stop                   ^| 26. Show Logs              ^|
echo ^| 23. ^Start                  ^| 25. Down                   ^| 27. Enter Shell            ^|
echo +----------------------------+----------------------------+----------------------------+
echo ^|                                                                                      ^|
echo +-----------------------------------^< 28. ^Status All ^>---------------------------------+
echo ^|                                                                                      ^|
echo +--------------------------------------^< 0. ^Exit ^>-------------------------------------+
echo.
set /p choice="Choice (0-28) >> "

cls
if "%choice%"=="1" goto system_up_detached_rebuild
if "%choice%"=="2" goto system_up_detached
if "%choice%"=="3" goto system_start
if "%choice%"=="4" goto system_stop
if "%choice%"=="5" goto system_down
if "%choice%"=="6" goto system_logs_all
if "%choice%"=="7" goto app_up_detached_rebuild
if "%choice%"=="8" goto app_up_detached
if "%choice%"=="9" goto app_start
if "%choice%"=="10" goto app_stop
if "%choice%"=="11" goto app_down
if "%choice%"=="12" goto app_logs
if "%choice%"=="13" goto app_internal_logs
if "%choice%"=="14" goto app_shell
if "%choice%"=="15" goto db_up_detached
if "%choice%"=="16" goto db_start
if "%choice%"=="17" goto db_stop
if "%choice%"=="18" goto db_down
if "%choice%"=="19" goto db_logs
if "%choice%"=="20" goto mysql_shell
if "%choice%"=="21" goto redis_shell
if "%choice%"=="22" goto broker_up_detached
if "%choice%"=="23" goto broker_start
if "%choice%"=="24" goto broker_stop
if "%choice%"=="25" goto broker_down
if "%choice%"=="26" goto broker_logs
if "%choice%"=="27" goto broker_shell
if "%choice%"=="28" goto status_all
if "%choice%"=="0" exit /b
goto menu

:system_up_detached
docker compose -f %COMPOSE_FILE_PATH% up -d
pause
cls
goto status_all

:system_up_detached_rebuild
docker compose -f %COMPOSE_FILE_PATH% up -d --build
docker image prune -f >nul
pause
cls
goto status_all

:system_start
docker compose -f %COMPOSE_FILE_PATH% ^start
pause
cls
goto status_all

:system_stop
docker compose -f %COMPOSE_FILE_PATH% stop
pause
cls
goto status_all

:system_down
docker compose -f %COMPOSE_FILE_PATH% down
pause
cls
goto status_all

:system_logs_all
echo.
echo -------------------^< APP LOGS ^>-----------------------
docker logs %APP_CONTAINER_NAME% 2>nul
echo -------------------^< APP LOGS ^>-----------------------
echo.
pause
cls
echo.
echo ------------------^< REDIS LOGS ^>----------------------
docker logs %REDIS_CONTAINER_NAME% 2>nul
echo ------------------^< REDIS LOGS ^>----------------------
echo.
pause
cls
echo.
echo ------------------^< MYSQL LOGS ^>----------------------
docker logs %MYSQL_CONTAINER_NAME% 2>nul
echo ------------------^< MYSQL LOGS ^>----------------------
echo.
pause
cls
echo.
echo -----------------^< BROKER LOGS ^>----------------------
docker logs %BROKER_CONTAINER_NAME% 2>nul
echo -----------------^< BROKER LOGS ^>----------------------
echo.
pause
cls
goto menu

:app_up_detached
docker compose -f %COMPOSE_FILE_PATH% up -d --no-deps %APP_SERVICE_NAME%
pause
cls
goto status_all

:app_up_detached_rebuild
docker compose -f %COMPOSE_FILE_PATH% up -d --no-deps --build %APP_SERVICE_NAME%
docker image prune -f >nul
pause
cls
goto status_all

:app_start
docker compose -f %COMPOSE_FILE_PATH% ^start %APP_SERVICE_NAME%
pause
cls
goto status_all

:app_stop
docker compose -f %COMPOSE_FILE_PATH% stop %APP_SERVICE_NAME%
pause
cls
goto status_all

:app_down
docker compose -f %COMPOSE_FILE_PATH% down %APP_SERVICE_NAME%
pause
cls
goto status_all

:app_shell
cls
docker exec -it %APP_CONTAINER_NAME% sh
exit /b

:app_logs
echo.
echo -------------------^< APP LOGS ^>-----------------------
docker logs %APP_CONTAINER_NAME% 2>nul
echo -------------------^< APP LOGS ^>-----------------------
echo.
pause
cls
goto menu

:app_internal_logs
for /f "tokens=* delims=\n" %%a in ('docker exec %APP_CONTAINER_NAME% ls %APP_LOG_PATH%') do (
    if /I "%%~xa"==".log" (
        echo.
        echo ^< %%a ^>
        docker exec %APP_CONTAINER_NAME% cat %APP_LOG_PATH%%%a 2>nul
        echo ^< %%a ^>
        echo.
        pause
        cls
    )
)
goto menu

:db_up_detached
docker compose -f %COMPOSE_FILE_PATH% up -d %REDIS_SERVICE_NAME% %MYSQL_SERVICE_NAME%
pause
cls
goto status_all

:db_start
docker compose -f %COMPOSE_FILE_PATH% ^start %REDIS_SERVICE_NAME% %MYSQL_SERVICE_NAME%
pause
cls
goto status_all

:db_stop
docker compose -f %COMPOSE_FILE_PATH% stop %REDIS_SERVICE_NAME% %MYSQL_SERVICE_NAME%
pause
cls
goto status_all

:db_down
docker compose -f %COMPOSE_FILE_PATH% down %REDIS_SERVICE_NAME% %MYSQL_SERVICE_NAME%
pause
cls
goto status_all

:mysql_shell
cls
docker exec -it %MYSQL_CONTAINER_NAME% mysql -h %MYSQL_HOST% -u %MYSQL_USER% --port %MYSQL_PORT% -p
exit /b

:redis_shell
cls
docker exec -it %REDIS_CONTAINER_NAME% redis-cli
exit /b

:db_logs
echo.
echo ------------------^< MYSQL LOGS ^>----------------------
docker logs %MYSQL_CONTAINER_NAME% 2>nul
echo ------------------^< MYSQL LOGS ^>----------------------
echo.
pause
cls
echo.
echo ------------------^< REDIS LOGS ^>----------------------
docker logs %REDIS_CONTAINER_NAME% 2>nul
echo ------------------^< REDIS LOGS ^>----------------------
echo.
pause
cls
goto menu

:broker_up_detached
docker compose -f %COMPOSE_FILE_PATH% up -d %BROKER_SERVICE_NAME% %BROKER_DEPS_SERVICE_NAME%
pause
cls
goto status_all

:broker_start
docker compose -f %COMPOSE_FILE_PATH% ^start %BROKER_SERVICE_NAME% %BROKER_DEPS_SERVICE_NAME%
pause
cls
goto status_all

:broker_stop
docker compose -f %COMPOSE_FILE_PATH% stop %BROKER_SERVICE_NAME% %BROKER_DEPS_SERVICE_NAME%
pause
cls
goto status_all

:broker_down
docker compose -f %COMPOSE_FILE_PATH% down %BROKER_SERVICE_NAME% %BROKER_DEPS_SERVICE_NAME%
pause
cls
goto status_all

:broker_logs
echo.
echo -----------------^< BROKER LOGS ^>----------------------
docker logs %BROKER_CONTAINER_NAME% 2>nul
echo -----------------^< BROKER LOGS ^>----------------------
echo.
pause
cls
goto menu

:broker_shell
docker exec -it %BROKER_CONTAINER_NAME% /bin/bash
exit /b

:status_all
echo.
echo --------------------^< IMAGES ^>------------------------
docker images
echo.
echo ------------------^< CONTAINERS ^>----------------------
docker ps -a
echo.
echo -------------------^< NETWORKS ^>-----------------------
docker network ls
echo.
pause
cls
goto menu

endlocal