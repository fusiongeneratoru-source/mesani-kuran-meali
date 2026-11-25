# -*- coding: utf-8 -*-
"""
Etap 3J Kilit Kavramlar (+6 Sure %100 Tam Kilidi [Sure 63, 66, 61, 100, 101, 88 -> 35 Tam Kilitli Sure!],
Kalan Tüm 2+ Açık Mesânî Tepe Uçları ve 13–12 Geçişli Yüksek Frekanslı Çekirdek Kökler — 50 Kök -> 750 Kilitli Kök)
Tabula Rasa Mesânî Çözümleme Sistemi (v3.0)

İlk 700 mühürlü kökten sonra (%94,24 köklü / %96,29 tüm kelime kapsamı),
6 sureyi daha %100 tam kilide geçiren 29 kökü (Sure 63 Münâfikûn, 66 Tahrîm, 61 Saff, 100 Âdiyât, 101 Kâria, 88 Ğâşiye
-> 35 tam kilitli sure; Sure 60–66 ve Sure 92–114 kesintisiz %100 kilit),
kalan tüm 2+ açık Mesânî/Furûk tepe uçlarını (10 kök) ve 13–12 geçişli en yüksek frekanslı 11 çekirdek kökü
(toplam 50 kök / 285 geçiş) indeksler; sözlüğü 750 kilitli köke (%94,81 köklü / %96,65 tüm kelime) ulaştırır.
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
ETAP_3J_ROOTS_SPEC = [
    # Kategori 1: Sure %100 Tam Kilidi (+6 Tam Sure: Sure 63, 66, 61, 100, 101, 88 -> 35 Tam Kilitli Sure! — 29 Kök)
    ('lwy', 'Sure %100 Kilidi', 'Leyy ve Telviye (Sure 63 Münâfikûn kilidi + 5 geçiş: 3:78, 3:153, 4:46, 4:135, 63:5 dili, başı veya sözü büküp çarpıtmak)'),
    ('jsm', 'Sure %100 Kilidi', 'Cism ve Ecsâm (Sure 63 Münâfikûn kilidi + 2 geçiş: 2:247, 63:4 fiziki gövde, cüsse ve dış bedensel yapı)'),
    ('x$b', 'Sure %100 Kilidi', 'Huşub (Sure 63 Münâfikûn kilidi: 63:4 içi boş, cansız kütük ve kereste gövdeler)'),
    ('snd', 'Sure %100 Kilidi', 'Müsennede (Sure 63 Münâfikûn son kilidi: 63:4 kendi başına duramayıp duvara dayandırılmış destekli gövde)'),
    ('bkr', 'Sure %100 Kilidi', 'Bükre, İbkâr ve Bikr (Sure 66 Tahrîm kilidi + 12 geçiş: 2:68, 3:41, 19:11, 56:36, 66:5 günün ilk taze vakti ve el değmemiş tazelik)'),
    ('syH', 'Sure %100 Kilidi', 'Siyâha ve Sâihât (Sure 66 Tahrîm kilidi + 3 geçiş: 9:2, 9:112, 66:5 yeryüzünde akıp dolaşmak ve özgürce yol almak)'),
    ('Sgw', 'Sure %100 Kilidi', 'Sağv ve Sağat (Sure 66 Tahrîm kilidi + 2 geçiş: 6:113, 66:4 kalbin/kulağın bir yana kayıp meyletmesi)'),
    ('vyb', 'Sure %100 Kilidi', 'Seyyibât (Sure 66 Tahrîm son kilidi: 66:5 daha önce evlilik deneyimi yaşamış kadınlar)'),
    ('Ayd', 'Sure %100 Kilidi', 'Eyd ve Te\'yîd (Sure 61 Saff kilidi + 11 geçiş: 2:87, 2:253, 3:13, 5:110, 8:26, 61:14 arka çıkıp sağlam kuvvetle desteklemek)'),
    ('dll', 'Sure %100 Kilidi', 'Delâlet ve Delîl (Sure 61 Saff kilidi + 8 geçiş: 7:22, 20:40, 20:120, 25:45, 28:12, 61:10 gizli veya açık iz üzerinden yol göstermek)'),
    ('mqt', 'Sure %100 Kilidi', 'Makt (Sure 61 Saff kilidi + 6 geçiş: 4:22, 35:39, 40:10, 40:35, 61:3 çirkin tutum ve tutarsızlığa karşı en şiddetli tiksinti ve öfke)'),
    ('TfA', 'Sure %100 Kilidi', 'İtfâ\' (Sure 61 Saff kilidi | 2M+3F + 3 geçiş: 5:64, 9:32, 61:8 yanan ateşi veya parlayan ışığı söndürüp bastırmak)'),
    ('rSS', 'Sure %100 Kilidi', 'Marsûs (Sure 61 Saff son kilidi: 61:4 aralıksız kenetlenip kurşun gibi tek blok hâlinde örülmüş sağlam yapı)'),
    ('vwr', 'Sure %100 Kilidi', 'İsâre (Sure 100 Âdiyât kilidi + 5 geçiş: 2:71, 30:9, 30:48, 35:9, 100:4 toprağı, bulutu veya tozu altüst edip havaya kaldırmak)'),
    ('HSl', 'Sure %100 Kilidi', 'Tahsîl ve Hussile (Sure 100 Âdiyât kilidi: 100:10 kabuktan/özden ayıklayıp göğüslerdeki gerçeği açığa çıkarmak)'),
    ('DbH', 'Sure %100 Kilidi', 'Dabh (Sure 100 Âdiyât kilidi: 100:1 hızla koşan atların nefes nefese soluma sesi)'),
    ('qdH', 'Sure %100 Kilidi', 'Kadh ve Mûriyât (Sure 100 Âdiyât kilidi: 100:2 sert çarpışmayla kıvılcım ve ateş çakmak)'),
    ('knd', 'Sure %100 Kilidi', 'Kenûd (Sure 100 Âdiyât kilidi: 100:6 iyilikleri yutup vermeyen çorak toprak gibi alabildiğine nankörlük)'),
    ('nqE', 'Sure %100 Kilidi', 'Nak\' (Sure 100 Âdiyât son kilidi: 100:4 hızla koparılıp göğe savrulan yoğun toz bulutu)'),
    ('bvv', 'Sure %100 Kilidi', 'Bess ve Mebsûs (Sure 101 Kâria & 88 Ğâşiye kilidi + 9 geçiş: 2:164, 4:1, 12:86, 88:16, 101:4 dört bir yana saçıp yaymak ve içteki derdi dökmek)'),
    ('Ey$', 'Sure %100 Kilidi', 'Îşe ve Meâş (Sure 101 Kâria kilidi + 8 geçiş: 7:10, 15:20, 20:124, 69:21, 101:7 geçim zemini ve yaşanılan hayat düzeyi)'),
    ('Hmy', 'Sure %100 Kilidi', 'Hamiyye ve Hâmiye (Sure 101 Kâria & 88 Ğâşiye kilidi | 1M + 6 geçiş: 5:103, 9:35, 48:26, 88:4, 101:11 kızışıp kor hâline gelmek ve koruyucu taşkınlık)'),
    ('fr$', 'Sure %100 Kilidi', 'Firâş ve Ferâş (Sure 101 Kâria kilidi | 1M+2F + 6 geçiş: 2:22, 6:142, 51:48, 55:54, 56:34, 101:4 yere serilen döşek ve yayılmış pervaneler)'),
    ('Ehn', 'Sure %100 Kilidi', 'Ihn (Sure 101 Kâria kilidi + 2 geçiş: 70:9, 101:5 renk renk boyanıp dağılmış ince yün lifleri)'),
    ('nf$', 'Sure %100 Kilidi', 'Nefş ve Menfûş (Sure 101 Kâria son kilidi + 2 geçiş: 21:78, 101:5 geceleyin dağılıp yayılmak ve atılıp kabartılmış yün)'),
    ('DrE', 'Sure %100 Kilidi', 'Tadarru\' ve Darî\' (Sure 88 Ğâşiye kilidi + 8 geçiş: 6:42, 6:43, 6:63, 7:55, 88:6 boyun bükerek alçakgönüllü yakarış ve kuru dikenli bitki)'),
    ('smn', 'Sure %100 Kilidi', 'Semîn ve Yusminu (Sure 88 Ğâşiye kilidi + 4 geçiş: 12:43, 12:46, 51:26, 88:7 besili/semiz olmak ve besleyip güçlendirmek)'),
    ('kwb', 'Sure %100 Kilidi', 'Ekvâb (Sure 88 Ğâşiye kilidi + 4 geçiş: 43:71, 56:18, 76:15, 88:14 kulpsuz, ağızı yuvarlak ve düzgün içecek kapları)'),
    ('sTH', 'Sure %100 Kilidi', 'Sutihat (Sure 88 Ğâşiye son kilidi: 88:20 geniş ve yaşanabilir bir yüzey hâlinde yayılıp döşenmek)'),

    # Kategori 2: Kalan Tüm 2+ Açık Mesânî ve 4+ Referanslı Tepe Uçlar (10 Kök)
    ('Tms', 'Açık Mesânî Zırhı', 'Tams (3 açık Mesânî ref: ع-ي-ن, ك-و-ك-ب, ن-ج-م! 5 geçiş: 4:47, 10:88, 36:66, 54:37, 77:8 izi, ışığı ve belirginliği tamamen silip belirsizleştirmek)'),
    ('vbT', 'Açık Mesânî Zırhı', 'Tesbît (3 açık Mesânî ref: ب-ع-ث, س-ر-ع, ع-د-د! 9:46 harekete geçmekten alıkoyup ağırlaştırarak geri bırakmak)'),
    ('gwr', 'Açık Mesânî Zırhı', 'Ğâr ve Ğavr (2 açık Mesânî ref: ع-ي-ن, م-و-ه! 4 geçiş: 9:40, 9:57, 18:41, 67:30 suyun dibe çekilip kaybolması ve sığınılan derin mağara)'),
    ('zll', 'Açık Mesânî Zırhı', 'Zelle ve İstizlâl (2 açık Mesânî ref: ث-ب-ت, ق-د-م! 4 geçiş: 2:36, 2:209, 3:155, 16:94 sağlam zeminden ayağın kayıp sendelemesi)'),
    ('gyD', 'Açık Mesânî Zırhı', 'Ğayd ve Tağîdu (2 açık Mesânî ref: ز-ي-د, ن-ه-ر! 2 geçiş: 11:44, 13:8 suyun veya rahimdeki birikimin eksilip çekilmesi)'),
    ('$ks', 'Açık Mesânî Zırhı', 'Müteşâkisûn (2 açık Mesânî ref: س-ل-م, س-و-ي! 39:29 birbiriyle sürekli çekişen, geçimsiz ve uyuşmaz ortaklar)'),
    ('sdy', 'Açık Mesânî Zırhı', 'Südâ (2 açık Mesânî ref: ح-س-ب, و-ق-ت! 75:36 amaçsız, sorumluluksuz ve başıboş salıverilmiş hâl)'),
    ('rkd', 'Açık Mesânî Zırhı', 'Ravâkid (2 açık Mesânî ref: ج-ر-ي, ر-و-ح! 42:33 rüzgâr kesilince denizin üstünde hareketsiz çakılıp duran gemiler)'),
    ('swd', 'Açık Mesânî Zırhı', 'Sevâd, Esved ve Seyyid (1M+3F: ب-ي-ض zıddı! 10 geçiş: 2:187, 3:39, 3:106, 12:25, 16:58 koyu siyahlık, kararmak ve önder/efendi)'),
    ('bxs', 'Açık Mesânî Zırhı', 'Bahs (1M+3F: و-ف-ي zıddı! 7 geçiş: 2:282, 7:85, 11:15, 11:85, 12:20, 20:102, 26:183 hak edilen ölçüyü ve değeri haksızca eksiltip kısmak)'),

    # Kategori 3: En Yüksek Frekanslı Kalan Çekirdek Kökler (13 & 12 Geçiş — 11 Kök -> 750 KÖK!)
    ('jwr', 'Yüksek Frekanslı Çekirdek', 'Câr, Civâr ve İcâre (13 geçiş — kalan son 13\'lük kök! 4:36, 8:48, 9:6, 13:4, 16:9, 23:88, 67:28 yakın komşuluk, himayeye almak ve yoldan sapmak)'),
    ('jby', 'Yüksek Frekanslı Çekirdek', 'İctibâ\' ve Cevâbî (12 geçiş | 1M: و-ح-ي! 3:179, 6:87, 7:203, 12:6, 16:121, 34:13 bir araya toplayıp süzmek, seçip ayırmak ve büyük su havuzları)'),
    ('jHd', 'Yüksek Frekanslı Çekirdek', 'Cuhûd (12 geçiş | 1M: ي-ق-ن! 6:33, 7:51, 11:59, 16:71, 27:14 içten bilip kesinleştiği hâlde inatla reddedip örtmek)'),
    ('Hsr', 'Yüksek Frekanslı Çekirdek', 'Hasre ve Mahsûr (12 geçiş: 2:167, 3:156, 6:31, 8:36, 17:29, 36:30, 67:4 elden kaçırılan fırsatın derin yanışı ve yorgun düşüp tükenmek)'),
    ('xrr', 'Yüksek Frekanslı Çekirdek', 'Harr ve Harra (12 geçiş: 7:143, 12:100, 16:26, 17:107, 22:31, 25:73 yüksekten ses çıkararak düşmek ve derhâl yüzüstü kapanmak)'),
    ('xTb', 'Yüksek Frekanslı Çekirdek', 'Hatb ve Hitâb (12 geçiş: 2:235, 11:37, 12:51, 15:57, 20:95, 38:20 yüz yüze hitap etmek, evlilik teklifi ve ağır mesele/iş)'),
    ('xwD', 'Yüksek Frekanslı Çekirdek', 'Havd ve Hâidîn (12 geçiş: 4:140, 6:68, 6:91, 9:65, 9:69, 74:45 suyun içine dalar gibi boş, alaycı ve yıkıcı lafa dalmak)'),
    ('sjn', 'Yüksek Frekanslı Çekirdek', 'Sicn ve Siccîn (12 geçiş | 1M: ع-ل-و! 12:25, 12:32-42, 26:29, 83:7-8 dar kapalı yere hapsedip kapatmak ve sıkı kilitli sicil)'),
    ('slk', 'Yüksek Frekanslı Çekirdek', 'Sülûk (12 geçiş: 15:12, 16:69, 20:53, 23:27, 26:200, 69:32, 74:42 bir geçide/yola girmek veya bir şeyi diğerinin içine geçirip dizmek)'),
    ('$ml', 'Yüksek Frekanslı Çekirdek', 'Şimâl ve İştemelet (12 geçiş | 1M: ي-م-ن! 6:143-144, 7:17, 16:48, 18:17, 56:41 sol yön/taraf ve rahmin içine alıp kuşatması)'),
    ('TmE', 'Yüksek Frekanslı Çekirdek', 'Tama\' (12 geçiş | 1M: خ-و-ف! 2:75, 5:84, 7:46, 7:56, 13:12, 32:16 gerçekleşmesini güçlü bir umut ve istekle arzulayıp beklemek)'),
]


def generate_etap_3j():
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
    for etap_rank, (bw, category, rationale) in enumerate(ETAP_3J_ROOTS_SPEC, 1):
        if bw in seen_bw:
            raise ValueError(f"ETAP_3J_ROOTS_SPEC içinde mükerrer kök: {bw}")
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
            'etap_3j_rank': etap_rank,
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
        'package': 'Faz 1 - Etap 3J (+6 Sure %100 Tam Kilidi [Sure 63, 66, 61, 100, 101, 88 -> 35 Sure], Kalan Tüm 2+ Açık Mesânî Tepe Uçları ve 13–12 Geçişli Çekirdek Kökler — 50 Kök -> 750 Kök)',
        'target_count': len(items),
        'locked_count': locked_cnt,
        'total_tokens_in_package': total_tokens,
        'total_corpus_tokens': total_corpus_tokens,
        'current_coverage_pct': round(current_cov_pct, 2),
        'target_coverage_pct': round(target_cov_pct, 2),
        'etap_3j_roots': items,
    }
    json_path = os.path.join(DATA_DIR, 'etap_3j_key_roots.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    pct_now_str = f"{current_cov_pct:.2f}".replace('.', ',')
    pct_target_str = f"{target_cov_pct:.2f}".replace('.', ',')
    md_lines = [
        "# ETAP 3J: +6 SURE %100 TAM KİLİDİ (35 SURE), KALAN TÜM 2+ AÇIK MESÂNÎ TEPE UÇLARI VE 13–12 GEÇİŞLİ ÇEKİRDEK KÖKLER (50 KÖK -> 750 KÖK)",
        "## Tabula Rasa Mesânî Çözümleme Sistemi (v3.0 — Faz 1 750 Kök & 35 Tam Kilitli Sure Zırhı)",
        "",
        "> [!IMPORTANT]",
        f"> **HEDEF KAPSAM:** İlk 700 mühürlü kökten (`%94,24`) sonra, `6` sureyi daha `%100` kilitleyen `29` kök (Sure 63 Münâfikûn, 66 Tahrîm, 61 Saff, 100 Âdiyât, 101 Kâria, 88 Ğâşiye → **35 tam kilitli sure**; Sure 60–66 ve Sure 92–114 kesintisiz `%100` kilit), kalan tüm `2+` açık Mesânî/Furûk tepe uçları (`10` kök) ve `13–12` geçişli `11` çekirdek kök olmak üzere **50 kök** ({total_tokens} geçiş) mühürlenerek toplam sözlük **750 kilitli köke (`%{pct_target_str}` kümülatif kök kapsamı, tüm Kur'an kelimelerinin `%96,65`'i)** ulaştırılır.",
        f"> **Etap 3J İçinde Şu Ana Kadar Mühürlenen:** {locked_cnt} / {len(items)} Kök (Toplam Mühürlü: {len(locked_roots)} Kök | Güncel Kapsam: %{pct_now_str})",
        "",
        "| Etap Sıra | Kategori | Genel Sıra | Kök (Arapça) | Kök (Latin) | Geçiş | Ayet | Örnek | Stratejik Önemi / Kavram Durumu | Durum |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |",
    ]
    for it in items:
        badge = "✅ **MÜHÜRLÜ**" if it['is_locked'] else "⏳ *Bekliyor*"
        desc = it['concept_label'] if it['is_locked'] else it['rationale']
        md_lines.append(
            f"| {it['etap_3j_rank']} | {it['category']} | {it['global_rank']} | "
            f"`{it['root_arabic']}` | `{it['root_latin']}` | **{it['frequency']}** | {it['unique_ayahs']} | "
            f"{it['sample_ayah']} | {desc} | {badge} |"
        )
    md_lines.append("")

    md_path = os.path.join(DATA_DIR, 'ETAP_3J_KAVRAM.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(
        f"Etap 3J JSON üretildi: {json_path} "
        f"({locked_cnt}/{len(items)} mühürlü | Güncel: %{pct_now_str} -> Hedef 750 kök: %{pct_target_str})"
    )
    print(f"Etap 3J Markdown üretildi: {md_path}")


if __name__ == '__main__':
    generate_etap_3j()
