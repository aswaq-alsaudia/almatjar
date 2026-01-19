import json
import re
import random
from pathlib import Path
from urllib.parse import quote
from datetime import datetime

def load_descriptions():
    """تحميل الوصف من ملف descriptions.json"""
    try:
        with open('descriptions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return list(data.values())
    except Exception as e:
        print(f"⚠️ خطأ في تحميل الوصف: {e}")
        return []

def get_random_description(title):
    """الحصول على وصف عشوائي مناسب للمنتج"""
    descriptions = load_descriptions()
    if not descriptions:
        return f"{title} - منتج أصلي بضمان الجودة. اطلب الآن من السوق السعودي!"
    return random.choice(descriptions)

def create_slug(product):
    """توليد slug فريد للمنتج"""
    stop_words = ['من', 'في', 'على', 'الى', 'عن', 'و', 'مع', 'يا', 'أيها']
    
    title = product['title']
    for word in stop_words:
        title = title.replace(f' {word} ', ' ')

    slug = re.sub(r'[^\w\s-]', '', title).strip().lower()
    slug = re.sub(r'\s+', '-', slug)
    return f"{product['id']}-{slug}"

def fix_image_url(url):
    """إصلاح رابط الصورة واستبدال الامتدادات غير المدعومة"""
    if not url:
        return ""
    
    lower_url = url.lower()
    if lower_url.endswith('.mp4'):
        return url[:-4] + '.jpg'
    elif lower_url.endswith('.webp'):
        return url[:-5] + '.jpg'
    return url

def get_product_category(title):
    """تحديد فئة المنتج بناءً على العنوان"""
    title_lower = title.lower()
    
    if any(word in title_lower for word in ['شعر', 'شامبو', 'بلسم', 'زيت', 'ماسك', 'صبغة', 'حلاقة']):
        return 'Health & Beauty > Personal Care > Hair Care', 'العناية بالشعر'
    elif any(word in title_lower for word in ['بشرة', 'كريم', 'سيروم', 'واقي', 'مرطب', 'تفتيح', 'صابون', 'غسول', 'مكياج', 'روج', 'شفاه']):
        return 'Health & Beauty > Personal Care > Cosmetics', 'العناية بالجمال'
    elif any(word in title_lower for word in ['جهاز', 'ماكينة', 'آلة', 'كهربائي', 'قابل للشحن', 'شاحن', 'سماعة', 'كاميرا', 'جوال', 'تابلت', 'ساعة']):
        return 'Electronics', 'الإلكترونيات'
    elif any(word in title_lower for word in ['فيتامين', 'مكمل', 'كبسولات', 'حبوب', 'علاج', 'مشد', 'مصحح', 'ركبة', 'ظهر']):
        return 'Health & Beauty > Health Care', 'الصحة والعافية'
    elif any(word in title_lower for word in ['ملابس', 'شورت', 'قميص', 'حقيبة', 'نظارة', 'حذاء', 'جورب']):
        return 'Apparel & Accessories', 'الأزياء والموضة'
    else:
        return 'Home & Garden', 'المنزل والأدوات'

def generate_product_html(product):
    """توليد صفحة HTML لمنتج واحد"""
    slug = create_slug(product)
    encoded_slug = quote(slug)
    image_link = fix_image_url(product['image_link'])
    
    discount = product['price'] - product['sale_price']
    discount_percentage = int((discount / product['price']) * 100) if product['price'] > 0 else 0
    
    description = get_random_description(product['title'])
    
    product_url = f"https://sherow1982.github.io/alsooq-alsaudi/products/{encoded_slug}.html"
    whatsapp_message = f"""مرحباً، أريد طلب المنتج التالي:

📦 المنتج: {product['title']}
💰 السعر: {product['sale_price']} ريال (السعر الأصلي: {product['price']} ريال)
💵 التوفير: {discount} ريال ({discount_percentage}% خصم)
🔗 الرابط: {product_url}

يرجى تأكيد التوفر والتوصيل."""
    
    whatsapp_link = f"https://wa.me/201110760081?text={quote(whatsapp_message)}"
    
    google_cat, product_type = get_product_category(product['title'])
    
    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description[:160]}">
    <meta property="og:title" content="{product['title']}">
    <meta property="og:description" content="{description[:200]}">
    <meta property="og:image" content="{image_link}">
    <title>{product['title']} | السوق السعودي</title>

    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','GTM-KD9H36GM');</script>
    <!-- End Google Tag Manager -->

    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            direction: rtl;
            background: #f8f9fa;
            color: #333;
            line-height: 1.8;
        }}

        .topbar {{
            background: #2c3e50;
            color: white;
            padding: 10px 0;
            font-size: 13px;
        }}

        .topbar-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
        }}

        .header {{
            background: white;
            border-bottom: 1px solid #e0e0e0;
            padding: 15px 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}

        .header-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo {{
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }}

        .back-btn {{
            background: #3498db;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            transition: all 0.3s;
        }}

        .back-btn:hover {{
            background: #2980b9;
        }}

        .container {{
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 20px;
        }}

        .product-main {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        .product-gallery {{
            position: relative;
        }}

        .product-image {{
            width: 100%;
            height: auto;
            border-radius: 12px;
            object-fit: cover;
        }}

        .product-info h1 {{
            font-size: 32px;
            color: #2c3e50;
            margin-bottom: 20px;
            line-height: 1.4;
        }}

        .prices {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }}

        .current-price {{
            font-size: 36px;
            font-weight: bold;
            color: #27ae60;
        }}

        .old-price {{
            font-size: 24px;
            text-decoration: line-through;
            color: #95a5a6;
        }}

        .discount {{
            background: #e74c3c;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 16px;
            font-weight: bold;
        }}

        .description {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            line-height: 1.8;
        }}

        .whatsapp-btn {{
            background: #25D366;
            color: white;
            padding: 15px 30px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            font-size: 18px;
            display: inline-block;
            margin-top: 20px;
            transition: all 0.3s;
        }}

        .whatsapp-btn:hover {{
            background: #128C7E;
            transform: translateY(-2px);
        }}

        .product-meta {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
        }}

        .meta-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #f0f0f0;
        }}

        .meta-label {{
            color: #666;
            font-weight: 500;
        }}

        .meta-value {{
            color: #2c3e50;
            font-weight: bold;
        }}

        @media (max-width: 768px) {{
            .product-main {{
                grid-template-columns: 1fr;
                padding: 20px;
            }}

            .product-image {{
                height: 300px;
            }}

            h1 {{
                font-size: 24px;
            }}
        }}
    </style>
