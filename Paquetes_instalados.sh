#!/bin/bash

# Verificar paquetes instalados en Debian
if [ -x "$(command -v dpkg)" ]; then
  echo "Paquetes instalados en Debian/Ubuntu:"
  dpkg --list
fi

# Verificar paquetes instalados en Red Hat
if [ -x "$(command -v rpm)" ]; then
  echo "Paquetes instalados en Red Hat/Fedora/CentOS:"
  rpm -qa
fi

# Verificar paquetes instalados en Arch Linux
if [ -x "$(command -v pacman)" ]; then
  echo "Paquetes instalados en Arch Linux/Manjaro:"
  pacman -Q
fi
