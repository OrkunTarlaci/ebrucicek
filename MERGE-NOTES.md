# Birleştirme notları (çizimli çiçek sistemi)

**Kaynaklar**
- `ebrucicek-main (4)`: çizimli çiçek tasarımcısı (`FLOWER_LIB`, “Hazır çiçekler”, “Kendi çiçeğini oluştur”, çizimli kartlar) ve `flowerSvg` çizim motoru — **yetkili kaynak**.
- `ebrucicek-cizim-modelleri-birlestirilmis`: katalog yönetimi (＋ Yeni Çiçek Ekle, düzenleme, indirim, sınırsız katalog, tek kaynak `urunler.json`, kademeli yükleme, “Tüm Çiçekler” paneli) — **temel proje**.

**Yapılanlar**
- “Gerçek çiçek fotoğrafı” alanı, fotoğraf yükleme/URL/kaldırma kodu, fotoğrafa özel kart ve yedek (fallback) mantığı çiçek kataloğundan tamamen kaldırıldı (`admin.html` ve `index.html`). `urunler.json` çiçeklerinde `photo` alanı yok; yönetim paneli eski kayıttaki alanı yüklerken siler. `image/flowers/` ve `tools/add-flower-photo.py` yoktur. Ürün/buket/vitrin/ekstra fotoğrafları ve yükleme akışı olduğu gibi korundu.
- `flowerSvg` `main (4)` sürümüyle değiştirildi; `index.html` ile `admin.html` birebir aynı çizimi üretir (39 modelin tümü doğrulandı). 
- `FLOWER_LIB` (149 çiçek) `admin.html`’e taşındı ve her girişe katalogdaki kararlı kimlik atandı. Rakip listeler (`INITIAL_FLOWERS` 25 çiçek, `MODEL_FLOWERS` 26 model) kaldırıldı: yalnızca bir çiçek kütüphanesi vardır.
- ＋ Yeni Çiçek Ekle artık `main (4)` çizimli seçicisini açar; “Kendi çiçeğini oluştur” sekmesine çeşit ve “ana listede göster” alanları eklendi. Düzenleme formu fotoğrafsız, çizim önizlemelidir.
- Katalog verisi: 164 çiçek, kimlikler benzersiz, kopya yok. Üç kayıtta çizim türü doğru modele çevrildi (`f_gerbera_pink`, `f_gerbera_orange` → `gerbera`; `f_orchid` → `orchid`); fiyat, renk, kategori ve diğer alanlara dokunulmadı.
- Araçlar (`tools/validate-catalog.py`, `tools/import-flower-models.py`) ve CI iş akışı yeni yapıya göre güncellendi.

**Dikkat**
- `fmvm80rh8u1j` (“gül”, 90 ₺) kaydı eski bir deneme kaydına benziyor; silmedim. İsterseniz panelden silebilirsiniz.

**Gerçekçi çizimler (ikinci tur)**
-  içinde en çok kullanılan 11 model gerçek çiçeklere yaklaştırıldı: gül, şakayık, karanfil, papatya, gerbera, ayçiçeği, yıldız çiçeği (dahlia), ortanca, lale (yandan görünüm, saplı), lilyum, orkide. Katmanlı taç yapraklar, gölge/ışık vurguları, damarlar, tohum spirali (ayçiçeği), organik çerçeve rengi.
- Diğer 28 model (örn. süsen, glayöl, gelincik, hibiskus, lavanta, yeşillikler) henüz eski düz stilde; aynı yöntemle sırayla geliştirilebilir. Çizim  ve ’de birebir aynıdır; tüm kayıtlar aynı // alanlarıyla çizilir.

**Optimizasyon ve yönetim paneli (Kasım 2026)**
- Fotoğraflar: panelde en uzun kenar 1600 px'e küçültülüp WebP'ye çevrilir (saydam PNG korunur), bellekte Blob olarak tutulur. Kaydet'te tüm fotoğraflar + `urunler.json` Git Data API ile **tek commit** olarak yazılır: fotoğraf sayısı sınırsız, yarıda kesilirse hiçbir şey bozulmaz, `urunler.json` başka yerden değiştiyse üzerine yazılmaz. Yeni fotoğraflar `image/urunler/` ve `image/ekstralar/` altına gider.
- Ürünlerde çoklu fotoğraf: `image` = kapak, `gallery` = ek fotoğraflar (dizi). Sitede karta tıklayınca galeri açılır; masaüstünde üzerine gelince 2. fotoğraf görünür.
- Ayarlar → “Kullanılmayan fotoğrafları bul”: sitede adı geçmeyen fotoğrafları listeler ve tek commit ile kaldırır (git geçmişinde kalır).
- Site artık Tailwind CDN ve tüm Lucide kütüphanesini yüklemez: `npm run build` → `assets/site.css` + `assets/icons.js` (index.html'deki `?v=` damgaları otomatik güncellenir). GitHub Actions (`.github/workflows/build-assets.yml`) index.html değişince bunu kendisi yapar.
