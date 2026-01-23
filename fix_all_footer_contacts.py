#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix footer contact details in ALL HTML files that contain the website URL
Updates to: Egypt, 6 October, Giza
"""

import os
import re
from pathlib import Path

NEW_CONTACT_SECTION = '''            <div class="footer-section">
                <h3>تواصل معنا</h3>
                <p>مؤسسة alsooq-alsaudi</p>
                <p>مصر، الجيزة، 6 أكتوبر</p>
                <p>الرمز البريدي: 12365</p>
                <p style="margin-top: 15px; color: var(--accent-color); font-weight: bold; font-size: 1.1rem;">واتساب: +201110760081</p>
                <p style="margin-top: 5px; font-size: 0.9rem;">البريد: sherow1982@gmail.com</p>
                <p style="margin-top: 10px; font-size: 0.9rem;">الموقع: <a href="https://sherow1982.github.io/alsooq-alsaudi" target="_blank" style="color: var(--primary-color);">https://sherow1982.github.io/alsooq-alsaudi</a></p>
            </div>'''

def fix_html_file(file_path):
    """
    Fix contact section in HTML file if it contains the website URL
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file contains the website URL
        if 'sherow1982.github.io/alsooq-alsaudi' not in content:
            return None  # File doesn't contain URL, skip it
        
        original_content = content
        
        # Pattern 1: Match the entire footer-section with "تواصل معنا" heading
        pattern = r'<div class="footer-section">\s*<h3>تواصل معنا</h3>.*?</div>\s*(?=</div>\s*<div class="footer-bottom">|</div>\s*</div>\s*<div class="footer-bottom">)'
        
        # Try to replace using pattern
        new_content = re.sub(pattern, NEW_CONTACT_SECTION, content, flags=re.DOTALL)
        
        if new_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        
        return False
    except Exception as e:
        print(f"  ❌ خطأ بالمعالجة: {str(e)}")
        return False

def main():
    print("🔧 بدء تصحيح الفوتر في جميع ملفات HTML...\n")
    print("="*70)
    
    # Get all HTML files recursively
    html_files = list(Path('.').rglob('*.html'))
    
    print(f"📊 وجدت {len(html_files)} ملف HTML\n")
    
    fixed = 0
    skipped = 0
    failed = 0
    
    for html_file in html_files:
        try:
            result = fix_html_file(html_file)
            
            if result is True:
                fixed += 1
                print(f"✅ {html_file}")
            elif result is None:
                skipped += 1
                print(f"⏭️  {html_file} (لا تحتوي على الموقع)")
            else:
                failed += 1
                print(f"⚠️  {html_file} (لم يتم التعديل)")
        except Exception as e:
            failed += 1
            print(f"❌ {html_file}: {str(e)}")
    
    print(f"\n{'='*70}")
    print(f"✅ تم تصحيح: {fixed} ملف")
    print(f"⏭️  تم تخطي: {skipped} ملف (لا تحتوي على الموقع)")
    print(f"❌ فشل: {failed} ملف")
    print(f"{'='*70}")
    
    if fixed > 0:
        print(f"\n🎉 البيانات الجديدة:")
        print(f"  🏢 مؤسسة: alsooq-alsaudi")
        print(f"  🇪🇬 الدولة: مصر")
        print(f"  🌟 المدينة: الجيزة، 6 أكتوبر")
        print(f"  📋 الرمز البريدي: 12365")
        print(f"  📞 واتساب: +201110760081")
        print(f"  📧 بريد: sherow1982@gmail.com")
        print(f"  🔗 الموقع: https://sherow1982.github.io/alsooq-alsaudi")
        print(f"\n💡 الآن استخدم:")
        print(f"  git add -A")
        print(f"  git commit -m 'تصحيح بيانات الاتصال في جميع الصفحات'")
        print(f"  git push")

if __name__ == '__main__':
    main()
