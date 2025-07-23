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

1. Clone this repository:

```bash
git clone https://github.com/odbayar/ibus-buuz.git
cd ibus-buuz
```

2. Install the IME:

```bash
python3 setup.py install
```

For detailed information about the local installation process, see [LOCAL_INSTALLATION.md](LOCAL_INSTALLATION.md).

3. Restart IBus (if not already done by the installer):

```bash
ibus restart
```

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
- Make sure IBus is running (`ibus-daemon -drx`)
- Check if the component file was correctly installed (`ls ~/.local/share/ibus/component/buuz.xml`)
- Check if the Python files were correctly installed (`ls ~/.local/share/ibus-buuz/*.py`)
- Check if the shell script wrapper was created (`ls ~/.local/bin/ibus-buuz`)
- Try restarting IBus again (`ibus restart`)
- Make sure `~/.local/bin` is in your PATH

If the IME doesn't work correctly:
- Check the system logs for any error messages
- Make sure all dependencies are installed
- Try restarting your session

## License

This project is licensed under the Apache License 2.0 - see the LICENSE.txt file for details.

## Acknowledgments

- The IBus team for the IBus framework
