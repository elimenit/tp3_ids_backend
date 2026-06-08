#!/bin/bash

inicializar_tecnologias() {
    sudo apt update && sudo apt upgrade -y
    sudo apt install -y python3 python3-pip
    sudo apt install -y docker.io docker-compose

    echo "Setup completo ..."
}

configuracion_punto_env() {

    echo -ne "MYSQL_USER='root'\nMYSQL_NAME_DB='restaurant'\nMYSQL_PASSWORD='userpass'\nMYSQL_HOST='db'\n" > .env
    echo -ne "MYSQL_PORT=3306\nFLASK_HOST='0.0.0.0'\nFLASK_PORT=15000\n" >> .env 
    echo -ne "SECRET_KEY='Clave_super_secreta_de_flask_seguridad'\n" >> .env
    echo "[+] Archivo .env creado"
}

correr_dockerfile() {
    docker build --load -t tp3_backend .
    docker run --name tp3_backend -p 15000:15000 tp3_backend
    docker container rm tp3_backend
    docker image rm tp3_backend
}
correr_docker_compose () {
    echo "Construiendo Contenedores"
    docker compose up --build
    echo "Contenedores construidos.., Vamos a colocarlos en espera de 100 segundos!."
    sleep 100
    echo "Eliminando contenedores"
    docker compose down
    echo "Contenedores eliminados"
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
    correr_docker_compose
}

main