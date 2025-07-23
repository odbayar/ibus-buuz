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

4. Enable the Buuz input method in IBus preferences:
   - Open IBus Preferences
   - Go to the Input Method tab
   - Click the Add button
   - Select Mongolian (Buuz) from the list
   - Click Add

## Troubleshooting

If you encounter any issues during installation:

1. If IBus doesn't detect the new input method after restarting, try restarting your session or computer.

2. Check if all required files were copied correctly:
   ```
   ls -la ~/.local/bin/ibus-buuz
   ls -la ~/.local/share/ibus-buuz/*.py
   ls -la ~/.local/share/ibus-buuz/icons/buuz.png
   ls -la ~/.local/share/ibus/component/buuz.xml
   ```

3. Check if IBus is properly configured to scan your local component directory:
   ```
   echo $IBUS_COMPONENT_PATH
   ```
   The output should include `~/.local/share/ibus/component`.

## Uninstallation

To uninstall ibus-buuz, simply remove the installed files:
```
rm -f ~/.local/bin/ibus-buuz
rm -rf ~/.local/share/ibus-buuz
rm -f ~/.local/share/ibus/component/buuz.xml
ibus restart
```
