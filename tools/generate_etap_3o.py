# -*- coding: utf-8 -*-
"""
Etap 3O Kilit Kavramlar (+5 Sure %100 Tam Kilidi [Sure 30 Rûm, 46 Ahkâf, 57 Hadîd, 13 Ra'd, 59 Haşr -> 60 Tam Kilitli Sure!]
ve Kalan Tüm 8 ve 7 Geçişli Çekirdek Kökler — 50 Kök -> 1.000 Kilitli Kök!)
Tabula Rasa Mesânî Çözümleme Sistemi (v3.0)

İlk 950 mühürlü kökten sonra (%96,78 köklü / %97,92 tüm kelime kapsamı),
5 sureyi daha %100 tam kilide geçiren 37 kökü (Sure 30 Rûm, 46 Ahkâf, 57 Hadîd, 13 Ra'd, 59 Haşr -> 60 tam kilitli sure; Sure 57–66 arası kesintisiz 10 surelik Medenî blok!),
kalan tüm 8 geçişli kökleri (6 kök -> ≥8 geçişli açık kök = 0!)
ve kalan tüm 7 geçişli kökleri (2'si bu 5 sure içinde [ب-ض-ع, م-ك-ث] + 7 ayrı = toplam 9 kök -> ≥7 geçişli açık kök = 0!)
olmak üzere toplam 50 kökü (224 geçiş) indeksler;
sözlüğü tarihî 1.000 kilitli kök eşiğine (%97,23 köklü / %98,21 tüm Kur'an kelimesi kapsamı) ulaştırır.
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
ETAP_3O_ROOTS_SPEC = [
    # Kategori 1: Sure %100 Tam Kilidi (+5 Tam Sure: Sure 30, 46, 57, 13, 59 -> 60 Tam Kilitli Sure! — 37 Kök)
    # --- Sure 30 Rûm (7 Kök -> 56. Tam Kilitli Sure) ---
    ('bDE', 'Sure %100 Kilidi', 'Bıd\' ve Bidâ\'a (Sure 30 Rûm kilidi + 7 geçiş: 12:19, 12:42, 12:62, 12:65, 12:88, 30:4 üç ile dokuz arası az sayı ve ticaret malı/sermaye)'),
    ('Hbr', 'Sure %100 Kilidi', 'Ahbâr ve Yuhberûn (Sure 30 Rûm kilidi + 6 geçiş: 5:44, 5:63, 9:31, 9:34, 30:15, 43:70 yazıp iz bırakan bilginler ve sevinçle ağırlanmak)'),
    ('ksf', 'Sure %100 Kilidi', 'Kisf ve Kisef (Sure 30 Rûm kilidi + 5 geçiş: 17:92, 26:187, 30:48, 34:9, 52:44 gökten veya buluttan koparılmış parça ve dilimler)'),
    ('$yb', 'Sure %100 Kilidi', 'Şeyb ve Şeybe (Sure 30 Rûm kilidi + 3 geçiş: 19:4, 30:54, 73:17 saçların ağarması, yaşlılık aklığı ve çocukları ağartan dehşet)'),
    ('rwD', 'Sure %100 Kilidi', 'Ravda ve Ravdât (Sure 30 Rûm kilidi + 2 geçiş: 30:15, 42:22 suyun biriktiği verimli, yemyeşil bahçeler)'),
    ('wdq', 'Sure %100 Kilidi', 'Vedk (Sure 30 Rûm kilidi + 2 geçiş: 24:43, 30:48 bulut yarıklarından süzülüp inen yağmur)'),
    ('msw', 'Sure %100 Kilidi', 'Tümsûn (Sure 30 Rûm son kilidi: 30:17 akşama girerken Allah\'ı tesbih etmek — 56. tam kilitli sure!)'),

    # --- Sure 46 Ahkâf (7 Kök -> 57. Tam Kilitli Sure) ---
    ('gwv', 'Sure %100 Kilidi', 'İstiğâse ve İğâse (Sure 46 Ahkâf kilidi + 5 geçiş: 8:9, 18:29, 28:15, 46:17 darlık anında imdat çağrısı yapmak ve yardıma yetişmek)'),
    ('jwz', 'Sure %100 Kilidi', 'Câveze ve Tecâveze (Sure 46 Ahkâf kilidi + 5 geçiş: 2:249, 7:138, 10:90, 18:62, 46:16 bir sınırı/suyu aşmak ve kusurları görmezden gelip geçmek)'),
    ('wzE', 'Sure %100 Kilidi', 'Evzi\' ve Yûze\'ûn (Sure 46 Ahkâf kilidi + 5 geçiş: 27:17, 27:19, 27:83, 41:19, 46:15 kalabalığı dağıtmadan düzende tutup sevk etmek ve gönlü şükre yönlendirmek)'),
    ('Aff', 'Sure %100 Kilidi', 'Üff (Sure 46 Ahkâf kilidi + 3 geçiş: 17:23, 21:67, 46:17 bıkkınlık ve küçümseme ünlemi)'),
    ('Eyy', 'Sure %100 Kilidi', 'Ayye (Sure 46 Ahkâf kilidi + 2 geçiş: 46:33, 50:15 ilk yaratmada yorulup acze düşmemek)'),
    ('nSt', 'Sure %100 Kilidi', 'Ensitû (Sure 46 Ahkâf kilidi + 2 geçiş: 7:204, 46:29 ses kesip pürdikkat dinlemek)'),
    ('Hqf', 'Sure %100 Kilidi', 'Ahkâf (Sure 46 Ahkâf son kilidi: 46:21 rüzgârla kıvrılmış uzun kum tepeleri bölgesi — 57. tam kilitli sure!)'),

    # --- Sure 57 Hadîd (7 Kök -> 58. Tam Kilitli Sure) ---
    ('fxr', 'Sure %100 Kilidi', 'Fahûr, Tefâhur ve Fahhâr (Sure 57 Hadîd kilidi + 6 geçiş: 4:36, 11:10, 31:18, 55:14, 57:20, 57:23 övünüp böbürlenmek ve pişmiş çanak çömlek)'),
    ('lms', 'Sure %100 Kilidi', 'Lemese, Lâmese ve İltemese (Sure 57 Hadîd kilidi + 5 geçiş: 4:43, 5:6, 6:7, 57:13, 72:8 elle dokunup yoklamak, temas etmek ve ışığı/yolu aramak)'),
    ('qfw', 'Sure %100 Kilidi', 'Kaffâ ve Takfu (Sure 57 Hadîd kilidi + 5 geçiş: 2:87, 5:46, 17:36, 57:27 art arda peşinden göndermek ve bilmediği şeyin ardına düşmemek)'),
    ('Amd', 'Sure %100 Kilidi', 'Emed (Sure 57 Hadîd kilidi + 4 geçiş: 3:30, 18:12, 57:16, 72:25 sonu belirli uzun zaman aralığı/süre)'),
    ('gyv', 'Sure %100 Kilidi', 'Gays ve Yuğâsu (Sure 57 Hadîd kilidi + 4 geçiş: 12:49, 31:34, 42:28, 57:20 kuraklığın ardından imdada yetişen canlandırıcı yağmur)'),
    ('qbs', 'Sure %100 Kilidi', 'Kabes ve Naktebis (Sure 57 Hadîd kilidi + 3 geçiş: 20:10, 27:7, 57:13 ateşten/ışıktan bir kor parçası alıp yararlanmak)'),
    ('hyj', 'Sure %100 Kilidi', 'Yehîc (Sure 57 Hadîd son kilidi: 39:21, 57:20 bitkinin olgunlaşıp sarararak kuruması — 58. tam kilitli sure!)'),

    # --- Sure 13 Ra\'d (8 Kök -> 59. Tam Kilitli Sure) ---
    ('mkv', 'Sure %100 Kilidi', 'Meks ve Mâkisûn (Sure 13 Ra\'d kilidi + 7 geçiş: 13:17, 17:106, 18:3, 20:10, 27:22, 28:29, 43:77 durup beklemek, yeryüzünde kalıcı olmak ve sindirerek ağır ağır okumak)'),
    ('drA', 'Sure %100 Kilidi', 'Der\' ve İddâra\'e (Sure 13 Ra\'d kilidi + 5 geçiş: 2:72, 3:168, 13:22, 24:8, 28:54 kötülüğü iyilikle veya cezayı savıp uzaklaştırmak, suçu birbirine atmak)'),
    ('syl', 'Sure %100 Kilidi', 'Seyl ve Esâle (Sure 13 Ra\'d kilidi + 4 geçiş: 13:17, 34:12, 34:16 vadilerden coşkun biçimde akan sel ve erimiş bakırı akıtmak)'),
    ('zbd', 'Sure %100 Kilidi', 'Zebed (Sure 13 Ra\'d kilidi + 3 geçiş: 13:17 selin ve eriyen madenin üstünde toplanıp uçup giden yüzeysel köpük)'),
    ('Snw', 'Sure %100 Kilidi', 'Sinvân (Sure 13 Ra\'d kilidi + 2 geçiş: 13:4 tek bir kökten çatallanıp yükselen ikiz hurma ağaçları)'),
    ('rEd', 'Sure %100 Kilidi', 'Ra\'d (Sure 13 Ra\'d kilidi + 2 geçiş: 2:19, 13:13 bulutlarda yankılanan gök gürültüsü)'),
    ('jfA', 'Sure %100 Kilidi', 'Cüfâ\' (Sure 13 Ra\'d kilidi: 13:17 selin kenara atıp savurduğu işe yaramaz posa/çerçöp)'),
    ('mHl', 'Sure %100 Kilidi', 'Mihâl (Sure 13 Ra\'d son kilidi: 13:13 karşı konulmaz sarsıcı kudret ve şiddetli karşılık — 59. tam kilitli sure!)'),

    # --- Sure 59 Haşr (8 Kök -> 60. Tam Kilitli Sure! Sure 57-66 Arası 10 Sure Kesintisiz %100!) ---
    ('rEb', 'Sure %100 Kilidi', 'Ru\'b (Sure 59 Haşr kilidi + 5 geçiş: 3:151, 8:12, 18:18, 33:26, 59:2 kalbi doldurup iradeyi felç eden derin ürperti ve korku)'),
    ('jdr', 'Sure %100 Kilidi', 'Cidâr ve Cüdur (Sure 59 Haşr kilidi + 4 geçiş: 9:97, 18:77, 18:82, 59:14 kuşatıcı duvar, siper ve bir şeye daha layık/yakışır olmak)'),
    ('xSS', 'Sure %100 Kilidi', 'Hasâsa ve Yahtassu (Sure 59 Haşr kilidi + 4 geçiş: 2:105, 3:74, 8:25, 59:9 başkalarından ayırıp tahsis etmek ve derin darlık/yoksulluk)'),
    ('Hwj', 'Sure %100 Kilidi', 'Hâce (Sure 59 Haşr kilidi + 3 geçiş: 12:68, 40:80, 59:9 gönülde taşınan arzu, ihtiyaç ve göğüsteki eksik hissi)'),
    ('dwl', 'Sure %100 Kilidi', 'Dûle ve Nüdâvilu (Sure 59 Haşr kilidi + 2 geçiş: 3:140, 59:7 günlerin insanlar arasında el değiştirmesi ve servetin yalnızca zenginler arasında dönüp durmaması)'),
    ('hmn', 'Sure %100 Kilidi', 'Müheymin (Sure 59 Haşr kilidi + 2 geçiş: 5:48, 59:23 gözetip koruyan, güven altında tutup denetleyen)'),
    ('wjf', 'Sure %100 Kilidi', 'Evcefe ve Vâcife (Sure 59 Haşr kilidi + 2 geçiş: 59:6, 79:8 binekleri hızla koşturmak ve kalplerin korkuyla küt küt çarpması)'),
    ('xrb', 'Sure %100 Kilidi', 'Harâb ve Yuhribûn (Sure 59 Haşr son kilidi: 2:114, 59:2 yapıyı yıkıp ıssız harabeye çevirmek — 60. tam kilitli sure!)'),

    # Kategori 2: Kalan Tüm 8 Geçişli Çekirdek Kökler (6 Kök -> ≥8 geçişli açık kök = 0!)
    ('sqT', 'Yüksek Frekanslı Çekirdek', 'Sukût ve İskât (8 geçiş: 6:59, 7:149, 9:49, 17:92, 19:25, 26:187, 34:9, 52:44 yukarıdan aşağıya düşmek, yaprağın ve hurmanın düşmesi, pişmanlık ve gökten parça düşürmek)'),
    ('slf', 'Yüksek Frekanslı Çekirdek', 'Selef ve Eslefe (8 geçiş: 2:275, 4:22, 4:23, 5:95, 8:38, 10:30, 43:56, 69:24 geride kalıp geçmiş olmak, önceden yapıp gönderdiğini görmek)'),
    ('hbT', 'Yüksek Frekanslı Çekirdek', 'Hubût (8 geçiş: 2:36, 2:38, 2:61, 2:74, 7:13, 7:24, 11:48, 20:123 yüksek konumdan aşağıya/yeryüzüne veya bir kente inmek)'),
    ('frT', 'Yüksek Frekanslı Çekirdek', 'Furt ve Tefrît (8 geçiş: 6:31, 6:38, 6:61, 12:80, 16:62, 18:28, 20:45, 39:56 sınırı aşıp ölçüsüzlüğe sapmak veya görevde ihmalkâr/eksik bırakmak)'),
    ('rjf', 'Yüksek Frekanslı Çekirdek', 'Recfe, Râcife ve Mürcifûn (8 geçiş: 7:78, 7:91, 7:155, 29:37, 33:60, 73:14, 79:6 şiddetli yer sarsıntısı ve şehirde panik yayan bozguncular)'),
    ('xwl', 'Yüksek Frekanslı Çekirdek', 'Hâl, Hâlât ve Havvele (8 geçiş: 4:23, 6:94, 24:61, 33:50, 39:8, 39:49 dayı, teyze ve emanet/nimet olarak bahşetmek — ≥8 geçişli açık kök = 0!)'),

    # Kategori 3: Kalan Tüm 7 Geçişli Çekirdek Kökler (7 Kök -> ≥7 geçişli açık kök = 0! 1.000. KÖK!)
    ('nSf', 'Yüksek Frekanslı Çekirdek', 'Nısf (7 geçiş: 2:237, 4:11, 4:12, 4:25, 4:176, 73:3, 73:20 bir bütünün tam ikiye bölünmüş yarısı — miras, mehir ve gece payı)'),
    ('HZZ', 'Yüksek Frekanslı Çekirdek', 'Hazz (7 geçiş: 3:176, 4:11, 4:176, 5:13, 5:14, 28:79, 41:35 bir kimseye düşen belirli pay, hisse ve büyük nasip)'),
    ('Emh', 'Yüksek Frekanslı Çekirdek', 'Ya\'mehûn (7 geçiş: 2:15, 6:110, 7:186, 10:11, 15:72, 23:75, 27:4 yön duygusunu yitirip şaşkınlık içinde bocalamak)'),
    ('xTf', 'Yüksek Frekanslı Çekirdek', 'Hatf ve Tehattuf (7 geçiş: 2:20, 8:26, 22:31, 28:57, 29:67, 37:10 aniden hızla kapıp götürmek ve şimşeğin gözleri kapıvermesi)'),
    ('mwj', 'Yüksek Frekanslı Çekirdek', 'Mevc ve Yemûc (7 geçiş: 10:22, 11:42, 11:43, 18:99, 24:40, 31:32 kabarıp çalkalanan deniz dalgaları ve kalabalıkların dalga dalga birbirine karışması)'),
    ('grf', 'Yüksek Frekanslı Çekirdek', 'Gurfe ve İğterefe (7 geçiş: 2:249, 25:75, 29:58, 34:37, 39:20 avuçla bir yudum su almak ve yüksek üst kat odaları/köşkler)'),
    ('bEl', 'Yüksek Frekanslı Çekirdek', 'Ba\'l ve Bu\'ûle (7 geçiş: 2:228, 4:128, 11:72, 24:31, 37:125 eş/koca ve eski kavimlerin taptığı Ba\'l — ≥7 geçişli açık kök = 0! 1.000. KÖK!)'),
]


def generate_etap_3o():
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
    for etap_rank, (bw, category, rationale) in enumerate(ETAP_3O_ROOTS_SPEC, 1):
        if bw in seen_bw:
            raise ValueError(f"ETAP_3O_ROOTS_SPEC içinde mükerrer kök: {bw}")
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
            'etap_3o_rank': etap_rank,
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
        'package': 'Faz 1 - Etap 3O (+5 Sure %100 Tam Kilidi [Sure 30, 46, 57, 13, 59 -> 60 Tam Kilitli Sure] ve Kalan Tüm 8 ve 7 Geçişli Çekirdek Kökler — 50 Kök -> 1.000 Kök!)',
        'target_count': len(items),
        'locked_count': locked_cnt,
        'total_tokens_in_package': total_tokens,
        'total_corpus_tokens': total_corpus_tokens,
        'current_coverage_pct': round(current_cov_pct, 2),
        'target_coverage_pct': round(target_cov_pct, 2),
        'etap_3o_roots': items,
    }
    json_path = os.path.join(DATA_DIR, 'etap_3o_key_roots.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    pct_now_str = f"{current_cov_pct:.2f}".replace('.', ',')
    pct_target_str = f"{target_cov_pct:.2f}".replace('.', ',')
    md_lines = [
        "# ETAP 3O: +5 SURE %100 TAM KİLİDİ (60 SURE) VE KALAN TÜM 8 & 7 GEÇİŞLİ ÇEKİRDEK KÖKLER (50 KÖK -> 1.000 KÖK!)",
        "## Tabula Rasa Mesânî Çözümleme Sistemi (v3.0 — Faz 1 1.000 Kök, %97,23 Kapsam & 60 Tam Kilitli Sure Zırhı)",
        "",
        "> [!IMPORTANT]",
        f"> **HEDEF KAPSAM:** İlk 950 mühürlü kökten (`%96,78`) sonra, `5` sureyi daha `%100` kilitleyen `37` kök (Sure 30 Rûm, 46 Ahkâf, 57 Hadîd, 13 Ra'd, 59 Haşr → **60 tam kilitli sure**; Sure 57–66 arası kesintisiz 10 surelik Medenî blok!), kalan tüm `8` geçişli kökler (`6` kök → `≥8` açık kök `0`!) ve kalan tüm `7` geçişli kökler (`2`'si bu surelerde + `7` ayrı = `≥7` açık kök `0`!) olmak üzere **50 kök** ({total_tokens} geçiş) mühürlenerek toplam sözlük **1.000 kilitli köke (`%{pct_target_str}` kümülatif kök kapsamı, tüm Kur'an kelimelerinin `%98,21`'i)** ulaştırılır.",
        f"> **Etap 3O İçinde Şu Ana Kadar Mühürlenen:** {locked_cnt} / {len(items)} Kök (Toplam Mühürlü: {len(locked_roots)} Kök | Güncel Kapsam: %{pct_now_str})",
        "",
        "| Etap Sıra | Kategori | Genel Sıra | Kök (Arapça) | Kök (Latin) | Geçiş | Ayet | Örnek | Stratejik Önemi / Kavram Durumu | Durum |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |",
    ]
    for it in items:
        badge = "✅ **MÜHÜRLÜ**" if it['is_locked'] else "⏳ *Bekliyor*"
        desc = it['concept_label'] if it['is_locked'] else it['rationale']
        md_lines.append(
            f"| {it['etap_3o_rank']} | {it['category']} | {it['global_rank']} | "
            f"`{it['root_arabic']}` | `{it['root_latin']}` | **{it['frequency']}** | {it['unique_ayahs']} | "
            f"{it['sample_ayah']} | {desc} | {badge} |"
        )
    md_lines.append("")

    md_path = os.path.join(DATA_DIR, 'ETAP_3O_KAVRAM.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(
        f"Etap 3O JSON üretildi: {json_path} "
        f"({locked_cnt}/{len(items)} mühürlü | Güncel: %{pct_now_str} -> Hedef 1000 kök: %{pct_target_str})"
    )
    print(f"Etap 3O Markdown üretildi: {md_path}")


if __name__ == '__main__':
    generate_etap_3o()
