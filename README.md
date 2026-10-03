<div align="center">

# 🎯 IP OSINT Tool

**Kırmızı temalı, 6 harita destekli, JSON export özellikli IP sorgulama aracı**

Termux ve Linux için tasarlandı. Tamamen ücretsiz, API anahtarı gerektirmez.

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-ef4444?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux-ef4444?style=for-the-badge&logo=linux&logoColor=white)](https://termux.dev/)

[![Stars](https://img.shields.io/github/stars/KULLANICI_ADIN/ip-osint-tool?style=for-the-badge&color=ef4444)](https://github.com/KULLANICI_ADIN/ip-osint-tool/stargazers)
[![Forks](https://img.shields.io/github/forks/KULLANICI_ADIN/ip-osint-tool?style=for-the-badge&color=ef4444)](https://github.com/KULLANICI_ADIN/ip-osint-tool/network/members)
[![Issues](https://img.shields.io/github/issues/KULLANICI_ADIN/ip-osint-tool?style=for-the-badge&color=ef4444)](https://github.com/KULLANICI_ADIN/ip-osint-tool/issues)

</div>

---

## 🎬 Önizleme

```text
╔══════════════════════════════════════════════════════════╗
║  🎯  IP OSINT Tool                                       ║
║  ──────────────────────────────────────────────────────  ║
║                                                          ║
║  🔍  [ 8.8.8.8                    ]  [ Sorgula → ]      ║
║                                                          ║
║  💡 8.8.8.8 (Google)  1.1.1.1 (Cloudflare)  Kendi IP'm  ║
║                                                          ║
║  ┌────────────────────────────────────────────────────┐  ║
║  │ ✅ Sorgu Başarılı                          8.8.8.8 │  ║
║  ├────────────┬────────────┬────────────┬─────────────┤  ║
║  │ 🌍 Ülke    │ 📍 Şehir   │ 🗺️ Bölge   │ 📮 Posta    │  ║
║  │ US         │ Mountain   │ California │ 94043       │  ║
║  ├────────────┼────────────┼────────────┼─────────────┤  ║
║  │ 🛰️ ISP    │ 🏢 Org     │ 🔢 AS      │ 🕐 Timezone │  ║
║  │ Google LLC │ Google DNS │ AS15169    │ America/LA  │  ║
║  └────────────┴────────────┴────────────┴─────────────┘  ║
║                                                          ║
║  🗺️  [ Dark ] [ Voyager ] [ Sade ] [ OSM ] [ Uydu ]...  ║
║  ┌────────────────────────────────────────────────────┐  ║
║  │                                                    │  ║
║  │              🌑  SİYAH HARİTA                     │  ║
║  │                  📍 (kırmızı pin)                 │  ║
║  │                                                    │  ║
║  └────────────────────────────────────────────────────┘  ║
║                                                          ║
║  📥 JSON   📋 Kopyala                                    ║
╚══════════════════════════════════════════════════════════╝
```

---

## ✨ Özellikler

<table>
<tr>
<td width="50%">

### 🔍 Detaylı Sorgu
- 🌍 Ülke, bölge, şehir, posta kodu
- 🛰️ ISP, organizasyon, AS numarası
- 📡 Enlem / boylam koordinatları
- 🕐 Zaman dilimi bilgisi
- 📱 Mobil / Proxy / Hosting tespiti

### 🗺️ 6 Harita Teması
- 🌑 **Dark** — CartoDB Dark Matter
- 🌕 **Voyager** — CartoDB Voyager
- ⚫ **Sade** — CartoDB Positron
- 🟢 **OSM** — OpenStreetMap
- 🛰️ **Uydu** — Esri World Imagery
- 🏔️ **Topo** — OpenTopoMap

</td>
<td width="50%">

### 🎨 Modern Arayüz
- 🔴 Kırmızı neon tema
- ✨ Animasyonlu gradient efektleri
- 📱 Tamamen mobil uyumlu
- 🍞 Toast bildirimleri
- ⚡ Loading spinner

### 🚀 İleri Özellikler
- 📜 Sorgu geçmişi (localStorage)
- 📥 JSON indirme + 📋 kopyalama
- 🛡️ Proxy / VPN uyarı banner'ı
- 🖱️ Haritaya tıklayarak IP sorgulama
- ⌨️ Klavye kısayolları (Ctrl+S, Ctrl+C)
- 💾 Tema tercihi otomatik kaydedilir

</td>
</tr>
</table>

---

## 🚀 Hızlı Başlangıç

### 📦 Kurulum

<table>
<tr>
<td width="50%">

**Termux (Android)**

```bash
pkg update && pkg upgrade -y
pkg install python git -y
git clone https://github.com/KULLANICI_ADIN/ip-osint-tool.git
cd ip-osint-tool
pip install -r requirements.txt
```

</td>
<td width="50%">

**Linux (Ubuntu / Debian)**

```bash
sudo apt update
sudo apt install python3 python3-pip git -y
git clone https://github.com/KULLANICI_ADIN/ip-osint-tool.git
cd ip-osint-tool
pip3 install -r requirements.txt
```

</td>
</tr>
</table>

### ▶️ Çalıştırma

```bash
python app.py
```

Terminalde şu çıktıyı görürsün:

```text
============================================================
  🎯  IP OSINT TOOL - Full Final v1.2
============================================================
  ✨ Özellikler:
     • Kırmızı tema + 6 farklı harita teması
     • Sorgu geçmişi (localStorage)
     • Haritaya tıklayarak IP sorgulama
     • Proxy/VPN uyarı banner'ı
     • 📥 JSON indirme + kopyalama
     • ⌨️  Klavye kısayolları (Ctrl+S, Ctrl+C)
============================================================
  🌐 Tarayıcıdan aç: http://127.0.0.1:5000
============================================================
```

Tarayıcından aç:

| Cihaz | URL |
|---|---|
| 📱 **Kendi cihazın** | `http://127.0.0.1:5000` |
| 💻 **Aynı WiFi'deki cihaz** | `http://YEREL_IP:5000` |

Yerel IP'ni bulmak için:

```bash
ifconfig | grep inet
```

---

## 🎮 Kullanım

### 1️⃣ IP Sorgulama
- Boş bırakıp **Sorgula**'ya bas → kendi IP'ni sorgular
- `8.8.8.8` gibi bir IP gir → o IP'yi sorgular
- Hızlı çiplerden birine tıkla → otomatik doldurur

### 2️⃣ Harita Teması Değiştirme
Haritanın üstündeki **6 tema butonundan** birine tıkla.
Seçtiğin tema **tarayıcıda kaydedilir**, sayfayı yenilesen bile hatırlanır. ✅

### 3️⃣ JSON İndirme
- **📥 JSON** butonu → dosya indir
- **📋 Kopyala** butonu → panoya kopyala
- <kbd>Ctrl</kbd> + <kbd>S</kbd> → JSON indir
- <kbd>Ctrl</kbd> + <kbd>C</kbd> → sonucu kopyala

### 4️⃣ Sorgu Geçmişi
Son 20 sorgu otomatik saklanır:
- Başlığa tıkla → aç / kapat
- Bir öğeye tıkla → tekrar sorgula
- 🗑️ ikonuna tıkla → tek öğeyi sil
- **Temizle** → tüm geçmişi sil

### 5️⃣ Haritaya Tıklayarak Sorgu
Haritada herhangi bir yere tıkla → o bölge için IP sorgu seçeneği çıkar.

---

## 🛠️ Teknoloji Yığını

<div align="center">

| Katman | Teknoloji |
|---|---|
| **Backend** | ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/-Flask-000000?logo=flask&logoColor=white) |
| **Frontend** | ![HTML5](https://img.shields.io/badge/-HTML5-E34F26?logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/-CSS3-1572B6?logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?logo=javascript&logoColor=black) |
| **Harita** | ![Leaflet](https://img.shields.io/badge/-Leaflet-199900?logo=leaflet&logoColor=white) ![CARTO](https://img.shields.io/badge/-CARTO-ef4444) |
| **API** | [ip-api.com](http://ip-api.com) (ücretsiz katman) |

</div>

---

## 📊 Örnek JSON Çıktısı

```json
{
  "_meta": {
    "tool": "IP OSINT Tool",
    "version": "1.0",
    "exported_at": "2026-10-03T14:23:11.456Z",
    "source": "ip-api.com"
  },
  "status": "success",
  "country": "United States",
  "countryCode": "US",
  "regionName": "California",
  "city": "Mountain View",
  "zip": "94043",
  "lat": 37.4056,
  "lon": -122.0775,
  "timezone": "America/Los_Angeles",
  "isp": "Google LLC",
  "org": "Google Public DNS",
  "as": "AS15169 Google LLC",
  "query": "8.8.8.8",
  "proxy": false,
  "hosting": true,
  "mobile": false
}
```

---

## 📁 Proje Yapısı

```
ip-osint-tool/
├── app.py                 # 🐍 Ana Flask uygulaması
├── requirements.txt       # 📦 Python bağımlılıkları
├── README.md              # 📖 Bu dosya
├── LICENSE                # ⚖️ MIT Lisansı
└── .gitignore             # 🚫 Git ignore kuralları
```

---

## ⌨️ Klavye Kısayolları

| Kısayol | İşlev |
|---|---|
| <kbd>Ctrl</kbd> + <kbd>S</kbd> | JSON olarak indir |
| <kbd>Ctrl</kbd> + <kbd>C</kbd> | Sonucu panoya kopyala |
| <kbd>Enter</kbd> | Sorgula (input odaktayken) |

---

## 🐛 Sorun Giderme

<table>
<tr>
<td width="50%">

### ❌ `python: command not found`

```bash
pkg install python -y         # Termux
sudo apt install python3 -y   # Linux
```

Sonra `python3 app.py` dene.

### ❌ `ModuleNotFoundError: No module named 'flask'`

```bash
pip install flask requests
```

</td>
<td width="50%">

### ❌ `Address already in use`

```bash
pkill -f "python app.py"
# veya
fuser -k 5000/tcp
```

### ❌ `bash app.py` çalışmıyor

`.py` dosyaları **bash** ile değil **python** ile çalışır:

```bash
python app.py   # ✅ Doğru
bash app.py     # ❌ Yanlış
```

</td>
</tr>
</table>

---

## 🗺️ Harita Temaları Detayı

| Tema | Kaynak | Stil | Anahtar |
|---|---|---|---|
| 🌑 Dark | CartoDB | Siyah, minimal | ❌ Gerekmez |
| 🌕 Voyager | CartoDB | Açık, renkli | ❌ Gerekmez |
| ⚫ Sade | CartoDB | Gri / beyaz | ❌ Gerekmez |
| 🟢 OSM | OpenStreetMap | Klasik sokak | ❌ Gerekmez |
| 🛰️ Uydu | Esri | Gerçek uydu | ❌ Gerekmez |
| 🏔️ Topo | OpenTopoMap | Topoğrafik | ❌ Gerekmez |

> ✅ Tüm harita temaları **ücretsiz** ve **API anahtarı gerektirmez**.

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! 🎉

1. 🍴 Fork'la
2. 🌿 Yeni branch oluştur (`git checkout -b feature/yeni-ozellik`)
3. 💾 Commit'le (`git commit -m '✨ Yeni özellik eklendi'`)
4. 📤 Push'la (`git push origin feature/yeni-ozellik`)
5. 🔃 Pull Request aç

---

## ⚠️ Yasal Uyarı

> **Bu araç yalnızca eğitim ve kendi sistemlerinizi test etmek için tasarlanmıştır.**
>
> Başkalarının IP adreslerini izinsiz sorgulamak:
> - Yerel yasalara aykırı olabilir
> - KVKK / GDPR gibi düzenlemeleri ihlal edebilir
> - Etik dışıdır
>
> **Sorumluluk tamamen kullanıcıya aittir.** Geliştirici, aracın kötüye kullanımından sorumlu tutulamaz.

---

## 📜 Lisans

Bu proje **MIT Lisansı** altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 🙏 Teşekkürler

- [ip-api.com](https://ip-api.com) — Ücretsiz IP geolokasyon API'si
- [Leaflet.js](https://leafletjs.com) — Açık kaynak harita kütüphanesi
- [CARTO](https://carto.com) — Ücretsiz harita tile'ları
- [OpenStreetMap](https://openstreetmap.org) — Açık kaynak harita verisi
- [Esri](https://esri.com) — Uydu görüntüleri

---

<div align="center">

### ⭐ Bu projeyi faydalı bulduysan yıldız vermeyi unutma!

**Yapımcı:** [@kadrbequit](https://github.com/KULLANICI_ADIN)

![Made with ❤️ in Turkey](https://img.shields.io/badge/Made%20with%20%E2%9D%A4%EF%B8%8F%20in-Turkey-ef4444?style=for-the-badge)

</div>
