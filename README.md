# 🎯 IP OSINT Tool

Termux ve Linux üzerinde çalışan, kırmızı temalı, harita destekli IP sorgu aracı.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-red)

## ✨ Özellikler

- 🌍 Detaylı IP sorgulama (ülke, şehir, ISP, AS, koordinat)
- 🗺️ Siyah harita üzerinde kırmızı pin ile konum gösterimi
- 📜 Sorgu geçmişi (localStorage ile tarayıcıda saklanır)
- 🛡️ Proxy / VPN / Hosting tespiti ve uyarı banner'ı
- 📥 JSON olarak indirme + 📋 panoya kopyalama
- ⌨️ Klavye kısayolları (Ctrl+S, Ctrl+C)
- 🔒 Sadece localhost — dışarıya açılmaz
- 💯 Ücretsiz, API anahtarı gerektirmez

## 📦 Kurulum

### Termux'ta

\`\`\`bash
pkg update && pkg upgrade -y
pkg install python git -y
git clone  https://github.com/kadrbequit/iposintv2.git
cd ip-osint-tool
pip install -r requirements.txt
\`\`\`

### Linux'ta

\`\`\`bash
sudo apt update
sudo apt install python3 python3-pip git -y
git clone https://github.com/kadrbequit/iposintv2.git
cd ip-osint-tool
pip3 install -r requirements.txt
\`\`\`

## 🚀 Kullanım

\`\`\`bash
python app.py
\`\`\`

Ardından tarayıcıdan aç:

- 📱 **Kendi cihazın:** http://127.0.0.1:5000
- 💻 **Aynı WiFi'deki cihaz:** http://YEREL_IP:5000

Yerel IP'ni öğrenmek için:

\`\`\`bash
ifconfig | grep inet
\`\`\`

## 🎬 Ekran Görüntüleri

*(Buraya ekran görüntüsü ekleyebilirsin)*

## 🛠️ Kullanılan Teknolojiler

- **Backend:** Python, Flask
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Harita:** Leaflet.js + CARTO Dark Matter
- **API:** ip-api.com (ücretsiz katman)

## 📊 Örnek JSON Çıktısı

\`\`\`json
{
  "_meta": {
    "tool": "IP OSINT Tool",
    "version": "1.0",
    "exported_at": "2026-10-03T14:23:11.456Z",
    "source": "ip-api.com"
  },
  "country": "United States",
  "city": "Mountain View",
  "isp": "Google LLC",
  "query": "8.8.8.8"
}
\`\`\`

## ⚠️ Yasal Uyarı

Bu araç yalnızca **eğitim ve kendi sistemlerinizi test etmek** için tasarlanmıştır.
Başkalarının IP adreslerini izinsiz sorgulamak yerel yasalara aykırı olabilir.
Sorumluluk kullanıcıya aittir.

## 📜 Lisans

MIT License — detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🤝 Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır. Büyük değişiklikler için önce bir issue açıp
ne yapmak istediğinizi tartışalım.

---

⭐ Bu projeyi faydalı bulduysanız yıldız vermeyi unutmayın!
