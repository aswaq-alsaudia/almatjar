import json
import re
from collections import Counter
import sys

# Force UTF-8 for output
sys.stdout.reconfigure(encoding='utf-8')

def audit_products():
    print("Starting Product Data Audit...")
    
    try:
        with open('products.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
    except FileNotFoundError:
        print("Error: products.json not found!")
        return
    except json.JSONDecodeError:
        print("Error: products.json is not valid JSON!")
        return

    print(f"Total Products: {len(products)}")
    
    issues = []
    ids = [p.get('id') for p in products]
    
    # Check 1: Duplicate IDs
    id_counts = Counter(ids)
    duplicates = [id for id, count in id_counts.items() if count > 1]
    if duplicates:
        issues.append(f"Duplicate IDs found: {duplicates}")
    
    # Check individual products
    for p in products:
        pid = p.get('id', 'UNKNOWN')
        title = p.get('title', '')
        price = p.get('price', 0)
        sale_price = p.get('sale_price', 0)
        image = p.get('image_link', '')
        
        # Check 2: Missing Fields
        if not title:
            issues.append(f"Product {pid}: Missing title")
        
        # Check 3: Pricing Issues
        if not isinstance(price, (int, float)) or price <= 0:
             # Some might be zero if free, but usually not for a store
             pass 
             
        if not isinstance(sale_price, (int, float)) or sale_price <= 0:
             pass 

        if sale_price > price:
            issues.append(f"Product {pid}: Sale price ({sale_price}) is higher than regular price ({price})")
            
        # Check 4: Image Links
        if not image or not image.startswith('http'):
            issues.append(f"Product {pid}: Invalid image link '{image}'")
            
    if not issues:
        print("No critical data issues found!")
    else:
        print(f"\nFound {len(issues)} issues:")
        for issue in issues[:20]: # Show first 20
            print(issue)
        if len(issues) > 20:
            print(f"... and {len(issues) - 20} more.")

if __name__ == "__main__":
    audit_products()
