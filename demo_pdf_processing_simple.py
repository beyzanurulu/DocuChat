"""
PDF Processing modülü basit demo script (Poppler gerektirmez)
Sadece model testleri ve veri yapılarını test eder
"""
import sys
import os
from pathlib import Path
import json

# Proje root'unu path'e ekle
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.models.document_models import DocumentElement, BoundingBox, ElementType, PageInfo, ProcessingResult
from src.pdf_processing.bbox_utils import BoundingBoxUtils


def test_models():
    """Model testleri"""
    print("🧪 Model testleri çalıştırılıyor...")
    
    # Test bounding box
    bbox = BoundingBox(x1=0.1, y1=0.2, x2=0.8, y2=0.6)
    print(f"✅ BoundingBox oluşturuldu: {bbox.to_tuple()}")
    print(f"   - Alan: {bbox.get_area():.4f}")
    
    # Test element
    element = DocumentElement(
        element_id="test_element_001",
        page_number=1,
        element_type=ElementType.PARAGRAPH,
        bbox=bbox,
        content="Bu bir test paragrafıdır. PDF processing modülümüz Qwen-VL model ile çalışır.",
        title="Test Paragrafı Başlığı",
        description="Bu element PDF processing pipeline test amaçlı oluşturulmuştur."
    )
    
    print(f"✅ DocumentElement oluşturuldu:")
    print(f"   - ID: {element.element_id}")
    print(f"   - Tip: {element.element_type}")
    print(f"   - Sayfa: {element.page_number}")
    print(f"   - İçerik uzunluğu: {len(element.content)} karakter")
    
    # Test page info
    page = PageInfo(
        page_number=1,
        width=800,
        height=600,
        elements=[element]
    )
    
    print(f"✅ PageInfo oluşturuldu:")
    print(f"   - Boyut: {page.width}x{page.height}")
    print(f"   - Element sayısı: {page.get_element_count()}")
    
    # Test processing result
    result = ProcessingResult(
        document_id="demo_doc_12345",
        filename="demo_document.pdf",
        total_pages=1,
        pages=[page],
        processing_time=2.5
    )
    
    print(f"✅ ProcessingResult oluşturuldu:")
    print(f"   - Döküman ID: {result.document_id}")
    print(f"   - Toplam sayfa: {result.total_pages}")
    print(f"   - Toplam element: {result.get_total_elements()}")
    print(f"   - İşlem süresi: {result.processing_time} saniye")
    
    return result


def test_bbox_utils():
    """BoundingBox utilities testleri"""
    print("\n🔧 BoundingBox Utils testleri...")
    
    # Normalization testi
    bbox_pixels = (100, 150, 300, 400)
    image_width, image_height = 800, 600
    
    normalized = BoundingBoxUtils.normalize_bbox(bbox_pixels, image_width, image_height)
    print(f"✅ Normalization:")
    print(f"   - Piksel: {bbox_pixels}")
    print(f"   - Normalize: {normalized.to_tuple()}")
    
    # Denormalization testi  
    pixels_back = BoundingBoxUtils.denormalize_bbox(normalized, image_width, image_height)
    print(f"   - Geri dönüşüm: {pixels_back}")
    
    # IoU testi
    bbox1 = BoundingBox(x1=0.1, y1=0.1, x2=0.5, y2=0.5)
    bbox2 = BoundingBox(x1=0.3, y1=0.3, x2=0.7, y2=0.7)
    
    iou = BoundingBoxUtils.calculate_iou(bbox1, bbox2)
    print(f"✅ IoU hesaplama:")
    print(f"   - Box1: {bbox1.to_tuple()}")
    print(f"   - Box2: {bbox2.to_tuple()}")
    print(f"   - IoU: {iou:.4f}")


def test_multiple_elements():
    """Çoklu element testleri"""
    print("\n📊 Çoklu element testleri...")
    
    elements = []
    
    # Farklı tipte elementler oluştur
    element_types = [ElementType.TITLE, ElementType.PARAGRAPH, ElementType.TABLE, ElementType.IMAGE]
    
    for i, elem_type in enumerate(element_types):
        element = DocumentElement(
            element_id=f"multi_elem_{i}",
            page_number=1,
            element_type=elem_type,
            bbox=BoundingBox(
                x1=0.1 + i*0.1, 
                y1=0.1 + i*0.15, 
                x2=0.9 - i*0.05, 
                y2=0.3 + i*0.1
            ),
            content=f"Bu bir {elem_type.value} elementidir. İçerik {i+1}.",
            title=f"{elem_type.value.title()} Başlığı {i+1}",
            description=f"{elem_type.value} tipinde element açıklaması"
        )
        elements.append(element)
    
    print(f"✅ {len(elements)} farklı tipte element oluşturuldu:")
    for elem in elements:
        print(f"   - {elem.element_type}: {elem.title}")
    
    # Filtreleme testi
    filtered = BoundingBoxUtils.filter_elements_by_area(elements, min_area=0.01, max_area=0.5)
    print(f"✅ Alan filtreleme: {len(filtered)}/{len(elements)} element kaldı")
    
    return elements


def export_test_data(result, elements):
    """Test verilerini export et"""
    print("\n💾 Test verileri export ediliyor...")
    
    # Output klasörü oluştur
    os.makedirs("demo_output", exist_ok=True)
    
    # ProcessingResult export
    with open("demo_output/test_processing_result.json", "w", encoding="utf-8") as f:
        json.dump(result.model_dump(), f, indent=2, ensure_ascii=False)
    
    # Elements export
    elements_data = [elem.model_dump() for elem in elements]
    with open("demo_output/test_elements.json", "w", encoding="utf-8") as f:
        json.dump(elements_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Test verileri kaydedildi:")
    print(f"   - demo_output/test_processing_result.json")
    print(f"   - demo_output/test_elements.json")


def main():
    """Ana test fonksiyonu"""
    print("=" * 60)
    print("🤖 DocuChat PDF Processing - Basit Demo")
    print("=" * 60)
    print("📝 Not: Bu demo Poppler gerektirmez, sadece veri yapılarını test eder")
    print()
    
    try:
        # Model testleri
        result = test_models()
        
        # BBox utils testleri
        test_bbox_utils()
        
        # Çoklu element testleri
        elements = test_multiple_elements()
        
        # Export
        export_test_data(result, elements)
        
        print("\n🎉 Tüm testler başarılı!")
        print("📁 Çıktı dosyaları demo_output/ klasöründe")
        
        print(f"\n📋 Sonraki adımlar:")
        print(f"1. Poppler'ı kur (install_poppler_windows.md'ye bak)")
        print(f"2. demo_pdf_processing.py'yi çalıştır") 
        print(f"3. Gerçek PDF analizi yap")
        
    except Exception as e:
        print(f"\n❌ Test hatası: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
