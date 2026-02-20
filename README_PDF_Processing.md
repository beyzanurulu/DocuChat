# PDF Processing Module 📄

DocuChat projesi için PDF işleme modülü. Qwen-VL model ile PDF'lerden akıllı içerik çıkarımı yapar.

## 🎯 Özellikler

- **Qwen-VL Entegrasyonu**: Görsel tabanlı PDF analizi
- **Element Detection**: Paragraf, tablo, görsel, başlık tespiti
- **Bounding Box**: Normalize edilmiş koordinat sistemi (0-1)
- **OCR & Content Extraction**: Akıllı içerik çıkarımı
- **Title & Description Generation**: AI ile başlık ve açıklama üretimi
- **Caching**: Hızlı tekrar işleme için cache sistemi
- **Visualization**: Bounding box görselleştirme

## 📁 Klasör Yapısı

```
src/pdf_processing/
├── __init__.py           # Module exports
├── qwen_processor.py     # Ana Qwen-VL processor
├── extractor.py          # Document extraction utilities  
└── bbox_utils.py         # Bounding box işlemleri

src/models/
└── document_models.py    # Pydantic veri modelleri

tests/
└── test_pdf_processing.py # Test dosyaları
```

## 🚀 Hızlı Başlangıç

### 1. Kurulum
```bash
pip install -r requirements.txt
```

### 2. Demo Çalıştırma
```bash
python demo_pdf_processing.py
```

### 3. Temel Kullanım
```python
from src.pdf_processing.extractor import DocumentExtractor

# Extractor oluştur
extractor = DocumentExtractor(cache_dir="cache")

# PDF'i işle
result = extractor.extract_pdf("sample.pdf")

# Sonuçları incele
print(f"Toplam sayfa: {result.total_pages}")
print(f"Toplam element: {result.get_total_elements()}")

# İstatistikleri görüntüle
stats = extractor.get_processing_stats(result)
print(stats)
```

## 📊 Veri Modelleri

### DocumentElement
```python
{
  "element_id": "page1_elem0_abc123",
  "page_number": 1,
  "element_type": "paragraph|table|image|title|list",
  "bbox": {
    "x1": 0.1, "y1": 0.2, 
    "x2": 0.9, "y2": 0.8
  },
  "content": "OCR ile çıkarılan metin",
  "title": "AI ile generate edilen başlık",
  "description": "Element açıklaması",
  "confidence": 0.85
}
```

### ProcessingResult
```python
{
  "document_id": "doc_unique_id",
  "filename": "sample.pdf", 
  "total_pages": 5,
  "pages": [PageInfo, ...],
  "processing_time": 45.2
}
```

## 🔧 Konfigürasyon

### QwenProcessor Settings
```python
processor = QwenProcessor(
    model_name="Qwen/Qwen2-VL-2B-Instruct"  # Model seçimi
)

# Custom DPI
images = processor.pdf_to_images("file.pdf", dpi=300)

# Custom prompt 
# qwen_processor.py içinde _create_analysis_prompt() fonksiyonunu düzenle
```

### Cache Ayarları
```python
extractor = DocumentExtractor(
    cache_dir="custom_cache"  # Cache klasörü
)

# Cache temizleme
extractor.clear_cache()
```

## 🎨 Visualization

### Bounding Box Çizimi
```python
from src.pdf_processing.bbox_utils import BoundingBoxUtils
from PIL import Image

# Görsel yükle
image = Image.open("page1.png")

# Elements var
elements = result.pages[0].elements

# Bbox'ları çiz
vis_image = BoundingBoxUtils.visualize_bboxes(
    image, elements, "output.png"
)
```

### Element Filtreleme
```python
# Alan bazında filtrele
filtered = BoundingBoxUtils.filter_elements_by_area(
    elements, 
    min_area=0.001,  # Çok küçük elementleri çıkar
    max_area=0.8     # Çok büyük elementleri çıkar
)

# Çakışan elementleri birleştir
merged = BoundingBoxUtils.merge_overlapping_boxes(
    elements, 
    iou_threshold=0.3
)
```

## 🧪 Test Etme

```bash
# Tüm testleri çalıştır
pytest tests/test_pdf_processing.py -v

# Specific test
pytest tests/test_pdf_processing.py::TestBoundingBoxUtils::test_calculate_iou -v
```

## 📝 Örnek Kullanım Senaryoları

### 1. Hızlı PDF Analizi
```python
# Sadece element sayısı öğrenmek için
result = extractor.extract_pdf("doc.pdf")
print(f"Bu PDF'de {result.get_total_elements()} element var")
```

### 2. Tablo Odaklı Analiz
```python
# Sadece tabloları bul
for page in result.pages:
    tables = page.get_elements_by_type(ElementType.TABLE)
    for table in tables:
        print(f"Sayfa {page.page_number}: {table.content}")
```

### 3. Export & Paylaşım
```python
# JSON olarak kaydet
extractor.export_to_json(result, "output.json")

# Statistikleri paylaş
stats = extractor.get_processing_stats(result)
print(json.dumps(stats, indent=2))
```

## ⚠️ Bilinen Limitler

- **Model boyutu**: Qwen-VL 2B model ~4GB RAM gerektirir
- **İşlem süresi**: Sayfa başına 3-10 saniye (GPU'ya göre)
- **PDF boyutu**: Çok büyük PDF'ler memory problemi yaratabilir
- **Dil desteği**: İngilizce optimize edilmiş

## 🔗 Diğer Modüllerle Entegrasyon

Bu modül vector database ve LLM modülleri ile entegre olacak:

```python
# Vector DB için hazırlık
all_elements = result.get_all_elements()
for element in all_elements:
    # Element'i embedding için hazırla
    text_for_embedding = f"{element.title} {element.content}"
    metadata = {
        "page": element.page_number,
        "bbox": element.bbox.to_tuple(),
        "type": element.element_type
    }
```

## 🆘 Sorun Giderme

### CUDA Memory Error
```python
# CPU'da çalıştır
processor = QwenProcessor()
processor.device = torch.device("cpu")
```

### PDF2Image Error
```bash
# Poppler kurulum (Ubuntu)
sudo apt-get install poppler-utils

# Poppler kurulum (Windows)
# https://github.com/oschwartz10612/poppler-windows
```

### Cache Problems
```python
# Cache'i temizle ve yeniden dene
extractor.clear_cache()
result = extractor.extract_pdf("file.pdf", use_cache=False)
```

---

**🎉 PDF Processing modülü hazır!** 

Diğer modüllerle entegrasyon için:
- Vector Database modülü (Pinecone)
- LLM modülü (Hermes 2 Pro)
- UI modülü (Gradio)
