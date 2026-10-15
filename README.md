# Buuz IBus IME

Buuz is an Input Method Engine (IME) for IBus that enables you to write in Mongolian Cyrillic using a Latin-based keyboard. For example, if you write "buuz id'ye", it will come out as "бууз идье".

This is a port of the [Buuz Windows IME](https://github.com/odbayar/buuz) to the Linux IBus framework.

## Requirements

- Linux with IBus framework
- Python 3.6 or higher
- IBus 1.5 or higher
- PyGObject (Python GObject Introspection)

## Installation

### Installing Dependencies

On Ubuntu/Debian systems:

```bash
sudo apt-get install python3-setuptools
```

On Fedora/RHEL systems:

```bash
sudo dnf install python3-setuptools
```

### Installing Buuz IBus IME

`setup.py` supports two install modes:

- System install (`--system`, available to all users) - recommended
- User install (default, current user only) - needs extra IBus setup, see below

User install places files in:

- `~/.local/bin/ibus-buuz` - Shell script wrapper that launches the Python application
- `~/.local/share/ibus-buuz/*.py` - Python application files
- `~/.local/share/ibus-buuz/icons/buuz.png` - Icon file
- `~/.local/share/ibus/component/buuz.xml` - IBus component file

System install places files in:

- `/usr/local/bin/ibus-buuz` - Shell script wrapper that launches the Python application
- `/usr/local/share/ibus-buuz/*.py` - Python application files
- `/usr/local/share/ibus-buuz/icons/buuz.png` - Icon file
- `/usr/share/ibus/component/buuz.xml` - IBus component file for all users

Follow these steps to install:

1. Clone this repository:

```bash
git clone https://github.com/odbayar/ibus-buuz.git
cd ibus-buuz
```

2. Install the IME for all users:

```bash
sudo python3 setup.py install --system
```

Or install it for your user only:

```bash
python3 setup.py install
```

IBus does not look in `~/.local/share/ibus/component` by default, so a user
install also needs `IBUS_COMPONENT_PATH` set in your session. Setting it
replaces the default directory, so list both. Add this line to
`~/.config/environment.d/ibus.conf` (with your home directory spelled out),
then log out and back in:

```
IBUS_COMPONENT_PATH=/usr/share/ibus/component:/home/you/.local/share/ibus/component
```

3. Restart IBus (if not already done by the installer):

```bash
ibus restart
```

For `--system` installs, this restart must be run in each user's session.

4. Enable the IME in IBus preferences:
   - Open IBus Preferences (from system settings or run `ibus-setup`)
   - Go to the "Input Method" tab
   - Click "Add" and select "Mongolian" from the language list
   - Select "Buuz" from the available input methods
   - Click "Add"

## Usage

Once installed and enabled, you can switch to the Buuz input method using your IBus keyboard shortcut (typically Super+Space or Ctrl+Space).

When the Buuz IME is active, you can type Latin characters and they will be automatically converted to Mongolian Cyrillic. The conversion follows the same rules as the original Buuz Windows IME.

### Basic Conversion Rules

| Latin | Cyrillic |
|-------|----------|
| a     | а        |
| b     | б        |
| v     | в        |
| g     | г        |
| d     | д        |
| ye    | е        |
| yo    | ё        |
| j     | ж        |
| z     | з        |
| i     | и        |
| i     | й        |
| k     | к        |
| l     | л        |
| m     | м        |
| n     | н        |
| o     | о        |
| o'    | ө        |
| p     | п        |
| r     | р        |
| s     | с        |
| t     | т        |
| u     | у        |
| u'    | ү        |
| f     | ф        |
| h     | х        |
| c     | ц        |
| ch    | ч        |
| sh    | ш        |
| sxc   | щ        |
| "     | ъ        |
| y     | ы        |
| '     | ь        |
| e     | э        |
| yu    | ю        |
| ya    | я        |

## Troubleshooting

If the IME doesn't appear in the IBus preferences:
- Make sure IBus is running (`ibus start`)
- Check if the component file was correctly installed:
  - User install: `ls ~/.local/share/ibus/component/buuz.xml`
  - System install: `ls /usr/share/ibus/component/buuz.xml`
- Check if the Python files were correctly installed:
  - User install: `ls ~/.local/share/ibus-buuz/*.py`
  - System install: `ls /usr/local/share/ibus-buuz/*.py`
- Check if the shell script wrapper was created:
  - User install: `ls ~/.local/bin/ibus-buuz`
  - System install: `ls /usr/local/bin/ibus-buuz`
- Try restarting IBus again (`ibus restart`)
- For a user install, check that IBus is configured to scan the user component directory:
  ```bash
  echo $IBUS_COMPONENT_PATH
  ```
  The output should include both `/usr/share/ibus/component` and
  `~/.local/share/ibus/component` (see step 2 of the installation).

If the IME doesn't work correctly:
- Check the system logs for any error messages
- Make sure all dependencies are installed
- Try restarting your session

## Uninstallation

To uninstall ibus-buuz, simply remove the installed files:
```bash
rm -f ~/.local/bin/ibus-buuz
rm -rf ~/.local/share/ibus-buuz
rm -f ~/.local/share/ibus/component/buuz.xml
ibus restart
```

For system-wide uninstall:
```bash
sudo rm -f /usr/local/bin/ibus-buuz
sudo rm -rf /usr/local/share/ibus-buuz
sudo rm -f /usr/share/ibus/component/buuz.xml
ibus restart
```

## License

This project is licensed under the Apache License 2.0 - see the LICENSE.txt file for details.

## Acknowledgments

- The IBus team for the IBus framework
- JetBrains for the awesome editor and the AI tools
