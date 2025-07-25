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
ICON_DIR = os.path.join(HOME_DIR, '.local/share/ibus-buuz/icons')
BIN_DIR = os.path.join(HOME_DIR, '.local/bin')
LIB_DIR = os.path.join(HOME_DIR, '.local/share/ibus-buuz')
IBUS_COMPONENT_DIR = os.path.join(HOME_DIR, '.local/share/ibus/component')

class CustomInstall:
    """
    Custom installation class to handle file copying and icon conversion
    """
    def run(self):
        # Create directories if they don't exist
        for directory in [ICON_DIR, BIN_DIR, LIB_DIR, IBUS_COMPONENT_DIR]:
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

        # Copy files
        self._copy_files()

        # Register with IBus
        self._register_with_ibus()

    def _copy_files(self):
        """Copy files to their destinations"""
        # Copy engine files
        engine_files = ['engine.py', 'composer.py', 'utils.py']
        for file in engine_files:
            src = os.path.join('engine', file)
            dst = os.path.join(LIB_DIR, file)
            shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")

        # Copy main script
        shutil.copy2('ibus-buuz.py', os.path.join(LIB_DIR, 'ibus-buuz.py'))
        print(f"Copied ibus-buuz.py to {LIB_DIR}/ibus-buuz.py")

        # Create shell script wrapper
        wrapper_path = os.path.join(BIN_DIR, 'ibus-buuz')
        with open(wrapper_path, 'w') as f:
            f.write('#!/bin/bash\n')
            f.write(f'exec python3 {LIB_DIR}/ibus-buuz.py "$@"\n')
        os.chmod(wrapper_path, 0o755)
        print(f"Created shell script wrapper at {wrapper_path}")

        # Copy icon
        shutil.copy2('icons/buuz.png', os.path.join(ICON_DIR, 'buuz.png'))
        print(f"Copied icons/buuz.png to {ICON_DIR}/buuz.png")

        # Copy component file with tilde paths replaced by absolute paths
        with open('buuz.xml', 'r') as f:
            content = f.read()

        # Replace tilde paths with absolute paths
        content = content.replace('~/', f'{HOME_DIR}/')

        # Write the modified content to the destination
        dest_path = os.path.join(IBUS_COMPONENT_DIR, 'buuz.xml')
        with open(dest_path, 'w') as f:
            f.write(content)

        print(f"Copied buuz.xml with absolute paths to {IBUS_COMPONENT_DIR}/buuz.xml")

    def _register_with_ibus(self):
        """Register the IME with IBus"""
        try:
            # Restart IBus to pick up the new component
            subprocess.run(['ibus', 'restart'], check=True)
            print("IBus restarted successfully")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Warning: Failed to restart IBus. Please restart it manually.")
            print("You can use: ibus restart")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'install':
        # Run custom installation
        installer = CustomInstall()
        installer.run()
    else:
        # Setup package metadata
        setup(
            name=PACKAGE_NAME,
            version='0.1.0',
            description='Buuz Mongolian Input Method for IBus',
            author='Odbayar Nyamtseren',
            author_email='odbayar.n@gmail.com',
            url='https://github.com/odbayar/ibus-buuz',
            packages=find_packages(),
            classifiers=[
                'Development Status :: 4 - Beta',
                'Environment :: X11 Applications :: GTK',
                'Intended Audience :: End Users/Desktop',
                'License :: OSI Approved :: Apache Software License',
                'Operating System :: POSIX :: Linux',
                'Programming Language :: Python :: 3',
                'Topic :: Software Development :: Libraries :: Python Modules',
                'Topic :: System :: Input/Output',
            ],
        )
