#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import html

def fix_html_encoding():
    """Fix HTML encoding issues in all product files"""
    
    products_dir = "products"
    html_files = glob.glob(os.path.join(products_dir, "*.html"))
    
    print(f"Found {len(html_files)} product files to fix...")
    
    fixed_count = 0
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if content is HTML encoded
            if '&lt;' in content or '&gt;' in content or '&quot;' in content:
                # Decode HTML entities
                decoded_content = html.unescape(content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(decoded_content)
                
                fixed_count += 1
                print(f"Fixed HTML encoding in file #{fixed_count}")
                
        except Exception as e:
            print(f"Error processing file: {str(e)[:50]}...")
    
    print(f"\nFixed HTML encoding in {fixed_count} out of {len(html_files)} product files!")

if __name__ == "__main__":
    fix_html_encoding()