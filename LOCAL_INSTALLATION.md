# Local Installation Guide for ibus-buuz

This document explains how to install ibus-buuz locally for the current user without requiring root privileges.

## File Organization

The installation process places files in the following locations:

- `~/.local/bin/ibus-buuz` - Shell script wrapper that launches the Python application
- `~/.local/share/ibus-buuz/*.py` - Python application files
- `~/.local/share/ibus-buuz/icons/buuz.png` - Icon file
- `~/.local/share/ibus/component/buuz.xml` - IBus component file

## Installation Instructions

1. Make sure you have Python 3 installed on your system.

2. Clone the repository or download the source code:
   ```
   git clone https://github.com/odbayar/ibus-buuz.git
   cd ibus-buuz
   ```

3. Run the installation script:
   ```
   python3 setup.py install
   ```

4. Restart IBus to pick up the new component:
   ```
   ibus restart
   ```

5. Enable the Buuz input method in IBus preferences:
   - Open IBus Preferences
   - Go to the Input Method tab
   - Click the Add button
   - Select Mongolian from the language list
   - Select Buuz from the input method list
   - Click Add

## Troubleshooting

If you encounter any issues during installation:

1. Make sure the `~/.local/bin` directory is in your PATH. You can add it by adding the following line to your `~/.bashrc` or `~/.zshrc` file:
   ```
   export PATH="$HOME/.local/bin:$PATH"
   ```

2. If IBus doesn't detect the new input method after restarting, try restarting your session or computer.

3. Check if all required files were copied correctly:
   ```
   ls -la ~/.local/bin/ibus-buuz
   ls -la ~/.local/share/ibus-buuz/*.py
   ls -la ~/.local/share/ibus-buuz/icons/buuz.png
   ls -la ~/.local/share/ibus/component/buuz.xml
   ```

## Uninstallation

To uninstall ibus-buuz, simply remove the installed files:
```
rm -f ~/.local/bin/ibus-buuz
rm -rf ~/.local/share/ibus-buuz
rm -f ~/.local/share/ibus/component/buuz.xml
ibus restart
```
