import requests
import json
from datetime import datetime

# Source JSON URL
JSON_URL = "https://raw.githubusercontent.com/MohammadKobirShah/AynaOTT-M3U/refs/heads/main/output/aynaott_live.json"
OUTPUT_M3U = "playlist.m3u"

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

    # JSON स्ट्रक्चर অনুযায়ী চ্যানেল কনভার্ট করা
    channels = []
    if isinstance(data, list):
        channels = data
    elif isinstance(data, dict):
        channels = data.get("channels", data.get("data", []))

    for channel in channels:
        name = channel.get("name") or channel.get("channel_name") or channel.get("title") or "Unknown Channel"
        logo = channel.get("logo") or channel.get("channel_logo") or channel.get("icon") or ""
        group = channel.get("group") or channel.get("category") or "General"
        url = channel.get("url") or channel.get("stream_url") or channel.get("link") or ""
        
        # ইউজার এডিটিং / কাস্টম হেডারের প্রয়োজন থাকলে
        user_agent = channel.get("user_agent") or channel.get("userAgent") or ""

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
        print("Generating M3U playlist...")
        m3u_text = generate_m3u(json_data)
        
        # ফাইল সেভ করা
        with open(OUTPUT_M3U, "w", encoding="utf-8") as f:
            f.write(m3u_text)
        print(f"Successfully updated {OUTPUT_M3U}")
    else:
        print("Failed to update playlist.")

if __name__ == "__main__":
    main()
