import pandas as pd
import numpy as np
import os
import argparse
from datetime import datetime

def trendyol_to_ikas(trendyol_file, ikas_template_file, output_file=None, sample_count=None):
    """
    Trendyol ürün listesini İkas formatına dönüştürür.
    
    Args:
        trendyol_file: Trendyol ürün listesi Excel dosyası
        ikas_template_file: İkas şablon Excel dosyası
        output_file: Çıktı Excel dosyası (Belirtilmezse otomatik oluşturulur)
        sample_count: Dönüştürülecek ürün sayısı (None ise tümü dönüştürülür)
    """
    print(f"Trendyol dosyası okunuyor: {trendyol_file}")
    trendyol_df = pd.read_excel(trendyol_file)
    
    print(f"İkas şablonu okunuyor: {ikas_template_file}")
    ikas_template_df = pd.read_excel(ikas_template_file)
    
    # Eğer belirli sayıda ürün isteniyorsa filtreleme yap
    if sample_count:
        # Önce benzersiz 'Model Kodu' değerlerini al
        unique_model_codes = trendyol_df['Model Kodu'].unique()
        
        # Eğer istenen sayıdan az benzersiz model kodu varsa, tümünü al
        if len(unique_model_codes) <= sample_count:
            selected_model_codes = unique_model_codes
        else:
            # İstenen sayıda benzersiz model kodu al
            selected_model_codes = unique_model_codes[:sample_count]
        
        # Seçilen model kodlarına sahip ürünleri filtrele
        trendyol_df = trendyol_df[trendyol_df['Model Kodu'].isin(selected_model_codes)]
        print(f"{len(selected_model_codes)} farklı model kodu için toplam {len(trendyol_df)} ürün satırı seçildi.")
    
    # Yeni İkas DataFrame'i oluştur (şablon sütunlarıyla)
    ikas_df = pd.DataFrame(columns=ikas_template_df.columns)
    
    # Model kodlarına göre ürünleri grupla
    grouped_products = trendyol_df.groupby('Model Kodu')
    
    # Her bir benzersiz ürün için işlem yap
    current_group_id = 1
    for model_code, group in grouped_products:
        print(f"Model Kodu: {model_code} işleniyor, varyasyon sayısı: {len(group)}")
        
        # Ana ürün bilgilerini al (ilk satırdan)
        first_product = group.iloc[0]
        
        # Ürünün ana özelliklerini belirle
        product_name = first_product['Ürün Adı']
        description = first_product['Ürün Açıklaması']
        price = first_product['Piyasa Satış Fiyatı (KDV Dahil)']
        brand = first_product['Marka']
        category = first_product['Kategori İsmi']
        desi = first_product['Desi']
        
        # Varyasyon tipi olarak "Ürün Rengi" kullanılacak
        variant_type = "Renk"
        
        # Grup içindeki her bir varyasyon için
        for idx, variant in group.iterrows():
            # Yeni bir satır oluştur
            new_row = pd.Series(index=ikas_df.columns)
            
            # Ürün grup ID'sini ayarla (aynı model kodundaki ürünler için aynı grup ID)
            new_row['Ürün Grup ID'] = current_group_id
            
            # Varyant ID'sini belirle
            new_row['Varyant ID'] = idx + 1  # Benzersiz bir ID
            
            # Temel ürün bilgilerini doldur
            new_row['İsim'] = str(product_name)  # String'e dönüştür
            new_row['Açıklama'] = str(description) if pd.notna(description) else ""
            new_row['Satış Fiyatı'] = price
            new_row['Alış Fiyatı'] = price * 0.7  # Örnek olarak, alış fiyatını satış fiyatının %70'i olarak ayarla
            new_row['Barkod Listesi'] = variant['Barkod']
            new_row['SKU'] = f"{model_code}-{variant['Ürün Rengi']}"
            new_row['Silindi mi?'] = "FALSE"  # "Hayır" yerine "FALSE" kullan
            new_row['Marka'] = brand
            new_row['Kategoriler'] = category
            
            # Görsel URL'lerini işle - tüm görselleri noktalı virgül ile ayırarak birleştir
            images = []
            for i in range(1, 8):  # Görsel 1 - Görsel 7
                img_col = f'Görsel {i}'
                if img_col in variant and pd.notna(variant[img_col]):
                    images.append(variant[img_col])
            
            # Tüm görselleri noktalı virgülle ayırarak tek bir URL alanında birleştir
            if images:
                new_row['Resim URL'] = ";".join(images)
            
            # Metadata alanlarını boş bırak (İkas otomatik oluşturacak)
            # new_row['Metadata Başlık'] = str(product_name)
            # new_row['Metadata Açıklama'] = meta_desc
            
            # Slug oluştur
            slug = str(product_name).lower().replace(' ', '-').replace('(', '').replace(')', '')
            new_row['Slug'] = slug
            
            # Stok bilgisini doldur (varsayılan olarak 10 adet)
            new_row['Stok:Ana Depo'] = 10
            
            # Ürün tipini ayarla
            new_row['Tip'] = "Fiziksel"
            
            # Varyasyon bilgilerini doldur
            new_row['Varyant Tip 1'] = variant_type
            new_row['Varyant Değer 1'] = variant['Ürün Rengi']
            
            # Eğer boyut/ebat varsa, bunu da ikinci varyant olarak ekle
            if 'Boyut/Ebat' in variant and pd.notna(variant['Boyut/Ebat']):
                new_row['Varyant Tip 2'] = "Ebat"
                new_row['Varyant Değer 2'] = variant['Boyut/Ebat']
            
            # Desi bilgisini ekle
            new_row['Desi'] = desi if pd.notna(desi) else 1
            
            # Diğer gerekli alanları doldur
            new_row['Varyant Aktiflik'] = "TRUE"  # "Evet" yerine "TRUE" kullan
            new_row['Stoğu Tükenince Satmaya Devam Et'] = "FALSE"  # "Hayır" yerine "FALSE" kullan
            new_row['Satış Kanalı:turkanlarhome'] = "VISIBLE"  # "Evet" yerine "VISIBLE" kullan
            
            # DataFrames'e satırı ekle
            ikas_df = pd.concat([ikas_df, pd.DataFrame([new_row])], ignore_index=True)
        
        # Sonraki ürün grubu için grup ID'sini artır
        current_group_id += 1
    
    # Eksik değerleri NaN ile doldur
    ikas_df = ikas_df.fillna(np.nan)
    
    # Çıktı dosyasını belirle
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"ikas_urunler_converted_{timestamp}.xlsx"
    
    # Excel dosyasına yazdır
    print(f"Sonuçlar {output_file} dosyasına yazılıyor...")
    ikas_df.to_excel(output_file, index=False)
    print(f"Dönüşüm tamamlandı! Toplam {len(ikas_df)} ürün varyasyonu oluşturuldu.")
    
    return output_file

