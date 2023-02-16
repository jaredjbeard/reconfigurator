#!/bin/bash

parent=$(dirname $(dirname $(realpath $0)))

bin_loc=$parent/bin
if ! test -d "$bin_loc"; then
    mkdir $bin_loc
fi

chmod +x $parent/reconfigurator.py

save_loc=$parent/bin/reconfigurator
if test -f "$save_loc"; then
    rm "$save_loc"
fi
ln -s $parent/reconfigurator.py $save_loc
    
export_path='export PATH="$PATH:parent/bin/"'
export_path=${export_path/parent/$parent}

if grep -Fxq "$export_path" ~/.bashrc; then
    echo "Reconfigurator CLI Updated!"
    exit 0
fi
echo $export_path >> ~/.bashrc
source ~/.bashrc

echo "Reconfigurator CLI added!"