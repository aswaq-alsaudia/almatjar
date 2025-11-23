#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكربت توليد صفحات المنتجات مع التقييمات والأوصاف
يقوم بإنشاء:
1. صفحات HTML لجميع المنتجات (2188 صفحة)
2. ملف reviews.json للتقييمات
3. ملف descriptions.json للأوصاف
"""

import json
import re
import os
import random
from datetime import datetime, timedelta
from urllib.parse import quote

# ════════════════════════════════════════════════════════════
# إعدادات المشروع
# ════════════════════════════════════════════════════════════
WHATSAPP_NUMBER = "201110760081"
PRODUCTS_FILE = "products.json"
OUTPUT_DIR = "products"
REVIEWS_FILE = "reviews.json"
DESCRIPTIONS_FILE = "descriptions.json"

# ════════════════════════════════════════════════════════════
# بيانات التقييمات
# ════════════════════════════════════════════════════════════

SAUDI_NAMES = [
    "محمد العتيبي", "عبدالله السبيعي", "فهد الدوسري", "سعود القحطاني",
    "خالد الشمري", "عبدالعزيز المطيري", "فيصل الحربي", "سلمان الغامدي",
    "ناصر الزهراني", "يوسف العنزي", "أحمد الشهري", "عمر البقمي",
    "علي الجهني", "حمد الرشيدي", "صالح العمري", "طلال السهلي",
    "نورة المالكي", "سارة الأحمدي", "منى الخالدي", "فاطمة العسيري",
    "هند القرشي", "ريم الثقفي", "لولوة العتيبي", "مها السديري",
    "عبير الدوسري", "أمل الحمد", "نادية السلمي", "وفاء المري",
    "بدر الجبرين", "ماجد الفهد", "تركي العبدالله", "راشد المنصور",
    "عادل الراجحي", "وليد الفوزان", "عبدالرحمن الصالح", "بندر العقيل",
    "جواهر الحسين", "لطيفة الناصر", "شهد الكريم", "دانة العلي"
]

REVIEW_TEMPLATES = [
    "منتج ممتاز وجودة عالية جداً، أنصح بالشراء بقوة",
    "وصلني المنتج في وقت قياسي والجودة فاقت التوقعات",
    "صراحة منتج رائع واستخدمته وحسيت بفرق واضح",
    "جودة ممتازة وسعر مناسب، تعاملت مع البائع أكثر من مرة",
    "المنتج أصلي ومطابق للوصف تماماً، شكراً للبائع",
    "استلمت الطلب بحالة ممتازة، التغليف احترافي جداً",
    "منتج يستحق الشراء، جربته وكانت النتيجة رائعة",
    "ما شاء الله المنتج فوق الممتاز، سأطلب مرة أخرى",
    "جودة عالية وسعر منافس، أنصح الجميع بالتجربة",
    "منتج أصلي ومضمون، شكراً على الخدمة الرائعة",
    "استخدمته من أسبوع والنتيجة واضحة، راضي جداً",
    "التوصيل سريع والمنتج بحالة ممتازة، شكراً",
    "منتج رهيب وفعال، لاحظت الفرق من أول استخدام",
    "جودة ممتازة ومطابق للمواصفات، ما تردد بالشراء",
    "البائع متعاون والمنتج أفضل من المتوقع",
    "صراحة منتج يستاهل كل ريال دفعته فيه",
    "جربت منتجات كثيرة لكن هذا الأفضل بلا منازع",
    "المنتج وصل بسرعة والتعبئة محترمة جداً",
    "راضي تماماً عن الجودة والسعر، شكراً",
    "منتج ممتاز ينفع هدية، طلبت منه أكثر من مرة",
    "جودة عالية وسعر معقول، تجربة ممتازة",
    "المنتج فعال ونتائجه سريعة، أنصح به بشدة",
    "استلمت الطلب في الموعد والمنتج فوق التوقعات",
    "تعامل راقي وجودة ممتازة، سأكون عميل دائم",
    "المنتج أصلي ومضمون، جربته وكانت النتيجة رائعة",
    "صراحة ما توقعت يكون بهذه الجودة، ممتاز جداً",
    "منتج يستحق التقييم الخمس نجوم، راضي تماماً",
    "جودة ممتازة وخدمة احترافية، شكراً لكم",
    "المنتج وصل بحالة ممتازة والسعر مناسب جداً",
    "تجربة رائعة من البداية للنهاية، أنصح بالشراء"
]

# ════════════════════════════════════════════════════════════
# دوال توليد الأوصاف الذكية
# ════════════════════════════════════════════════════════════

def generate_smart_description(product_title):
    """توليد وصف ذكي للمنتج حسب نوعه"""
    
    title_lower = product_title.lower()
    
    # منتجات العناية بالشعر
    if any(word in title_lower for word in ['شعر', 'شامبو', 'بلسم', 'زيت', 'ماسك']):
        descriptions = [
            f"يوفر {product_title} عناية متكاملة للشعر من الجذور حتى الأطراف بتركيبة غنية بالمكونات الطبيعية. يعمل على تقوية بصيلات الشعر وتغذيتها بعمق لمنحك شعر صحي ولامع. مناسب للاستخدام اليومي على جميع أنواع الشعر.",
            f"تم تصميم {product_title} خصيصاً لمعالجة مشاكل الشعر الشائعة وتحسين مظهره بشكل ملحوظ. يحتوي على تركيبة متوازنة تغذي الشعر وتحميه من التلف والتقصف. يمنحك نتائج احترافية من الاستخدام الأول.",
            f"يتميز {product_title} بتركيبة فريدة تجمع بين الفعالية والأمان للعناية المثالية بالشعر. يعمل على ترطيب الشعر بعمق وإصلاح التلف الناتج عن العوامل الخارجية. منتج موثوق يحقق نتائج مذهلة في وقت قصير."
        ]
    
    # منتجات العناية بالبشرة
    elif any(word in title_lower for word in ['بشرة', 'كريم', 'سيروم', 'واقي', 'مرطب', 'تفتيح']):
        descriptions = [
            f"يقدم {product_title} حلاً متكاملاً للعناية بالبشرة بمكونات طبيعية آمنة وفعالة. يعمل على تحسين ملمس البشرة ومظهرها مع ترطيب عميق يدوم طويلاً. مناسب لجميع أنواع البشرة ويمنح نتائج مرئية سريعة.",
            f"صمم {product_title} بعناية فائقة ليمنح بشرتك العناية التي تستحقها بأعلى معايير الجودة. يحتوي على مكونات نشطة تعمل على تجديد خلايا البشرة ومكافحة علامات التقدم بالعمر. منتج آمن ومختبر طبياً لضمان أفضل النتائج.",
            f"يتميز {product_title} بتركيبة متطورة تجمع بين الفعالية والأمان لبشرة صحية ومشرقة. يعمل على معالجة مشاكل البشرة الشائعة ويمنحها النضارة والحيوية. استخدام منتظم يضمن نتائج استثنائية وبشرة خالية من العيوب."
        ]
    
    # الأجهزة الإلكترونية
    elif any(word in title_lower for word in ['جهاز', 'ماكينة', 'آلة', 'كهربائي', 'قابل للشحن']):
        descriptions = [
            f"يجمع {product_title} بين التقنية الحديثة والتصميم العملي لتوفير أداء متميز وموثوق. مصنوع من مواد عالية الجودة تضمن المتانة والاستخدام طويل الأمد. سهل الاستخدام ويحقق نتائج احترافية في المنزل.",
            f"صمم {product_title} ليقدم لك تجربة استخدام مريحة وفعالة مع أحدث المواصفات التقنية. يتميز بأداء قوي وموثوق يلبي احتياجاتك اليومية بكفاءة عالية. استثمار ذكي يوفر عليك الوقت والجهد.",
            f"يتميز {product_title} بجودة تصنيع عالية وأداء استثنائي يفوق التوقعات. مزود بخصائص متقدمة تسهل عليك المهام اليومية وتحقق نتائج ممتازة. منتج موثوق يجمع بين الجودة والسعر المناسب."
        ]
    
    # المكملات والصحة
    elif any(word in title_lower for word in ['فيتامين', 'مكمل', 'كبسولات', 'حبوب', 'علاج']):
        descriptions = [
            f"يوفر {product_title} الدعم الغذائي المثالي لصحة أفضل بمكونات طبيعية مختارة بعناية. تركيبة متوازنة تلبي احتياجات الجسم اليومية وتعزز الصحة العامة. منتج آمن ومطابق لأعلى معايير الجودة العالمية.",
            f"يتميز {product_title} بتركيبة فعالة تدعم وظائف الجسم الحيوية وتعزز الصحة بشكل طبيعي. مكونات نقية عالية الجودة تضمن الامتصاص الأمثل والنتائج الفعالة. مثالي للاستخدام اليومي ضمن نمط حياة صحي.",
            f"صمم {product_title} لتوفير العناصر الأساسية التي يحتاجها جسمك بصورة متوازنة وآمنة. يساعد على تحسين الصحة العامة والحيوية مع الاستخدام المنتظم. منتج موثوق يحظى بثقة آلاف المستخدمين."
        ]
    
    # الملابس والإكسسوارات
    elif any(word in title_lower for word in ['مشد', 'ملابس', 'شورت', 'قميص', 'ساعة']):
        descriptions = [
            f"يجمع {product_title} بين الجودة العالية والتصميم العصري ليمنحك الراحة والأناقة. مصنوع من مواد فاخرة تدوم طويلاً وتحافظ على شكلها بعد الاستخدام المتكرر. خيار مثالي لمن يبحث عن الجودة والمظهر المميز.",
            f"يتميز {product_title} بتصميم عملي وجودة تصنيع ممتازة تضمن الراحة والمتانة. مناسب للاستخدام اليومي ويمنحك إطلالة جذابة وعصرية. استثمار رائع يجمع بين الأناقة والجودة بسعر مناسب.",
            f"صمم {product_title} بعناية فائقة ليوفر لك الراحة القصوى مع مظهر أنيق ومميز. مواد عالية الجودة ومقاسات دقيقة تناسب الجميع. منتج عملي يدوم طويلاً ويحافظ على جودته مع الاستخدام."
        ]
    
    # افتراضي لأي منتج آخر
    else:
        descriptions = [
            f"يقدم {product_title} جودة استثنائية وأداء موثوق يلبي احتياجاتك بكفاءة عالية. مصنوع من مواد عالية الجودة تضمن المتانة والاستخدام طويل الأمد. خيار ممتاز يجمع بين الجودة والسعر المناسب.",
            f"يتميز {product_title} بمواصفات عالية الجودة وتصميم عملي يسهل الاستخدام اليومي. منتج موثوق يحقق نتائج ممتازة ويوفر قيمة حقيقية مقابل المال. استثمار ذكي لكل من يبحث عن الجودة والكفاءة.",
            f"صمم {product_title} ليوفر لك تجربة استخدام مميزة بأعلى معايير الجودة والأمان. يجمع بين الفعالية والموثوقية لتحقيق أفضل النتائج. منتج عملي يلبي توقعاتك ويفوقها بكل تأكيد."
        ]
    
    return random.choice(descriptions)

# ════════════════════════════════════════════════════════════
# دوال مساعدة
# ════════════════════════════════════════════════════════════

def create_slug(product):
    """إنشاء slug آمن من ID والعنوان"""
    # استخدام ID + أول 80 حرف من العنوان
    title_part = product['title'][:80].strip().replace(' ', '-')
    # إزالة جميع الحروف الخطرة
    title_part = re.sub(r'[<>:"/\\|?*+()]', '', title_part)
    
    return f"{product['id']}-{title_part}"

def generate_reviews(product_id, product_title):
    """توليد تقييمات عشوائية للمنتج"""
    num_reviews = random.randint(15, 20)
    reviews = []
    used_names = set()
    used_texts = set()
    
    for _ in range(num_reviews):
        # اختيار اسم غير مكرر
        available_names = [n for n in SAUDI_NAMES if n not in used_names]
        if not available_names:
            used_names.clear()
            available_names = SAUDI_NAMES.copy()
        
        name = random.choice(available_names)
        used_names.add(name)
        
        # اختيار نص تقييم غير مكرر
        available_texts = [t for t in REVIEW_TEMPLATES if t not in used_texts]
        if not available_texts:
            used_texts.clear()
            available_texts = REVIEW_TEMPLATES.copy()
        
        text = random.choice(available_texts)
        used_texts.add(text)
        
        # تقييم من 4 أو 5 نجوم
        rating = random.choice([4, 4, 5, 5, 5])  # ترجيح 5 نجوم
        
        # تاريخ عشوائي في آخر 6 أشهر
        days_ago = random.randint(1, 180)
        date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        reviews.append({
            'name': name,
            'rating': rating,
            'text': text,
            'date': date
        })
    
    # ترتيب حسب التاريخ (الأحدث أولاً)
    reviews.sort(key=lambda x: x['date'], reverse=True)
    
    return reviews

def generate_product_html(product, description, reviews):
    """توليد صفحة HTML لمنتج واحد"""
    slug = create_slug(product)
    discount = product['price'] - product['sale_price']
    discount_percentage = int((discount / product['price']) * 100) if product['price'] > 0 else 0
    
    # حساب متوسط التقييم
    avg_rating = sum(r['rating'] for r in reviews) / len(reviews)
    
    # توليد نجوم التقييم
    stars_html = '★' * int(avg_rating) + '☆' * (5 - int(avg_rating))
    
    # رسالة واتساب محسّنة
    product_url = f"https://sherow1982.github.io/alsooq-alsaudi/products/{slug}.html"
    whatsapp_message = f"""مرحباً، أريد طلب المنتج التالي:

