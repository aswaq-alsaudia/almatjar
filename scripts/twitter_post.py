#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tweepy
import json
import os
import sys
import random
import requests
from io import BytesIO
from PIL import Image

# تحميل المنتجات
with open('products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# قراءة آخر منتج تم نشره
index_file = 'scripts/post_index.txt'
if os.path.exists(index_file):
    with open(index_file, 'r') as f:
        last_index = int(f.read().strip())
else:
    last_index = -1

# تحديد المنتج التالي
next_index = (last_index + 1) % len(products)
product = products[next_index]

# API Keys من Secrets
api_key = os.environ.get('TWITTER_API_KEY')
api_secret = os.environ.get('TWITTER_API_SECRET')
access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
access_secret = os.environ.get('TWITTER_ACCESS_SECRET')
bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')

if not all([api_key, api_secret, access_token, access_secret]):
    print("❌ Twitter API keys missing!")
    sys.exit(1)

try:
    # Twitter API v1.1 للميديا
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
    api_v1 = tweepy.API(auth)
    
    # Twitter API v2 للتويتات
    client = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret
    )
    
    # تحميل الصورة
    media_id = None
    if product.get('image_link'):
        try:
            response = requests.get(product['image_link'], timeout=10)
            if response.status_code == 200:
                # تحويل لـ JPEG إذا كانت MP4 أو غير مدعومة
                image = Image.open(BytesIO(response.content))
                if image.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                    image = background
                
                img_byte_arr = BytesIO()
                image.save(img_byte_arr, format='JPEG', quality=85)
                img_byte_arr.seek(0)
                
                media = api_v1.media_upload(filename="product.jpg", file=img_byte_arr)
                media_id = media.media_id
                print(f"✅ تم رفع الصورة: {media_id}")
        except Exception as e:
            print(f"⚠️ فشل رفع الصورة: {e}")
    
    # إنشاء التغريدة
    title = product['title']
    price = product.get('price', '')
    sale_price = product.get('sale_price', '')
    product_id = product['id']
    
    # رابط المنتج
    product_url = f"https://sherow1982.github.io/alsooq-alsaudi/products/{product_id}.html"
    
    # نص التغريدة
    if sale_price and sale_price != price:
        tweet_text = f"🔥 {title}\n\n💰 السعر: ~{price}~ ريال\n✨ العرض: {sale_price} ريال\n\n🛒 اطلب الآن:\n{product_url}\n\n#السوق_السعودي #عروض #تسوق"
    else:
        tweet_text = f"🔥 {title}\n\n💰 السعر: {price} ريال\n\n🛒 اطلب الآن:\n{product_url}\n\n#السوق_السعودي #عروض #تسوق"
    
    # نشر التغريدة
    if media_id:
        response = client.create_tweet(text=tweet_text, media_ids=[media_id])
    else:
        response = client.create_tweet(text=tweet_text)
    
    print(f"✅ تم النشر بنجاح: منتج #{product_id}")
    print(f"📊 Tweet ID: {response.data['id']}")
    
    # حفظ الفهرس الجديد
    with open(index_file, 'w') as f:
        f.write(str(next_index))
    
except Exception as e:
    print(f"❌ خطأ: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
