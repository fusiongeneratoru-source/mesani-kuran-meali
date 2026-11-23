# -*- coding: utf-8 -*-
"""
Etap 3E Kilit Kavramlar (Kısa Sure Son Tekil Kilitleri, Açık Mesânî/Furûk Uçları
ve 500. Kök Tam Zırh Paketi — 50 Kök -> 500 Kilitli Kök) İndeks Üreticisi
Tabula Rasa Mesânî Çözümleme Sistemi (v3.0)

İlk 450 mühürlü kökten sonra (%86,92 kapsam), meal aşamasına (Faz 2) geçmeden önce
kısa surelerin (98-114: İhlâs, Felak, Nâs, Kevser, Mâûn, Hümeze, Kâria, Zilzâl, Beyyine)
kalan son tekil kavram kilitlerini, mühürlü 450 kökün Mesânî/Furûk alanlarında referans
verilen açık uçlu eşlenikleri ve 25+ geçişli doktrinel/çekirdek kavramları (50 kök / 789 geçiş)
indeksler ve toplam kilitli sözlüğü 500 köke (%88,50 kapsam) tamamlar.
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
ETAP_3E_ROOTS_SPEC = [
    # Kategori 1: Kısa Surelerin (Sûre 107-114) Kalan Son Tekil Kavram Kilitleri (10 kök: 3E-1 & 3E-2)
    ('kfA', 'Kısa Sure Son Kilidi', 'Küfüv (112:4 İhlâs Sûresi\'nin son tekil kilidi: "O\'na hiçbir şey denk/eşdeğer olmamıştır")'),
    ('flq', 'Kısa Sure Son Kilidi', 'Felak ve Fâlik (113:1 Felak Sûresi kilidi, 6:95-96 ve 26:63 karanlığı ve tohumu yarıp çıkaran yaratılış aydınlığı)'),
    ('gsq', 'Kısa Sure Son Kilidi', 'Gâsik, Gasak ve Gassâk (113:3 Felak Sûresi, 17:78, 38:57, 78:25 koyulaşıp çöken gece karanlığı ve soğuk irin)'),
    ('wqb', 'Kısa Sure Son Kilidi', 'Vakb (113:3 Felak Sûresi\'nin son kilidi: "çöküp her yanı kapladığı zaman karanlık [غَاسِقٍ إِذَا وَقَبَ]")'),
    ('xns', 'Kısa Sure Son Kilidi', 'Hannâs ve Hünnes (114:4 Nâs Sûresi\'nin son kilidi ve 81:15 sinsice geri çekilip pusuya yatan / yörüngesinde çekilen)'),
    ('btr', 'Kısa Sure Son Kilidi', 'Ebter (108:3 Kevser Sûresi kilidi: hayırdan ve kalıcı izden kesilmiş, arkası/kökü kesik olan)'),
    ('$nA', 'Kısa Sure Son Kilidi', 'Şâni\' ve Şeneân (108:3 Kevser Sûresi ve 5:2, 5:8 "bir topluma duyulan kin ve düşmanlık sizi adaletsizliğe sevk etmesin" yasası)'),
    ('dEE', 'Kısa Sure Son Kilidi', 'Da\'\' (107:2 Mâûn Sûresi "yetimi şiddetle itip kakıştıran" ve 52:13 ateşe kakıştırılma)'),
    ('HDD', 'Kısa Sure Son Kilidi', 'Hadd ve Tehâdd (107:3 Mâûn Sûresi, 69:34, 89:18 yoksulu doyurmaya önayak olup birbirini teşvik etmeme)'),
    ('shw', 'Kısa Sure Son Kilidi', 'Sâhûn (107:5 Mâûn Sûresi "salâtlarının özünden/amacından gafil olup dalgınlığa düşenler" ve 51:11)'),

    # Kategori 2: Kısa Sure (98-104) Tamamlayıcıları ve En Yüksek Açık Mesânî/Furûk Kilitleri I (10 kök: 3E-3 & 3E-4)
    ('hmz', 'Kısa Sure & Açık Mesânî', 'Hümeze, Hemmâz ve Hemezât (104:1 Hümeze Sûresi, 68:11, 23:97 arkadan çekiştirip kıran ve dürtüp kışkırtmalar)'),
    ('lmz', 'Kısa Sure & Açık Mesânî', 'Lümeze (104:1 Hümeze Sûresi, 9:58, 9:79, 49:11 kaş-göz ve sözle insanları ayıplayıp alaya almak)'),
    ('qrE', 'Kısa Sure & Açık Mesânî', 'Kâriah (101:1-3 Kâria Sûresi kilidi ve 13:31 şiddetle çarpıp sarsan felaket/uyanış)'),
    ('zlzl', 'Kısa Sure & Açık Mesânî', 'Zilzâl ve Zelzele (99:1 Zilzâl Sûresi kilidi, 2:214, 22:1, 33:11 yerin ve gönüllerin şiddetle sarsılması)'),
    ('SHf', 'Kısa Sure & Açık Mesânî', 'Suhuf ve Sıhâf (98:2 Beyyine Sûresi, 87:18-19, 80:13, 74:52, 53:36 arınmış yazılı vahyî sayfalar)'),
    ('x*l', 'Kısa Sure & Açık Mesânî', 'Hızlân ve Mahzûl (5 açık Mesânî ref! ن-ص-ر [yardım] kökünün doğrudan zıddı: 3:160, 17:22, 25:29 yardımsız/yüzüstü bırakmak)'),
    ('f$l', 'Kısa Sure & Açık Mesânî', 'Feşel (4 Mesânî + 2 Furûk ref! ث-ب-ت ve ص-ب-ر zıddı: 3:122, 3:152, 8:43, 8:46 gevşeyip yılgınlığa ve moral çöküntüsüne düşmek)'),
    ('qsw', 'Kısa Sure & Açık Mesânî', 'Kasvet ve Kâsiye (4 açık Mesânî ref! ل-ي-ن ve خ-ش-ع zıddı: 2:74, 5:13, 39:22, 57:16 kalplerin taşlaşıp katılaşması)'),
    ('qSd', 'Kısa Sure & Açık Mesânî', 'Kasd ve Muktesıd (4 açık Mesânî ref! 16:9, 31:19, 35:32 aşırılık ve gevşeklik arasındaki dengeli orta yürüyüş)'),
    ('yAs', 'Kısa Sure & Açık Mesânî', 'Ye\'s ve Yeûs (4 Mesânî + 1 Furûk ref! ر-ج-و zıddı ve ق-ن-ط eşleniği: 12:87, 41:49, 60:13 umudunu tamamen kesmek)'),

    # Kategori 3: Açık Mesânî ve Furûk Eşlenikleri II (10 kök: 3E-5 & 3E-6)
    ('n$A', 'Açık Mesânî Eşleniği', 'İnşâ\' ve Neş\'et (4 Mesânî + 1 Furûk ref! 6:98, 29:20, 53:47, 56:62 ilk ve yeni yaratılış/filizlendirip yükseltme)'),
    ('frH', 'Açık Mesânî Eşleniği', 'Ferah ve Farih (4 açık Mesânî ref! ح-ز-ن ve ق-ن-ط zıddı: 10:58 Allah\'ın lütfuyla sevinmek vs 28:76 şımarıkça böbürlenmek)'),
    ('xff', 'Açık Mesânî Eşleniği', 'Hıffet ve Tahfîf (4 açık Mesânî ref! ث-ق-ل [ağır gelmek] kökünün doğrudan zıddı: 101:8 tartıları hafif gelmek ve 4:28 yükü hafifletmek)'),
    ('lbv', 'Açık Mesânî Eşleniği', 'Lübs ve Lâbisîn (3 açık Mesânî ref! ع-ج-ل zıddı: 2:259, 18:19, 23:112-114 bir yerde/halde bekleyip kalmak)'),
    ('k$f', 'Açık Mesânî Eşleniği', 'Keşf ve Kâşif (3 açık Mesânî ref! 6:17, 10:107, 27:62, 50:22 sıkıntıyı, örtüyü ve perdeyi kaldırıp açmak)'),
    ('Eln', 'Açık Mesânî Eşleniği', 'İ\'lân ve Alâniye (3 açık Mesânî ref! س-ر-ر [gizlemek] kökünün doğrudan zıddı: 2:77, 13:22, 14:31, 35:29 açığa vurmak)'),
    ('jhr', 'Açık Mesânî Eşleniği', 'Cehr ve Cehreh (3 açık Mesânî ref! س-ر-ر ve خ-ف-ت zıddı: 6:3, 7:205, 17:110, 20:7, 67:13 sözü açıktan ve yüksek sesle söylemek)'),
    ('DyE', 'Açık Mesânî Eşleniği', 'İdâa (3 açık Mesânî ref! ح-ف-ظ zıddı: 3:195, 12:90, 18:30 yapılan güzel emeği zayi etmemek ve 19:59 salâtı zayi etmek)'),
    ('bgD', 'Açık Mesânî Eşleniği', 'Bağdâ\' (3 açık Mesânî ref! ح-ب-ب ve و-د-د zıddı: 3:118, 5:14, 5:64, 5:91, 60:4 taşان nefret ve düşmanlık)'),
    ('Dyq', 'Açık Mesânî Eşleniği', 'Dîk ve Dayyik (2 Mesânî + 2 Furûk ref! و-س-ع ve ش-ر-ح zıddı: 6:125, 9:25, 9:118, 15:97 göğsün ve yeryüzünün daralması)'),

    # Kategori 4: Açık Mesânî/Furûk Eşlenikleri III ve Doktrinel Mayınlı Kökler (10 kök: 3E-7 & 3E-8)
    ('glb', 'Mesânî & Doktrinel Zırh', 'Galebe, Gâlib ve Mağlûb (2 açık Mesânî ref! 5:23, 8:65, 12:21, 30:2-3, 58:21 üstün gelmek ve yenilgiye uğramak)'),
    ('grr', 'Mesânî & Doktrinel Zırh', 'Gurûr ve Garûr (2 açık Mesânî ref! 3:185, 31:33, 35:5, 57:14, 82:6 aldatıcı kuruntu/avuntu ve ayartıcı aldanış)'),
    ('Awb', 'Mesânî & Doktrinel Zırh', 'Evvâb ve Meâb (2 açık Mesânî ref! 13:29, 34:10, 38:17-49, 50:32 her fırsatta gönülden Rabbine dönen ve güzel dönüş yeri)'),
    ('HbT', 'Mesânî & Doktrinel Zırh', 'Habt ve İhbât (2 açık Mesânî ref! 2:217, 3:22, 5:5, 39:65, 47:28, 49:2 zehirli ot yemiş hayvan gibi amellerin şişip boşa gitmesi)'),
    ('drk', 'Mesânî & Doktrinel Zırh', 'İdrâk, Tedârük ve Derk (3 açık Furûk ref! 4:145 en alt basamak, 6:103 gözlerin O\'nu kuşatamaması ve 10:90 yetişip yakalamak)'),
    ('whn', 'Mesânî & Doktrinel Zırh', 'Vehn ve Evhen (2 açık Mesânî ref! ق-و-ي zıddı: 3:139, 3:146, 19:4, 29:41, 31:14 gevşeyip güçten düşmek ve en çürük ev)'),
    ('Sly', 'Mesânî & Doktrinel Zırh', 'Saly ve Istılâ\' (111:3 Tebbet, 88:4, 4:10, 27:7 ateşe girip yaslanmak/ısınmak — ص-ل-و [salât] köküyle karışıklığı önleyen kilit!)'),
    ('bTn', 'Mesânî & Doktrinel Zırh', 'Batn, Bâtın ve Bıtâne (ظ-ه-ر [Zâhir] kökünün doğrudan Mesânî eşleniği: 6:120, 6:151, 31:20, 57:3,13 iç yüz ve 3:118 sırdaş)'),
    ('$ry', 'Mesânî & Doktrinel Zırh', 'Şirâ\' ve İştirâ\' (ب-ي-ع eşleniği: 2:16, 2:90, 2:102, 2:207, 9:111 bir bedel karşılığında canını/emeğini veya hidayeti satmak/satın almak)'),
    ('whb', 'Mesânî & Doktrinel Zırh', 'Hibe ve el-Vehhâb (3:8, 3:38, 19:5, 38:9,35 hiçbir karşılık beklemeksizin gönülden bağışlamak)'),

    # Kategori 5: En Yüksek Frekanslı (28-45 Geçiş) Çekirdek Eylem ve Yaratılış Kökleri (10 kök: 3E-9 & 3E-10 -> 500 KÖK!)
    ('w*r', 'Yüksek Frekanslı Çekirdek', 'Zer ve Yezaru (45 geçişle henüz mühürlenmemiş #1 en yüksek frekanslı kök! 6:70, 62:9, 74:11, 75:20 bırakıp terk etmek)'),
    ('kfy', 'Yüksek Frekanslı Çekirdek', 'Kifâyet ve Kâfî (33 geçiş: 4:6, 13:43, 29:51, 33:3,39, 39:36 "Allah kuluna yetmez mi?" ve koruyup başkasına muhtaç bırakmamak)'),
    ('mdd', 'Yüksek Frekanslı Çekirdek', 'Medd, İmdâd ve Meded (32 geçiş: 104:9 Hümeze, 3:125, 17:20, 19:75, 25:45, 31:27 uzatmak, süre ve kesintisiz destek vermek)'),
    ('wry', 'Yüksek Frekanslı Çekirdek', 'Müvârât, Mûriyât ve Verâ\' (32 geçiş: 100:2 Âdiyât kıvılcım çakmak, 5:31, 7:20,26 gizleyip örtmek ve arkada/ötede olan)'),
    ('Srf', 'Yüksek Frekanslı Çekirdek', 'Sarf ve Tasrîf (30 geçiş: 6:16, 12:24,34, 17:41,89, 18:54, 25:50 kötülüğü savuşturup çevirmek ve ayetleri çok yönlü açıklamak)'),
    ('g$w', 'Yüksek Frekanslı Çekirdek', 'Gaşy, İğşâ\' ve Gâşiye (29 geçiş: 88:1 Gâşiye Sûresi, 91:4, 92:1, 2:7, 24:40, 53:16 gece veya perde gibi her yanı bürüyüp kaplamak)'),
    ('Syr', 'Yüksek Frekanslı Çekirdek', 'Masîr ve Sayrûret (29 geçiş: 2:126, 2:285, 3:28, 42:53 "işlerin evrilip varacağı son dönüş durağı [وَإِلَيْكَ ٱلْمَصِيرُ]")'),
    ('jdl', 'Yüksek Frekanslı Çekirdek', 'Cidâl ve Mücâdele (29 geçiş: 16:125, 18:54, 29:46, 58:1 ipi sıkıca bükmekten hareketle en güzel yolla kanıt ortaya koymak vs kısır çekişme)'),
    ('rjw', 'Yüksek Frekanslı Çekirdek', 'Recâ\' ve Mürcûn (28 geçiş: خ-و-ف ve ي-أ-س eşleniği; 2:218, 18:110, 29:5, 33:21, 71:13 Allah\'a kavuşmayı umup beklemek)'),
    ('HwT', 'Yüksek Frekanslı Çekirdek', 'İhâta ve Muhît (28 geçiş: 2:19, 2:255, 18:68,91, 41:54, 65:12, 85:20 ilahi bilgi ve kudretin her şeyi çepeçevre kuşatması)'),
]


def generate_etap_3e():
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
            m_root = re.search(r'ROOT:([^|]+)', line)
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
            m_lem = re.search(r'LEM:([^|]+)', line)
            if m_lem:
                roots_lemmas[bw][m_lem.group(1)] += 1

    global_ranks = {bw: idx for idx, (bw, _) in enumerate(roots_count.most_common(), 1)}
    total_corpus_tokens = sum(roots_count.values())

    items = []
    seen_bw = set()
    spec_bw_set = set()
    for etap_rank, (bw, category, rationale) in enumerate(ETAP_3E_ROOTS_SPEC, 1):
        if bw in seen_bw:
            raise ValueError(f"ETAP_3E_ROOTS_SPEC içinde mükerrer kök: {bw}")
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
            'etap_3e_rank': etap_rank,
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
        'package': 'Faz 1 - Etap 3E (Kısa Sure Son Tekil Kilitleri, Açık Mesânî/Furûk Uçları ve 500. Kök Tam Zırh Paketi — 50 Kök)',
        'target_count': len(items),
        'locked_count': locked_cnt,
        'total_tokens_in_package': total_tokens,
        'total_corpus_tokens': total_corpus_tokens,
        'current_coverage_pct': round(current_cov_pct, 2),
        'target_coverage_pct': round(target_cov_pct, 2),
        'etap_3e_roots': items,
    }
    json_path = os.path.join(DATA_DIR, 'etap_3e_key_roots.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    pct_now_str = f"{current_cov_pct:.2f}".replace('.', ',')
    pct_target_str = f"{target_cov_pct:.2f}".replace('.', ',')
    md_lines = [
        "# ETAP 3E: KISA SURE SON TEKİL KİLİTLERİ, AÇIK MESÂNÎ/FURÛK UÇLARI VE 500. KÖK TAM ZIRH PAKETİ (50 KÖK -> 500 KÖK)",
        "## Tabula Rasa Mesânî Çözümleme Sistemi (v3.0 — Faz 2 Öncesi 500 Kök Tam Zırhı)",
        "",
        "> [!IMPORTANT]",
        f"> **HEDEF KAPSAM:** İlk 450 mühürlü kökten (`%86,92`) sonra, meal aşamasına geçmeden önce kısa surelerin (98-114) kalan son tekil kavram kilitlerini, mühürlü köklerin referans verdiği açık Mesânî/Furûk eşleniklerini ve 25+ geçişli doktrinel/çekirdek kavramları kapatan **50 kritik kök** ({total_tokens} geçiş) mühürlenerek toplam sözlük **500 kilitli köke (`%{pct_target_str}` kümülatif kök kapsamı, tüm Kur'an kelimelerinin `%92,58`'i)** ulaştırılır.",
        f"> **Etap 3E İçinde Şu Ana Kadar Mühürlenen:** {locked_cnt} / {len(items)} Kök (Toplam Mühürlü: {len(locked_roots)} Kök | Güncel Kapsam: %{pct_now_str})",
        "",
        "| Etap Sıra | Kategori | Genel Sıra | Kök (Arapça) | Kök (Latin) | Geçiş | Ayet | Örnek | Stratejik Önemi / Kavram Durumu | Durum |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |",
    ]
    for it in items:
        badge = "✅ **MÜHÜRLÜ**" if it['is_locked'] else "⏳ *Bekliyor*"
        desc = it['concept_label'] if it['is_locked'] else it['rationale']
        md_lines.append(
            f"| {it['etap_3e_rank']} | {it['category']} | {it['global_rank']} | "
            f"`{it['root_arabic']}` | `{it['root_latin']}` | **{it['frequency']}** | {it['unique_ayahs']} | "
            f"{it['sample_ayah']} | {desc} | {badge} |"
        )
    md_lines.append("")

    md_path = os.path.join(DATA_DIR, 'ETAP_3E_KAVRAM.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(
        f"Etap 3E JSON üretildi: {json_path} "
        f"({locked_cnt}/{len(items)} mühürlü | Güncel: %{pct_now_str} -> Hedef 500 kök: %{pct_target_str})"
    )
    print(f"Etap 3E Markdown üretildi: {md_path}")


if __name__ == '__main__':
    generate_etap_3e()
