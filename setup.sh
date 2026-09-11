mkdir -p ~/.streamlit/

echo "\
[theme]\n\
base=\"dark\"\n\
primaryColor=\"#818cf8\"\n\
backgroundColor=\"#0f172a\"\n\
secondaryBackgroundColor=\"#1e293b\"\n\
textColor=\"#f8fafc\"\n\
font=\"sans serif\"\n\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
" > ~/.streamlit/config.toml
