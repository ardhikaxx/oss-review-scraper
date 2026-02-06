import json
import csv
import time
from datetime import datetime
from google_play_scraper import app, reviews, Sort
import pandas as pd
from config import APP_CONFIG, OUTPUT_CONFIG

def scrape_oss_reviews():
    """Fungsi utama untuk scraping review OSS Indonesia"""
    
    print(f"Memulai scraping review untuk {APP_CONFIG['app_name']}...")
    
    try:
        # Mendapatkan informasi dasar aplikasi
        app_info = app(
            APP_CONFIG['app_id'],
            lang=APP_CONFIG['lang'],
            country=APP_CONFIG['country']
        )
        
        print(f"\nInformasi Aplikasi:")
        print(f"Nama: {app_info['title']}")
        print(f"Rating: {app_info['score']}")
        print(f"Jumlah Review: {app_info['reviews']}")
        print(f"Developer: {app_info['developer']}\n")
        
        # Mengambil review dengan pagination
        all_reviews = []
        continuation_token = None
        
        for i in range(20):
            print(f"Mengambil batch review ke-{i+1}...")
            
            result, continuation_token = reviews(
                APP_CONFIG['app_id'],
                lang=APP_CONFIG['lang'],
                country=APP_CONFIG['country'],
                sort=Sort.NEWEST,
                count=100,
                continuation_token=continuation_token
            )
            
            all_reviews.extend(result)
            
            if not continuation_token:
                break
                
            time.sleep(2)  # Delay untuk menghindari blocking
        
        # Memproses data review
        processed_reviews = []
        
        for rev in all_reviews:
            # Format tanggal
            review_date = rev['at'].strftime('%Y-%m-%d %H:%M:%S')
            
            processed_reviews.append({
                'review_id': rev['reviewId'],
                'user_name': rev['userName'],
                'user_image': rev['userImage'],
                'rating': rev['score'],
                'review_content': rev['content'],
                'review_date': review_date,
                'thumbs_up': rev['thumbsUpCount'],
                'reply_content': rev['replyContent'] if rev['replyContent'] else '',
                'reply_date': rev['repliedAt'].strftime('%Y-%m-%d %H:%M:%S') if rev['repliedAt'] else ''
            })
        
        print(f"\nTotal review berhasil diambil: {len(processed_reviews)}")
        
        # Menyimpan data ke JSON
        save_to_json(processed_reviews)
        
        # Menyimpan data ke CSV
        save_to_csv(processed_reviews)
        
        # Menampilkan preview data
        display_preview(processed_reviews)
        
        return processed_reviews
        
    except Exception as e:
        print(f"Error saat scraping: {str(e)}")
        return []

def save_to_json(reviews_data):
    """Menyimpan data ke format JSON"""
    os.makedirs('data', exist_ok=True)
    
    output_data = {
        'app_id': APP_CONFIG['app_id'],
        'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_reviews': len(reviews_data),
        'reviews': reviews_data
    }
    
    with open(OUTPUT_CONFIG['json_file'], 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"Data disimpan ke: {OUTPUT_CONFIG['json_file']}")

def save_to_csv(reviews_data):
    """Menyimpan data ke format CSV"""
    os.makedirs('data', exist_ok=True)
    
    df = pd.DataFrame(reviews_data)
    df.to_csv(OUTPUT_CONFIG['csv_file'], index=False, encoding='utf-8-sig')
    
    print(f"Data disimpan ke: {OUTPUT_CONFIG['csv_file']}")

def display_preview(reviews_data):
    """Menampilkan preview data"""
    print("\nPreview Data Review:")
    print("=" * 80)
    
    for i, rev in enumerate(reviews_data[:3]):  # Tampilkan 3 review pertama
        print(f"\nReview #{i+1}:")
        print(f"Nama: {rev['user_name']}")
        print(f"Rating: {'★' * rev['rating']}{'☆' * (5 - rev['rating'])} ({rev['rating']}/5)")
        print(f"Tanggal: {rev['review_date']}")
        print(f"Ulasan: {rev['review_content'][:100]}..." if len(rev['review_content']) > 100 else f"Ulasan: {rev['review_content']}")
        print("-" * 40)

def analyze_reviews(reviews_data):
    """Analisis sederhana terhadap data review"""
    if not reviews_data:
        print("Tidak ada data untuk dianalisis")
        return
    
    df = pd.DataFrame(reviews_data)
    
    print("\n📊 Analisis Data Review:")
    print("=" * 50)
    
    # Statistik rating
    rating_stats = df['rating'].value_counts().sort_index()
    print("\nDistribusi Rating:")
    for rating, count in rating_stats.items():
        percentage = (count / len(df)) * 100
        print(f"Rating {rating}: {count} review ({percentage:.1f}%)")
    
    # Rating rata-rata
    avg_rating = df['rating'].mean()
    print(f"\nRating Rata-rata: {avg_rating:.2f}/5.0")
    
    # Review dengan balasan
    replied_reviews = df[df['reply_content'] != '']
    print(f"Review yang dibalas: {len(replied_reviews)} ({len(replied_reviews)/len(df)*100:.1f}%)")

if __name__ == "__main__":
    import os
    
    # Pastikan folder data ada
    os.makedirs('data', exist_ok=True)
    
    # Jalankan scraping
    reviews_data = scrape_oss_reviews()
    
    # Analisis data jika berhasil
    if reviews_data:
        analyze_reviews(reviews_data)