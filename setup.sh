#!/bin/bash

export option=$1

inicializar_tecnologias() {
    sudo apt update && sudo apt upgrade -y
    sudo apt install -y python3 python3-pip
    sudo apt install -y docker.io docker-compose

    echo "Setup completo ..."
}

configuracion_punto_env_docker() {

    echo -ne "MYSQL_USER='root'\nMYSQL_NAME_DB='restaurant'\nMYSQL_PASSWORD='userpass'\nMYSQL_HOST='db'\n" > .env
    echo -ne "MYSQL_PORT=3306\nFLASK_HOST='0.0.0.0'\nFLASK_PORT=15000\n" >> .env 
    echo -ne "SECRET_KEY='Clave_super_secreta_de_flask_seguridad'\n" >> .env
    echo -ne "EMAIL_PASS='vwfn zvuq oeem csyu'\nEMAIL_USER='restaurante.tp.uba.grupo53@gmail.com'\n" >> .env
    echo -ne "API_URL='http://127.0.0.1:15000'" >> .env
    echo "[+] Archivo .env creado"
}
setting_env() {
    echo -ne "MYSQL_USER='root'\nMYSQL_NAME_DB='restaurant'\nMYSQL_PASSWORD='password'\nMYSQL_HOST='localhost'\n" > .env
    echo -ne "MYSQL_PORT=3306\nFLASK_HOST='0.0.0.0'\nFLASK_PORT=15000\n" >> .env 
    echo -ne "SECRET_KEY='Clave_super_secreta_de_flask_seguridad'\n" >> .env
    echo "[+] Archivo .env creado"
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
correr_solo_aplicacion() {
    if [[ ! -d ".venv" ]]; then
        python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip3 install -r requirements.txt --resume-retries=20
    if [[ -f "app.py" ]]; then 
        python3 -m app 
    else
        echo "No existe el archivo app.py !!!"
        exit 0
    fi
}
salir_error() {

    if [[ $? -ne 0 ]]; then
        echo "[-] El comando anterior falló ..."
        exit 1
    fi
}
menu() {
    echo "1) Correr aplicacion de flask app.py "
    echo "2) Correr Docker compose"
    echo "3) Salir"
}
ejecutar_opcion() {
    option=$1
    if [[ $option -eq 1 ]]; then
        setting_env
        echo "Corriendo Aplicacion, Agrega Datos (python3 cargar_datos.py)"
        correr_solo_aplicacion
    elif [[ $option -eq 2 ]]; then
        echo "Actualización del archivo .env ..."
        configuracion_punto_env_docker
        echo "Corriendo aplicación backend ..."
        correr_docker_compose
    elif [[ $option -eq 3 ]]; then
        echo "Saliendo del script "
        exit 0
    else
        echo "opcion No valida"
    fi
}
main() {
    
    echo "Actualizando e instalando servicios necesarios ..."
    #inicializar_tecnologias
    salir_error

    if [[ ! $option ]]; then
        menu
        read -p "Ingres una Opcion: " option
    fi
    ejecutar_opcion $option
    
    
}

main