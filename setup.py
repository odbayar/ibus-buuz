#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2009-2025 Odbayar Nyamtseren <odbayar.n@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import shlex
import shutil
import subprocess
from xml.sax.saxutils import escape
from setuptools import setup, find_packages

# Define paths
PACKAGE_NAME = 'ibus-buuz'
HOME_DIR = os.path.expanduser('~')
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
# IBus reads components from here unless IBUS_COMPONENT_PATH is set
SYSTEM_COMPONENT_DIR = '/usr/share/ibus/component'


def get_install_paths(mode):
    if mode == 'system':
        return {
            'icon_dir': '/usr/local/share/ibus-buuz/icons',
            'bin_dir': '/usr/local/bin',
            'lib_dir': '/usr/local/share/ibus-buuz',
            'component_dir': SYSTEM_COMPONENT_DIR,
        }

    return {
        'icon_dir': os.path.join(HOME_DIR, '.local/share/ibus-buuz/icons'),
        'bin_dir': os.path.join(HOME_DIR, '.local/bin'),
        'lib_dir': os.path.join(HOME_DIR, '.local/share/ibus-buuz'),
        'component_dir': os.path.join(HOME_DIR, '.local/share/ibus/component'),
    }

class CustomInstall:
    """
    Custom installation class to handle file copying and icon conversion
    """
    def __init__(self, mode='user'):
        self.mode = mode
        self.paths = get_install_paths(mode)

    def run(self):
        try:
            # Create directories if they don't exist
            for directory in [
                self.paths['icon_dir'],
                self.paths['bin_dir'],
                self.paths['lib_dir'],
                self.paths['component_dir'],
            ]:
                if not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)
        except PermissionError:
            if self.mode == 'system':
                print("Permission denied creating system directories.")
                print("Run with elevated privileges, for example:")
                print("  sudo python3 setup.py install --system")
            else:
                print("Permission denied creating local installation directories.")
            sys.exit(1)

        try:
            # Copy files
            self._copy_files()
        except PermissionError:
            if self.mode == 'system':
                print("Permission denied writing system files.")
                print("Run with elevated privileges, for example:")
                print("  sudo python3 setup.py install --system")
            else:
                print("Permission denied writing local installation files.")
            sys.exit(1)

        # Register with IBus
        self._register_with_ibus()

    def _copy_files(self):
        """Copy files to their destinations"""
        # Copy engine files
        engine_files = ['engine.py', 'composer.py', 'utils.py']
        for file in engine_files:
            src = os.path.join(SRC_DIR, 'engine', file)
            dst = os.path.join(self.paths['lib_dir'], file)
            shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")

        # Copy main script
        script_path = os.path.join(self.paths['lib_dir'], 'ibus-buuz.py')
        shutil.copy2(os.path.join(SRC_DIR, 'ibus-buuz.py'), script_path)
        print(f"Copied ibus-buuz.py to {script_path}")

        # Create shell script wrapper
        wrapper_path = os.path.join(self.paths['bin_dir'], 'ibus-buuz')
        with open(wrapper_path, 'w') as f:
            f.write('#!/bin/bash\n')
            f.write(f'exec python3 {shlex.quote(script_path)} "$@"\n')
        os.chmod(wrapper_path, 0o755)
        print(f"Created shell script wrapper at {wrapper_path}")

        # Copy icon
        icon_path = os.path.join(self.paths['icon_dir'], 'buuz.png')
        shutil.copy2(os.path.join(SRC_DIR, 'icons', 'buuz.png'), icon_path)
        print(f"Copied icons/buuz.png to {icon_path}")

        # Copy component file with absolute executable/icon paths.
        with open(os.path.join(SRC_DIR, 'buuz.xml.in'), 'r') as f:
            content = f.read()

        # IBus splits <exec> like a shell command line, so quote the path
        content = content.replace('$EXEC_PATH', escape(shlex.quote(wrapper_path)))
        content = content.replace('$ICON_PATH', escape(icon_path))

        # Write the modified content to the destination
        dest_path = os.path.join(self.paths['component_dir'], 'buuz.xml')
        with open(dest_path, 'w') as f:
            f.write(content)

        print(f"Copied buuz.xml with absolute paths to {self.paths['component_dir']}/buuz.xml")

    def _register_with_ibus(self):
        """Register the IME with IBus"""
        if self.mode == 'system':
            print("System-wide install complete.")
            print("Restart IBus in each user session to load Buuz:")
            print("  ibus restart")
            return

        # IBus ignores the user component directory unless it is listed in
        # IBUS_COMPONENT_PATH, which replaces the system directory entirely.
        component_path = os.environ.get('IBUS_COMPONENT_PATH', '').split(os.pathsep)
        if self.paths['component_dir'] not in component_path:
            print()
            print("Warning: IBus will not find Buuz yet. IBus only loads components from")
            print(f"{SYSTEM_COMPONENT_DIR} unless IBUS_COMPONENT_PATH says otherwise.")
            print("To use this user install, add this line to")
            print("~/.config/environment.d/ibus.conf, then log out and back in:")
            print(f"  IBUS_COMPONENT_PATH={SYSTEM_COMPONENT_DIR}:{self.paths['component_dir']}")
            print("Or install for all users instead:")
            print("  sudo python3 setup.py install --system")
            print()

        try:
            # Restart IBus to pick up the new component
            subprocess.run(['ibus', 'restart'], check=True)
            print("IBus restarted successfully")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Warning: Failed to restart IBus. Please restart it manually.")
            print("You can use: ibus restart")

if __name__ == '__main__':
    if 'install' in sys.argv[1:]:
        options = [arg for arg in sys.argv[1:] if arg != 'install']
        unknown = [arg for arg in options if arg != '--system']
        if unknown:
            print(f"Unknown option(s): {' '.join(unknown)}")
            print("Usage: python3 setup.py install [--system]")
            sys.exit(2)
        install_mode = 'system' if '--system' in options else 'user'

        # Under sudo, a user install would land in root's home directory
        if install_mode == 'user' and os.geteuid() == 0:
            print("Refusing to do a user install as root.")
            print("To install for all users, run:")
            print("  sudo python3 setup.py install --system")
            sys.exit(1)

        # Run custom installation
        installer = CustomInstall(mode=install_mode)
        installer.run()
    else:
        # Setup package metadata
        setup(
            name=PACKAGE_NAME,
            version='1.0',
            description='Buuz - Mongolian Cyrillic Input Method',
            author='Odbayar Nyamtseren',
            author_email='odbayar.n@gmail.com',
            url='https://github.com/odbayar/ibus-buuz',
            packages=find_packages(),
            classifiers=[
                'Private :: Do Not Upload',
                'Development Status :: 5 - Production/Stable',
                'Intended Audience :: End Users/Desktop',
                'License :: OSI Approved :: Apache Software License',
                'Operating System :: POSIX :: Linux',
                'Programming Language :: Python :: 3',
            ],
        )