📦 المنتج: {product['title']}
💰 السعر: {product['sale_price']} ريال
🔗 الرابط: {product_url}

📝 بيانات الطلب:
👤 الاسم: 
📍 العنوان: 
📱 رقم بديل: """
    
    # توليد HTML التقييمات
    reviews_html = '\n'.join([f"""
                <div class="review-item">
                    <div class="review-header">
                        <div class="reviewer-info">
                            <span class="reviewer-name">{review['name']}</span>
                            <span class="review-date">{review['date']}</span>
                        </div>
                        <div class="review-rating">{'★' * review['rating']}{'☆' * (5 - review['rating'])}</div>
                    </div>
                    <p class="review-text">{review['text']}</p>
                </div>
    """ for review in reviews])

    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description[:160]}">
    <meta property="og:title" content="{product['title']}">
    <meta property="og:description" content="{description[:200]}">
    <meta property="og:image" content="{product['image_link']}">
    <title>{product['title']} | السوق السعودي</title>

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
            line-height: 1.6;
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
            margin: 30px auto;
            padding: 0 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .product-main {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            padding: 30px;
        }}
        
        .product-gallery {{
            text-align: center;
        }}
        
        .product-image {{
            width: 100%;
            max-width: 500px;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        }}
        
        .product-info {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        
        .product-title {{
            font-size: 28px;
            font-weight: 600;
            color: #2c3e50;
        }}
        
        .product-rating {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 18px;
            color: #f39c12;
        }}
        
        .rating-count {{
            color: #7f8c8d;
            font-size: 14px;
        }}
        
        .price-section {{
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-right: 4px solid #27ae60;
        }}
        
        .current-price {{
            font-size: 36px;
            font-weight: bold;
            color: #27ae60;
        }}
        
        .old-price {{
            font-size: 20px;
            text-decoration: line-through;
            color: #95a5a6;
            margin-right: 10px;
        }}
        
        .discount-badge {{
            display: inline-block;
            background: #e74c3c;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
            margin-top: 10px;
        }}
        
        .whatsapp-btn {{
            background: #25D366;
            color: white;
            padding: 18px 30px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
            text-decoration: none;
            display: block;
        }}
        
        .whatsapp-btn:hover {{
            background: #128C7E;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(37, 211, 102, 0.3);
        }}
        
        .product-details {{
            padding: 30px;
            border-top: 1px solid #e0e0e0;
        }}
        
        .section-title {{
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 15px;
            color: #2c3e50;
        }}
        
        .description-text {{
            font-size: 16px;
            line-height: 1.8;
            color: #555;
        }}
        
        .reviews-section {{
            padding: 30px;
            border-top: 1px solid #e0e0e0;
        }}
        
        .reviews-summary {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        
        .avg-rating {{
            text-align: center;
        }}
        
        .avg-number {{
            font-size: 48px;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .avg-stars {{
            font-size: 24px;
            color: #f39c12;
        }}
        
        .review-item {{
            padding: 20px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .review-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }}
        
        .reviewer-name {{
            font-weight: 600;
            color: #2c3e50;
        }}
        
        .review-date {{
            color: #95a5a6;
            font-size: 14px;
            margin-right: 10px;
        }}
        
        .review-rating {{
            color: #f39c12;
        }}
        
        .review-text {{
            color: #555;
            line-height: 1.6;
        }}
        
        .product-id {{
            color: #95a5a6;
            font-size: 14px;
            margin-top: 10px;
        }}
        
        @media (max-width: 768px) {{
            .product-main {{
                grid-template-columns: 1fr;
            }}
            
            .current-price {{
                font-size: 28px;
            }}
            
            .product-title {{
                font-size: 22px;
            }}
        }}
    </style>
</head>
<body>
    <div class="topbar">
        <div class="topbar-content">
            <span>📞 خدمة العملاء: {WHATSAPP_NUMBER}</span>
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
                <img src="{product['image_link']}" alt="{product['title']}" class="product-image" loading="lazy">
            </div>
            
            <div class="product-info">
                <h1 class="product-title">{product['title']}</h1>
                
                <div class="product-rating">
                    <span class="avg-stars">{stars_html}</span>
                    <span class="rating-count">({len(reviews)} تقييم)</span>
                </div>
                
                <div class="price-section">
                    <div>
                        <span class="current-price">{product['sale_price']} ر.س</span>
                        <span class="old-price">{product['price']} ر.س</span>
                    </div>
                    <div class="discount-badge">وفّر {discount} ر.س ({discount_percentage}% خصم)</div>
                </div>
                
                <a href="https://wa.me/{WHATSAPP_NUMBER}?text={quote(whatsapp_message)}" 
                   class="whatsapp-btn" target="_blank">
                    📱 اطلب الآن عبر واتساب
                </a>
                
                <div class="product-id">رقم المنتج: PROD-{product['id']}</div>
            </div>
        </div>
        
        <div class="product-details">
            <h2 class="section-title">وصف المنتج</h2>
            <p class="description-text">{description}</p>
        </div>
        
        <div class="reviews-section">
            <h2 class="section-title">تقييمات العملاء</h2>
            
            <div class="reviews-summary">
                <div class="avg-rating">
                    <div class="avg-number">{avg_rating:.1f}</div>
                    <div class="avg-stars">{stars_html}</div>
                    <div class="rating-count">{len(reviews)} تقييم</div>
                </div>
            </div>
            
            <div class="reviews-list">
                {reviews_html}
            </div>
        </div>
    </div>
</body>
</html>"""
    
    return html


