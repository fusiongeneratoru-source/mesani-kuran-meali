# Sıfır Önyargılı Mesânî Kur'an Meali (Tabula Rasa v3.0)

Bu depo; Kur'an kavramlarını geleneksel terim ve ön kabullerden arındırılmış biçimde, canlı sözlük/Sami dilleri doğrulaması, Rasm-ı Osmânî iskelet metni, Çift Yönlü Mesânî ve Aynı Ayet İçi Furûk kurallarıyla çözümleyen **Tabula Rasa v3.0** projesinin tek gerçek kaynağıdır.

## 🧭 Yapay Zeka Ajanları İçin Başlangıç (PC ve Antigravity Web)

Yeni bir oturumda (yerel PC veya Google AI Studio **Antigravity Agent Preview** web ortamında) çalışmaya başlamadan önce aşağıdaki sırayı izle:

1. Ana sistem anayasasını oku: `PROMPT.md` (Özellikle 7 Anayasal Kırmızı Çizgi ve **Aşırı Mekanikleşme Yasağı / Yaşayan Türkçe** ilkesi)
2. Kalite sigortalarını oku: `tools/QUALITY_CONSTITUTION.md` (13 Kural)
3. Mevcut ilerleme durumunu kontrol et:
   - `data/locked_roots.json` (kilitli ana kök sözlüğü: **800 kök mühürlü**, `%95,43` köklü kapsam / tüm Kur'an kelimelerinin `%97,05`'i / `40` sure `%100` kilitli)
   - `data/top_100_roots.json` & `data/TOP_100_KAVRAM.md` (tamamlanan Etap 1 listesi: `100/100`)
   - `data/second_100_roots.json` & `data/SECOND_100_KAVRAM.md` (tamamlanan Etap 2 listesi: `100/100`)
   - `data/etap_2_5_key_roots.json` & `data/ETAP_2_5_KAVRAM.md` (tamamlanan Etap 2.5 kilit kavramlar listesi: `16/16`)
   - `data/etap_3_key_roots.json` & `data/ETAP_3_KAVRAM.md` (tamamlanan **Etap 3** listesi: **131/131 kök [%100] TAMAMLANDI** — Etap 3A Çekirdek `55/55`, Etap 3B Tam Zırh `76/76`)
   - `data/etap_3c_key_roots.json` & `data/ETAP_3C_KAVRAM.md` (tamamlanan **Etap 3C** — Son Mayın Temizliği, Hukuk-Ritüel-Kısa Sure Kilitleri ve Açık Mesânî Zırhı: **48/48 kök [%100] TAMAMLANDI**)
   - `data/etap_3d_key_roots.json` & `data/ETAP_3D_KAVRAM.md` (tamamlanan **Etap 3D** — Fâtiha & Kısa Sure Tam Kilidi, Açık Mesânî Zırhı ve Yüksek Frekanslı Çekirdek Kavramlar: **50/50 kök [%100] TAMAMLANDI** [`450` toplam kilitli kök / `%86,92` kapsam])
   - `data/etap_3e_key_roots.json` & `data/ETAP_3E_KAVRAM.md` (tamamlanan **Etap 3E** — Kısa Sure Son Tekil Kilitleri, Açık Mesânî/Furûk Uçları ve 500. Kök Tam Zırh Paketi: **50/50 kök [%100] TAMAMLANDI** [`500` toplam kilitli kök / `%88,50` köklü kapsam, tüm Kur'an kelimelerinin `%92,58`'i])
   - `data/etap_3f_key_roots.json` & `data/ETAP_3F_KAVRAM.md` (tamamlanan **Etap 3F** — Kısa Sure Tam Kilitleri, 3+ Açık Mesânî Tepe Uçları (6/6), Doktrinel Mayınlar ve Yüksek Frekanslı Çekirdek Kökler: **50/50 kök [%100] TAMAMLANDI** [`550` toplam kilitli kök / `%90,24` köklü kapsam, tüm Kur'an kelimelerinin `%93,70`'i, `15` sure `%100` kilitli: 1, 94, 96–99, 102, 103, 107–110, 112–114])
   - `data/etap_3g_key_roots.json` & `data/ETAP_3G_KAVRAM.md` (tamamlanan **Etap 3G** — 5 Yeni Kısa Sure Tam Kilidi [106 Kureyş, 95 Tîn, 92 Leyl, 93 Duhâ, 82 İnfitâr], 3+ Açık Mesânî/Furûk Tepe Uçları ve 600. Kök Yüksek Frekanslı Çekirdek Paketi: **50/50 kök [%100] TAMAMLANDI** [`600` toplam kilitli kök / `%91,77` köklü kapsam, tüm Kur'an kelimelerinin `%94,79`'u, `20` sure `%100` kilitli: 1, 82, 92–99, 102, 103, 106–110, 112–114])
   - `data/etap_3h_key_roots.json` & `data/ETAP_3H_KAVRAM.md` (tamamlanan **Etap 3H** — 5 Yeni Sure Tam Kilidi [60 Mümtehine, 64 Teğâbün, 65 Talâk, 85 Bürûc, 87 A'lâ], 3+ Açık Mesânî/Furûk Tepe Uçları ve 650. Kök Yüksek Frekanslı Çekirdek Paketi: **50/50 kök [%100] TAMAMLANDI** [`650` toplam kilitli kök / `%93,13` köklü kapsam, tüm Kur'an kelimelerinin `%95,56`'sı, `25` sure `%100` kilitli: 1, 60, 64, 65, 82, 85, 87, 92–99, 102, 103, 106–110, 112–114])
   - `data/etap_3i_key_roots.json` & `data/ETAP_3I_KAVRAM.md` (tamamlanan **Etap 3I** — Yüksek Frekanslı Çekirdek Kökler [18–13 Geçiş] ve +4 Sure Tam Kilidi [62 Cum'a, 104 Hümeze, 105 Fîl, 111 Mesed]: **50/50 kök [%100] TAMAMLANDI** [`700` toplam kilitli kök / `%94,24` köklü kapsam, tüm Kur'an kelimelerinin `%96,29`'u, `29` sure `%100` kilitli: 1, 60, 62, 64, 65, 82, 85, 87, 92–99, 102–114])
   - `data/etap_3j_key_roots.json` & `data/ETAP_3J_KAVRAM.md` (tamamlanan **Etap 3J** — +6 Sure Tam Kilidi [61 Saff, 63 Münâfikûn, 66 Tahrîm, 88 Ğâşiye, 100 Âdiyât, 101 Kâria], Kalan Tüm 2+ Açık Mesânî Tepe Uçları ve 13–12 Geçişli Çekirdek Kökler: **50/50 kök [%100] TAMAMLANDI** [`750` toplam kilitli kök / `%94,81` köklü kapsam, tüm Kur'an kelimelerinin `%96,65`'i, `35` sure `%100` kilitli: 1, 60–66, 82, 85, 87–88, 92–114])
   - `data/etap_3k_key_roots.json` & `data/ETAP_3K_KAVRAM.md` (tamamlanan **Etap 3K** — +5 Sure Tam Kilidi [84 İnşikâk, 86 Târık, 90 Beled, 91 Şems, 45 Câsiye] ve 12–11 Geçişli Yüksek Frekanslı Çekirdek Kökler: **50/50 kök [%100] TAMAMLANDI** [`800` toplam kilitli kök / `%95,43` köklü kapsam, tüm Kur'an kelimelerinin `%97,05`'i, `40` sure `%100` kilitli: 1, 45, 60–66, 82, 84–88, 90–114 — son 25 sure kesintisiz `%100`!])

## 📁 Depo Yapısı

- `PROMPT.md`: Tüm çalışma protokolü (10 Uzman Disiplin, Sözlükler Hakem Masası, JSON v3.0 şeması, devam motoru)
- `data/locked_roots.json`: Mühürlenmiş tüm köklerin tam v3.0 veritabanı (`800` kilitli kök)
- `data/locked_roots_compact.json`: Hızlı okuma için sıkıştırılmış kök özeti
- `data/kavramlar/*.json`: Her mühürlü kavramın Kur'an'da geçtiği tüm ayet dökümleri (`800` kavram JSON dosyası)
- `data/top_100_roots.json` & `data/TOP_100_KAVRAM.md`: İlk 100 kök indeksi (`100/100` tamamlandı)
- `data/second_100_roots.json` & `data/SECOND_100_KAVRAM.md`: İkinci 100 yeni kök indeksi (`100/100` tamamlandı)
- `data/etap_2_5_key_roots.json` & `data/ETAP_2_5_KAVRAM.md`: Top 200 dışında kalan 16 kilit kavram (`ث-ن-ي [Mesânî]` dahil) indeksi (`16/16` tamamlandı)
- `data/etap_3_key_roots.json` & `data/ETAP_3_KAVRAM.md`: Faz 2 öncesi kafa karıştıran kavramlar ve açık Mesânî/Furûk eşlenikleri indeksi (**131/131 [%100] TAMAMLANDI:** `3A: 55/55` [`%80,14`], `3B: 76/76` [`%83,08`])
- `data/etap_3c_key_roots.json` & `data/ETAP_3C_KAVRAM.md`: Meal öncesi son mayın temizliği (ceza-aile-ibadet hukuku, kısa sure kilitleri ve en yüksek açık Mesânî referansları — **48/48 [%100] TAMAMLANDI**, `400` kilitli kök / `%84,51` kapsam)
- `data/etap_3d_key_roots.json` & `data/ETAP_3D_KAVRAM.md`: Fâtiha & Kısa Sure Tam Kilidi, 3+ Açık Mesânî Zırhı ve Yüksek Frekanslı Çekirdek Kavramlar (**50/50 [%100] TAMAMLANDI**, `450` kilitli kök / `%86,92` kapsam)
- `data/etap_3e_key_roots.json` & `data/ETAP_3E_KAVRAM.md`: Kısa Sure Son Tekil Kilitleri (98–114), Açık Mesânî/Furûk Uçları ve 500. Kök Tam Zırh Paketi (**50/50 [%100] TAMAMLANDI**, `500` kilitli kök / `%88,50` köklü kapsam, tüm Kur'an kelimelerinin `%92,58`'i)
- `data/etap_3f_key_roots.json` & `data/ETAP_3F_KAVRAM.md`: 8 kısa sureyi daha `%100` kilitleyen kökler (toplam `15` tam kilitli sure), 3+ açık Mesânî referanslı tepe uçlar (6/6), doktrinel/çok-asıllı mayınlar ve kalan en yüksek frekanslı çekirdek kökler (**50/50 [%100] TAMAMLANDI**, `550` kilitli kök / `%90,24` köklü kapsam, tüm Kur'an kelimelerinin `%93,70`'i)
- `data/etap_3g_key_roots.json` & `data/ETAP_3G_KAVRAM.md`: 5 kısa sureyi daha `%100` kilitleyen kökler (106 Kureyş, 95 Tîn, 92 Leyl, 93 Duhâ, 82 İnfitâr — toplam `20` tam kilitli sure), 3+ açık Mesânî/Furûk tepe uçları ve 600. kök yüksek frekanslı çekirdek paketi (**50/50 [%100] TAMAMLANDI**, `600` kilitli kök / `%91,77` köklü kapsam, tüm Kur'an kelimelerinin `%94,79`'u)
- `data/etap_3h_key_roots.json` & `data/ETAP_3H_KAVRAM.md`: 5 sureyi daha `%100` kilitleyen kökler (60 Mümtehine, 64 Teğâbün, 65 Talâk, 85 Bürûc, 87 A'lâ — toplam `25` tam kilitli sure), 3+ açık Mesânî/Furûk tepe uçları ve 650. kök yüksek frekanslı çekirdek paketi (**50/50 [%100] TAMAMLANDI**, `650` kilitli kök / `%93,13` köklü kapsam, tüm Kur'an kelimelerinin `%95,56`'sı)
- `data/etap_3i_key_roots.json` & `data/ETAP_3I_KAVRAM.md`: 4 sureyi daha `%100` kilitleyen kökler (62 Cum'a, 104 Hümeze, 105 Fîl, 111 Mesed — toplam `29` tam kilitli sure; Sure 102–114 arası kesintisiz `%100` kilit) ve kalan `18–13` geçişli yüksek frekanslı çekirdek kökler (**50/50 [%100] TAMAMLANDI**, `700` kilitli kök / `%94,24` köklü kapsam, tüm Kur'an kelimelerinin `%96,29`'u)
- `data/etap_3j_key_roots.json` & `data/ETAP_3J_KAVRAM.md`: 6 sureyi daha `%100` kilitleyen kökler (61 Saff, 63 Münâfikûn, 66 Tahrîm, 88 Ğâşiye, 100 Âdiyât, 101 Kâria — toplam `35` tam kilitli sure; Sure 60–66 ve Sure 92–114 arası kesintisiz `%100` kilit), kalan tüm 2+ açık Mesânî tepe uçları ve `13–12` geçişli çekirdek kökler (**50/50 [%100] TAMAMLANDI**, `750` kilitli kök / `%94,81` köklü kapsam, tüm Kur'an kelimelerinin `%96,65`'i)
- `data/etap_3k_key_roots.json` & `data/ETAP_3K_KAVRAM.md`: 5 sureyi daha `%100` kilitleyen kökler (84 İnşikâk, 86 Târık, 90 Beled, 91 Şems, 45 Câsiye — toplam `40` tam kilitli sure; Sure 60–66, Sure 84–88 ve Sure 90–114 [son 25 sure] arası kesintisiz `%100` kilit) ve `12–11` geçişli yüksek frekanslı çekirdek kökler (**50/50 [%100] TAMAMLANDI**, `800` kilitli kök / `%95,43` köklü kapsam, tüm Kur'an kelimelerinin `%97,05`'i)
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
python3 tools/generate_etap_3e.py
python3 tools/generate_etap_3f.py
python3 tools/generate_etap_3g.py
python3 tools/generate_etap_3h.py
python3 tools/generate_etap_3i.py
python3 tools/generate_etap_3j.py
python3 tools/generate_etap_3k.py
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
