#!/bin/bash
# Test script to verify local installation of ibus-buuz

echo "Testing local installation of ibus-buuz..."

# Run the installation
python3 setup.py install

# Check if directories were created
echo "Checking if directories were created..."
if [ -d ~/.local/bin ] && [ -d ~/.local/share/ibus-buuz ] && [ -d ~/.local/share/ibus-buuz/icons ] && [ -d ~/.local/share/ibus/component ]; then
    echo "✓ Directories created successfully"
else
    echo "✗ Directory creation failed"
    exit 1
fi

# Check if files were copied
echo "Checking if files were copied..."
if [ -f ~/.local/bin/ibus-buuz ] && \
   [ -f ~/.local/share/ibus-buuz/ibus-buuz.py ] && \
   [ -f ~/.local/share/ibus-buuz/engine.py ] && \
   [ -f ~/.local/share/ibus-buuz/composer.py ] && \
   [ -f ~/.local/share/ibus-buuz/icons/buuz.png ] && \
   [ -f ~/.local/share/ibus/component/buuz.xml ]; then
    echo "✓ Files copied successfully"
else
    echo "✗ File copying failed"
    ls -la ~/.local/bin/ibus-buuz
    ls -la ~/.local/share/ibus-buuz/
    ls -la ~/.local/share/ibus-buuz/icons/
    ls -la ~/.local/share/ibus/component/
    exit 1
fi

# Check if the script is executable
echo "Checking if ibus-buuz is executable..."
if [ -x ~/.local/bin/ibus-buuz ]; then
    echo "✓ ibus-buuz is executable"
else
    echo "✗ ibus-buuz is not executable"
    exit 1
fi

# Check if the shell script wrapper is correct
echo "Checking shell script wrapper content..."
if grep -q "exec python3.*ibus-buuz.py" ~/.local/bin/ibus-buuz; then
    echo "✓ Shell script wrapper content is correct"
else
    echo "✗ Shell script wrapper content is incorrect"
    cat ~/.local/bin/ibus-buuz
    exit 1
fi

# Check if buuz.xml references the correct executable
echo "Checking buuz.xml content..."
if grep -q "<exec>$HOME/.local/bin/ibus-buuz --ibus</exec>" ~/.local/share/ibus/component/buuz.xml; then
    echo "✓ buuz.xml references the correct executable"
else
    echo "✗ buuz.xml references the wrong executable"
    grep "<exec>" ~/.local/share/ibus/component/buuz.xml
    exit 1
fi

echo "Local installation test completed successfully!"
