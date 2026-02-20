"""
PDF conversion test script
"""
import pdf2image
import os

def test_pdf_conversion():
    """PDF conversion'ı test et"""
    pdf_path = "demo_files/sample.pdf"
    poppler_path = r"C:\Users\beyza\Desktop\capstone\poppler\poppler-23.11.0\Library\bin"
    
    print(f"🔍 PDF conversion test ediliyor...")
    print(f"📄 PDF: {pdf_path}")
    print(f"🔧 Poppler: {poppler_path}")
    print(f"📁 Dosya var mı: {os.path.exists(pdf_path)}")
    
    try:
        # PDF'i görsel'e çevir
        images = pdf2image.convert_from_path(
            pdf_path,
            dpi=150,  # Düşük DPI ile test
            first_page=1,
            last_page=1,  # Sadece ilk sayfa
            poppler_path=poppler_path
        )
        
        print(f"✅ Başarılı! {len(images)} sayfa convert edildi")
        print(f"📏 İlk sayfa boyutu: {images[0].size}")
        
        # Test görseli kaydet
        test_image_path = "test_output.png"
        images[0].save(test_image_path)
        print(f"💾 Test görseli kaydedildi: {test_image_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

if __name__ == "__main__":
    test_pdf_conversion()
