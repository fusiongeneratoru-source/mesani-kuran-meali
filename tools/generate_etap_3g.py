# -*- coding: utf-8 -*-
"""
Etap 3G Kilit Kavramlar (Kısa Sureler %100 Tam Kilit Genişletmesi [15->20 Sure],
Açık Mesânî Tepe Uçları ve 600. Kök Yüksek Frekanslı Çekirdek Zırh Paketi — 50 Kök -> 600 Kilitli Kök)
Tabula Rasa Mesânî Çözümleme Sistemi (v3.0)

İlk 550 mühürlü kökten sonra (%90,24 köklü / %93,70 tüm kelime kapsamı),
5 sureyi daha %100 kilitleyen 20 kökü (Sure 82 İnfitâr, 92 Leyl, 93 Duhâ, 95 Tîn, 106 Kureyş -> 20 tam kilitli sure),
3 ve 2 açık Mesânî referanslı 10 kritik tepe eşleniğini ve kalan en yüksek frekanslı 20 çekirdek kökü
(50 kök / 839 geçiş) indeksler; toplam sözlüğü 600 köke (%91,92 köklü / %94,79 tüm kelime) ulaştırır.
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
ETAP_3G_ROOTS_SPEC = [
    # Kategori 1: Kısa Sureler %100 Kilidi I (Sure 106 Kureyş, Sure 95 Tîn, Sure 92 Leyl -> +3 Tam Kilitli Sure!)
    ('rHl', 'Kısa Sure %100 Kilidi', 'Rıhle ve Rihâl (Sure 106 Kureyş kilidi + 12:62, 12:70, 12:75: göç/ticaret yolculuğu ve yük semerleri)'),
    ('$tw', 'Kısa Sure %100 Kilidi', 'Şitâ\' (Sure 106 Kureyş kilidi: 106:2 kış mevsimi yolculuğu — ص-ي-ف Mesânî çifti)'),
    ('Syf', 'Kısa Sure %100 Kilidi', 'Sayf (Sure 106 Kureyş son kilidi: 106:2 yaz mevsimi yolculuğu — ش-ت-و Mesânî çifti)'),
    ('bld', 'Kısa Sure %100 Kilidi', 'Beled ve Büldân (Sure 95 Tîn & 90 Beled kilidi + 19 geçiş: 2:126, 7:57-58, 90:1-2, 95:3 güvenli belde/yurt ve toprak)'),
    ('Twr', 'Kısa Sure %100 Kilidi', 'Tûr ve Etvâr (Sure 95 Tîn kilidi + 11 geçiş: 2:63, 19:52, 52:1, 95:2 Tûr dağı ve 71:14 evre evre yaratılış)'),
    ('zyt', 'Kısa Sure %100 Kilidi', 'Zeyt ve Zeytûn (Sure 95 Tîn kilidi + 7 geçiş: 6:99, 24:35, 80:29, 95:1 zeytin ağacı ve aydınlatıcı saf zeytinyağı)'),
    ('tyn', 'Kısa Sure %100 Kilidi', 'Tîn (Sure 95 Tîn son kilidi: 95:1 incir — zeytin, Tûr-i Sînîn ve güvenli belde dörtlü yemin dizisi)'),
    ('$qw', 'Kısa Sure %100 Kilidi', 'Şakî, Eşķâ ve Şikve (Sure 92 Leyl & 87 A\'lâ kilidi + 12 geçiş: س-ع-د zıddı 11:105-106, 19:4, 20:2, 92:15 kendi yıkımına sürüklenmek)'),
    ('rdy', 'Kısa Sure %100 Kilidi', 'Tereddî ve İrdâ\' (Sure 92 Leyl kilidi + 6 geçiş: 20:16, 37:56, 53:40, 69:29, 92:11 uçurumdan aşağı yuvarlanıp helak olmak)'),
    ('jlw', 'Kısa Sure %100 Kilidi', 'Tecellî ve Cilâ\' (Sure 92 Leyl & 91 Şems kilidi + 5 geçiş: 7:143, 7:187, 91:3, 92:2 örtünün sıyrılıp parlakça açığa çıkması)'),

    # Kategori 2: Kısa Sureler %100 Kilidi II (Sure 92 Sonu, Sure 93 Duhâ, Sure 82 İnfitâr -> 20 Tam Kilitli Sure!)
    ('lZy', 'Kısa Sure %100 Kilidi', 'Lezâ ve Telezzî (Sure 92 Leyl son kilidi + 70:15: 92:14 alevlenip parlayan kavurucu ateş)'),
    ('DHw', 'Kısa Sure %100 Kilidi', 'Duhâ (Sure 93 Duhâ & 91 Şems kilidi + 2 açık Mesânî ref! ل-ي-ل zıddı 7 geçiş: 7:98, 20:59, 20:119, 79:29, 93:1 kuşluk aydınlığı)'),
    ('wdE', 'Kısa Sure %100 Kilidi', 'Vedâ\' ve Da\' (Sure 93 Duhâ kilidi + 4 geçiş: 33:48, 93:3 terk edip bırakmak — "Rabbin seni terk etmedi")'),
    ('Eyl', 'Kısa Sure %100 Kilidi', 'Âil ve Ayle (Sure 93 Duhâ kilidi + 9:28: 93:8 yoksul/muhtaç olmak ve geçim darlığı — غ-ن-ي Mesânî zıddı)'),
    ('qly', 'Kısa Sure %100 Kilidi', 'Kalâ ve Kâlîn (Sure 93 Duhâ kilidi + 26:168: 93:3 darılıp nefret etmek / itip dışlamak)'),
    ('sjw', 'Kısa Sure %100 Kilidi', 'Secâ (Sure 93 Duhâ son kilidi: 93:2 gecenin durulup sakinleşmesi ve örtüsüyle dinginleşmesi)'),
    ('rkb', 'Kısa Sure %100 Kilidi', 'Rükûb, Rekûb ve Terkîb (Sure 82 İnfitâr kilidi + 1 Mesânî ref, 15 geçiş: 82:8 parçaları birleştirip sentezlemek ve bineğe/gemiye binmek)'),
    ('kwkb', 'Kısa Sure %100 Kilidi', 'Kevkeb ve Kevâkib (Sure 82 İnfitâr kilidi + 5 geçiş: 6:76, 12:4, 24:35, 37:6, 82:2 parlak gezegen ve yıldızlar)'),
    ('nvr', 'Kısa Sure %100 Kilidi', 'İntisâr ve Mensûr (Sure 82 İnfitâr kilidi + 3 geçiş: 25:23, 54:7, 82:2 saçılıp dağılmak)'),
    ('bEvr', 'Kısa Sure %100 Kilidi', 'Ba\'sere (Sure 82 İnfitâr son kilidi + Sure 100 Âdiyât: 82:4, 100:9 altını üstüne getirip dışarı saçmak)'),

    # Kategori 3: 3 ve 2 Açık Mesânî Referanslı Tepe Eşlenikler (10 Kök)
    ('xwn', 'Açık Mesânî Zırhı', 'Hıyânet ve Hâin (3 açık Mesânî ref! أ-م-ن doğrudan zıddı 16 geçiş: 4:105, 8:27, 8:58, 12:52, 40:19, 66:10 emanete ve ahde ihanet etmek)'),
    ('grb', 'Açık Mesânî Zırhı', 'Mağrib, Gurûb ve Garâbîb (2 Mesânî + 1 Furûk ref! ش-ر-ق ve ط-ل-ع zıddı 19 geçiş: güneşin batışı, batı yönü ve 35:27 kuzguni siyah)'),
    ('gbr', 'Açık Mesânî Zırhı', 'Gâbirîn ve Gabere (2 açık Mesânî ref! ن-ج-و zıddı 8 geçiş: 7:83, 15:60, 26:171, 29:32 yıkımda geride kalanlar ve 80:40 toz çökmüş yüzler)'),
    ('HSr', 'Açık Mesânî Zırhı', 'Hasr, İhsâr ve Hasîr (2 açık Mesânî ref! 6 geçiş: 2:196, 2:273 kuşatılıp alıkonulmak, 4:90 göğüsleri daralmak, 17:8 kuşatıcı tutukevi)'),
    ('$HH', 'Açık Mesânî Zırhı', 'Şuhh ve Eşıhha\' (2 açık Mesânî ref! و-ق-ي ve ي-س-ر eşleniği 5 geçiş: 4:128, 33:19, 59:9, 64:16 benliğin doymak bilmez bencil cimriliği)'),
    ('brd', 'Açık Mesânî Zırhı', 'Berd ve Bered (2 açık Mesânî ref! ح-م-م ve ن-و-ر zıddı 5 geçiş: 21:69 serinlik ve esenlik, 24:43 dolu taneleri, 56:44, 78:24 serinlik)'),
    ('fwt', 'Açık Mesânî Zırhı', 'Fevt ve Tefâvüt (2 açık Mesânî ref! 5 geçiş: 34:51, 57:23, 60:11 elden kaçıp gitmek ve 67:3 yaratılışta uyumsuzluk/kopukluk olmaması)'),
    ('xwy', 'Açık Mesânî Zırhı', 'Hâviye (2 açık Mesânî ref! ع-ر-ش eşleniği 5 geçiş: 2:259, 18:42, 22:45, 27:52, 69:7 içi boşalıp tavanları üzerine çökmüş harabe/kütük)'),
    ('Eff', 'Açık Mesânî Zırhı', 'İffet, İsti\'fâf ve Teaffüf (2 açık Mesânî ref! 4 geçiş: 2:273 onurlu tok gözlülük, 4:6 yetim malından, 24:33, 24:60 gayrimeşru ilişkiden sakınmak)'),
    ('ASr', 'Açık Mesânî Zırhı', 'İsr (2 Mesânî + 1 Furûk ref! غ-ل-ل eşleniği 3 geçiş: 2:286, 7:157 insanı bağlayıp ezen ağır yük/boyunduruk ve 3:81 bağlayıcı ağır ahit)'),

    # Kategori 4: En Yüksek Frekanslı Çekirdek Kökler I (28-36 Geçiş — Genel Sıra 256-326)
    ('Any', 'Yüksek Frekanslı Çekirdek', 'İnâ, Ânâ\', Âniye ve Ân (36 geçiş — #1 kalan kök! 33:53 pişme vakti, 3:113 gece saatleri, 76:15 kaplar ve 55:44 kaynama zirvesi)'),
    ('Hyn', 'Yüksek Frekanslı Çekirdek', 'Hîn (35 geçiş — #2 kalan kök! 2:36, 14:25, 21:111, 38:88 belirli zaman dilimi, vade ve olgunlaşma vakti)'),
    ('mrr', 'Yüksek Frekanslı Çekirdek', 'Merr, Merre, Müstemirr, Murr ve Mirre (35 geçiş — #3 kalan kök! Geçip gitmek, kez/defa, 54:46 daha acı ve 53:6 sağlam güç)'),
    ('$ms', 'Yüksek Frekanslı Çekirdek', 'Şems (33 geçiş — #4 kalan kök + Sure 91 Şems! Güneş, ışık/ısı kaynağı ve gölge/zaman ölçüsü)'),
    ('vlv', 'Yüksek Frekanslı Çekirdek', 'Selâse, Sülüs ve Sâlis (32 geçiş | 1M — #5 kalan kök! Üç sayısı, miras payları ve 4:171, 5:73 "üçtür / üçüncüsüdür" iddiasının reddi)'),
    ('Hyv', 'Yüksek Frekanslı Çekirdek', 'Haysü (31 geçiş — #6 kalan kök! 2:35, 2:144, 2:191, 65:3 konum, yön ve mekan zarfı: "nerede / nereden / hiç beklemediği yerden")'),
    ('Esy', 'Yüksek Frekanslı Çekirdek', 'Asâ (30 geçiş — #7 kalan kök! 2:216, 4:19, 17:8, 66:5 beklenti, umut ve ihtimal kapısı açan fiil: "umulur ki / bakarsınız")'),
    ('jnd', 'Yüksek Frekanslı Çekirdek', 'Cünd ve Cünûd (29 geçiş — #8 kalan kök! 2:249, 9:26, 33:9, 37:173, 48:4, 74:31 derlenip toplanmış ordular ve kozmik güçler)'),
    ('sbE', 'Yüksek Frekanslı Çekirdek', 'Seb\', Seb\'a ve Sebu\' (28 geçiş — #9 kalan kök! Yedi gök/başak/deniz/gece ve 5:3 yırtıcı hayvanın yediği)'),
    ('xlw', 'Yüksek Frekanslı Çekirdek', 'Halâ ve Halet (28 geçiş — #10 kalan kök! 2:14, 2:76 baş başa kalmak, 13:30 gelip geçmiş ümmetler ve 9:5 yollarını serbest bırakmak)'),

    # Kategori 5: En Yüksek Frekanslı Çekirdek Kökler II (24-27 Geçiş -> 600 KÖK & %91,92 KÖK KAPSAMI!)
    ('$jr', 'Yüksek Frekanslı Çekirdek', 'Şecer ve Şecere (27 geçiş: 2:35, 14:24, 24:35, 36:80 ağaç/bitki ve 4:65 aralarında dallanıp budaklanan anlaşmazlık çıkması)'),
    ('E$r', 'Yüksek Frekanslı Çekirdek', 'Aşr, Işrûn, Ma\'şer ve Muâşeret (27 geçiş: 6:160 bire on karşılık, 89:2 on gece, 6:130 topluluk ve 4:19 eşlerle iyi geçinmek)'),
    ('Ejb', 'Yüksek Frekanslı Çekirdek', 'Aceb ve İ\'câb (27 geçiş: 10:2, 11:72, 18:9, 38:4, 50:2 şaşırıp tuhaf bulmak ve 2:204, 57:20 dış görünüşüyle hayran bırakmak)'),
    ('bwb', 'Yüksek Frekanslı Çekirdek', 'Bâb ve Ebvâb (27 geçiş | 1M+1F: 2:189, 6:44, 12:23, 15:44, 38:50, 39:71-73 evlerin, göğün, rızkın ve karşılık yurtlarının kapıları)'),
    ('qmr', 'Yüksek Frekanslı Çekirdek', 'Kamer (27 geçiş + Sure 91 Şems & 54 Kamer! ش-م-س kozmik eşleniği ay, menziller ve zaman hesabı: 10:5, 36:39, 54:1, 55:5)'),
    ('syr', 'Yüksek Frekanslı Çekirdek', 'Seyr, Tesyîr ve Sîre (27 geçiş: 12:109, 29:20, 30:9 yeryüzünde gezip gözlem yapmak, 18:47, 78:20, 81:3 dağların yürütülmesi ve 20:21 ilk hâl)'),
    ('nbt', 'Yüksek Frekanslı Çekirdek', 'Nebât ve İnbât (26 geçiş: 2:261, 3:37, 6:99, 24:35, 50:7, 71:17 topraktan bitkiyi ve insanı filizlendirip güzelce yetiştirmek)'),
    ('Hwl', 'Yüksek Frekanslı Çekirdek', 'Havl, Hîle ve Tahvîl (25 geçiş | 1M+1F: 2:233 tam yıl döngüsü, 4:98 çare/güç, 8:24 kalp ile kişi arasına girmek ve 17:77 yasada sapma olmaması)'),
    ('sqy', 'Yüksek Frekanslı Çekirdek', 'Saky, İskâ\' ve Sukyâ (25 geçiş | 1F + Sure 91 Şems: 2:71, 16:66, 26:79, 28:23-24, 72:16, 91:13 su içirmek, sulamak ve su nöbeti)'),
    ('wqE', 'Yüksek Frekanslı Çekirdek', 'Vukû\' ve Vâkıa (24 geçiş: 4:100, 7:118, 7:134, 15:29, 27:82, 56:1-2 hükmün ve gerçeğin kaçınılmaz biçimde inip gerçekleşmesi)'),
]


def generate_etap_3g():
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
    for etap_rank, (bw, category, rationale) in enumerate(ETAP_3G_ROOTS_SPEC, 1):
        if bw in seen_bw:
            raise ValueError(f"ETAP_3G_ROOTS_SPEC içinde mükerrer kök: {bw}")
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
            'etap_3g_rank': etap_rank,
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
        'package': 'Faz 1 - Etap 3G (Kısa Sureler %100 Tam Kilit Genişletmesi [20 Sure], Açık Mesânî Tepe Uçları ve 600. Kök Çekirdek Zırh Paketi — 50 Kök)',
        'target_count': len(items),
        'locked_count': locked_cnt,
        'total_tokens_in_package': total_tokens,
        'total_corpus_tokens': total_corpus_tokens,
        'current_coverage_pct': round(current_cov_pct, 2),
        'target_coverage_pct': round(target_cov_pct, 2),
        'etap_3g_roots': items,
    }
    json_path = os.path.join(DATA_DIR, 'etap_3g_key_roots.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    pct_now_str = f"{current_cov_pct:.2f}".replace('.', ',')
    pct_target_str = f"{target_cov_pct:.2f}".replace('.', ',')
    md_lines = [
        "# ETAP 3G: KISA SURELER %100 TAM KİLİT GENİŞLETMESİ (20 SURE), AÇIK MESÂNÎ TEPE UÇLARI VE 600. KÖK ÇEKİRDEK PAKETİ (50 KÖK -> 600 KÖK)",
        "## Tabula Rasa Mesânî Çözümleme Sistemi (v3.0 — Faz 1 600 Kök & 20 Tam Kilitli Sure Zırhı)",
        "",
        "> [!IMPORTANT]",
        f"> **HEDEF KAPSAM:** İlk 550 mühürlü kökten (`%90,24`) sonra, 5 sureyi daha `%100` kilitleyen kökler (Sure 82 İnfitâr, 92 Leyl, 93 Duhâ, 95 Tîn, 106 Kureyş → **20 tam kilitli sure**), 3 ve 2 açık Mesânî referanslı tepe uçlar (10 kök) ve kalan en yüksek frekanslı çekirdek kökler (20 kök, 24–36 geçiş) olmak üzere **50 kök** ({total_tokens} geçiş) mühürlenerek toplam sözlük **600 kilitli köke (`%{pct_target_str}` kümülatif kök kapsamı, tüm Kur'an kelimelerinin `%94,79`'u)** ulaştırılır.",
        f"> **Etap 3G İçinde Şu Ana Kadar Mühürlenen:** {locked_cnt} / {len(items)} Kök (Toplam Mühürlü: {len(locked_roots)} Kök | Güncel Kapsam: %{pct_now_str})",
        "",
        "| Etap Sıra | Kategori | Genel Sıra | Kök (Arapça) | Kök (Latin) | Geçiş | Ayet | Örnek | Stratejik Önemi / Kavram Durumu | Durum |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |",
    ]
    for it in items:
        badge = "✅ **MÜHÜRLÜ**" if it['is_locked'] else "⏳ *Bekliyor*"
        desc = it['concept_label'] if it['is_locked'] else it['rationale']
        md_lines.append(
            f"| {it['etap_3g_rank']} | {it['category']} | {it['global_rank']} | "
            f"`{it['root_arabic']}` | `{it['root_latin']}` | **{it['frequency']}** | {it['unique_ayahs']} | "
            f"{it['sample_ayah']} | {desc} | {badge} |"
        )
    md_lines.append("")

    md_path = os.path.join(DATA_DIR, 'ETAP_3G_KAVRAM.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(
        f"Etap 3G JSON üretildi: {json_path} "
        f"({locked_cnt}/{len(items)} mühürlü | Güncel: %{pct_now_str} -> Hedef 600 kök: %{pct_target_str})"
    )
    print(f"Etap 3G Markdown üretildi: {md_path}")


if __name__ == '__main__':
    generate_etap_3g()
