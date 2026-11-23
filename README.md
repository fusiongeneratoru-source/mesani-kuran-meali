# Sıfır Önyargılı Mesânî Kur'an Meali (Tabula Rasa v3.0)

Bu depo; Kur'an kavramlarını geleneksel terim ve ön kabullerden arındırılmış biçimde, canlı sözlük/Sami dilleri doğrulaması, Rasm-ı Osmânî iskelet metni, Çift Yönlü Mesânî ve Aynı Ayet İçi Furûk kurallarıyla çözümleyen **Tabula Rasa v3.0** projesinin tek gerçek kaynağıdır.

## 🧭 Yapay Zeka Ajanları İçin Başlangıç (PC ve Antigravity Web)

Yeni bir oturumda (yerel PC veya Google AI Studio **Antigravity Agent Preview** web ortamında) çalışmaya başlamadan önce aşağıdaki sırayı izle:

1. Ana sistem anayasasını oku: `PROMPT.md`
2. Kalite sigortalarını oku: `tools/QUALITY_CONSTITUTION.md`
3. Mevcut ilerleme durumunu kontrol et:
   - `data/locked_roots.json` (kilitli ana kök sözlüğü: **450 kök mühürlü**, `%86,92` güncel kapsam)
   - `data/top_100_roots.json` & `data/TOP_100_KAVRAM.md` (tamamlanan Etap 1 listesi: `100/100`)
   - `data/second_100_roots.json` & `data/SECOND_100_KAVRAM.md` (tamamlanan Etap 2 listesi: `100/100`)
   - `data/etap_2_5_key_roots.json` & `data/ETAP_2_5_KAVRAM.md` (tamamlanan Etap 2.5 kilit kavramlar listesi: `16/16`)
   - `data/etap_3_key_roots.json` & `data/ETAP_3_KAVRAM.md` (tamamlanan **Etap 3** listesi: **131/131 kök [%100] TAMAMLANDI** — Etap 3A Çekirdek `55/55`, Etap 3B Tam Zırh `76/76`)
   - `data/etap_3c_key_roots.json` & `data/ETAP_3C_KAVRAM.md` (tamamlanan **Etap 3C** — Son Mayın Temizliği, Hukuk-Ritüel-Kısa Sure Kilitleri ve Açık Mesânî Zırhı: **48/48 kök [%100] TAMAMLANDI**)
   - `data/etap_3d_key_roots.json` & `data/ETAP_3D_KAVRAM.md` (tamamlanan **Etap 3D** — Fâtiha & Kısa Sure Tam Kilidi, Açık Mesânî Zırhı ve Yüksek Frekanslı Çekirdek Kavramlar: **50/50 kök [%100] TAMAMLANDI** [`450` toplam kilitli kök / `%86,92` kapsam])

## 📁 Depo Yapısı

