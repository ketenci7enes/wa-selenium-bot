import time
import random
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ================= AYARLAR VE DOSYA KONUMLARI =================
EXCEL_YOLU = Desktop\wp_bot\kisiler.xlsx"
FOTO1_YOLU = Desktop\wp_bot\mfoto1.jpeg"
FOTO2_YOLU = Desktop\wp_bot\mfoto2.jpeg"

# ================= HACKER TAKTİĞİ: RESİM GÖNDERME FONKSİYONU =================
def resim_gonder(driver, dosya_yolu):
    try:
        # 1. Artı (+) butonuna tıkla
        ekle_butonu = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="plus-rounded"] | //span[@data-icon="plus"]'))
        )
        ekle_butonu.click()
        time.sleep(1.5) 
        
        # 2. TARAYICIYA KANCA AT (Windows penceresini engelle ve input'u çal)
        driver.execute_script("""
            window.whatsappGalleryInput = null;
            if (!window.originalInputClick) {
                window.originalInputClick = HTMLInputElement.prototype.click;
            }
            // WhatsApp dosya seçiciyi açmaya çalıştığında araya giriyoruz
            HTMLInputElement.prototype.click = function() {
                if (this.type === 'file') {
                    window.whatsappGalleryInput = this; // Kanalı yakala
                    // originalInputClick fonksiyonunu çağırmıyoruz, böylece pencere açılmıyor!
                } else {
                    window.originalInputClick.call(this);
                }
            };
        """)

        try:
            # 3. Fotoğraflar ve Videolar butonuna tıkla (JS kancamız sayesinde pencere açılmayacak)
            foto_video_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Fotoğraflar ve Videolar"]'))
            )
            foto_video_btn.click()

            # 4. Çaldığımız gizli input kanalının gelmesini bekle
            galeri_input = None
            for _ in range(10): # 5 saniyeye kadar bekle
                galeri_input = driver.execute_script("return window.whatsappGalleryInput;")
                if galeri_input:
                    break
                time.sleep(0.5)
        finally:
            # İşimiz bitince tarayıcıyı normale döndür (Bozuk kalmasın)
            driver.execute_script("if(window.originalInputClick) { HTMLInputElement.prototype.click = window.originalInputClick; }")

        if not galeri_input:
            print("   ❌ Hata: Gizli kanal yakalanamadı!")
            return False

        # 5. Yakalanan doğru kanala fotoğrafı gönder
        galeri_input.send_keys(dosya_yolu)

        # 6. Resim önizleme ekranının gelmesini bekle
        time.sleep(2.5) 

        # 7. GÖNDER BUTONUNA JAVASCRIPT İLE ZORLA TIKLAMA
        gonder_butonu = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//span[@data-testid="wds-ic-send-filled"] | //span[@data-icon="wds-ic-send-filled"] | //span[@data-icon="send"]'))
        )
        driver.execute_script("arguments[0].click();", gonder_butonu)

        print(f"   -> Resim (Normal Format) başarıyla gönderildi.")
        time.sleep(3) 
        return True

    except Exception as e:
        print(f"   ❌ Hata: Resim yüklenemedi. Detay: {e}")
        return False

# ================= VERİ OKUMA İŞLEMİ =================
print("Excel dosyası okunuyor...")
wb = openpyxl.load_workbook(EXCEL_YOLU)
sayfa = wb.active
kisiler = []

for satir in sayfa.iter_rows(min_row=2, min_col=3, max_col=4, values_only=True):
    if satir[0] and satir[1]:
        isim = str(satir[0]).strip()
        numara = str(satir[1]).strip()
        if not numara.startswith('90'):
            numara = '90' + numara
        kisiler.append({'isim': isim, 'numara': numara})

print(f"Toplam {len(kisiler)} kişi hafızaya alındı.")

# ================= TARAYICI BAŞLATMA =================
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True) 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

driver.get("https://web.whatsapp.com")
print("\nLütfen QR kodu okutun ve sohbetler gelince terminale dönüp ENTER'a basın...")
input() 

# ================= ANA DÖNGÜ =================
basarili = 0
for kisi in kisiler[:3]: # Test için ilk 3 kişi
    isim, numara = kisi['isim'], kisi['numara']
    print(f"\n==========================================")
    print(f"İşlem Başlatıldı: {isim} ({numara})")
    
    try:
        driver.get(f"https://web.whatsapp.com/send?phone={numara}")
        
        # Sayfanın yüklendiğinden emin ol
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//span[@data-icon="plus-rounded"] | //span[@data-icon="plus"]'))
        )
        time.sleep(3)
        
        print("-> 1. Fotoğraf yollanıyor...")
        resim_gonder(driver, FOTO1_YOLU)
        
        print("-> 2. Fotoğraf yollanıyor...")
        resim_gonder(driver, FOTO2_YOLU)
        
        print("-> Metin mesajı yollanıyor...")
        mesaj_kutusu = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        
        mesaj_metni = f"Merhaba {isim}, bu mesaj bir test mesajıdır. Fotoğrafları normal formatta aldınız mı?"
        mesaj_kutusu.send_keys(mesaj_metni + Keys.ENTER)
        
        basarili += 1
        print(f"✅ Tüm içerikler başarıyla iletildi: {isim}")
        
    except Exception as e:
        print(f"❌ Hata: {isim} - Detay: {e}")

    # Spam Koruması
    bekleme = random.randint(60, 90)
    print(f"Spam koruması: {bekleme} saniye bekleniyor...")
    time.sleep(bekleme)

print(f"\n==========================================")
print(f"BİTTİ! Toplam {basarili} başarılı gönderim yapıldı.")