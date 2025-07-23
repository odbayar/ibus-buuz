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
import signal
import locale
import getopt
import gettext

# Add the engine directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "engine"))

import gi
gi.require_version('IBus', '1.0')
from gi.repository import IBus, GLib, GObject

# Import our engine
from engine import BuuzEngine

# Define constants
BUUZ_ENGINE_PATH = "/org/freedesktop/IBus/Buuz/Engine/"
BUUZ_ENGINE_NAME = "buuz"

class IMApp:
    """
    IBus IME Application
    """
    def __init__(self, exec_by_ibus):
        self.exec_by_ibus = exec_by_ibus
        self.bus = None
        self.engine = None
        self.mainloop = GLib.MainLoop()
        
    def run(self):
        """
        Run the application
        """
        # Initialize IBus connection
        self._init_bus()
        
        # Register the component
        self._register_component()
        
        # Run the main loop
        self.mainloop.run()
    
    def _init_bus(self):
        """
        Initialize the IBus connection
        """
        IBus.init()
        self.bus = IBus.Bus()
        self.bus.connect("disconnected", self._bus_disconnected_cb)
        
    def _bus_disconnected_cb(self, bus):
        """
        Callback for when the bus is disconnected
        """
        self.mainloop.quit()
        
    def _register_component(self):
        """
        Register the component with IBus
        """
        # Create a factory for our engine
        factory = IBus.Factory.new(self.bus.get_connection())
        factory.add_engine(BUUZ_ENGINE_NAME, 
                          GObject.type_from_name("BuuzEngine"))
        
        if self.exec_by_ibus:
            # If executed by IBus, just exit
            self.bus.request_name(f"org.freedesktop.IBus.{BUUZ_ENGINE_NAME}", 0)
        else:
            # If executed standalone, register the component
            component = self._create_component()
            self.bus.register_component(component)
            
    def _create_component(self):
        """
        Create an IBus component
        
        Returns:
            The IBus component
        """
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create a component
        component = IBus.Component.new(
            f"org.freedesktop.IBus.{BUUZ_ENGINE_NAME}",
            "Buuz Mongolian Input Method",
            "0.1.0",
            "Apache License 2.0",
            "Odbayar Nyamtseren <odbayar.n@gmail.com>",
            "https://github.com/odbayar/ibus-buuz",
            os.path.join(current_dir, "ibus-buuz.py"),
            "ibus-buuz"
        )
        
        # Create a description for the engine
        engine = IBus.EngineDesc.new(
            BUUZ_ENGINE_NAME,
            "Buuz",
            "Mongolian Cyrillic Input Method",
            "mn",
            "Apache License 2.0",
            "Odbayar Nyamtseren <odbayar.n@gmail.com>",
            os.path.join(current_dir, "icons", "buuz.png"),
            "us"
        )
        
        # Add the engine to the component
        component.add_engine(engine)
        
        return component

def print_help(out, v=0):
    """
    Print help message
    
    Args:
        out: The output stream
        v: Verbosity level
    """
    print("-i, --ibus             executed by IBus", file=out)
    print("-h, --help             show this help message", file=out)
    print("-d, --daemonize        daemonize ibus", file=out)
    sys.exit(v)

def main():
    """
    Main function
    """
    # Disable output buffering for debugging
    sys.stdout = open(sys.stdout.fileno(), mode='w', buffering=1)
    sys.stderr = open(sys.stderr.fileno(), mode='w', buffering=1)

    try:
        locale.setlocale(locale.LC_ALL, "")
    except:
        pass
    
    # Parse command line options
    exec_by_ibus = False
    daemonize = False
    
    shortopt = "ihd"
    longopt = ["ibus", "help", "daemonize"]
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], shortopt, longopt)
    except getopt.GetoptError as err:
        print_help(sys.stderr, 1)
    
    for o, a in opts:
        if o in ("-h", "--help"):
            print_help(sys.stdout)
        elif o in ("-i", "--ibus"):
            exec_by_ibus = True
        elif o in ("-d", "--daemonize"):
            daemonize = True
        else:
            print("Unknown argument: %s" % o, file=sys.stderr)
            print_help(sys.stderr, 1)
    
    # Daemonize if requested
    if daemonize:
        if os.fork():
            sys.exit()
    
    # Create and run the application
    app = IMApp(exec_by_ibus)
    app.run()

if __name__ == "__main__":
    main()
