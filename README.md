# Ebru Çiçekçilik

Statik web sitesi (derleme adımı yok): `index.html`, yönetim paneli `admin.html`, katalog `urunler.json`.

## Yerelde çalıştırma
```
python3 -m http.server 8000
```
Ardından http://localhost:8000 adresini açın. (`urunler.json` `fetch` ile okunduğu için dosyayı doğrudan çift tıklayarak değil, bir sunucu üzerinden açın.)

## Yayına alma
GitHub Pages üzerinde yayınlanır; alan adı `CNAME` dosyasındadır. `canonical`, `og:url`, `robots.txt` ve `sitemap.xml` içindeki adres `https://www.orkuntarlaci.me/` olarak ayarlıdır. Alan adı değişirse bu dört yerdeki adresi güncelleyin.

## Ürün yönetimi
`admin.html` GitHub API üzerinden `urunler.json` dosyasını günceller. Giriş için "Contents: Read and write" iznine sahip bir GitHub erişim anahtarı gerekir; anahtar depoda saklanmaz, yalnızca "Bu cihazda hatırla" işaretlenirse o tarayıcıda tutulur.

## Dış bağımlılıklar (CDN)
Tailwind (`cdn.tailwindcss.com`), Lucide (`unpkg.com`, v0.469.0), Google Fonts ve Cloudinary (hero videosu). Bu kaynaklar erişilemezse sayfa biçimsiz görünebilir.

## Çiçek kataloğu (Buket Tasarla)
- Tek kaynak `urunler.json` → `flowers`. `index.html` ve yönetim paneli aynı listeyi okur; yedek/sabit çiçek listesi yoktur. **Çiçek sayısında üst sınır yoktur.**
- **Çiçekler çizimle gösterilir, fotoğrafla değil.** Çizim sistemi 39 SVG çiçek modelinden oluşur (`index.html` ve `admin.html` içinde birebir aynı `flowerSvg`; panelde `FLOWER_SHAPES`). Her kayıt `shape` (çizim türü), `color`, `center` alanlarıyla çizilir; tanınmayan çizim türü gül çizimiyle gösterilir. Ürün, buket ve vitrin fotoğrafları bundan etkilenmez.
- Panel → **Çiçekler (Buket Tasarla)** → **＋ Yeni Çiçek Ekle** iki sekmeli çizimli seçici açar:
  - **Hazır çiçekler:** “Çiçek ekle” penceresinde 149 çizimli çiçek modeli (arama, kategori). Bunlar yalnızca model kütüphanesidir; katalog 25 çiçekle başlar ve bir model ancak “+ Ekle”ye basılınca kataloğa girer. “Kendi çiçeğini oluştur” sekmesi de vardır.
  - **Kendi çiçeğini oluştur:** 130+ gerçek çiçek türünden oluşan aranabilir galeriden çiçek seçilir (ad, botanik çeşit, renkler, çizim, kategori ve fiyat otomatik dolar; renkler isteğe bağlı ince ayarlanır), kategori (yeni kategori yazılabilir), fiyat, “ana listede göster”. Çizim, renkle canlı önizlenir.
  - Mevcut çiçek için **Düzenle**: ad, çeşit, renk, çizim türü, kategori, fiyat, indirim; **Sil**.
- `urunler.json` içinde `flowerCatalog.initialized` işareti varsa panel katalağa girişte dokunmaz: silinen çiçek geri gelmez, eklenenler silinmez. İşaret yoksa mevcut çiçekler korunur; katalog boşsa hazır çiçekler kurulur.
- Panel girişte katalogu kendiliğinden değiştirmez: çiçek listesi her zaman `urunler.json` ile birebir aynıdır (sitedeki “Tüm Çiçekler” ile aynı liste). Çiçek yalnızca “＋ Yeni Çiçek Ekle” ile eklenir. `tools/import-flower-models.py` yalnızca elle çalıştırılırsa toplu ekleme yapar.
- Büyük kataloglar: panelde liste kısıtlanmaz, tüm çiçekler görünür; arama ve kategori filtresi tüm veride çalışır. Katalog 25 çiçekle başlar. “Kendi Buketini Tasarla” listesi katalogdaki tüm çiçekleri gösterir (26. çiçek eklenince 26 çiçek); aynı çiçekler “Tüm Çiçekler” panelinde (arama, kategori, 48’er kademeli yükleme) erişilebilir; “Tüm Çiçekler” düğmesindeki çeşit sayısı katalogla birlikte artar.
- Değişiklikler **Kaydet ve Yayınla** ile `urunler.json`’a yazılır.
- `tools/validate-catalog.py` (CI) yalnızca gerçek hataları yakalar: yinelenen/boş kimlik, boş ad, geçersiz fiyat/renk, yinelenen çizim+ad+çeşit+renk, eski `photo` alanı. Sayı denetimi yoktur.

## Günün Çiçeği animasyonu
Beyaz parlama, ışıltı ve nabız animasyonları, bilgisayarda animasyonlar kapalı (`prefers-reduced-motion: reduce`) olsa bile çalışır; bu kural bilerek kaldırıldı.

## Çiçek çizimlerinin gerçekçiliği
`flowerSvg` (index.html ve admin.html'de aynı) artık taç yapraklarda tabandan uca renk geçişi, her yaprakta doğal sapma, merkezde gölge, çanak yaprakları ve yumuşak gölge çizer.
