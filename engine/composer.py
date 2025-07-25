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

from utils import debug_print

# Conversion rule flags
X_AC = 0x0001  # allow case conversion
X_M  = 0x0002  # only for male words
X_F  = 0x0004  # only for female words
X_MM = 0x0008  # make the word male
X_MF = 0x0010  # make the word female

class ConversionRule:
    """
    Represents a conversion rule for transliteration
    """
    def __init__(self, from_str, to_str, flags):
        self.from_str = from_str
        self.to_str = to_str
        self.flags = flags

class Composer:
    """
    Handles transliteration from Latin to Mongolian Cyrillic
    """
    def __init__(self):
        self.rules = []
        self.rule_lengths = []

        # Initialize conversion rules
        self._init_rules()

        # Compute and store rule lengths in descending order to ensure longer matches
        # are attempted first during conversion (e.g. 'SH' should match before 'S')
        self._compute_rule_lengths()

    def _init_rules(self):
        """Initialize the conversion rules"""
        # Add rules from the Windows IME
        self._add_rule("А"   , "А" , X_M | X_F | X_MM | X_AC)
        self._add_rule("АI"  , "АЙ", X_M | X_F | X_MM | X_AC)
        self._add_rule("О"   , "О" , X_M | X_F | X_MM | X_AC)
        self._add_rule("ОI"  , "ОЙ", X_M | X_F | X_MM | X_AC)
        self._add_rule("У"   , "У" , X_M | X_F | X_MM | X_AC)
        self._add_rule("УI"  , "УЙ", X_M | X_F | X_MM | X_AC)
        self._add_rule("Э"   , "Э" , X_M | X_F | X_MF | X_AC)
        self._add_rule("ЭI"  , "ЭЙ", X_M | X_F | X_MF | X_AC)
        self._add_rule("Ө"   , "Ө" , X_M | X_F | X_MF | X_AC)
        self._add_rule("ӨI"  , "ӨЙ", X_M | X_F | X_MF | X_AC)
        self._add_rule("Ү"   , "Ү" , X_M | X_F | X_MF | X_AC)
        self._add_rule("ҮI"  , "ҮЙ", X_M | X_F | X_MF | X_AC)

        self._add_rule("ИI"  , "ИЙ", X_M | X_F |    0 | X_AC)

        self._add_rule("A"   , "А" , X_M | X_F | X_MM | X_AC)
        self._add_rule("AI"  , "АЙ", X_M | X_F | X_MM | X_AC)
        self._add_rule("B"   , "Б" , X_M | X_F |    0 | X_AC)
        self._add_rule("C"   , "Ц" , X_M | X_F |    0 | X_AC)
        self._add_rule("CH"  , "Ч" , X_M | X_F |    0 | X_AC)
        self._add_rule("D"   , "Д" , X_M | X_F |    0 | X_AC)
        self._add_rule("E"   , "Э" , X_M | X_F | X_MF | X_AC)
        self._add_rule("EI"  , "ЭЙ", X_M | X_F | X_MF | X_AC)
        self._add_rule("F"   , "Ф" , X_M | X_F |    0 | X_AC)
        self._add_rule("G"   , "Г" , X_M | X_F |    0 | X_AC)
        self._add_rule("H"   , "Х" , X_M | X_F |    0 | X_AC)
        self._add_rule("I"   , "И" , X_M | X_F |    0 | X_AC)
        self._add_rule("II"  , "ИЙ", X_M | X_F |    0 | X_AC)
        self._add_rule("III" , "Ы" , X_M | X_F |    0 | X_AC)
        self._add_rule("J"   , "Ж" , X_M | X_F |    0 | X_AC)
        self._add_rule("K"   , "К" , X_M | X_F |    0 | X_AC)
        self._add_rule("KH"  , "Х" , X_M | X_F |    0 | X_AC)
        self._add_rule("L"   , "Л" , X_M | X_F |    0 | X_AC)
        self._add_rule("M"   , "М" , X_M | X_F |    0 | X_AC)
        self._add_rule("N"   , "Н" , X_M | X_F |    0 | X_AC)

        self._add_rule("O"   , "О" , X_M |   0 |    0 | X_AC)
        self._add_rule("OI"  , "ОЙ", X_M |   0 |    0 | X_AC)
        self._add_rule("O\"" , "О" , X_M | X_F | X_MM | X_AC)
        self._add_rule("O\"I", "ОЙ", X_M | X_F | X_MM | X_AC)
        self._add_rule("\"O" , "О" , X_M | X_F | X_MM | X_AC)
        self._add_rule("\"OI", "ОЙ", X_M | X_F | X_MM | X_AC)

        self._add_rule("O"   , "Ө" ,   0 | X_F |    0 | X_AC)
        self._add_rule("OI"  , "ӨЙ",   0 | X_F |    0 | X_AC)
        self._add_rule("Q"   , "Ө" , X_M | X_F | X_MF | X_AC)
        self._add_rule("QI"  , "ӨЙ", X_M | X_F | X_MF | X_AC)
        self._add_rule("O'"  , "Ө" , X_M | X_F | X_MF | X_AC)
        self._add_rule("O'I" , "ӨЙ", X_M | X_F | X_MF | X_AC)
        self._add_rule("'O"  , "Ө" , X_M | X_F | X_MF | X_AC)
        self._add_rule("'OI" , "ӨЙ", X_M | X_F | X_MF | X_AC)

        self._add_rule("P"   , "П" , X_M | X_F |    0 | X_AC)
        self._add_rule("R"   , "Р" , X_M | X_F |    0 | X_AC)
        self._add_rule("S"   , "С" , X_M | X_F |    0 | X_AC)
        self._add_rule("SH"  , "Ш" , X_M | X_F |    0 | X_AC)
        self._add_rule("SXC" , "Щ" , X_M | X_F |    0 | X_AC)
        self._add_rule("T"   , "Т" , X_M | X_F |    0 | X_AC)

        self._add_rule("U"   , "У" , X_M |   0 |    0 | X_AC)
        self._add_rule("UI"  , "УЙ", X_M |   0 |    0 | X_AC)
        self._add_rule("U\"" , "У" , X_M | X_F | X_MM | X_AC)
        self._add_rule("U\"I", "УЙ", X_M | X_F | X_MM | X_AC)
        self._add_rule("\"U" , "У" , X_M | X_F | X_MM | X_AC)
        self._add_rule("\"UI", "УЙ", X_M | X_F | X_MM | X_AC)

        self._add_rule("U"   , "Ү" ,   0 | X_F |    0 | X_AC)
        self._add_rule("UI"  , "ҮЙ",   0 | X_F |    0 | X_AC)
        self._add_rule("W"   , "Ү" , X_M | X_F | X_MF | X_AC)
        self._add_rule("WI"  , "ҮЙ", X_M | X_F | X_MF | X_AC)
        self._add_rule("U'"  , "Ү" , X_M | X_F | X_MF | X_AC)
        self._add_rule("U'I" , "ҮЙ", X_M | X_F | X_MF | X_AC)
        self._add_rule("'U"  , "Ү" , X_M | X_F | X_MF | X_AC)
        self._add_rule("'UI" , "ҮЙ", X_M | X_F | X_MF | X_AC)

        self._add_rule("V"   , "В" , X_M | X_F |    0 | X_AC)
        self._add_rule("X"   , "Х" , X_M | X_F |    0 | X_AC)
        self._add_rule("Y"   , "Ы" , X_M | X_F |    0 | X_AC)
        self._add_rule("YA"  , "Я" , X_M | X_F | X_MM | X_AC)
        self._add_rule("YE"  , "Е" , X_M | X_F | X_MF | X_AC)
        self._add_rule("YO"  , "Ё" , X_M | X_F | X_MM | X_AC)
        self._add_rule("YU"  , "Ю" , X_M | X_F | X_MM | X_AC)
        self._add_rule("Z"   , "З" , X_M | X_F |    0 | X_AC)

        self._add_rule("\""  , "ъ" , X_M | X_F |    0 |    0)
        self._add_rule("\"\"", "Ъ" , X_M | X_F |    0 |    0)
        self._add_rule("'"   , "ь" , X_M | X_F |    0 |    0)
        self._add_rule("''"  , "Ь" , X_M | X_F |    0 |    0)

    def _add_rule(self, from_str, to_str, flags):
        """
        Add a conversion rule

        Args:
            from_str: The source string (Latin)
            to_str: The target string (Cyrillic)
            flags: Rule flags
        """
        # If the rule allows case conversion, handle all case variants
        if flags & X_AC:
            # Map alphabetic characters in 'from' to positions in 'to'
            char_pos_map = []
            to_pos = 0
            for i in range(len(from_str)):
                if from_str[i].isalpha() and to_pos < len(to_str):
                    char_pos_map.append(to_pos)
                    to_pos += 1
                else:
                    char_pos_map.append(-1)

            # Generate all possible case variants using recursion
            def generate_case_variants(pos, to_pos, current_from, current_to):
                if pos >= len(from_str):
                    # We've processed all characters, add the rule
                    self.rules.append(ConversionRule(current_from, current_to, flags))
                    return

                if from_str[pos].isalpha():
                    # For alphabetic characters, try both uppercase and lowercase
                    # 1. Uppercase variant
                    new_from = current_from + from_str[pos].upper()
                    new_to = current_to + to_str[to_pos].upper() if to_pos < len(to_str) else current_to

                    generate_case_variants(pos + 1, to_pos + 1, new_from, new_to)

                    # 2. Lowercase variant
                    new_from = current_from + from_str[pos].lower()
                    new_to = current_to + to_str[to_pos].lower() if to_pos < len(to_str) else current_to

                    generate_case_variants(pos + 1, to_pos + 1, new_from, new_to)
                else:
                    # For non-alphabetic characters, just add them as is
                    generate_case_variants(pos + 1, to_pos, current_from + from_str[pos], current_to)

            # Start generating case variants
            # Note: We don't add the original rule here as it will be handled by the recursive function
            generate_case_variants(0, 0, "", "")
        else:
            self.rules.append(ConversionRule(from_str, to_str, flags))

    def _compute_rule_lengths(self):
        """
        Computes the unique lengths of `from_str` attributes in rules and updates
        the sorted list in descending order.
        """
        lengths = set()
        for rule in self.rules:
            lengths.add(len(rule.from_str))
        self.rule_lengths = sorted(lengths, reverse=True)

    def dump_rules(self, filename):
        """
        Dump the current conversion rules to a file for debugging purposes

        Args:
            filename: The path to the file where rules should be saved
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Write header
                f.write("# Mongolian Cyrillic IME Conversion Rules\n")
                import datetime
                f.write("# Generated: {}\n\n".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                f.write("{:<20} {:<10} {:<10}\n".format("From", "To", "Flags"))
                f.write("-" * 50 + "\n")

                # Write rules
                for rule in self.rules:
                    flags_str = []
                    if rule.flags & X_AC: flags_str.append("X_AC")
                    if rule.flags & X_M: flags_str.append("X_M")
                    if rule.flags & X_F: flags_str.append("X_F")
                    if rule.flags & X_MM: flags_str.append("X_MM")
                    if rule.flags & X_MF: flags_str.append("X_MF")

                    f.write("{:<20} {:<10} {:<10}\n".format(
                        repr(rule.from_str),
                        repr(rule.to_str),
                        " | ".join(flags_str) or "0"
                    ))

                debug_print(f"Rules successfully dumped to {filename}")
        except Exception as e:
            debug_print(f"Error dumping rules to {filename}: {e}")

    def should_process_key(self, keyval):
        """
        Check if a key should be processed by the IME

        Args:
            keyval: The key value

        Returns:
            True if the key should be processed, False otherwise
        """
        # Convert keyval to character
        try:
            char = chr(keyval)
        except ValueError:
            return False

        # Check if it's an input character
        return self._is_input_char(char)

    def _is_input_char(self, char):
        """
        Check if a character is an input character

        Args:
            char: The character to check

        Returns:
            True if the character is an input character, False otherwise
        """
        return char == "'" or char == '"' or ('a' <= char <= 'z') or ('A' <= char <= 'Z')

    def convert(self, text):
        """
        Convert Latin text to Mongolian Cyrillic

        Args:
            text: The Latin text to convert

        Returns:
            The converted Mongolian Cyrillic text
        """
        if not text:
            return ""

        result = ""
        word_flags = X_M  # Start with male word flag

        i = 0
        while i < len(text):
            # Try to match rules of different lengths
            matched = False

            for length in self.rule_lengths:
                if i + length > len(text):
                    continue

                # Get the substring to match
                substr = text[i:i+length]

                # Try to find a matching rule
                for rule in self.rules:
                    if rule.from_str == substr and (word_flags & rule.flags) == word_flags:
                        # Apply the rule
                        result += rule.to_str

                        # Update word flags
                        if rule.flags & X_MF:
                            word_flags = X_F
                        elif rule.flags & X_MM:
                            word_flags = X_M

                        # Move the index
                        i += length
                        matched = True
                        break

                if matched:
                    break

            # If no rule matched, copy the character as is
            if not matched:
                result += text[i]
                i += 1

        return result
