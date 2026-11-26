# -*- coding: utf-8 -*-
"""
Etap 3N Kilit Kavramlar (+5 Sure %100 Tam Kilidi [Sure 32 Secde, 44 Duhân, 78 Nebe, 76 İnsân, 70 Meâric -> 55 Tam Kilitli Sure!]
ve Kalan Tüm 9 Geçişli Çekirdek Kökler + 2 Stratejik Kök — 50 Kök -> 950 Kilitli Kök)
Tabula Rasa Mesânî Çözümleme Sistemi (v3.0)

İlk 900 mühürlü kökten sonra (%96,32 köklü / %97,62 tüm kelime kapsamı),
5 sureyi daha %100 tam kilide geçiren 38 kökü (Sure 32 Secde, 44 Duhân, 78 Nebe, 76 İnsân, 70 Meâric -> 55 tam kilitli sure),
kalan tüm 9 geçişli çekirdek kökleri (4'ü bu 5 sure içinde + 10'u ayrı = toplam 14 kök -> ≥9 geçişli açık kök = 0!)
ve 2 stratejik kökü (م-ل-ح [2 açık Mesânî referansı] + ل-ط-ف [8 geçiş]) olmak üzere toplam 50 kökü (231 geçiş) indeksler;
sözlüğü 950 kilitli köke (%96,78 köklü / %97,92 tüm Kur'an kelimesi kapsamı) ulaştırır.
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
ETAP_3N_ROOTS_SPEC = [
    # Kategori 1: Sure %100 Tam Kilidi (+5 Tam Sure: Sure 32, 44, 78, 76, 70 -> 55 Tam Kilitli Sure! — 38 Kök)
    # --- Sure 32 Secde (7 Kök -> 51. Tam Kilitli Sure) ---
    ('Erj', 'Sure %100 Kilidi', 'Urûc, Meâric ve A\'rec (Sure 32 Secde + Sure 70 Meâric ortak kilidi | 1M + 9 geçiş: 15:14, 24:61, 32:5, 34:2, 43:33, 48:17, 57:4, 70:3, 70:4 basamaklı yükselme/çıkış merdivenleri ve yürüyüşte aksama)'),
    ('nsl', 'Sure %100 Kilidi', 'Nesl ve Yensilûn (Sure 32 Secde kilidi + 4 geçiş: 2:205, 21:96, 32:8, 36:51 soydan süzülüp çıkma ve tepelerden/kabirlerden hızla akın etme)'),
    ('DjE', 'Sure %100 Kilidi', 'Medâci\' (Sure 32 Secde kilidi + 3 geçiş: 3:154, 4:34, 32:16 yan üzere uzanılan yataklar ve düşüp yatılan yerler)'),
    ('nks', 'Sure %100 Kilidi', 'Neks, Nâkisû ve Tenkîs (Sure 32 Secde kilidi + 3 geçiş: 21:65, 32:12, 36:68 baş aşağı çevirmek, başını mahcubiyetle eğmek ve yaşlılıkta yaratılışı geriye döndürmek)'),
    ('sll', 'Sure %100 Kilidi', 'Sülâle ve Yetesellelûn (Sure 32 Secde kilidi + 3 geçiş: 23:12, 24:63, 32:8 yumuşakça süzülüp çekilen öz ve sezdirmeden sıvışıp çıkma)'),
    ('jrz', 'Sure %100 Kilidi', 'Cüruz (Sure 32 Secde kilidi + 2 geçiş: 18:8, 32:27 bitkisiz, kupkuru, tamamen sıyrılıp tıraşlanmış çorak toprak)'),
    ('jfw', 'Sure %100 Kilidi', 'Tetecâfâ (Sure 32 Secde son kilidi: 32:16 yanların yataklardan uzaklaşıp ayrılması — 51. tam kilitli sure!)'),

    # --- Sure 44 Duhân (7 Kök -> 52. Tam Kilitli Sure) ---
    ('bky', 'Sure %100 Kilidi', 'Bükâ ve Ebkâ (Sure 44 Duhân kilidi + 7 geçiş: 9:82, 12:16, 17:109, 19:58, 44:29, 53:43, 53:60 gözyaşı döküp ağlamak ve ağlatmak)'),
    ('Ady', 'Sure %100 Kilidi', 'Edâ (Sure 44 Duhân kilidi + 6 geçiş: 2:178, 2:283, 3:75, 4:58, 44:18 emaneti, borcu veya sorumluluğu eksiksiz biçimde sahibine ulaştırıp ödemek)'),
    ('zqm', 'Sure %100 Kilidi', 'Zakkûm (Sure 44 Duhân kilidi + 3 geçiş: 37:62, 44:43, 56:52 yutulması güç, acı ve yakıcı ceza ağacı)'),
    ('Etl', 'Sure %100 Kilidi', 'Atül ve Utüll (Sure 44 Duhân kilidi + 2 geçiş: 44:47, 68:13 şiddetle yakalayıp sürüklemek ve kaba/haşin zorbalık)'),
    ('dxn', 'Sure %100 Kilidi', 'Duhân (Sure 44 Duhân kilidi + 2 geçiş: 41:11, 44:10 göğün ilk oluşumundaki gaz/duman hâli ve apaçık kuşatan duman)'),
    ('gly', 'Sure %100 Kilidi', 'Galy (Sure 44 Duhân kilidi + 2 geçiş: 44:45, 44:46 kaynar suyun karınlarda erimiş maden gibi fokurdayıp kaynaması)'),
    ('rhw', 'Sure %100 Kilidi', 'Rehv (Sure 44 Duhân son kilidi: 44:24 denizi yarılmış, dingin ve açık bir geçit hâlinde bırakmak — 52. tam kilitli sure!)'),

    # --- Sure 78 Nebe (8 Kök -> 53. Tam Kilitli Sure) ---
    ('nwm', 'Sure %100 Kilidi', 'Nevm ve Menâm (Sure 78 Nebe kilidi + 9 geçiş: 2:255, 7:97, 8:43, 25:47, 30:23, 37:102, 39:42, 68:19, 78:9 dinlendirici uyku, uyku hâli ve Allah\'ın uykudan münezzeh oluşu)'),
    ('kAs', 'Sure %100 Kilidi', 'Ke\'s (Sure 78 Nebe + Sure 76 İnsân ortak kilidi + 6 geçiş: 37:45, 52:23, 56:18, 76:5, 76:17, 78:34 içiyle dolu ikram kadehi)'),
    ('kEb', 'Sure %100 Kilidi', 'Ka\'b, Ka\'be ve Kevâib (Sure 78 Nebe kilidi + 4 geçiş: 5:6, 5:95, 5:97, 78:33 çıkıntılı eklem/topuk, küp biçimli Kâbe ve olgunlaşıp serpilen eşler)'),
    ('srb', 'Sure %100 Kilidi', 'Serâb ve Sârib (Sure 78 Nebe kilidi + 4 geçiş: 13:10, 18:61, 24:39, 78:20 çöldeki yanıltıcı serap, gündüzün açığa çıkıp yol almak ve balığın suda yol açması)'),
    ('wfq', 'Sure %100 Kilidi', 'Tevfîk ve Vifâk (Sure 78 Nebe kilidi + 4 geçiş: 4:35, 4:62, 11:88, 78:26 uyumlu uzlaşma, başarıya denk düşürme ve tam denk karşılık)'),
    ('dhq', 'Sure %100 Kilidi', 'Dihâk (Sure 78 Nebe kilidi: 78:34 ağzına kadar dopdolu, taşacak derecede doldurulmuş kadeh)'),
    ('vjj', 'Sure %100 Kilidi', 'Seccâc (Sure 78 Nebe kilidi: 78:14 yağmur yüklü bulutlardan şarıl şarıl, kesintisiz dökülen su)'),
    ('whj', 'Sure %100 Kilidi', 'Vehhâc (Sure 78 Nebe son kilidi: 78:13 hem parıl parıl ışık hem yakıcı ısı yayan güneş kandili — 53. tam kilitli sure!)'),

    # --- Sure 76 İnsân (8 Net Kök -> 54. Tam Kilitli Sure) ---
    ('Hly', 'Sure %100 Kilidi', 'Hilye ve Huliyy (Sure 76 İnsân kilidi + 9 geçiş: 7:148, 13:17, 16:14, 18:31, 22:23, 35:12, 35:33, 43:18, 76:21 takı, ziynet ve bileziklerle süslenmek)'),
    ('xDr', 'Sure %100 Kilidi', 'Hadır ve Hudr (Sure 76 İnsân kilidi + 8 geçiş: 6:99, 12:43, 12:46, 18:31, 22:63, 36:80, 55:76, 76:21 canlı yeşil bitki örtüsü, yeşil başaklar ve yeşil dokumalar)'),
    ('lAlA', 'Sure %100 Kilidi', 'Lü\'lü\' (Sure 76 İnsân kilidi + 6 geçiş: 22:23, 35:33, 52:24, 55:22, 56:23, 76:19 denizden çıkarılan sedefli ve parlak inci)'),
    ('slsl', 'Sure %100 Kilidi', 'Silsile ve Selâsil (Sure 76 İnsân kilidi + 3 geçiş: 40:71, 69:32, 76:4 halkaları birbirine kenetli uzun zincirler)'),
    ('qTf', 'Sure %100 Kilidi', 'Kutûf (Sure 76 İnsân kilidi + 2 geçiş: 69:23, 76:14 el uzatılınca kolayca devşirilebilen salkım/meyveler)'),
    ('m$j', 'Sure %100 Kilidi', 'Emşâc (Sure 76 İnsân kilidi: 76:2 birbirine karışmış/bileşik hâldeki damla özü)'),
    ('qmTr', 'Sure %100 Kilidi', 'Kamtârîr (Sure 76 İnsân kilidi: 76:10 şiddetinden yüzleri buruşturan, pek çetin ve somurtkan gün)'),
    ('zmhr', 'Sure %100 Kilidi', 'Zemherîr (Sure 76 İnsân son kilidi: 76:13 dondurucu ve yakıcı derecede şiddetli ayaz — 54. tam kilitli sure!)'),

    # --- Sure 70 Meâric (8 Net Kök -> 55. Tam Kilitli Sure) ---
    ('dwm', 'Sure %100 Kilidi', 'Devâm ve Dâim (Sure 70 Meâric kilidi + 9 geçiş: 3:75, 5:24, 5:96, 5:117, 11:107, 11:108, 13:35, 19:31, 70:23 kesintiye uğramadan sürmek, sebatlı devamlılık)'),
    ('hTE', 'Sure %100 Kilidi', 'Muhti\'în (Sure 70 Meâric kilidi + 3 geçiş: 14:43, 54:8, 70:36 boyunlarını ileri uzatıp gözlerini dikerek hızla koşanlar)'),
    ('jdv', 'Sure %100 Kilidi', 'Ecdâs (Sure 70 Meâric kilidi + 3 geçiş: 36:51, 54:7, 70:43 ölülerin gömülü bulunduğu mezarlar/kabirler)'),
    ('$wy', 'Sure %100 Kilidi', 'Şevâ ve Yeşvî (Sure 70 Meâric kilidi + 2 geçiş: 18:29, 70:16 yüzleri kavurup haşlayan sıcaklık ve baş derisi/uzuvlar)'),
    ('jzE', 'Sure %100 Kilidi', 'Cezû\' ve Ceza\' (Sure 70 Meâric kilidi + 2 geçiş: 14:21, 70:20 musibet karşısında direncini yitirip sızlanarak paniklemek)'),
    ('Ezw', 'Sure %100 Kilidi', 'Izîn (Sure 70 Meâric kilidi: 70:37 sağdan ve soldan dağınık halkalar/gruplar hâlinde toplanmak)'),
    ('hlE', 'Sure %100 Kilidi', 'Helû\' (Sure 70 Meâric kilidi: 70:19 darlıkta çabuk sızlanan, bollukta cimrileşen aşırı hırslı ve dayanıksız yapı)'),
    ('wfD', 'Sure %100 Kilidi', 'Yûfidûn (Sure 70 Meâric son kilidi: 70:43 dikili hedeflere doğru aceleyle koşuşturmak — 55. tam kilitli sure!)'),

    # Kategori 2: Kalan Tüm 9 Geçişli Çekirdek Kökler (10 Kök -> ≥9 geçişli açık kök = 0!)
    ('Enq', 'Yüksek Frekanslı Çekirdek', 'Unuk ve A\'nâk (9 geçiş: 8:12, 13:5, 17:13, 17:29, 26:4, 34:33, 36:8, 38:33, 40:71 boyun, sorumluluğun boyna dolanması ve boyun eğmek)'),
    ('Ewm', 'Yüksek Frekanslı Çekirdek', 'Âm ve Âmeyn (9 geçiş: 2:259, 9:28, 9:37, 9:126, 12:49, 29:14, 31:14 mevsim döngüsünü tamamlayan tam yıl)'),
    ('Ezm', 'Yüksek Frekanslı Çekirdek', 'Azm ve Azeme (9 geçiş: 2:227, 2:235, 3:159, 3:186, 20:115, 31:17, 42:43, 46:35, 47:21 tereddütsüz kararlılık ve niyeti kesinleştirip bağlamak)'),
    ('bqr', 'Yüksek Frekanslı Çekirdek', 'Bakara ve Bakarât (9 geçiş: 2:67, 2:68, 2:69, 2:70, 2:71, 6:144, 6:146, 12:43, 12:46 sığır/inek kıssası, kurallar ve rüya sembolü)'),
    ('fyD', 'Yüksek Frekanslı Çekirdek', 'Efâda ve Tefîdu (9 geçiş: 2:198, 2:199, 5:83, 7:50, 9:92, 10:61, 24:14, 46:8 taşmak, gözyaşı dökmek, topluca akın etmek ve söze dalmak)'),
    ('hmm', 'Yüksek Frekanslı Çekirdek', 'Hemme ve Ehemme (9 geçiş: 3:122, 3:154, 4:113, 5:11, 9:13, 9:74, 12:24, 40:5 bir işe niyetlenip yönelmek ve kaygıyla zihni meşgul etmek)'),
    ('lwn', 'Yüksek Frekanslı Çekirdek', 'Levn ve Elvân (9 geçiş: 2:69, 16:13, 16:69, 30:22, 35:27, 35:28, 39:21 yaratılıştaki renk, ton ve dış görünüş çeşitliliği)'),
    ('q*f', 'Yüksek Frekanslı Çekirdek', 'Kazf (9 geçiş: 20:39, 20:87, 21:18, 33:26, 34:48, 34:53, 37:8, 59:2 uzağa fırlatıp atmak, kalplere korku salmak ve hakkı batılın üzerine fırlatmak)'),
    ('qbD', 'Yüksek Frekanslı Çekirdek', 'Kabd ve Makbûda (9 geçiş: 2:245, 2:283, 9:67, 20:96, 25:46, 39:67, 67:19 avuçlayıp toplamak, daraltıp kısmak ve kanatlarını kapamak)'),
    ('xyl', 'Yüksek Frekanslı Çekirdek', 'Hayl, Muhtâl ve Yuhayyel (9 geçiş: 3:14, 4:36, 8:60, 16:8, 17:64, 20:66, 31:18, 57:23, 59:6 atlı birlikler, kibirle böbürlenen ve gözde canlanan yanılsama — ≥9 geçişli açık kök = 0!)'),

    # Kategori 3: Açık Mesânî Referansı ve 8 Geçişli Çekirdek (2 Kök -> 950 KÖK!)
    ('mlH', 'Mesânî Karşılık Köprüsü', 'Milh ve Ücâc (2 açık Mesânî referansı + 2 geçiş: 25:53, 35:12 acı/tuzlu suyun tatlı suyla karışmadan yan yana akması)'),
    ('lTf', 'Yüksek Frekanslı Çekirdek', 'Latîf ve Yetelattaf (8 geçiş: 6:103, 12:100, 18:19, 22:63, 31:16, 33:34, 42:19, 67:14 en ince ayrıntıya nüfuz eden incelik ve yumuşak/nazik davranış — 950. Kök!)'),
]


def generate_etap_3n():
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
    for etap_rank, (bw, category, rationale) in enumerate(ETAP_3N_ROOTS_SPEC, 1):
        if bw in seen_bw:
            raise ValueError(f"ETAP_3N_ROOTS_SPEC içinde mükerrer kök: {bw}")
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
            'etap_3n_rank': etap_rank,
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
        'package': 'Faz 1 - Etap 3N (+5 Sure %100 Tam Kilidi [Sure 32, 44, 78, 76, 70 -> 55 Tam Kilitli Sure] ve Kalan Tüm 9 Geçişli Çekirdek Kökler + 2 Stratejik Kök — 50 Kök -> 950 Kök)',
        'target_count': len(items),
        'locked_count': locked_cnt,
        'total_tokens_in_package': total_tokens,
        'total_corpus_tokens': total_corpus_tokens,
        'current_coverage_pct': round(current_cov_pct, 2),
        'target_coverage_pct': round(target_cov_pct, 2),
        'etap_3n_roots': items,
    }
    json_path = os.path.join(DATA_DIR, 'etap_3n_key_roots.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    pct_now_str = f"{current_cov_pct:.2f}".replace('.', ',')
    pct_target_str = f"{target_cov_pct:.2f}".replace('.', ',')
    md_lines = [
        "# ETAP 3N: +5 SURE %100 TAM KİLİDİ (55 SURE) VE KALAN TÜM 9 GEÇİŞLİ ÇEKİRDEK KÖKLER (50 KÖK -> 950 KÖK)",
        "## Tabula Rasa Mesânî Çözümleme Sistemi (v3.0 — Faz 1 950 Kök, %96,78 Kapsam & 55 Tam Kilitli Sure Zırhı)",
        "",
        "> [!IMPORTANT]",
        f"> **HEDEF KAPSAM:** İlk 900 mühürlü kökten (`%96,32`) sonra, `5` sureyi daha `%100` kilitleyen `38` kök (Sure 32 Secde, 44 Duhân, 78 Nebe, 76 İnsân, 70 Meâric → **55 tam kilitli sure**), kalan tüm `9` geçişli çekirdek kökler (`4`'ü bu surelerde + `10` ayrı = `≥9` geçişli açık kök `0`!) ve `2` stratejik kök (`م-ل-ح` açık Mesânî köprüsü + `ل-ط-ف` 8 geçiş) olmak üzere **50 kök** ({total_tokens} geçiş) mühürlenerek toplam sözlük **950 kilitli köke (`%{pct_target_str}` kümülatif kök kapsamı, tüm Kur'an kelimelerinin `%97,92`'si)** ulaştırılır.",
        f"> **Etap 3N İçinde Şu Ana Kadar Mühürlenen:** {locked_cnt} / {len(items)} Kök (Toplam Mühürlü: {len(locked_roots)} Kök | Güncel Kapsam: %{pct_now_str})",
        "",
        "| Etap Sıra | Kategori | Genel Sıra | Kök (Arapça) | Kök (Latin) | Geçiş | Ayet | Örnek | Stratejik Önemi / Kavram Durumu | Durum |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |",
    ]
    for it in items:
        badge = "✅ **MÜHÜRLÜ**" if it['is_locked'] else "⏳ *Bekliyor*"
        desc = it['concept_label'] if it['is_locked'] else it['rationale']
        md_lines.append(
            f"| {it['etap_3n_rank']} | {it['category']} | {it['global_rank']} | "
            f"`{it['root_arabic']}` | `{it['root_latin']}` | **{it['frequency']}** | {it['unique_ayahs']} | "
            f"{it['sample_ayah']} | {desc} | {badge} |"
        )
    md_lines.append("")

    md_path = os.path.join(DATA_DIR, 'ETAP_3N_KAVRAM.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(
        f"Etap 3N JSON üretildi: {json_path} "
        f"({locked_cnt}/{len(items)} mühürlü | Güncel: %{pct_now_str} -> Hedef 950 kök: %{pct_target_str})"
    )
    print(f"Etap 3N Markdown üretildi: {md_path}")


if __name__ == '__main__':
    generate_etap_3n()