</head>
<body>
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KD9H36GM"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->

    <div class="topbar">
        <div class="topbar-content">
            <span>📞 خدمة العملاء: 201110760081</span>
            <span>🚚 توصيل سريع لجميع أنحاء المملكة</span>
        </div>
    </div>

    <header class="header">
        <div class="header-content">
            <div class="logo">🛍️ السوق السعودي</div>
            <a href="../index.html" class="back-btn">← العودة للرئيسية</a>
        </div>
    </header>

    <div class="container">
        <div class="product-main">
            <div class="product-gallery">
                <img src="{image_link}" alt="{product['title']}" class="product-image" loading="lazy">
            </div>
            
            <div class="product-info">
                <h1>{product['title']}</h1>
                
                <div class="prices">
                    <span class="current-price">{product['sale_price']} ر.س</span>
                    <span class="old-price">{product['price']} ر.س</span>
                    <span class="discount">-{discount_percentage}%</span>
                </div>

                <div class="description">
                    <strong>📝 وصف المنتج:</strong><br><br>
                    {description}
                </div>

                <a href="{whatsapp_link}" class="whatsapp-btn" target="_blank">
                    📱 اطلب عبر واتساب
                </a>

                <div class="product-meta">
                    <div class="meta-item">
                        <span class="meta-label">💵 التوفير</span>
                        <span class="meta-value">{discount} ريال</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">📦 الفئة</span>
                        <span class="meta-value">{product_type}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">🚚 الشحن</span>
                        <span class="meta-value">مجاناً لجميع المملكة</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">⏱️ التوصيل</span>
                        <span class="meta-value">1-3 أيام عمل</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer style="background: #2c3e50; color: white; padding: 40px 20px; margin-top: 60px; text-align: center;">
        <p>&copy; 2025 السوق السعودي. جميع الحقوق محفوظة.</p>
    </footer>
