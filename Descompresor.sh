#!/bin/bash

# Solicitar el nombre del archivo
read -p "Ingrese el nombre del archivo comprimido: " ARCHIVO_COMPIMIDO

# Verificar si se proporcionó el nombre del archivo
if [ -z "$ARCHIVO_COMPIMIDO" ]; then
  echo "Debes proporcionar el nombre del archivo comprimido."
  exit 1
fi

# Verificar si el archivo existe
if [ ! -f "$ARCHIVO_COMPIMIDO" ]; then
  echo "El archivo $ARCHIVO_COMPIMIDO no existe."
  exit 1
fi

# Intentar descomprimir el archivo
echo "Intentando descomprimir $ARCHIVO_COMPIMIDO..."

# Comprobar la extensión del archivo
if [[ "$ARCHIVO_COMPIMIDO" =~ \.zip$ ]]; then
  # Descomprimir archivo zip
  unzip "$ARCHIVO_COMPIMIDO"
elif [[ "$ARCHIVO_COMPIMIDO" =~ \.tar\.gz$ ]] || [[ "$ARCHIVO_COMPIMIDO" =~ \.tgz$ ]]; then
  # Descomprimir archivo tar.gz
  tar -xzvf "$ARCHIVO_COMPIMIDO"
elif [[ "$ARCHIVO_COMPIMIDO" =~ \.tar$ ]]; then
  # Descomprimir archivo tar
  tar -xvf "$ARCHIVO_COMPIMIDO"
elif [[ "$ARCHIVO_COMPIMIDO" =~ \.gz$ ]]; then
  # Descomprimir archivo gzip
  gunzip "$ARCHIVO_COMPIMIDO"
elif [[ "$ARCHIVO_COMPIMIDO" =~ \.bz2$ ]]; then
  # Descomprimir archivo bzip2
  bunzip2 "$ARCHIVO_COMPIMIDO"
elif [[ "$ARCHIVO_COMPIMIDO" =~ \.xz$ ]]; then
  # Descomprimir archivo xz
  unxz "$ARCHIVO_COMPIMIDO"
else
  echo "No se reconoce la extensión del archivo $ARCHIVO_COMPIMIDO."
  exit 1
fi

echo "Descompresión exitosa."
