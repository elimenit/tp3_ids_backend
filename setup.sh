#!/bin/bash

inicializar_tecnologias() {
    sudo apt update && sudo apt upgrade -y

    sudo apt install -y mysql-server
    sudo apt install -y python3 python3-pip
    sudo apt install -y docker.io docker-compose

    echo "Setup completo ..."
    sleep 2
}

configuracion_punto_env() {

    echo -ne "MYSQL_USER='root'\nMYSQL_NAME_DB='techlibre'\nMYSQL_PASSWORD='password'\nMYSQL_PORT=3306\nMYSQL_HOST='127.0.0.1'\nFLASK_HOST='127.0.0.1'\nFLASK_PORT=5000" > .env

    echo "[+] Archivo .env creado"
}

correr_aplicacion_backend() {
    if [[ ! -d ".venv" ]]; then
        python3 -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt
    fi
    if [[ -f "app.py" ]]; then
        python3 -m app
    else
        echo "[-] No existe app.py"
        exit 1
    fi
}

salir_error() {

    if [[ $? -ne 0 ]]; then
        echo "[-] El comando anterior falló ..."
        exit 1
    fi
}

main() {

    echo "Actualizando e instalando servicios necesarios ..."
    #inicializar_tecnologias
    salir_error

    NAME_DB="root"
    PASSWORD_DB="password"

    echo "Iniciando configuración de credenciales ..."
    #credenciales_base_datos "$NAME_DB" "$PASSWORD_DB"
    #salir_error

    echo "Actualización del archivo .env ..."
    configuracion_punto_env
    salir_error

    echo "Corriendo aplicación backend ..."
    correr_aplicacion_backend
}

main