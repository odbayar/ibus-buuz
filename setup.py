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
import shutil
import subprocess
from setuptools import setup, find_packages

# Define paths
PACKAGE_NAME = 'ibus-buuz'
HOME_DIR = os.path.expanduser('~')


def get_install_paths(mode):
    if mode == 'system':
        return {
            'icon_dir': '/usr/local/share/ibus-buuz/icons',
            'bin_dir': '/usr/local/bin',
            'lib_dir': '/usr/local/share/ibus-buuz',
            # IBus scans /usr/share/ibus/component on typical distro packages.
            'component_dir': '/usr/share/ibus/component',
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
            src = os.path.join('engine', file)
            dst = os.path.join(self.paths['lib_dir'], file)
            shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")

        # Copy main script
        shutil.copy2('ibus-buuz.py', os.path.join(self.paths['lib_dir'], 'ibus-buuz.py'))
        print(f"Copied ibus-buuz.py to {self.paths['lib_dir']}/ibus-buuz.py")

        # Create shell script wrapper
        wrapper_path = os.path.join(self.paths['bin_dir'], 'ibus-buuz')
        with open(wrapper_path, 'w') as f:
            f.write('#!/bin/bash\n')
            f.write(f'exec python3 {self.paths["lib_dir"]}/ibus-buuz.py "$@"\n')
        os.chmod(wrapper_path, 0o755)
        print(f"Created shell script wrapper at {wrapper_path}")

        # Copy icon
        shutil.copy2('icons/buuz.png', os.path.join(self.paths['icon_dir'], 'buuz.png'))
        print(f"Copied icons/buuz.png to {self.paths['icon_dir']}/buuz.png")

        # Copy component file with absolute executable/icon paths.
        with open('buuz.xml.in', 'r') as f:
            content = f.read()

        exec_path = os.path.join(self.paths['bin_dir'], 'ibus-buuz')
        icon_path = os.path.join(self.paths['icon_dir'], 'buuz.png')
        content = content.replace('$EXEC_PATH', exec_path)
        content = content.replace('$ICON_PATH', icon_path)

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

        try:
            # Restart IBus to pick up the new component
            subprocess.run(['ibus', 'restart'], check=True)
            print("IBus restarted successfully")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Warning: Failed to restart IBus. Please restart it manually.")
            print("You can use: ibus restart")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'install':
        install_mode = 'user'
        if '--system' in sys.argv:
            install_mode = 'system'
            sys.argv.remove('--system')

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