if __name__ == "__main__":
    # Komut satırı argümanlarını tanımla
    parser = argparse.ArgumentParser(description='Trendyol ürün listesini İkas formatına dönüştürür.')
    parser.add_argument('--trendyol', default='aktifurunler.xlsx',
                        help='Trendyol ürün listesi Excel dosyası')
    parser.add_argument('--ikas', default='ikas-urunler (1).xlsx',
                        help='İkas şablon Excel dosyası')
    parser.add_argument('--output', default=None,
                        help='Çıktı Excel dosyası (Belirtilmezse otomatik oluşturulur)')
    parser.add_argument('--sample', type=int, default=None,
                        help='Dönüştürülecek ürün sayısı (Belirtilmezse tümü dönüştürülür)')
    
    # Argümanları ayrıştır
    args = parser.parse_args()
    
    # Dönüşümü gerçekleştir
    output_file = trendyol_to_ikas(
        args.trendyol,
        args.ikas,
        args.output,
        args.sample
    )
    
    print(f"\nÇıktı dosyası: {output_file}")
    print("\nKullanım örnekleri:")
    print("  python trendyol_to_ikas.py --sample 10  # İlk 10 ürünü dönüştür")
    print("  python trendyol_to_ikas.py --output ikas_sonuc.xlsx  # Belirtilen dosyaya kaydet")
    print("  python trendyol_to_ikas.py --trendyol baska_dosya.xlsx  # Farklı bir Trendyol dosyası kullan") 