#!/bin/bash

# Enumera las unidades de disco del sistema
echo "Unidades de disco del sistema:"
df -h

# Muestra el espacio libre en cada unidad de disco
echo "Espacio libre en cada unidad de disco:"
df -h --output=source,size,used,avail,pct

# Muestra el espacio libre en formato más legible
echo "Espacio libre en formato más legible:"
lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT,USED,AVAIL,USE%

