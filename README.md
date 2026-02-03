# OSS Indonesia Review Scraper

Scraper sederhana untuk mengambil ulasan aplikasi OSS Indonesia di Google Play Store. Output disimpan dalam format JSON dan CSV, serta menampilkan analisis ringkas di terminal.

## Fitur
- Mengambil data: nama pengguna, ulasan, rating, tanggal review, balasan developer
- Menyimpan data dalam format JSON dan CSV
- Analisis statistik sederhana (distribusi rating, rata-rata rating, jumlah balasan)
- Pagination otomatis untuk mengambil banyak review

## Prasyarat
- Python 3.8+
- Pip

## Instalasi
1. Clone repository ini.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Konfigurasi
Konfigurasi aplikasi dan output berada di `config.py`:
- `APP_CONFIG` untuk menentukan `app_id`, bahasa, dan negara.
- `OUTPUT_CONFIG` untuk lokasi file output JSON/CSV.

Contoh default:
```python
APP_CONFIG = {
    'app_id': 'id.go.oss',
    'app_name': 'OSS Indonesia',
    'country': 'id',
    'lang': 'id'
}
```

## Penggunaan
Jalankan script utama:
```bash
python scraper.py
```

Script akan:
1. Mengambil informasi dasar aplikasi.
2. Mengumpulkan review terbaru secara bertahap.
3. Menyimpan hasil ke `data/reviews.json` dan `data/reviews.csv`.
4. Menampilkan preview dan analisis ringkas.

## Struktur Output
Contoh field di `data/reviews.json` dan `data/reviews.csv`:
- `review_id`
- `user_name`
- `user_image`
- `rating`
- `review_content`
- `review_date`
- `thumbs_up`
- `reply_content`
- `reply_date`

## Struktur Proyek
```
.
├── config.py          # Konfigurasi aplikasi dan output
├── scraper.py         # Script utama scraper
├── data/              # Folder output JSON/CSV
└── requirements.txt   # Dependencies
```

## Catatan
- Scraper menggunakan delay untuk menghindari blocking.
- Pastikan koneksi internet stabil saat menjalankan scraper.
