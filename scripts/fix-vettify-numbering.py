#!/usr/bin/env python3
"""
Script pentru remaparea numerotării din roadmap Vettify
De la 800-900 la 310-399 pentru consistență cu umbrela F2
"""

import re
import sys

def remap_step_numbers(content):
    """Remap step numbers from 800-900 range to 310-399 range"""
    
    # Mapping dictionary: old_number -> new_number
    # 800-810 -> 310-320
    # 811-820 -> 321-330
    # etc.
    
    step_mapping = {}
    for old_num in range(800, 900):  # 800-899 inclusive (90 steps)
        new_num = old_num - 490  # 800->310, 801->311, ..., 899->409
        # Limit to F2 range 310-399 (90 steps max)
        if new_num <= 399:
            step_mapping[old_num] = new_num
    
    # Replace step numbers in JSON
    def replace_step(match):
        old_step = int(match.group(1))
        if old_step in step_mapping:
            return f'"step":{step_mapping[old_step]}'
        return match.group(0)
    
    # Replace context references like "Module creat (800)"
    def replace_context(match):
        old_step = int(match.group(1))
        if old_step in step_mapping:
            return f'({step_mapping[old_step]})'
        return match.group(0)
    
    # Apply replacements
    content = re.sub(r'"step":(\d+)', replace_step, content)
    content = re.sub(r'\((\d+)\)', replace_context, content)
    
    return content

def main():
    file_path = "/var/www/GeniusERP_Suite_v0_1/Documentation/8_roadmap_vettify.md"
    
    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remap numbers
    new_content = remap_step_numbers(content)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Numerotarea a fost actualizată cu succes!")
    print("📊 Remapare: 800-900 → 310-399")

if __name__ == "__main__":
    main()
