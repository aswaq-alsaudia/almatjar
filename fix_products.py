#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import re

def fix_product_files():
    """Fix all product HTML files by updating CSS and asset paths"""
    
    # Get all HTML files in products directory
    products_dir = "products"
    html_files = glob.glob(os.path.join(products_dir, "*.html"))
    
    print(f"Found {len(html_files)} product files to fix...")
    
    # Patterns to fix
    fixes = [
        # CSS and favicon paths - remove leading slash or add ../
        (r'href="/css/main\.css"', 'href="../css/main.css"'),
        (r'href="/favicon\.svg"', 'href="../favicon.svg"'),
        (r'href="css/main\.css"', 'href="../css/main.css"'),
        (r'href="favicon\.svg"', 'href="../favicon.svg"'),
        
        # Logo and navigation paths
        (r'href="/index\.html"', 'href="../index.html"'),
        (r'src="/logo\.png"', 'src="../logo.png"'),
        (r'href="/about\.html"', 'href="../about.html"'),
        (r'href="/contact\.html"', 'href="../contact.html"'),
        
        # Policy pages paths
        (r'href="/shipping\.html"', 'href="../shipping.html"'),
        (r'href="/return-policy\.html"', 'href="../return-policy.html"'),
        (r'href="/terms\.html"', 'href="../terms.html"'),
        (r'href="/privacy\.html"', 'href="../privacy.html"'),
    ]
    
    fixed_count = 0
    
    for file_path in html_files:
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Apply all fixes
            for pattern, replacement in fixes:
                content = re.sub(pattern, replacement, content)
            
            # Only write if content changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1
                print(f"Fixed file #{fixed_count}")
            
        except Exception as e:
            print(f"Error processing file: {str(e)[:50]}...")
    
    print(f"\nFixed {fixed_count} out of {len(html_files)} product files!")

if __name__ == "__main__":
    fix_product_files()