def main():
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  🚀 سكربت توليد صفحات المنتجات مع التقييمات والأوصاف    ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    # قراءة المنتجات
    try:
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            
            # إصلاح التنسيق
            if not content.startswith('['):
                content = '[' + content
            if not content.endswith(']'):
                if content.endswith(','):
                    content = content[:-1]
                content = content + ']'
            
            products = json.loads(content)
            
        print(f"✅ تم تحميل {len(products)} منتج من {PRODUCTS_FILE}")
    except Exception as e:
        print(f"❌ خطأ في قراءة الملف: {str(e)}")
        return
    
    # إنشاء مجلد products
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"✅ تم إنشاء مجلد {OUTPUT_DIR}")
    
    # توليد التقييمات والأوصاف
    print("\n📝 جاري توليد التقييمات والأوصاف...")
    all_reviews = {}
    all_descriptions = {}
    
    for product in products:
        product_id = str(product['id'])
        all_reviews[product_id] = generate_reviews(product['id'], product['title'])
        all_descriptions[product_id] = generate_smart_description(product['title'])
    
    # حفظ التقييمات
    with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_reviews, f, ensure_ascii=False, indent=2)
    print(f"✅ تم حفظ التقييمات في {REVIEWS_FILE}")
    
    # حفظ الأوصاف
    with open(DESCRIPTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_descriptions, f, ensure_ascii=False, indent=2)
    print(f"✅ تم حفظ الأوصاف في {DESCRIPTIONS_FILE}")
    
    # توليد صفحات المنتجات
    print("\n📦 جاري توليد صفحات المنتجات...")
    print("─" * 60)
    
    success_count = 0
    fail_count = 0
    
    for idx, product in enumerate(products, 1):
        product_id = str(product['id'])
        slug = create_slug(product)
        file_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
        
        try:
            description = all_descriptions[product_id]
            reviews = all_reviews[product_id]
            html_content = generate_product_html(product, description, reviews)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            success_count += 1
            if idx % 50 == 0:  # عرض التقدم كل 50 منتج
                print(f"✅ [{idx}/{len(products)}] {product['title'][:50]}...")
        
        except Exception as e:
            fail_count += 1
            print(f"❌ [{idx}/{len(products)}] خطأ: {str(e)}")
    
    print()
    print("─" * 60)
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                    📊 النتيجة النهائية                    ║")
    print("╠════════════════════════════════════════════════════════════╣")
    print(f"║  ✅ نجح: {success_count:4d} صفحة                              ║")
    print(f"║  ❌ فشل: {fail_count:4d} صفحة                               ║")
    print(f"║  📁 المجموع: {len(products):4d} صفحة                         ║")
    print("╠════════════════════════════════════════════════════════════╣")
    print(f"║  📄 ملف التقييمات: {REVIEWS_FILE:30s} ║")
    print(f"║  📄 ملف الأوصاف: {DESCRIPTIONS_FILE:32s} ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    print(f"📂 الملفات: {os.path.abspath(OUTPUT_DIR)}")
    print(f"🌐 افتح index.html لعرض المتجر")

if __name__ == "__main__":
    main()
