#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix all product page headers and footers in batch
Run this script locally to update all product files
"""

import os
import re
from pathlib import Path

MODERN_HEADER = '''    <div class="topbar">
        <div class="topbar-content">
            <div class="topbar-left">
                <span>🏅 منتجات أصلية 100% بضمان السوق السعودي</span>
            </div>
            <div class="topbar-right">
                <span>📞 خدمة العملاء: 201110760081</span>
            </div>
        </div>
    </div>

    <header class="header">
        <div class="header-content">
            <div class="logo">
                <a href="../index.html">
                    <img src="../logo.png" alt="السوق السعودي">
                </a>
            </div>
            <nav class="nav-links" id="navLinks">
                <a href="../index.html">الرئيسية</a>
                <a href="../about.html">من نحن</a>
                <a href="../contact.html">تواصل معنا</a>
                <a href="https://wa.me/201110760081" class="whatsapp-cta" target="_blank">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766 0-3.18-2.587-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217s.231.006.332.012c.109.006.252-.041.397.308.145.348.499 1.223.541 1.312.041.089.068.191.008.312-.06.121-.09.197-.181.302-.09.105-.19.235-.272.316-.09.09-.184.188-.079.365.105.177.465.766.997 1.239.685.611 1.26.802 1.437.89.177.089.282.075.387-.041.105-.116.443-.518.562-.695.119-.177.239-.148.405-.087.166.061 1.054.497 1.234.587s.3.135.344.209c.044.075.044.436-.1.841z"/></svg>
                    <span>اطلب عبر واتساب</span>
                </a>
            </nav>
            <div class="menu-toggle" id="menuToggle">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    </header>'''

MODERN_FOOTER = '''    <a href="https://wa.me/201110760081" class="floating-whatsapp" target="_blank" title="تواصل معنا بالواتساب">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766 0-3.18-2.587-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217s.231.006.332.012c.109.006.252-.041.397.308.145.348.499 1.223.541 1.312.041.089.068.191.008.312-.06.121-.09.197-.181.302-.09.105-.19.235-.272.316-.09.09-.184.188-.079.365.105.177.465.766.997 1.239.685.611 1.26.802 1.437.89.177.089.282.075.387-.041.105-.116.443-.518.562-.695.119-.177.239-.148.405-.087.166.061 1.054.497 1.234.587s.3.135.344.209c.044.075.044.436-.1.841z"/></svg>
    </a>

    <footer>
        <div class="footer-content">
            <div class="footer-section">
                <h3>عن السوق السعودي</h3>
                <p>نحن وجهتك الأولى لتسوق أفضل المنتجات الأصلية في المملكة، نجمع بين الجودة والفخامة وخدمة التوصيل السريع لضمان أفضل تجربة تسوق.</p>
            </div>
            <div class="footer-section">
                <h3>روابط سريعة</h3>
                <ul class="footer-links">
                    <li><a href="../index.html">الرئيسية</a></li>
                    <li><a href="../about.html">من نحن</a></li>
                    <li><a href="../contact.html">تواصل معنا</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h3>السياسات القانونية</h3>
                <ul class="footer-links">
                    <li><a href="../shipping.html">سياسة الشحن</a></li>
                    <li><a href="../return-policy.html">سياسة الإرجاع</a></li>
                    <li><a href="../terms.html">الشروط والأحكام</a></li>
                    <li><a href="../privacy.html">سياسة الخصوصية</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h3>تواصل معنا</h3>
                <p>مؤسسة alsooq-alsaudi</p>
                <p>المملكة العربية السعودية، السعودية</p>
                <p>الرياض 12211</p>
                <p style="margin-top: 15px; color: var(--accent-color); font-weight: bold; font-size: 1.1rem;">واتساب: +201110760081</p>
                <p style="margin-top: 5px; font-size: 0.9rem;">البريد: sherow1982@gmail.com</p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>جميع الحقوق محفوظة © 2026 السوق السعودي - فخامة التسوق بين يديك</p>
        </div>
    </footer>

    <script>
        // Mobile Menu Toggle
        const menuToggle = document.getElementById('menuToggle');
        const navLinks = document.getElementById('navLinks');
        
        if (menuToggle && navLinks) {
            menuToggle.addEventListener('click', () => {
                navLinks.classList.toggle('active');
                menuToggle.classList.toggle('active');
            });

            // Close menu when clicking a link
            document.querySelectorAll('.nav-links a').forEach(link => {
                link.addEventListener('click', () => {
                    navLinks.classList.remove('active');
                    menuToggle.classList.remove('active');
                });
            });
        }
    </script>'''

def fix_product_file(file_path):
    """Fix a single product file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract head section
    head_match = re.search(r'<head>(.*?)</head>', content, re.DOTALL)
    if not head_match:
        return False
    
    head = head_match.group(1)
    
    # Extract main content
    main_match = re.search(r'(<main.*?</main>)', content, re.DOTALL)
    if not main_match:
        return False
    
    main_content = main_match.group(1)
    
    # Build new file
    new_content = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>{head}
</head>
<body>
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KD9H36GM"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

{MODERN_HEADER}

    {main_content}

{MODERN_FOOTER}
</body>
</html>'''
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    products_dir = Path('products')
    
    if not products_dir.exists():
        print("❌ مجلد products غير موجود")
        return
    
    html_files = list(products_dir.glob('*.html'))
    print(f"🔍 وجدت {len(html_files)} ملف منتج")
    
    fixed = 0
    failed = 0
    
    for html_file in html_files:
        try:
            if fix_product_file(html_file):
                fixed += 1
                print(f"✅ {html_file.name}")
            else:
                failed += 1
                print(f"❌ {html_file.name}")
        except Exception as e:
            failed += 1
            print(f"❌ {html_file.name}: {str(e)}")
    
    print(f"\n{'='*50}")
    print(f"✅ تم تصحيح: {fixed} ملف")
    print(f"❌ فشل: {failed} ملف")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
