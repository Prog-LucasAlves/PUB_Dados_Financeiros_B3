#!/bin/bash

mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"seu-email@dominio.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[theme]\n\
base='light'\n\
primaryColor='#000000'\n\
backgroundColor='#fbf6d0'\n\
secondaryBackgroundColor = '#9ccc65'\n\
textColor='#0e1862'\n\

[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml