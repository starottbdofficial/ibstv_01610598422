import requests
import json
from datetime import datetime
import re

# Source JSON URL
JSON_URL = "https://raw.githubusercontent.com/MohammadKobirShah/AynaOTT-M3U/refs/heads/main/output/aynaott_live.json"
OUTPUT_M3U = "playlist.m3u"

# Keywords used to match channel names and assign the specific updated categories
CATEGORY_KEYWORDS = {
    "SPORTS": [
        "sport", "sports", "t sports", "star sports", "sony ten", "ten", "cricket", "football", 
        "eurosport", "willow", "ptv sports", "sky sports", "fancode", "sports18"
    ],
    "ISLAMIC": [
        "islam", "islamic", "quran", "makkah", "madinah", "peace tv", "iqra", "madani", 
        "sunnah", "deen", "kaba", "prophet"
    ],
    "CARTOON": [
        "cartoon", "nick", "nickelodeon", "pogo", "disney", "hungama", "animax", "kids", 
        "sonic", "duronto", "boomerang", "baby"
    ],
    "MUSIC": [
        "music", "sangeet", "zoom", "mtv", "vh1", "musiq", "gane", "song", "b4u music", 
        "9xm", "9x jalwa", "zing"
    ],
    "MOVIES": [
        "movie", "cinema", "film", "zee cinema", "star gold", "sony max", "colors cineplex", 
        "hbo", "star movies", "wb", "zee bangla cinema", "jalsha movies"
    ],
    "BANGLADESH": [
        "somoy", "jamuna", "ekattor", "independent", "channel i", "ati", "atn bangla", 
        "atn news", "ntv", "rtv", "deepto", "bangla vision", "boishakhi", "dbc", "news24", 
        "maasranga", "desh tv", "channel 24", "bijoy tv", "nagorik", "saatv", "titas"
    ],
    "INDIAN BANGLA": [
        "zee bangla", "star jalsha", "colors bangla", "sun bangla", "enterr10 bangla", 
        "rupeshi bangla", "akash aath"
    ],
    "INDIAN": [
        "star plus", "colors", "zee tv", "sony tv", "sab tv", "star bharat", "dd", 
        "aaj tak", "ndtv", "india today", "zee news", "republic", "news18"
    ]
}

def categorize_channel(channel_name, original_group=""):
    """
    Determines the appropriate category for a channel based on its name and original group.
    """
    text_to_check = f"{channel_name} {original_group}".lower()
    
    # Priority check for explicit matches
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            # Match whole words or standard substring boundaries
            if re.search(r'\b' + re.escape(keyword) + r'\b', text_to_check):
                return category

    # Secondary check without word boundaries for custom channel tags
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_to_check:
                return category

    # Default fallback category if no keyword matches
    return "OTHERS"

def fetch_json_data(url):
    """JSON ডেটা রিড করার ফাংশন"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching JSON: {e}")
        return None

def generate_m3u(data):
    """M3U প্লেলিস্ট তৈরি করার ফাংশন"""
    # বর্তমান তারিখ এবং সময় (UTC)
    current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    # প্লেলিস্টের হেডার অংশ
    m3u_header = f"""#EXTM3U
# Playlist update dates and times: {current_time} UTC
# Playlist owner: STAR OTT BD
# Playlist Creator: MD shakib Hasan
# What's app: +8801610598422
# Telegram: https://t.me/ibstvbdn# Our official partner : IBS TV. STAR SHARE. OPPLEX.
"""
    
    m3u_content = m3u_header

    # JSON স্ট্রাকচার অনুযায়ী চ্যানেল কনভার্ট করা
    channels = []
    if isinstance(data, list):
        channels = data
    elif isinstance(data, dict):
        channels = data.get("channels", data.get("data", []))

    for channel in channels:
        name = channel.get("name") or channel.get("channel_name") or channel.get("title") or "Unknown Channel"
        logo = channel.get("logo") or channel.get("channel_logo") or channel.get("icon") or ""
        original_group = channel.get("group") or channel.get("category") or ""
        url = channel.get("url") or channel.get("stream_url") or channel.get("link") or ""
        user_agent = channel.get("user_agent") or channel.get("userAgent") or ""

        # Update category using auto-categorization logic
        group = categorize_channel(name, original_group)

        if url:
            # M3U ট্যাগ তৈরি
            extinf = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}", {name}\n'
            if user_agent:
                extinf += f'#EXTVLCOPT:http-user-agent={user_agent}\n'
            
            m3u_content += extinf + f'{url}\n\n'

    return m3u_content

def main():
    print("Fetching JSON data...")
    json_data = fetch_json_data(JSON_URL)
    
    if json_data:
        print("Categorizing channels and generating M3U playlist...")
        m3u_text = generate_m3u(json_data)
        
        # ফাইল সেভ করা
        with open(OUTPUT_M3U, "w", encoding="utf-8") as f:
            f.write(m3u_text)
        print(f"Successfully updated {OUTPUT_M3U} with custom categories!")
    else:
        print("Failed to update playlist.")

if __name__ == "__main__":
    main()
```
