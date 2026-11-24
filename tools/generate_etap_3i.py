# -*- coding: utf-8 -*-
"""
Etap 3I Kilit Kavramlar (Yüksek Frekanslı Çekirdek Kökler [18–13 Geçiş] ve
+4 Sure %100 Tam Kilidi [Sure 104, 62, 105, 111 -> 29 Tam Kilitli Sure!] — 50 Kök -> 700 Kilitli Kök)
Tabula Rasa Mesânî Çözümleme Sistemi (v3.0)

İlk 650 mühürlü kökten sonra (%93,13 kümülatif kök kapsamı),
kalan 18–14 geçişli 20 çekirdek kökü, 4 sureyi daha %100 tam kilide geçiren 19 kökü
(Sure 104 Hümeze, Sure 62 Cum'a, Sure 105 Fîl, Sure 111 Mesed -> 29 tam kilitli sure)
ve 13 geçişli 11 çekirdek kökü (toplam 50 kök) indeksler; sözlüğü 700 köke taşır.
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
ETAP_3I_ROOTS_SPEC = [
    # Kategori 1: En Yüksek Frekanslı Çekirdek Kökler I (18-14 Geçiş — 20 Kök)
    ('mkn', 'Yüksek Frekanslı Çekirdek', 'Temkîn ve Mekîn (18 geçiş / 16 ayet: 6:6, 7:10, 8:71, 12:21, 12:54 sağlam zemin, yerleşik güç ve korunaklı konum)'),
    ('mdn', 'Yüksek Frekanslı Çekirdek', 'Medîne ve Medâin (17 geçiş / 17 ayet: 7:111, 7:123, 9:101, 9:120, 12:30 düzenli şehir ve uygar yerleşim merkezi)'),
    ('bwA', 'Yüksek Frekanslı Çekirdek', 'Bev\' ve Tebevvü\' (17 geçiş / 16 ayet: 2:61, 2:90, 3:112, 3:121, 3:162 bir yere yerleşmek, konaklamak ve dönüp yüklenmek)'),
    ('swq', 'Yüksek Frekanslı Çekirdek', 'Sevk, Sâk ve Esveâk (17 geçiş / 16 ayet: 7:57, 8:6, 19:86, 25:7, 25:20 gütmek/sevk etmek, baldır ve çarşı)'),
    ('rbS', 'Yüksek Frekanslı Çekirdek', 'Terabbus ve Müterabbis (17 geçiş / 12 ayet: 2:226, 2:228, 2:234, 4:141, 9:24 fırsat veya süre tamamlanmasını beklemek/gözetlemek)'),
    ('Etd', 'Yüksek Frekanslı Çekirdek', 'Atîd ve A\'tede (16 geçiş / 16 ayet: 4:18, 4:37, 4:151, 4:161, 12:31 eksiği kalmamış şekilde önceden hazırlayıp hazır bekletmek)'),
    ('gdw', 'Yüksek Frekanslı Çekirdek', 'Gudüvv ve Gad (16 geçiş / 16 ayet: 3:121, 6:52, 7:205, 12:12, 13:15 sabahın ilk aydınlık vakti, erkenden çıkış ve yarın)'),
    ('mhd', 'Yüksek Frekanslı Çekirdek', 'Mehd, Mihâd ve Temhîd (16 geçiş / 15 ayet: 2:206, 3:12, 3:46, 3:197, 5:110 beşikten yayvan döşeğe kadar düzleştirip hazırlanan zemin)'),
    ('kyl', 'Yüksek Frekanslı Çekirdek', 'Keyl, Mikyâl ve İktiyâl (16 geçiş / 13 ayet: 6:152, 7:85, 11:84, 11:85, 12:59 hacim ölçüsü ve hak ölçüsünü tam teslim etmek)'),
    ('swm', 'Yüksek Frekanslı Çekirdek', 'Sevm, Sîmâ ve Müsevvem (15 geçiş / 15 ayet: 2:49, 2:273, 3:14, 3:125, 7:46 belirgin işaret/damga, salıverme ve azaba maruz bırakma)'),
    ('kff', 'Yüksek Frekanslı Çekirdek', 'Keff, Keffân ve Kâffe (15 geçiş / 14 ayet: 2:208, 4:77, 4:84, 4:91, 5:11 avuç içi, elini tutup durdurmak ve topyekûn kuşatma)'),
    ('mTr', 'Yüksek Frekanslı Çekirdek', 'Matar ve İmtâr (15 geçiş / 9 ayet: 4:102, 7:84, 8:32, 11:82, 15:74 gökten yoğun yağmur ve taş yağdırılması)'),
    ('E$w', 'Yüksek Frekanslı Çekirdek', 'Aşiyy, İşâ\' ve Ya\'şû (14 geçiş / 14 ayet: 3:41, 6:52, 12:16, 18:28, 19:11 gün batımı akşam karanlığı ve zifiri körlük/gaflet)'),
    ('vwy', 'Yüksek Frekanslı Çekirdek', 'Mesvâ ve Sâvî (14 geçiş / 14 ayet: 3:151, 6:128, 12:21, 12:23, 16:29 kalıcı konak/ikamet yeri ve sükûnla yerleşmek)'),
    ('wSf', 'Yüksek Frekanslı Çekirdek', 'Vasf ve Yasifûn (14 geçiş / 14 ayet: 6:100, 6:139, 12:18, 12:77, 16:62 yakıştırma/nitelendirme ile asılsız isnatta bulunmak)'),
    ('Sff', 'Yüksek Frekanslı Çekirdek', 'Saff, Sâffât ve Masfûfe (14 geçiş / 12 ayet: 18:48, 20:64, 22:36, 24:41, 37:1 düzgün sıra hâlinde dizilmek ve kanat açıp süzülmek)'),
    ('lwm', 'Yüksek Frekanslı Çekirdek', 'Levm, Melûm ve Mulîm (14 geçiş / 12 ayet: 5:54, 12:32, 14:22, 17:29, 17:39 kınamak, suçlamak ve kınanmayı hak etmek)'),
    ('zrE', 'Yüksek Frekanslı Çekirdek', 'Zer\', Zurrâ\' ve Tezraûn (14 geçiş / 12 ayet: 6:141, 12:47, 13:4, 14:37, 16:11 tohum ekip yeşertmek, ekin ve ekin yetiştirenler)'),
    ('Hrv', 'Yüksek Frekanslı Çekirdek', 'Hars ve Tahrüsûn (14 geçiş / 11 ayet: 2:71, 2:205, 2:223, 3:14, 3:117 toprağı sürüp ekine hazırlamak ve emeğin ürün verimi)'),
    ('wlj', 'Yüksek Frekanslı Çekirdek', 'Vülûc, Îlâc ve Velîce (14 geçiş / 9 ayet: 3:27, 7:40, 9:16, 22:61, 31:29 bir şeyi dar boşluğun/diğerinin içine geçirip sokmak)'),

    # Kategori 2: Sure %100 Tam Kilidi (+4 Tam Sure: Sure 104, 62, 105, 111 -> 29 Tam Kilitli Sure! — 19 Kök)
    ('Emd', 'Sure %100 Kilidi', 'Amed ve Müteammed (Sure 104 Hümeze kilidi + 7 geçiş: 4:93, 5:95, 13:2, 31:10, 104:9 taşıyıcı direk/sütun ve kasten yönelmek)'),
    ('HTm', 'Sure %100 Kilidi', 'Hutame ve Hutâm (Sure 104 Hümeze kilidi + 6 geçiş: 27:18, 39:21, 56:65, 57:20, 104:4 kırıp ufalayarak öğütmek)'),
    ('nb*', 'Sure %100 Kilidi', 'Nebz ve İntibâz (Sure 104 Hümeze kilidi + 12 geçiş: 2:100, 2:101, 3:187, 8:58, 19:16 önemsemeyip arkaya atmak ve fırlatmak)'),
    ('wSd', 'Sure %100 Kilidi', 'Vasîd ve Mü\'sade (Sure 104 Hümeze son kilidi + 18:18, 90:20, 104:8 geçit vermeyecek şekilde sımsıkı kilitleyip kapamak)'),
    ('Hmr', 'Sure %100 Kilidi', 'Hımâr ve Humur (Sure 62 Cum\'a kilidi + 6 geçiş: 2:259, 16:8, 31:19, 35:27, 62:5 yük taşıyıcı eşek ve kızıl çizgi/renk)'),
    ('fDD', 'Sure %100 Kilidi', 'Fidda ve İnfidâd (Sure 62 Cum\'a kilidi + 9 geçiş: 3:14, 3:159, 9:34, 43:33, 62:11 katı kalp/dağılıp savrulmak ve beyaz gümüş)'),
    ('lHq', 'Sure %100 Kilidi', 'Lühûk ve İlhâk (Sure 62 Cum\'a kilidi + 6 geçiş: 3:170, 12:101, 26:83, 34:27, 52:21 geriden yetişip katılmak ve bağlamak)'),
    ('sfr', 'Sure %100 Kilidi', 'Sefer, Esfâr ve Müsfira (Sure 62 Cum\'a kilidi + 12 geçiş: 2:184, 2:185, 4:43, 5:6, 62:5 aydınlanıp açığa çıkmak, yolculuk ve büyük yazılı tomarlar)'),
    ('tjr', 'Sure %100 Kilidi', 'Ticâret (Sure 62 Cum\'a son kilidi + 9 geçiş: 2:16, 2:282, 4:29, 9:24, 62:11 kâr amacı güden mal ve değer değişimi)'),
    ('Abl', 'Sure %100 Kilidi', 'İbil ve Ebâbîl (Sure 105 Fîl kilidi + 3 geçiş: 6:144, 88:17, 105:3 yük devesi ve art arda sürüler hâlinde gelen gruplar)'),
    ('ESf', 'Sure %100 Kilidi', 'Asf ve Âsıfe (Sure 105 Fîl kilidi + 7 geçiş: 10:22, 14:18, 21:81, 55:12, 105:5 fırtınalı rüzgârla savrulup yenmiş saman kabuğu)'),
    ('fyl', 'Sure %100 Kilidi', 'Fîl (Sure 105 Fîl kilidi: 105:1 devasa zırhlı fil ordusu sahibi)'),
    ('rmy', 'Sure %100 Kilidi', 'Remy (Sure 105 Fîl kilidi + 9 geçiş: 4:112, 8:17, 24:4, 24:6, 105:4 taş veya asılsız suçlama fırlatıp atmak)'),
    ('sjl', 'Sure %100 Kilidi', 'Siccîl ve Sicill (Sure 105 Fîl son kilidi + 4 geçiş: 11:82, 15:74, 21:104, 105:4 yazılı kayıt tomarı ve fırınlanmış/damgalı sert taş)'),
    ('HTb', 'Sure %100 Kilidi', 'Hatab (Sure 111 Mesed kilidi + 2 geçiş: 72:15, 111:4 yakacak odun)'),
    ('Hbl', 'Sure %100 Kilidi', 'Habl ve Hıbâl (Sure 111 Mesed kilidi + 7 geçiş: 3:103, 3:112, 20:66, 26:44, 50:16, 111:5 bağlayıcı ip, ahit bağı ve şah damarı)'),
    ('jyd', 'Sure %100 Kilidi', 'Cîd (Sure 111 Mesed kilidi: 111:5 gerdan ve boyun)'),
    ('lhb', 'Sure %100 Kilidi', 'Leheb (Sure 111 Mesed kilidi + 3 geçiş: 77:31, 111:1, 111:3 dumansız harlı alev)'),
    ('msd', 'Sure %100 Kilidi', 'Mesed (Sure 111 Mesed son kilidi: 111:5 sıkı bükülmüş hurma lifinden halat)'),

    # Kategori 3: En Yüksek Frekanslı Çekirdek Kökler II (13 Geçiş — İlk 11 Kök -> 700 KÖK!)
    ('$hw', 'Yüksek Frekanslı Çekirdek', 'Şehvet ve İştihâ\' (13 geçiş / 13 ayet: 3:14, 4:27, 7:81, 16:57, 19:59 nefsin şiddetle arzulayıp yöneldiği çekim gücü)'),
    ('SyH', 'Yüksek Frekanslı Çekirdek', 'Sayha (13 geçiş / 13 ayet: 11:67, 11:94, 15:73, 15:83, 23:41 çatlatıcı gök gürlemesi ve parçalayan tek sarsıntı sesi)'),
    ('bgt', 'Yüksek Frekanslı Çekirdek', 'Bağte (13 geçiş / 13 ayet: 6:31, 6:44, 6:47, 7:95, 7:187 hiç işaret vermeden ansızın bastırıp yakalamak)'),
    ('fwh', 'Yüksek Frekanslı Çekirdek', 'Fû ve Efvâh (13 geçiş / 13 ayet: 3:118, 3:167, 5:41, 9:8, 9:30 söz ve nefes çıkış kapısı olan ağız ve ağızlar)'),
    ('glZ', 'Yüksek Frekanslı Çekirdek', 'Galîz, Gılze ve Uğluz (13 geçiş / 13 ayet: 3:159, 4:21, 4:154, 9:73, 9:123 bükülmez katılık, sağlam bağ ve sert tavır)'),
    ('glm', 'Yüksek Frekanslı Çekirdek', 'Gulâm (13 geçiş / 13 ayet: 3:40, 12:19, 15:53, 18:74, 18:80 genç erkek çocuk ve hizmetkâr delikanlı)'),
    ('rAf', 'Yüksek Frekanslı Çekirdek', 'Re\'fe ve Raûf (13 geçiş / 13 ayet: 2:143, 2:207, 3:30, 9:117, 9:128 zararı önleyen ince şefkat ve üstün koruma hassasiyeti)'),
    ('xll', 'Yüksek Frekanslı Çekirdek', 'Hilâl, Halîl ve Hulle (13 geçiş / 13 ayet: 2:254, 4:125, 9:47, 14:31, 17:5 aralık/boşluktan sızmak ve kalp boşluğunu dolduran dostluk)'),
    ('xzn', 'Yüksek Frekanslı Çekirdek', 'Hazine, Hâzin ve Hazene (13 geçiş / 13 ayet: 6:50, 11:31, 12:55, 15:21, 15:22 koruyup biriktirmek ve kaynak ambarları/görevlileri)'),
    ('Hlf', 'Yüksek Frekanslı Çekirdek', 'Half ve Hallâf (13 geçiş / 12 ayet: 4:62, 5:89, 9:42, 9:56, 9:62 kesin yemin sözü vermek ve sık yemin etmek)'),
    ('nSH', 'Yüksek Frekanslı Çekirdek', 'Nush ve Nâsih (13 geçiş / 11 ayet: 7:21, 7:62, 7:68, 7:79, 7:93 hileden arınmış saf iyi niyet ve içten öğüt)'),
]


def generate_etap_3i():
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
    for etap_rank, (bw, category, rationale) in enumerate(ETAP_3I_ROOTS_SPEC, 1):
        if bw in seen_bw:
            raise ValueError(f"ETAP_3I_ROOTS_SPEC içinde mükerrer kök: {bw}")
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
            'etap_3i_rank': etap_rank,
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
        'package': 'Faz 1 - Etap 3I (18-13 Geçiş Çekirdek Zırhı ve +4 Sure %100 Tam Kilidi [Sure 104, 62, 105, 111 -> 29 Sure] — 50 Kök -> 700 Kök)',
        'target_count': len(items),
        'locked_count': locked_cnt,
        'total_tokens_in_package': total_tokens,
        'total_corpus_tokens': total_corpus_tokens,
        'current_coverage_pct': round(current_cov_pct, 2),
        'target_coverage_pct': round(target_cov_pct, 2),
        'etap_3i_roots': items,
    }
    json_path = os.path.join(DATA_DIR, 'etap_3i_key_roots.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    pct_now_str = f"{current_cov_pct:.2f}".replace('.', ',')
    pct_target_str = f"{target_cov_pct:.2f}".replace('.', ',')
    md_lines = [
        "# ETAP 3I: YÜKSEK FREKANSLI ÇEKİRDEK KÖKLER (18-13 GEÇİŞ) VE +4 SURE %100 TAM KİLİDİ (50 KÖK -> 700 KÖK)",
        "## Tabula Rasa Mesânî Çözümleme Sistemi (v3.0 — Faz 1 700 Kök & 29 Tam Kilitli Sure Zırhı)",
        "",
        "> [!IMPORTANT]",
        f"> **HEDEF KAPSAM:** İlk 650 mühürlü kökten (`%93,13`) sonra, kalan `18-14` geçişli `20` çekirdek kök, `4` sureyi daha `%100` kilitleyen `19` kök (Sure 104 Hümeze, 62 Cum'a, 105 Fîl, 111 Mesed → **29 tam kilitli sure**) ve `13` geçişli `11` çekirdek kök olmak üzere **50 kök** ({total_tokens} geçiş) mühürlenerek toplam sözlük **700 kilitli köke (`%{pct_target_str}` kümülatif kök kapsamı)** ulaştırılır.",
        f"> **Etap 3I İçinde Şu Ana Kadar Mühürlenen:** {locked_cnt} / {len(items)} Kök (Toplam Mühürlü: {len(locked_roots)} Kök | Güncel Kapsam: %{pct_now_str})",
        "",
        "| Etap Sıra | Kategori | Genel Sıra | Kök (Arapça) | Kök (Latin) | Geçiş | Ayet | Örnek | Stratejik Önemi / Kavram Durumu | Durum |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |",
    ]
    for it in items:
        badge = "✅ **MÜHÜRLÜ**" if it['is_locked'] else "⏳ *Bekliyor*"
        desc = it['concept_label'] if it['is_locked'] else it['rationale']
        md_lines.append(
            f"| {it['etap_3i_rank']} | {it['category']} | {it['global_rank']} | "
            f"`{it['root_arabic']}` | `{it['root_latin']}` | **{it['frequency']}** | {it['unique_ayahs']} | "
            f"{it['sample_ayah']} | {desc} | {badge} |"
        )
    md_lines.append("")

    md_path = os.path.join(DATA_DIR, 'ETAP_3I_KAVRAM.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(
        f"Etap 3I JSON üretildi: {json_path} "
        f"({locked_cnt}/{len(items)} mühürlü | Güncel: %{pct_now_str} -> Hedef 700 kök: %{pct_target_str})"
    )
    print(f"Etap 3I Markdown üretildi: {md_path}")


if __name__ == '__main__':
    generate_etap_3i()
