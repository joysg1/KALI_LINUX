#!/bin/bash

# Solicitar el nombre del archivo
read -p "Ingrese el nombre del archivo: " archivo

# Obtener la ruta del script
ruta_script=$(dirname "$0")

# Construir la ruta completa del archivo
archivo_completo="$ruta_script/$archivo"

# Verificar que el archivo existe
if [ ! -f "$archivo_completo" ]; then
    echo "Error: El archivo '$archivo' no existe en la ruta del script"
    exit 1
fi

echo ""
echo "Calculando hashes para: $archivo"
echo "========================================="

# Lista de algoritmos hash comunes
algoritmos=(
    "md5sum"
    "sha1sum"
    "sha224sum"
    "sha256sum"
    "sha384sum"
    "sha512sum"
    "b2sum"
)

# Calcular cada hash disponible
for cmd in "${algoritmos[@]}"; do
    if command -v $cmd &> /dev/null; then
        echo ""
        echo "$cmd:"
        $cmd "$archivo_completo" | awk '{print $1}'
    fi
done

# CRC32 (si está disponible cksum)
if command -v cksum &> /dev/null; then
    echo ""
    echo "CRC32 (cksum):"
    cksum "$archivo_completo"
fi

# Algoritmos adicionales con openssl (si está disponible)
if command -v openssl &> /dev/null; then
    echo ""
    echo "Hashes adicionales con OpenSSL:"
    echo "--------------------------------"
    
    openssl_algos=("md4" "ripemd160" "whirlpool" "sm3")
    
    for algo in "${openssl_algos[@]}"; do
        if openssl dgst -$algo "$archivo_completo" 2>/dev/null; then
            true
        fi
    done
fi

echo ""
echo "========================================="