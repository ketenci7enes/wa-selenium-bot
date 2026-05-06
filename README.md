# wa-selenium-bot
Python ve Selenium ile geliştirilmiş, JS Hooking tekniği ile native dosya seçici engelini aşan WhatsApp Web otomasyon botu.
# 📱 WhatsApp Web Automation Bot (with Native Picker Bypass)

Bu proje, Python ve Selenium kullanarak WhatsApp Web üzerinden otomatik olarak medya (fotoğraf/video) ve metin mesajları göndermeyi sağlayan bir otomasyon botudur. 

Projenin en öne çıkan özelliği, WhatsApp'ın dinamik arayüzünde karşılaşılan **"Sticker/Dosya Seçici Kilitlenmesi" (Native File Picker Block)** sorununun ileri seviye bir **JavaScript Hooking (Monkey Patching)** tekniği ile aşılmış olmasıdır.

## ✨ Öne Çıkan Özellikler

* **Native File Picker Bypass (JS Hooking):** WhatsApp'ta "Fotoğraflar ve Videolar" butonuna tıklandığında işletim sisteminin "Dosya Seç" penceresinin açılması Selenium'u kilitler. Bu projede tarayıcının `HTMLInputElement.prototype.click` metoduna kanca atılarak (hooking) pencerenin açılması engellenmiş ve anlık olarak oluşturulan doğru DOM elementi yakalanarak dosya aktarımı sağlanmıştır.
* **Sticker (Çıkartma) Sorununa Kesin Çözüm:** Yanlış `input` etiketlerine dosya gönderildiğinde medyanın zorla çıkartma (sticker) yapılması sorunu, araya girme taktiği ile tamamen çözülmüştür. Fotoğraflar orijinal çözünürlüğünde galeri medyası olarak gider.
* **Excel Entegrasyonu:** Gönderilecek kişilerin isim ve numaraları `openpyxl` kullanılarak Excel (`.xlsx`) dosyasından dinamik olarak okunur.
* **Spam Koruması:** WhatsApp'ın anti-spam algoritmalarına takılmamak için gönderimler arasına rastgele gecikmeler (random sleep) eklenmiştir.
* **Sıfır Kurulum Derdi:** `webdriver-manager` sayesinde Chrome sürücüleri (ChromeDriver) otomatik olarak indirilir ve güncel tutulur.

## 🛠️ Kullanılan Teknolojiler
* **Python 3.x**
* **Selenium WebDriver** (Tarayıcı Otomasyonu)
* **JavaScript DOM Manipulation** (Hooking & Event Bypassing)
* **Openpyxl** (Veri Okuma)
* **Webdriver-Manager**

## 🚀 Kurulum ve Çalıştırma

1. Repoyu bilgisayarınıza klonlayın:
   ```bash
   git clone [https://github.com/KULLANICI_ADIN/whatsapp-automation-bot.git](https://github.com/KULLANICI_ADIN/whatsapp-automation-bot.git)
   cd whatsapp-automation-bot
GEREKLİ KÜTÜPHANELERİ YÜKLEYİN!
   pip install selenium openpyxl webdriver-manager
   BOTU ÇALIŞTIRIN 
   python wbot.py
   🧠 Teknik Detay: "Araya Girme" (Man-in-the-Middle) Mantığı
WhatsApp menüsündeki dosya yükleme kanalı, kullanıcı butona fiziksel olarak tıklayana kadar DOM'da var olmaz. Tıklama gerçekleştiğinde ise Windows'un Dosya Seçici penceresi açılır ve bot kilitlenir.

Bu kısır döngüyü kırmak için uygulanan algoritma:

Python üzerinden sayfaya özel bir JS scripti enjekte edilir.

Sayfadaki her tıklama dinlenir, eğer tıklanan element type="file" ise orijinal tıklama emri iptal edilir.

Böylece işletim sistemi penceresi açılmaz, ancak WhatsApp'ın oluşturduğu doğru input kanalı bir JS değişkenine (window.whatsappGalleryInput) hapsedilir.

Python bu gizli kanalı alır ve resmi direkt olarak içine enjekte eder (send_keys).

⚠️ Uyarı ve Yasal Sorumluluk
Bu yazılım tamamen eğitim ve süreç otomasyonu (kişisel kullanım) amacıyla geliştirilmiştir. Toplu spam mesaj gönderimi yapmak, WhatsApp Hizmet Şartları'na aykırıdır ve hesabınızın kalıcı olarak kapatılmasına yol açabilir. Projenin kötüye kullanımından doğacak hiçbir sorumluluk kabul edilmemektedir. Sorumlu kullanınız.

👨‍💻 Geliştirici
Mustafa Enes Ketenci

Bilgisayar Mühendisliği Öğrencisi | Süleyman Demirel Üniversitesi
