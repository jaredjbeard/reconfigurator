#!/bin/bash

read -p "Would you like to add command line interface? [y/n]: " add_cli

if [[ $add_cli == "Y" || $add_cli == "y" ]]; then

    parent=$(dirname $(dirname $(realpath $0)))

    mkdir bin

    chmod +x reconfigurator/reconfigurator.py
    ln -s ../reconfigurator/reconfigurator.py bin/reconfigurator
    
    export_path='export PATH="$PATH:$parent/../bin/"'
    echo $export_path >> ~/.bashrc
    source ~/.bashrc

    echo "Reconfigurator CLI added!"
else
    echo "Reconfigurator CLI not added."
fi


