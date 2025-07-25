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

import gi
gi.require_version('IBus', '1.0')
from gi.repository import IBus

# Import our custom modules
from composer import Composer
from utils import debug_print

# Maximum composition length
MAX_COMP_LENGTH = 50

class BuuzEngine(IBus.Engine):
    """
    IBus Engine for Mongolian Cyrillic input
    """
    __gtype_name__ = 'BuuzEngine'

    def __init__(self):
        super(BuuzEngine, self).__init__()

        # Create composer instance for transliteration
        self.composer = Composer()

        # Composition state
        self.preedit_string = ""
        self.is_composing = False

        debug_print("BuuzEngine initialized")

    def do_focus_in(self):
        """Called when the engine gains focus"""
        debug_print("do_focus_in")

    def do_focus_out(self):
        """Called when the engine loses focus"""
        debug_print("do_focus_out")
        self.commit_preedit()

    def do_reset(self):
        """Reset the engine state"""
        debug_print("do_reset")
        self._reset_state()

    def _reset_state(self):
        self.is_composing = False
        self.preedit_string = ""
        self.update_preedit()

    def do_process_key_event(self, keyval, keycode, state):
        """
        Process a key event

        Args:
            keyval: The key value
            keycode: The key code
            state: The key state (modifiers)

        Returns:
            True if the key was handled, False otherwise
        """
        debug_print(f"do_process_key_event(keyval={keyval}, keycode={keycode}, state={state})")

        # Ignore key release events
        if state & IBus.ModifierType.RELEASE_MASK:
            return False

        # Handle special keys
        if keyval == IBus.KEY_BackSpace:
            if self.preedit_string:
                self.preedit_string = self.preedit_string[:-1]
                self.update_preedit()
                return True
            return False

        # Ignore shift and caps lock keys
        elif keyval in (IBus.KEY_Shift_L, IBus.KEY_Shift_R, IBus.KEY_Caps_Lock):
            return False

        # Handle regular input
        elif (len(self.preedit_string) < MAX_COMP_LENGTH and self.composer.should_process_key(keyval) and
              state & ~IBus.ModifierType.SHIFT_MASK == 0):
            # If we're not composing yet, start composition
            if not self.is_composing:
                self.is_composing = True

            # Convert keyval to character
            char = chr(keyval)

            # Add to preedit string
            self.preedit_string += char

            # Update the display
            self.update_preedit()
            return True

        # If we're composing and a non-handled key is pressed, commit and let it through
        elif self.is_composing:
            self.commit_preedit()

        return False

    def update_preedit(self):
        """Update the preedit text"""
        if self.is_composing:
            # Convert the input text to Mongolian Cyrillic
            converted_text = self.composer.convert(self.preedit_string)

            # Create an IBus text with the converted text
            text = IBus.Text.new_from_string(converted_text)

            # Set attributes (underline the text)
            attrs = IBus.AttrList()
            length = len(converted_text)
            if length > 0:
                attrs.append(IBus.Attribute.new(IBus.AttrType.UNDERLINE,
                                               IBus.AttrUnderline.SINGLE, 0, length))
            text.set_attributes(attrs)

            # Update the preedit text
            self.update_preedit_text(text, length, length > 0)
        else:
            # Clear the preedit text
            self.hide_preedit_text()

    def commit_preedit(self):
        """Commit the current preedit text"""
        if self.is_composing:
            # Convert the input text to Mongolian Cyrillic
            converted_text = self.composer.convert(self.preedit_string)

            # Commit the text
            self.commit_text(IBus.Text.new_from_string(converted_text))

            # Reset the state
            self._reset_state()
