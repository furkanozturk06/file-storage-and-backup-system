# Dosya Depolama ve Yedekleme Sistemi

Bu proje, sistemdeki dosya güvenliğini artırmak, belirlenen dosyaları gerçek zamanlı yedeklemek, logları izlemek ve kullanıcı davranışlarını analiz ederek güvenlik ihlallerini tespit etmek amacıyla geliştirilmiştir.

Proje **Python** dili kullanılarak; **Multiprocessing (Çoklu İşlem)** ve **Multithreading (Çoklu İş Parçacığı)** mimarileri üzerine inşa edilmiştir.

## 🎯 Projenin Amacı ve Kapsam
Sistem; güvenli profil yönetimi, otomatik dosya yedekleme/senkronizasyon ve siber güvenlik tehditlerine (anormal davranışlar) karşı gerçek zamanlı izleme sağlar.

## 🚀 Özellikler

### 1. Kullanıcı Profilleri ve Arayüz
Kullanıcılar sisteme giriş yaparak arayüz üzerinden işlemlerini gerçekleştirebilir.
* **Bireysel Kullanıcılar:**
    * Dosya yükleme, indirme ve düzenleme.
    * **Takım Sistemi:** Başka kullanıcıları takım üyesi ekleme ve dosya paylaşımı.
    * Güvenli Parola Yönetimi (Şifreli saklama).
* **Sistem Yöneticileri:**
    * Kullanıcıların depolama limitlerini belirleme.
    * Parola değiştirme taleplerini onaylama.
    * Tüm sistem dosyalarına, loglara ve şifreli parolalara erişim.

### 2. Dosya Yedekleme ve Senkronizasyon
* Belirlenen kaynak dizindeki değişiklikler bir **Process** tarafından izlenir.
* Değişiklik algılandığında dosyalar hedef dizine kopyalanır ve senkronize edilir.
* Kopyalama işlemi arayüzü dondurmamak için **Thread** ile yapılır.

### 3. Loglama ve Anormallik Tespiti
Sistem logları `.txt` formatında tutulur ve sürekli izlenir. Aşağıdaki durumlar "Anormal Durum" olarak tespit edilir ve uyarı verilir:
* Yedekleme/Senkronizasyon işleminin beklenmedik kesintisi.
* Kısa sürede olağandışı dosya yükleme/indirme.
* Yetkisiz dosya paylaşım girişimleri.
* Kısa sürede 3'ten fazla başarısız giriş denemesi.

### 4. Kullanıcı Davranışı Analizi
* Kullanıcıların giriş-çıkış aktiviteleri izlenir.
* Şüpheli durumlar (örn: sürekli parola değiştirme isteği) tespit edildiğinde yöneticiye ve kullanıcıya bildirim gönderilir.

## ⚙️ Teknik Mimari (Process & Thread Yapısı)

Proje gereksinimlerine uygun olarak aşağıdaki çoklu işlem ve iş parçacığı yapıları kullanılmıştır:

| Görev | Kullanılan Yapı | Açıklama |
| :--- | :--- | :--- |
| **Dosya İzleme** | `Process` | Kaynak dizindeki değişiklikleri sürekli takip eder. |
| **Yedekleme (Kopyalama)** | `Thread` | Dosyaları arka planda kopyalar. |
| **Arayüz Güncelleme** | `Thread` | İlerleme çubuğunu (Progress Bar) günceller. |
| **Log Okuma** | `Process` | Log dosyasını satır satır okur. |
| **Anormal Durum Tespiti** | `Process` | Log verilerini analiz edip tehditleri bulur. |
| **Davranış Analizi** | `Process` | Kullanıcı giriş-çıkış aktivitelerini izler. |

## 📂 Log Sistemi Detayları

Log dosyaları `.txt` uzantılıdır ve aşağıdaki bilgileri içerir:
* İşlem Başlangıç/Bitiş Tarihi
* İşlem Türü Kodu & Durum Kodu
* Kaynak Dizin & Veri Miktarı

**Log Kategorileri:**
* Takım Üyesi Belirleme & Dosya Paylaşımı
* Parola İşlemleri (Talep/Onay)
* Profile Girişler & Yedeklemeler
* Anormal Durumlar

## 🛠️ Kurulum ve Çalıştırma

1.  Projeyi bilgisayarınıza indirin.
2.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```
3.  Uygulamayı başlatın:
    ```bash
    python main.py
    ```

## 👨‍💻 Geliştirici Bilgileri

* **Ad Soyad:** [Furkan Öztürk]
* **Proje:** Dosya Depolama ve Yedekleme Sistemi
