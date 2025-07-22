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

import sys
import os

# Add the engine directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "engine"))

# Import the Composer class
from composer import Composer

def run_tests():
    """Run a series of tests to verify the transliteration logic"""
    # Create a composer instance
    composer = Composer()
    
    # Define test cases: (input, expected_output)
    test_cases = [
        # Basic alphabet
        ("a", "а"),
        ("b", "б"),
        ("v", "в"),
        ("g", "г"),
        ("d", "д"),
        ("ye", "е"),
        ("yo", "ё"),
        ("j", "ж"),
        ("z", "з"),
        ("i", "и"),
        ("k", "к"),
        ("l", "л"),
        ("m", "м"),
        ("n", "н"),
        ("o", "о"),
        ("p", "п"),
        ("r", "р"),
        ("s", "с"),
        ("t", "т"),
        ("u", "у"),
        ("f", "ф"),
        ("h", "х"),
        ("c", "ц"),
        ("ch", "ч"),
        ("sh", "ш"),
        ("sxc", "щ"),
        ("\"", "ъ"),
        ("y", "ы"),
        ("'", "ь"),
        ("e", "э"),
        ("yu", "ю"),
        ("ya", "я"),
        
        # Special cases
        ("o'", "ө"),
        ("u'", "ү"),
        ("ii", "ий"),
        
        # Case preservation
        ("A", "А"),
        ("B", "Б"),
        ("V", "В"),
        
        # Mixed case
        ("Buuz", "Бууз"),
        
        # Phrases
        ("buuz id'ye", "бууз идье"),
        ("Mongol hel", "Монгол хэл"),
        ("Ulaanbaatar", "Улаанбаатар"),
        
        # Gender-specific rules
        ("dorj", "дорж"),  # Male name
        ("delgereh", "дэлгэрэх"),  # Female word
    ]
    
    # Run the tests
    passed = 0
    failed = 0
    
    print("Running transliteration tests...")
    print("-" * 50)
    
    for i, (input_text, expected) in enumerate(test_cases, 1):
        result = composer.convert(input_text)
        
        if result == expected:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"
            failed += 1
        
        print(f"Test {i:2d}: {status} | Input: '{input_text}' | Expected: '{expected}' | Got: '{result}'")
    
    print("-" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    
    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
