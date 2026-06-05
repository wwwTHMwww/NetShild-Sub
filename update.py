#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import re
import sys
from datetime import datetime

# رنگ‌های ترمینال برای لاگ زیبا
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def log_info(msg):
    print(f"{GREEN}[✓]{RESET} {msg}")

def log_error(msg):
    print(f"{RED}[✗]{RESET} {msg}")

def log_step(msg):
    print(f"{BLUE}➜{RESET} {msg}")

SOURCE_URL = "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/V2Ray-Config-By-EbraSha.txt"
OUTPUT_FILE = "sub.txt"

def fetch_configs():
    log_step(f"در حال دریافت کانفیگ‌ها از: {SOURCE_URL}")
    try:
        with urllib.request.urlopen(SOURCE_URL, timeout=30) as response:
            data = response.read().decode('utf-8')
            log_info(f"دریافت موفق - {len(data)} کاراکتر")
            return data
    except Exception as e:
        log_error(f"خطا در دریافت: {str(e)}")
        return None

def clean_and_tag_configs(raw_text):
    lines = raw_text.splitlines()
    cleaned = []
    removed_count = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # حذف "# By EbraSha" و هر ایموجی بعد از آن
        # الگو: # By EbraSha و هر کاراکتر (از جمله ایموجی) تا آخر خط
        cleaned_line = re.sub(r'#\s*By\s+EbraSha.*$', '', line).strip()
        
        # اگر خط بعد از حذف خالی شد، ردش کن
        if not cleaned_line:
            removed_count += 1
            continue
        
        # اضافه کردن #netishield به انتها
        final_line = cleaned_line + " #netishield"
        cleaned.append(final_line)
    
    return cleaned, removed_count

def save_configs(configs_list):
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("\n".join(configs_list))
        log_info(f"فایل {OUTPUT_FILE} ذخیره شد - {len(configs_list)} کانفیگ معتبر")
        return True
    except Exception as e:
        log_error(f"خطا در ذخیره فایل: {str(e)}")
        return False

def main():
    print(f"\n{YELLOW}🔄 NetShild-Sub Updater - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}\n")
    
    raw = fetch_configs()
    if raw is None:
        log_error("پایان کار به دلیل خطا.")
        sys.exit(1)
    
    log_step("پردازش و پاکسازی کانفیگ‌ها...")
    cleaned_configs, removed = clean_and_tag_configs(raw)
    
    if not cleaned_configs:
        log_error("هیچ کانفیگ معتبری پیدا نشد!")
        sys.exit(1)
    
    log_info(f"تعداد کانفیگ نهایی: {len(cleaned_configs)}")
    if removed > 0:
        log_info(f"{removed} خط ناخواسته حذف شد.")
    
    if save_configs(cleaned_configs):
        log_info("✅ به‌روزرسانی با موفقیت کامل شد.")
        # نمایش چند نمونه اول
        preview_count = min(3, len(cleaned_configs))
        if preview_count > 0:
            print(f"\n{YELLOW}📌 نمونه از کانفیگ‌های ذخیره شده:{RESET}")
            for i in range(preview_count):
                print(f"  {cleaned_configs[i][:80]}...")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