- `PROMPT.md`: Tüm çalışma protokolü (10 Uzman Disiplin, Sözlükler Hakem Masası, JSON v3.0 şeması, devam motoru)
- `data/locked_roots.json`: Mühürlenmiş tüm köklerin tam v3.0 veritabanı (`450` kilitli kök)
- `data/locked_roots_compact.json`: Hızlı okuma için sıkıştırılmış kök özeti
- `data/kavramlar/*.json`: Her mühürlü kavramın Kur'an'da geçtiği tüm ayet dökümleri (`450` kavram JSON dosyası)
- `data/top_100_roots.json` & `data/TOP_100_KAVRAM.md`: İlk 100 kök indeksi (`100/100` tamamlandı)
- `data/second_100_roots.json` & `data/SECOND_100_KAVRAM.md`: İkinci 100 yeni kök indeksi (`100/100` tamamlandı)
- `data/etap_2_5_key_roots.json` & `data/ETAP_2_5_KAVRAM.md`: Top 200 dışında kalan 16 kilit kavram (`ث-ن-ي [Mesânî]` dahil) indeksi (`16/16` tamamlandı)
- `data/etap_3_key_roots.json` & `data/ETAP_3_KAVRAM.md`: Faz 2 öncesi kafa karıştıran kavramlar ve açık Mesânî/Furûk eşlenikleri indeksi (**131/131 [%100] TAMAMLANDI:** `3A: 55/55` [`%80,14`], `3B: 76/76` [`%83,08`])
- `data/etap_3c_key_roots.json` & `data/ETAP_3C_KAVRAM.md`: Meal öncesi son mayın temizliği (ceza-aile-ibadet hukuku, kısa sure kilitleri ve en yüksek açık Mesânî referansları — **48/48 [%100] TAMAMLANDI**, `400` kilitli kök / `%84,51` kapsam)
- `data/etap_3d_key_roots.json` & `data/ETAP_3D_KAVRAM.md`: Fâtiha & Kısa Sure Tam Kilidi, 3+ Açık Mesânî Zırhı ve Yüksek Frekanslı Çekirdek Kavramlar (**50/50 [%100] TAMAMLANDI**, `450` kilitli kök / `%86,92` kapsam)
- `data/particles_and_prepositions.json` & `data/EDAT_VE_HARFICER_HARITASI.md`: Kur'an'daki köksüz edatlar (`10` harf-i cer, `11` yapısal/mantıksal edat) ve `13` köksüz/ödünç anahtar kavram haritası (Faz 2 omurgası)
- `data/quran-*.txt` & `data/quranic-corpus-morphology-0.4.txt`: Yerel Kur'an metinleri ve morfoloji korpusu
- `tools/`: Saf Python standart kütüphanesiyle çalışan doğrulama ve üretim araçları (ek paket kurulumu gerektirmez)

## 🛠️ Doğrulama ve Güncelleme Komutları (Linux / macOS / Windows)

Tüm araçlar harici paket gerektirmeden Python 3 ile çalışır:

```bash
# Yeni mühürlenen kök sonrası kavram JSON dosyasını üret/güncelle
python3 tools/build_kavramlar.py

# İndeksleri ve özet dosyaları yenile
python3 tools/generate_top_100.py
python3 tools/generate_second_100.py
python3 tools/generate_etap_2_5.py
python3 tools/generate_etap_3.py
python3 tools/generate_etap_3c.py
python3 tools/generate_etap_3d.py
python3 tools/generate_compact_roots.py

# Zorunlu sıfır hata bütünlük doğrulaması (her kök sonrası şart)
python3 tools/verify_project.py
```

## 🌐 Web (Antigravity Remote Agents / Agent Preview) Çalışma ve Senkronizasyon Kuralları

**Antigravity Web (`antigravity.google.com` / Remote Agents)** veya bulut ortamında devam ederken:

1. **Başlangıç:** Yeni bir sohbet açıldığında ajan önce `README.md`, `PROMPT.md` ve `tools/QUALITY_CONSTITUTION.md` dosyalarını okuyarak güncel ilerlemeyi (`data/locked_roots.json` ve `data/etap_3_key_roots.json`) teyit eder.
2. **Zorunlu Doğrulama:** Her yeni kök, sure çözümlemesi veya dosya değişikliği sonrasında `python3 tools/verify_project.py` çalıştırılıp **SIFIR HATA** doğrulanır.
3. **Kalıcı Kayıt ve GitHub Senkronizasyonu (ZORUNLU KURAL):** Bulut (Remote Agents) oturumları geçici bir çalışma kopyası üzerinde çalıştığından, yapılan değişikliklerin kaybolmaması için ajan **doğrulanan her görev/etap sonunda** kullanıcıya hemen hatırlatarak onay alır ve değişiklikleri GitHub deposuna (`git commit` ve `git push`) kalıcı olarak gönderir. Kullanıcı oturum başında otomatik gönderim onayı verdiyse her doğrulanan adım sonunda doğrudan GitHub'a işler.
4. **PC ile Eşitleme:** Web oturumunda GitHub'a işlenen güncellemeler, yerel PC'ye dönüldüğünde tek adımda (`git pull`) bilgisayara çekilerek iki ortam %100 senkron tutulur.
