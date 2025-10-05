#!/bin/bash

echo "======================================"
echo "  INFORMACIÓN DEL SISTEMA LINUX"
echo "======================================"
echo ""

# Detectar distribución Linux
echo "📦 DISTRIBUCIÓN:"
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "   Nombre: $NAME"
    echo "   Versión: $VERSION"
    echo "   ID: $ID"
elif [ -f /etc/lsb-release ]; then
    . /etc/lsb-release
    echo "   $DISTRIB_DESCRIPTION"
else
    echo "   $(uname -s) $(uname -r)"
fi

echo ""

# Detectar entorno de escritorio
echo "🖥️  ENTORNO DE ESCRITORIO:"

if [ -n "$XDG_CURRENT_DESKTOP" ]; then
    echo "   $XDG_CURRENT_DESKTOP"
elif [ -n "$DESKTOP_SESSION" ]; then
    echo "   $DESKTOP_SESSION"
elif [ -n "$GDMSESSION" ]; then
    echo "   $GDMSESSION"
else
    # Intentar detectar por procesos en ejecución
    if pgrep -x "gnome-shell" > /dev/null; then
        echo "   GNOME"
    elif pgrep -x "kwin" > /dev/null; then
        echo "   KDE Plasma"
    elif pgrep -x "xfce4-session" > /dev/null; then
        echo "   XFCE"
    elif pgrep -x "mate-session" > /dev/null; then
        echo "   MATE"
    elif pgrep -x "cinnamon" > /dev/null; then
        echo "   Cinnamon"
    elif pgrep -x "lxsession" > /dev/null; then
        echo "   LXDE"
    elif pgrep -x "i3" > /dev/null; then
        echo "   i3"
    else
        echo "   No detectado o modo terminal"
    fi
fi

echo ""
echo "======================================"