</body>
</html>"""
    
    return html

def generate_product_feed(products):
    """توليد ملف product-feed.xml لـ Google Merchant Center"""
    base_url = "https://sherow1982.github.io/alsooq-alsaudi"
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<rss xmlns:g="http://base.google.com/ns/1.0" version="2.0">')
    xml.append('  <channel>')
    xml.append('    <title>السوق السعودي</title>')
    xml.append(f'    <link>{base_url}/</link>')
    xml.append('    <description>أفضل العروض والمنتجات الأصلية بأسعار تنافسية</description>')
    
    for product in products:
        slug = create_slug(product)
        encoded_slug = quote(slug)
        product_link = f"{base_url}/products/{encoded_slug}.html"
        
        image_link = fix_image_url(product['image_link'])
        google_cat, product_type = get_product_category(product['title'])
        
        discount = product['price'] - product['sale_price']
        description = f"{product['title']} - منتج أصلي بضمان الجودة. وفر {discount} ريال الآن!"
        
        xml.append('    <item>')
        xml.append(f'      <g:id>{product["id"]}</g:id>')
        xml.append(f'      <g:title><![CDATA[{product["title"]}]]></g:title>')
        xml.append(f'      <g:description><![CDATA[{description}]]></g:description>')
        xml.append(f'      <g:link>{product_link}</g:link>')
        xml.append(f'      <g:image_link>{image_link}</g:image_link>')
        xml.append('      <g:condition>new</g:condition>')
        xml.append('      <g:availability>in stock</g:availability>')
        xml.append(f'      <g:price>{product["price"]} SAR</g:price>')
        xml.append(f'      <g:sale_price>{product["sale_price"]} SAR</g:sale_price>')
        xml.append('      <g:brand>السوق السعودي</g:brand>')
        xml.append(f'      <g:google_product_category>{google_cat}</g:google_product_category>')
        xml.append(f'      <g:product_type>{product_type}</g:product_type>')
        xml.append('      <g:shipping>')
        xml.append('        <g:country>SA</g:country>')
        xml.append('        <g:service>Standard</g:service>')
        xml.append('        <g:price>0 SAR</g:price>')
        xml.append('      </g:shipping>')
        xml.append('    </item>')
        
    xml.append('  </channel>')
    xml.append('</rss>')
    
    with open('product-feed.xml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml))
    print("✅ تم توليد product-feed.xml بنجاح")

def generate_sitemap(products):
    """توليد sitemap.xml"""
    base_url = "https://sherow1982.github.io/alsooq-alsaudi"
    today = datetime.now().strftime('%Y-%m-%d')
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">')
    
    xml.append('  <url>')
    xml.append(f'    <loc>{base_url}/</loc>')
    xml.append(f'    <lastmod>{today}</lastmod>')
    xml.append('    <changefreq>daily</changefreq>')
    xml.append('    <priority>1.0</priority>')
    xml.append('  </url>')
    
    xml.append('  <url>')
    xml.append(f'    <loc>{base_url}/about.html</loc>')
    xml.append(f'    <lastmod>{today}</lastmod>')
    xml.append('    <changefreq>weekly</changefreq>')
    xml.append('    <priority>0.8</priority>')
    xml.append('  </url>')
    
    xml.append('  <url>')
    xml.append(f'    <loc>{base_url}/contact.html</loc>')
    xml.append(f'    <lastmod>{today}</lastmod>')
    xml.append('    <changefreq>weekly</changefreq>')
    xml.append('    <priority>0.8</priority>')
    xml.append('  </url>')
    
    for product in products:
        slug = create_slug(product)
        encoded_slug = quote(slug)
        image_link = fix_image_url(product['image_link'])
        
        xml.append('  <url>')
        xml.append(f'    <loc>{base_url}/products/{encoded_slug}.html</loc>')
        xml.append(f'    <lastmod>{today}</lastmod>')
        xml.append('    <changefreq>weekly</changefreq>')
        xml.append('    <priority>0.8</priority>')
        xml.append('    <image:image>')
        xml.append(f'      <image:loc>{image_link}</image:loc>')
        xml.append(f'      <image:title>{product["title"]}</image:title>')
        xml.append('    </image:image>')
        xml.append('  </url>')
        
    xml.append('</urlset>')
    
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml))
    print("✅ تم توليد sitemap.xml بنجاح")

def main():
    """الدالة الرئيسية لتشغيل السكريبت"""
    print("🚀 بدء توليد صفحات المنتجات...\n")
    
    products_dir = Path('products')
    products_dir.mkdir(exist_ok=True)
    
    with open('products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print(f"📦 عدد المنتجات: {len(products)}\n")
    
    success_count = 0
    for i, product in enumerate(products, 1):
        try:
            slug = create_slug(product)
            html = generate_product_html(product)
            
            file_path = products_dir / f"{slug}.html"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html)
            
            success_count += 1
            if i % 100 == 0:
                print(f"✅ تم إنشاء {i} صفحة...")
        except Exception as e:
            print(f"❌ خطأ في المنتج {i}: {e}")
    
    print(f"\n✅ تم إنشاء {success_count} صفحة منتج بنجاح\n")
    
    generate_sitemap(products)
    generate_product_feed(products)

    print()
    print("─" * 60)
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                    ✨ تم الانتهاء بنجاح! ✨                  ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("─" * 60)
    print()

if __name__ == "__main__":
    main()
