## ✨ Özellikler

### 🎨 Genel
- **Otomatik Platform Algılama** - URL'yi girin, Spotify veya YouTube otomatik tanınır
- **Otomatik FFmpeg Kurulumu** - FFmpeg yoksa otomatik kurar
- **Hızlı İndirme** - 4 paralel bağlantı ile maksimum hız
- **Güzel CLI Arayüzü** - Rich kütüphanesi ile renkli ve modern görünüm
- **Basit Kullanım** - Sadece URL girin, kalite seçin, indirin!

### ♫ Spotify
- Şarkı, Albüm, Playlist ve Sanatçı indirme
- MP3, M4A, FLAC format desteği
- 128-320 kbps kalite seçenekleri
- Otomatik metadata ekleme

### ▶ YouTube
- Video, Playlist ve Canlı Yayın indirme
- MP4, MKV, WEBM format desteği
- Sadece ses indirme (MP3)
- 480p - 1080p+ kalite seçenekleri
- **Otomatik metadata ve thumbnail ekleme**
- Başlık, sanatçı, süre bilgileri otomatik

## 🚀 Kurulum

### Gereksinimler
- Python 3.8 veya üzeri
- FFmpeg (otomatik kurulur)

### Kurulum

```bash
# 1. Repoyu klonla
git clone https://github.com/noramuaol/NoraDownloader.git
cd NoraDownloader

# 2. Paketleri yükle
pip install -r requirements.txt

# 3. Çalıştır
python main.py -i
```

Veya Windows'ta:
```bash
install.bat
run.bat
```

## 📖 Kullanım

### Hızlı Başlangıç (Önerilen)

```bash
python main.py
```

Program size rehberlik edecek:
1. URL'yi girin (Spotify veya YouTube)
2. Platform otomatik algılanır ✨
3. Kalite ve format seçin
4. İndirme başlasın!

### Komut Satırı

```bash
# Spotify
python main.py -u "https://open.spotify.com/playlist/..."

# YouTube Video
python main.py -u "https://www.youtube.com/watch?v=..."

# YouTube (Sadece Ses + Metadata)
python main.py -u "https://youtube.com/..." --audio
```

### Parametreler

```
-u, --url          Spotify veya YouTube URL
-o, --output       Çıktı dizini (varsayılan: downloads)
-p, --platform     Platform: spotify, youtube, auto (varsayılan: auto)
--audio            Sadece ses olarak indir (YouTube için)
-i, --interactive  İnteraktif mod (önerilen)
```

## 🎯 Örnekler

### Spotify Playlist
```bash
python main.py -u "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"
```

### YouTube Video (Sadece Ses + Metadata)
```bash
python main.py -u "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --audio
```
İndirilen MP3 dosyası şunları içerir:
- ✅ Başlık
- ✅ Sanatçı (uploader)
- ✅ Süre
- ✅ Thumbnail (kapak resmi)
- ✅ Bitrate bilgisi

### YouTube Playlist
```bash
python main.py -u "https://www.youtube.com/playlist?list=..."
```

## 🎨 Ekran Görüntüleri

Program çalıştığında:
- ✨ Otomatik platform algılama
- 📊 Desteklenen platformlar tablosu
- ⏳ Gerçek zamanlı indirme ilerlemesi
- 📝 Metadata bilgileri (başlık, sanatçı, süre, bitrate)
- ✅ İndirilen dosyalar özeti

Örnek çıktı:
```
✓ Sarki Adi.mp3
  Boyut: 4.52 MB
  Baslik: Sarki Adi | Sanatci: Artist Name
  Sure: 3:45 | Bitrate: 320 kbps
```

## ⚡ Performans

- **4 Paralel Bağlantı** - Spotify ve YouTube için
- **Otomatik Metadata** - YouTube'dan indirilen şarkılara otomatik eklenir
- **Thumbnail Ekleme** - MP3 dosyalarına kapak resmi
- **Optimize Ayarlar** - Maksimum hız için ayarlanmış
