import pandas as pd

# Trendyol ürünleri dosyasını oku
trendyol_file = 'aktifurunler.xlsx'
try:
    trendyol_df = pd.read_excel(trendyol_file)
    print("\nTRENDYOL DOSYASI SÜTUNLARI:")
    print(trendyol_df.columns.tolist())
    print("\nTRENDYOL ÖRNEKLERİ (İlk 3 satır):")
    print(trendyol_df.head(3).to_string())
except Exception as e:
    print(f"Trendyol dosyası okunurken hata: {e}")

# İkas şablon dosyasını oku
ikas_file = 'ikas-urunler (1).xlsx'
try:
    ikas_df = pd.read_excel(ikas_file)
    print("\nİKAS DOSYASI SÜTUNLARI:")
    print(ikas_df.columns.tolist())
    print("\nİKAS ÖRNEKLERİ (İlk 3 satır):")
    print(ikas_df.head(3).to_string())
except Exception as e:
    print(f"İkas dosyası okunurken hata: {e}") 