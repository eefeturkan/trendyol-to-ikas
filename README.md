# Trendyol'dan İkas'a Ürün Aktarımı

Bu proje, Trendyol platformundaki ürün verilerini İkas e-ticaret platformunun kabul ettiği formata dönüştürmek için geliştirilmiş bir Python uygulamasıdır.

## Özellikler

- Trendyol ürün Excel listesini İkas formatına dönüştürme
- Ürün varyasyonlarını doğru bir şekilde işleme (renk, ebat vb.)
- Ürün görselleri için çoklu resim URL'lerini destekleme
- Seçilebilir örnek sayısı ile test imkanı
- Otomatik çıktı dosyası oluşturma

## Kurulum

```bash
# Depoyu klonlayın
git clone https://github.com/eefeturkan/trendyol-to-ikas.git
cd trendyol-to-ikas

# Gerekli paketleri yükleyin
pip install pandas numpy openpyxl
```

## Kullanım

Ana script olan `trendyol_to_ikas.py` aşağıdaki parametrelerle çalıştırılabilir:

```bash
# Temel kullanım
python trendyol_to_ikas.py

# Belirli sayıda ürünü dönüştürme
python trendyol_to_ikas.py --sample 10

# Özel dosya adları ile kullanım
python trendyol_to_ikas.py --trendyol kendi_trendyol_dosyam.xlsx --ikas kendi_ikas_sablonum.xlsx --output sonuc.xlsx
```

### Parametreler

- `--trendyol`: Trendyol ürün listesi Excel dosyası (varsayılan: aktifurunler.xlsx)
- `--ikas`: İkas şablon Excel dosyası (varsayılan: ikas-urunler (1).xlsx)
- `--output`: Çıktı Excel dosyası (belirtilmezse otomatik tarihli isim oluşturulur)
- `--sample`: Dönüştürülecek ürün sayısı (belirtilmezse tüm ürünler dönüştürülür)

## Dosya Yapısı

- `trendyol_to_ikas.py`: Ana dönüşüm scripti
- `examine_excel.py`: Excel dosyalarını incelemek için yardımcı script
- `duzenlenmis_aciklamalar.txt`: Örnek düzenlenmiş ürün açıklamaları

## Gereksinimler

- Python 3.6+
- pandas
- numpy
- openpyxl

## Notlar

- İkas'a yükleme yaparken, çoklu görsel URL'leri noktalı virgül ile ayrılmış şekilde tek bir alanda birleştirilmelidir.
- Metadata alanları boş bırakılmalıdır, İkas bu alanları otomatik olarak dolduracaktır.
- TRUE/FALSE değerleri için metin formatında "TRUE" ve "FALSE" kullanılmalıdır.

## Lisans

MIT 