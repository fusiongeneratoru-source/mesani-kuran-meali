# -*- coding: utf-8 -*-
"""
Etap 3F Kilit Kavramlar (Kısa Sureler %100 Tam Kilit Genişletmesi [7->15 Sure],
3 Açık Mesânî Tepe Uçları ve %90+ Kök Kapsamı Zırh Paketi — 50 Kök -> 550 Kilitli Kök)
Tabula Rasa Mesânî Çözümleme Sistemi (v3.0)

İlk 500 mühürlü kökten sonra (%88,50 köklü / %92,58 tüm kelime kapsamı),
8 kısa sureyi daha %100 kilitleyen 13+1 kökü (Sure 94, 96, 97, 98, 99, 102, 103, 110),
3 açık Mesânî referanslı 6 tepe ucunun tamamını, 2 açık Mesânî referanslı kritik eşlenikleri,
yüksek etkili doktrinel/çok-asıllı mayınları ve kalan en yüksek frekanslı çekirdek kökleri
(50 kök / 870 geçiş) indeksler; toplam sözlüğü 550 köke (%90,24 köklü / %93,70 tüm kelime) ulaştırır.
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_kavramlar import ROOT_CONFIG
from quran_analyzer import DATA_DIR, to_arabic_root, to_latin_root

# (buckwalter, category, rationale)
ETAP_3F_ROOTS_SPEC = [
    # Kategori 1: Kısa Sureler %100 Kilidi I (7 Yeni %100 Kilitli Sure: 99, 102, 103, 110, 94, 97, 98 -> 14 Sure!)
    ('$tt', 'Kısa Sure %100 Kilidi', 'Şettâ ve Eştât (Sure 99 Zilzâl son kilidi + 2 açık Mesânî ref! ج-م-ع zıddı: 99:6 bölük bölük, 59:14 dağınık kalpler)'),
    ('qbr', 'Kısa Sure %100 Kilidi', 'Kabr, Makâbir ve Ekbera (Sure 102 Tekâsür son kilidi + Sure 100, 82: mezarlar ve 80:21 insanı kabre koyup örtmek)'),
    ('ESr', 'Kısa Sure %100 Kilidi', 'Asr, Mu\'sırât ve Ya\'sıru (Sure 103 Asr son kilidi + 12:49, 78:14 sıkıp özünü çıkaran zaman/çağ ve yağmur yüklü bulutlar)'),
    ('fwj', 'Kısa Sure %100 Kilidi', 'Fevc ve Efvâc (Sure 110 Nasr son kilidi + 27:83, 67:8, 78:18 dalga dalga akın eden kalabalık insan grupları)'),
    ('rgb', 'Kısa Sure %100 Kilidi', 'Rağbet ve Râğib (Sure 94 İnşirâh kilidi + 2 açık Mesânî ref! ر-ه-ب zıddı: 94:8 yalnızca Rabbine yönelip arzulamak)'),
    ('frg', 'Kısa Sure %100 Kilidi', 'Ferâğ ve Efrağa (Sure 94 İnşirâh son kilidi + 2:250, 18:96, 55:31 bir işi bitirip boşalmak ve üzerlerine sabır/bakır boşaltmak)'),
    ('$hr', 'Kısa Sure %100 Kilidi', 'Şehr ve Eşhur (Sure 97 Kadir kilidi + 21 geçiş: 2:185, 9:36, 97:3 gökyüzünde belirginleşen kamerî ay birimi)'),
    ('TlE', 'Kısa Sure %100 Kilidi', 'Tulû\', Matla\' ve İttılâ\' (Sure 97 Kadir son kilidi + Sure 104 Hümeze, 19 geçiş: doğup yükselmek, gönüllere işlemek, muttali olmak)'),
    ('Abd', 'Kısa Sure %100 Kilidi', 'Ebeden (Sure 98 Beyyine kilidi + 28 geçiş: uzun ve kesintisiz süreklilik — "ebedîlik" doktrinel ayrımı)'),
    ('fkk', 'Kısa Sure %100 Kilidi', 'Fekk ve Münfekkîn (Sure 98 Beyyine son kilidi + Sure 90:13: 98:1 ayrılıp kopmamak, 90:13 esir boynunu bağından çözüp kurtarmak)'),

    # Kategori 2: Kısa Sure %100 Kilidi II (Alak 96 -> 15 Sure!) + 3 Açık Mesânî Tepe Uçları (6/6 Sıfırlama)
    ('nSy', 'Kısa Sure & Tepe Mesânî', 'Nâsiye (Sure 96 Alak kilidi + 11:56, 55:41: alın perçemi / karar merkezi — 96:15-16 yalancı ve hatalı alın)'),
    ('sfE', 'Kısa Sure & Tepe Mesânî', 'Sef\' (Sure 96 Alak kilidi: 96:15 alnından sertçe tutup sürükleyip yakalamak)'),
    ('zbn', 'Kısa Sure & Tepe Mesânî', 'Zebâniye (Sure 96 Alak son kilidi: 96:18 itip geri püskürten görevli güçler — ünlü geleneksel mitoloji mayını)'),
    ('mHw', 'Kısa Sure & Tepe Mesânî', 'Mahv (3 açık Mesânî + 1 Furûk ref! ث-ب-ت zıddı: 13:39 "Allah dilediğini siler, dilediğini sabitler", 17:12 gece ayetini silmek)'),
    ('Ekf', 'Kısa Sure & Tepe Mesânî', 'Ukûf, Âkif ve Ma\'kûf (3 açık Mesânî ref! 2:125, 2:187, 7:138, 21:52 bir şeye veya mekâna sebatla bağlanıp kapanmak)'),
    ('jwE', 'Kısa Sure & Tepe Mesânî', 'Cû\' (3 açık Mesânî ref + Sure 106 Kureyş & 88 Gâşiye: 106:4 açlıktan doyurmak, 2:155, 16:112, 20:118)'),
    ('bwr', 'Kısa Sure & Tepe Mesânî', 'Bûr ve Bevâr (3 açık Mesânî ref! 14:28 helak yurdu, 35:10, 35:29 kesada uğrayıp çürümeyen ticaret)'),
    ('nfd', 'Kısa Sure & Tepe Mesânî', 'Nefâd (3 açık Mesânî ref! ب-ق-ي zıddı: 16:96 yanınızdaki tükenir, 18:109, 31:27, 38:54 tükenmez rızık)'),
    ('fny', 'Kısa Sure & Tepe Mesânî', 'Fânî (3 açık Mesânî ref! ب-ق-ي zıddı: 55:26 "üzerindeki her şey tükenip yok olucudur")'),
    ('ndd', 'Kısa Sure & Tepe Mesânî', 'Endâd (1 Mesânî + 3 Furûk ref! 2:22, 2:165, 14:30, 39:8, 41:9 Allah\'a rakip eş ve denkler koşmak)'),

    # Kategori 3: 2 Açık Mesânî Eşlenikleri & Doktrinel Kökler I (10 kök)
    ('Sgr', 'Açık Mesânî & Doktrin', 'Sağîr, Sağîra ve Sâğirûn (2 Mesânî + 2 Furûk ref! ك-ب-ر ve ع-ظ-م zıddı: 18:49 küçük-büyük her kayıt, 7:13 küçülmüş olarak)'),
    ('Hmm', 'Açık Mesânî & Doktrin', 'Hamîm ve Yahmûm (2 Mesânî + 1 Furûk ref! 21 geçiş: kaynar yakıcı su VE candan yakın dost çift kolu!)'),
    ('$fy', 'Açık Mesânî & Doktrin', 'Şifâ\' ve Yeşfî (2 Mesânî + 1 Furûk ref! 10:57, 16:69, 17:82, 26:80, 41:44 gönüllere ve bedenlere onarıcı şifa)'),
    ('$yE', 'Açık Mesânî & Doktrin', 'Şîa, Şiye\' ve Teşîa (2 açık Mesânî ref! 6:65, 6:159, 28:4, 30:32 fırkalara bölünmek ve 24:19 çirkinliğin yayılması)'),
    ('E*r', 'Açık Mesânî & Doktrin', 'Uzr, Ma\'zire ve İ\'tizâr (2 açık Mesânî ref! 7:164, 9:90, 18:76, 77:6 geçerli mazeret sunmak ve bahaneler üretmek)'),
    ('Ezl', 'Açık Mesânî & Doktrin', 'İ\'tizâl ve Ma\'zil (2 açık Mesânî ref! 2:222, 11:42, 18:16, 19:48-49, 26:212 kenara çekilip uzaklaşmak)'),
    ('dmr', 'Açık Mesânî & Doktrin', 'Tedmîr (2 açık Mesânî ref! 7:137, 17:16, 25:36, 46:25, 47:10 kökten yıkıp tarumar etmek)'),
    ('brz', 'Açık Mesânî & Doktrin', 'Burûz ve Bârize (2 açık Mesânî ref! 2:250, 3:154, 14:21, 18:47, 40:16 açık düzlüğe ve ortaya çıkmak)'),
    ('snn', 'Açık Mesânî & Doktrin', 'Sünnet, Mesnûn ve Sinn (21 geçiş — DEV doktrinel kök! Allah\'ın değişmez yasası [33:62, 35:43], şekillenmiş balçık [15:26], diş [5:45])'),
    ('mny', 'Açık Mesânî & Doktrin', 'Ümniyye, Emânî, Temennî ve Menî (1 Mesânî + 2 Furûk ref! 21 geçiş: kuruntu/okuma [2:78, 22:52] ve menî/ölçü [53:46, 75:37])'),

    # Kategori 4: Yüksek Etkili Doktrinel, Hukuki ve Çok Asıllı Kökler II (10 kök)
    ('Alw', 'Doktrinel & Çok Asıllı', 'Âlâ\', Îlâ\' ve Ye\'lû (37 geçiş — 3 ayrı kol! Rahmân suresi 31x "nimet/güzellikler", 2:226 eşlerden uzaklaşma yemini, 3:118 geri durmama)'),
    ('qrn', 'Doktrinel & Çok Asıllı', 'Karîn, Karn, Mukarrenîn ve Zü\'l-Karneyn (36 geçiş: yakın eş/yoldaş [43:36, 50:23], nesil/çağ [6:6], zincirle bağlananlar [14:49])'),
    ('Awy', 'Doktrinel & Çok Asıllı', 'Me\'vâ, Îvâ ve Evâ (36 geçiş | 1M+2F + Sure 93 Duhâ: barındırıp sığınak sağlamak [93:6, 8:72, 18:10] ve nihai barınak [79:39-41])'),
    ('Tyr', 'Doktrinel & Çok Asıllı', 'Tayr, Tâir ve Tetayyur (29 geçiş | 1M + Sure 105 Fîl: kuşlar, 17:13 herkesin sorumluluk kaydı ve 7:131, 27:47 uğursuzluk hurafesi)'),
    ('fty', 'Doktrinel & Çok Asıllı', 'İftâ\', İstiftâ\' ve Fetâ (21 geçiş: 4:127, 4:176, 12:43 hukuki/bilgisel hüküm sormak-vermek ve 18:10, 21:60 yiğit gençler)'),
    ('drj', 'Doktrinel & Çok Asıllı', 'Derecât ve İstidrac (20 geçiş | 1M: 2:228, 6:132, 58:11 kademe/dereceler ve 7:182, 68:44 fark ettirmeden adım adım yakalamak)'),
    ('frD', 'Doktrinel & Çok Asıllı', 'Farz, Farîza ve Mefrûd (18 geçiş: 2:197, 4:7, 4:11, 9:60, 24:1, 28:85, 33:38 kesip belirlenmiş hukuki pay ve yükümlülük)'),
    ('nwb', 'Doktrinel & Çok Asıllı', 'İnâbe ve Münîb (18 geçiş: 11:75, 30:31, 39:8, 39:54, 50:33, 60:4 ت-و-ب ve أ-و-ب furûku: kalben merkeze yönelip dönmek)'),
    ('swr', 'Doktrinel & Çok Asıllı', 'Sûre, Sûr ve Esâvir (17 geçiş: 2:23, 9:64, 24:1 Kur\'an suresi, 57:13 aradaki sur, 18:31 bilezikler ve 38:21 duvardan aşmak)'),
    ('Sfw', 'Doktrinel & Çok Asıllı', 'Istıfâ\', Mustafeyn ve Safvân (17 geçiş: 2:130, 3:33, 3:42, 22:75, 35:32 arındırıp özünü seçmek ve 2:264 pürüzsüz kaya)'),

    # Kategori 5: En Yüksek Frekanslı Kalan Çekirdek Kökler (24-45 Geçiş -> 550 KÖK & %90+ KÖK KAPSAMI!)
    ('SbH', 'Yüksek Frekanslı Çekirdek', 'Subh, İsbâh ve Esbaha (45 geçiş | 1M + Sure 81, 100 — #1 kalan kök! 81:18 ağaran sabah ve 3:103, 5:30 yeni bir hâle dönüşmek)'),
    ('bHr', 'Yüksek Frekanslı Çekirdek', 'Bahr ve Bahîra (42 geçiş | 2M + Sure 81, 82 — #2 kalan kök! ب-ر-ر zıddı denizler ve 5:103 cahiliye kulağı yarık deve geleneği)'),
    ('jbl', 'Yüksek Frekanslı Çekirdek', 'Cebel ve Cibille (41 geçiş | 1M + Sure 78, 79, 81, 88, 101 — #3 kalan kök! Dağlar ve 26:184, 36:62 kalabalık insan kitleleri)'),
    ('$rb', 'Yüksek Frekanslı Çekirdek', 'Şurb, Şarâb ve Meşreb (39 geçiş | 2M + Sure 78, 83 — #4 kalan kök! ط-ع-م ve ص-و-م eşleniği içmek, içecek ve 2:93 kalbe sindirmek)'),
    ('hzA', 'Yüksek Frekanslı Çekirdek', 'Hüzüv ve İstihzâ\' (34 geçiş | 1M: 2:15, 2:67, 6:10, 9:65, 15:95, 18:56 hakikat ve ayetlerle alay edip küçümsemek)'),
    ('Zll', 'Yüksek Frekanslı Çekirdek', 'Zıll, Zulle ve Zalle (33 geçiş | 1M: 2:57, 13:15, 16:48, 25:45, 56:30 gölge/gölgelik ve 16:58, 26:71 gün boyu bir hâlde sürmek)'),
    ('Anv', 'Yüksek Frekanslı Çekirdek', 'Ünsâ (30 geçiş | 1M + Sure 92 Leyl: ذ-ك-ر [eril] kökünün doğrudan Mesânî zıddı dişil; 3:36, 4:11, 49:13, 53:45, 92:3)'),
    ('xzy', 'Yüksek Frekanslı Çekirdek', 'Hizy, İhzâ\' ve Muhzî (26 geçiş | 1M: 2:85, 3:192, 11:78, 20:134, 66:8 hakikat karşısında açıkça rezil ve rüsvay olmak)'),
    ('flk', 'Yüksek Frekanslı Çekirdek', 'Fülk ve Felek (25 geçiş: 2:164, 11:37, 23:27 suları yaran gemi VE 21:33, 36:40 gök cisimlerinin döndüğü yörünge)'),
    ('mrD', 'Yüksek Frekanslı Çekirdek', 'Maraz ve Marîd (24 geçiş | 1M: ش-ف-ي doğrudan zıddı! 2:10, 8:49, 33:12, 74:31 kalplerdeki manevi hastalık ve bedensel rahatsızlık)'),
]


def generate_etap_3f():
    morph_file = os.path.join(DATA_DIR, 'quranic-corpus-morphology-0.4.txt')
    locked_file = os.path.join(DATA_DIR, 'locked_roots.json')

    with open(locked_file, 'r', encoding='utf-8') as f:
        locked_roots = set(json.load(f)['locked_roots'].keys())

    roots_count = Counter()
    roots_ayahs = defaultdict(set)
    roots_lemmas = defaultdict(Counter)
    roots_sample_loc = {}

    with open(morph_file, 'r', encoding='utf-8') as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line.startswith('('):
                continue
            m_root = re.search(r'ROOT:([^|\s]+)', line)
            if not m_root:
                continue
            bw = m_root.group(1)
            roots_count[bw] += 1
            m_loc = re.match(r'\((\d+):(\d+):(\d+):', line)
            if m_loc:
                s, a = int(m_loc.group(1)), int(m_loc.group(2))
                roots_ayahs[bw].add((s, a))
                if bw not in roots_sample_loc:
                    roots_sample_loc[bw] = f"{s}:{a}"
            m_lem = re.search(r'LEM:([^|\s]+)', line)
            if m_lem:
                roots_lemmas[bw][m_lem.group(1)] += 1

    global_ranks = {bw: idx for idx, (bw, _) in enumerate(roots_count.most_common(), 1)}
    total_corpus_tokens = sum(roots_count.values())

    items = []
    seen_bw = set()
    spec_bw_set = set()
    for etap_rank, (bw, category, rationale) in enumerate(ETAP_3F_ROOTS_SPEC, 1):
        if bw in seen_bw:
            raise ValueError(f"ETAP_3F_ROOTS_SPEC içinde mükerrer kök: {bw}")
        seen_bw.add(bw)
        spec_bw_set.add(bw)
        ar_root = to_arabic_root(bw)
        is_locked = ar_root in locked_roots
        top_lemmas = [lem for lem, _ in roots_lemmas[bw].most_common(4)]
        concept_desc = (
            ROOT_CONFIG[ar_root]['concept_name']
            if (is_locked and ar_root in ROOT_CONFIG)
            else f"Analiz Bekliyor ({', '.join(top_lemmas)})"
        )
        items.append({
            'etap_3f_rank': etap_rank,
            'category': category,
            'global_rank': global_ranks.get(bw),
            'root_arabic': ar_root,
            'root_latin': to_latin_root(bw),
            'buckwalter': bw,
            'frequency': roots_count.get(bw, 0),
            'unique_ayahs': len(roots_ayahs[bw]),
            'rationale': rationale,
            'concept_label': concept_desc,
            'is_locked': is_locked,
            'sample_ayah': roots_sample_loc.get(bw, ''),
            'top_lemmas': top_lemmas,
        })

    all_target_bw = set(spec_bw_set)
    for ar_r in locked_roots:
        cfg = ROOT_CONFIG.get(ar_r)
        if cfg and cfg.get('buckwalter'):
            all_target_bw.add(cfg['buckwalter'])
    target_covered_tokens = sum(roots_count[b] for b in all_target_bw)
    target_cov_pct = (target_covered_tokens / total_corpus_tokens) * 100.0

    locked_bw_now = {
        ROOT_CONFIG[ar_r]['buckwalter']
        for ar_r in locked_roots
        if ar_r in ROOT_CONFIG and ROOT_CONFIG[ar_r].get('buckwalter')
    }
    current_cov_pct = (sum(roots_count[b] for b in locked_bw_now) / total_corpus_tokens) * 100.0

    locked_cnt = sum(1 for i in items if i['is_locked'])
    total_tokens = sum(i['frequency'] for i in items)

    out_json = {
        'package': 'Faz 1 - Etap 3F (Kısa Sureler %100 Tam Kilit Genişletmesi [15 Sure], 3 Açık Mesânî Tepe Uçları ve %90+ Kök Kapsamı Paketi — 50 Kök)',
        'target_count': len(items),
        'locked_count': locked_cnt,
        'total_tokens_in_package': total_tokens,
        'total_corpus_tokens': total_corpus_tokens,
        'current_coverage_pct': round(current_cov_pct, 2),
        'target_coverage_pct': round(target_cov_pct, 2),
        'etap_3f_roots': items,
    }
    json_path = os.path.join(DATA_DIR, 'etap_3f_key_roots.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    pct_now_str = f"{current_cov_pct:.2f}".replace('.', ',')
    pct_target_str = f"{target_cov_pct:.2f}".replace('.', ',')
    md_lines = [
        "# ETAP 3F: KISA SURELER %100 TAM KİLİT GENİŞLETMESİ, 3 AÇIK MESÂNÎ TEPE UÇLARI VE %90+ KÖK KAPSAMI PAKETİ (50 KÖK -> 550 KÖK)",
        "## Tabula Rasa Mesânî Çözümleme Sistemi (v3.0 — Faz 2 Öncesi 550 Kök & 15 Tam Kilitli Sure Zırhı)",
        "",
        "> [!IMPORTANT]",
        f"> **HEDEF KAPSAM:** İlk 500 mühürlü kökten (`%88,50`) sonra, 8 kısa sureyi daha `%100` kilitleyen kökler (Sure 94, 96, 97, 98, 99, 102, 103, 110 → **15 tam kilitli sure**), 3 açık Mesânî referanslı tüm tepe uçlar (6/6), kritik doktrinel/çok-asıllı mayınlar ve kalan en yüksek frekanslı çekirdek kökler (**50 kök** / {total_tokens} geçiş) mühürlenerek toplam sözlük **550 kilitli köke (`%{pct_target_str}` kümülatif kök kapsamı, tüm Kur'an kelimelerinin `%93,70`'i)** ulaştırılır.",
        f"> **Etap 3F İçinde Şu Ana Kadar Mühürlenen:** {locked_cnt} / {len(items)} Kök (Toplam Mühürlü: {len(locked_roots)} Kök | Güncel Kapsam: %{pct_now_str})",
        "",
        "| Etap Sıra | Kategori | Genel Sıra | Kök (Arapça) | Kök (Latin) | Geçiş | Ayet | Örnek | Stratejik Önemi / Kavram Durumu | Durum |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |",
    ]
    for it in items:
        badge = "✅ **MÜHÜRLÜ**" if it['is_locked'] else "⏳ *Bekliyor*"
        desc = it['concept_label'] if it['is_locked'] else it['rationale']
        md_lines.append(
            f"| {it['etap_3f_rank']} | {it['category']} | {it['global_rank']} | "
            f"`{it['root_arabic']}` | `{it['root_latin']}` | **{it['frequency']}** | {it['unique_ayahs']} | "
            f"{it['sample_ayah']} | {desc} | {badge} |"
        )
    md_lines.append("")

    md_path = os.path.join(DATA_DIR, 'ETAP_3F_KAVRAM.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(
        f"Etap 3F JSON üretildi: {json_path} "
        f"({locked_cnt}/{len(items)} mühürlü | Güncel: %{pct_now_str} -> Hedef 550 kök: %{pct_target_str})"
    )
    print(f"Etap 3F Markdown üretildi: {md_path}")


if __name__ == '__main__':
    generate_etap_3f()
