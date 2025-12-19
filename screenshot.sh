
#!/bin/zsh

source ~/.zprofile

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Run the python script
python3 "$SCRIPT_DIR/main.py"
