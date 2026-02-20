"""
PDF Processing modülü demo script
Qwen-VL ile PDF analizi örneği
"""
import sys
import os
from pathlib import Path

# Proje root'unu path'e ekle
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.pdf_processing.extractor import DocumentExtractor
from src.pdf_processing.bbox_utils import BoundingBoxUtils


def main():
    """Ana demo fonksiyonu"""
    print("🚀 PDF Processing Demo Başlatılıyor...")
    
    # Extractor oluştur
    extractor = DocumentExtractor(cache_dir="demo_cache")
    
    # Demo PDF dosyası kontrolü
    demo_pdf_path = "demo_files/sample.pdf"
    
    if not os.path.exists(demo_pdf_path):
        print(f"❌ Demo PDF dosyası bulunamadı: {demo_pdf_path}")
        print("\n📋 Demo için gerekli adımlar:")
        print("1. demo_files/ klasörü oluşturun")
        print("2. Rolls-Royce PDF'ini sample.pdf olarak kaydedin")
        print("3. Bu scripti tekrar çalıştırın")
        
        # Demo klasörünü oluştur
        os.makedirs("demo_files", exist_ok=True)
        
        print(f"\n✅ demo_files/ klasörü oluşturuldu")
        print("🔗 Rolls-Royce PDF indirme bağlantıları:")
        print("- https://www.rolls-royce.com/investors/annual-report")
        print("- https://investor.rolls-royce.com/annual-report")
        return
    
    try:
        print(f"📄 PDF analiz ediliyor: {demo_pdf_path}")
        
        # PDF'i işle
        result = extractor.extract_pdf(demo_pdf_path, use_cache=True)
        
        print(f"\n✅ PDF işleme tamamlandı!")
        print(f"📊 İstatistikler:")
        print(f"   - Toplam sayfa: {result.total_pages}")
        print(f"   - Toplam element: {result.get_total_elements()}")
        print(f"   - İşlem süresi: {result.processing_time:.2f} saniye")
        
        # Detaylı istatistikler
        stats = extractor.get_processing_stats(result)
        
        print(f"\n📈 Element tipi dağılımı:")
        for element_type, count in stats["elements_by_type"].items():
            print(f"   - {element_type}: {count}")
        
        print(f"\n📋 Sayfa bazında element sayısı:")
        for page_stat in stats["elements_per_page"][:5]:  # İlk 5 sayfa
            print(f"   - Sayfa {page_stat['page']}: {page_stat['count']} element")
        
        if len(stats["elements_per_page"]) > 5:
            print(f"   - ... ve {len(stats['elements_per_page']) - 5} sayfa daha")
        
        # Örnek elementleri göster
        print(f"\n🔍 Örnek elementler (ilk 3):")
        all_elements = result.get_all_elements()
        
        for i, element in enumerate(all_elements[:3]):
            print(f"\n   Element {i+1}:")
            print(f"   - Tip: {element.element_type}")
            print(f"   - Sayfa: {element.page_number}")
            print(f"   - Başlık: {element.title}")
            print(f"   - İçerik: {element.content[:100]}{'...' if len(element.content) > 100 else ''}")
            print(f"   - Bbox: ({element.bbox.x1:.3f}, {element.bbox.y1:.3f}, {element.bbox.x2:.3f}, {element.bbox.y2:.3f})")
        
        # JSON export
        output_file = "demo_output/processing_result.json"
        os.makedirs("demo_output", exist_ok=True)
        extractor.export_to_json(result, output_file)
        print(f"\n💾 Sonuç JSON olarak kaydedildi: {output_file}")
        
        # Visualization örneği (eğer PIL varsa)
        try:
            from PIL import Image
            import pdf2image
            
            print(f"\n🎨 İlk sayfa için bbox visualization oluşturuluyor...")
            
            # İlk sayfayı görsel'e çevir
            images = pdf2image.convert_from_path(demo_pdf_path, dpi=300, first_page=1, last_page=1)
            if images:
                first_page_image = images[0]
                first_page_elements = [elem for elem in all_elements if elem.page_number == 1]
                
                # Bbox'ları çiz
                vis_image = BoundingBoxUtils.visualize_bboxes(
                    first_page_image, 
                    first_page_elements,
                    "demo_output/page1_visualization.png"
                )
                
                print(f"✅ Visualization kaydedildi: demo_output/page1_visualization.png")
        
        except ImportError:
            print(f"\n⚠️  PIL/pdf2image bulunamadı, visualization atlanıyor")
        except Exception as e:
            print(f"\n⚠️  Visualization hatası: {e}")
        
        print(f"\n🎉 Demo tamamlandı!")
        print(f"📁 Çıktı dosyaları demo_output/ klasöründe")
        
    except Exception as e:
        print(f"\n❌ Demo hatası: {e}")
        import traceback
        traceback.print_exc()


def test_models():
    """Model test fonksiyonu"""
    print("\n🧪 Model testleri çalıştırılıyor...")
    
    from src.models.document_models import DocumentElement, BoundingBox, ElementType
    
    # Test element oluştur
    bbox = BoundingBox(x1=0.1, y1=0.2, x2=0.8, y2=0.6)
    element = DocumentElement(
        element_id="test_element",
        page_number=1,
        element_type=ElementType.PARAGRAPH,
        bbox=bbox,
        content="Bu bir test paragrafıdır.",
        title="Test Paragrafı",
        description="Bu element test amaçlı oluşturulmuştur."
    )
    
    print(f"✅ Test element oluşturuldu:")
    print(f"   - ID: {element.element_id}")
    print(f"   - Tip: {element.element_type}")
    print(f"   - Alan: {element.bbox.get_area():.4f}")
    print(f"   - İçerik uzunluğu: {len(element.content)} karakter")
    
    # Bbox utils test
    print(f"\n🔧 BoundingBox utils test:")
    pixels = BoundingBoxUtils.denormalize_bbox(bbox, 800, 600)
    print(f"   - Normalized: {bbox.to_tuple()}")
    print(f"   - Pixels (800x600): {pixels}")


if __name__ == "__main__":
    print("=" * 60)
    print("🤖 DocuChat PDF Processing Demo")
    print("=" * 60)
    
    # Model testleri
    test_models()
    
    # Ana demo
    main()
    
    print("=" * 60)
