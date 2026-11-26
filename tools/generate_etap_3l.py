# -*- coding: utf-8 -*-
"""
Etap 3L Kilit Kavramlar (+5 Sure %100 Tam Kilidi [Sure 71 Nûh, 49 Hucurât, 58 Mücâdele, 77 Mürselât, 89 Fecr -> 45 Tam Kilitli Sure!],
Kalan Tüm 4+ Açık Furûk Tepe Uçları, Kalan Tüm 11 Geçişli Çekirdek Kökler ve İlk 10 Geçişli Kök — 50 Kök -> 850 Kilitli Kök)
Tabula Rasa Mesânî Çözümleme Sistemi (v3.0)

İlk 800 mühürlü kökten sonra (%95,43 köklü / %97,05 tüm kelime kapsamı),
5 sureyi daha %100 tam kilide geçiren 40 kökü (Sure 71 Nûh, 49 Hucurât, 58 Mücâdele, 77 Mürselât, 89 Fecr
-> 45 tam kilitli sure; Sure 60–66 ve Sure 84–114 [son 31 sure] kesintisiz %100 kilit),
kalan tüm 4+ açık Furûk tepe uçlarını (2 kök: ص-ع-د, ب-ر-ق), kalan tüm 11 geçişli çekirdek kökleri (7 kök)
ve 10 geçişli ilk çekirdek kökü (1 kök: أ-ص-ل) olmak üzere toplam 50 kökü (254 geçiş) indeksler;
sözlüğü 850 kilitli köke (%95,94 köklü / %97,38 tüm Kur'an kelimesi kapsamı) ulaştırır.
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
ETAP_3L_ROOTS_SPEC = [
    # Kategori 1: Sure %100 Tam Kilidi (+5 Tam Sure: Sure 71, 49, 58, 77, 89 -> 45 Tam Kilitli Sure! — 40 Kök)
    ('wqr', 'Sure %100 Kilidi', 'Vakr, Vakâr ve Tevkîr (Sure 71 Nûh kilidi + 9 geçiş: 6:25, 17:46, 18:57, 31:7, 41:5, 41:44, 48:9, 51:2, 71:13 kulaktaki ağırlık/tıkanıklık, ağır yük taşıyan bulut ve yüce saygınlık)'),
    ('tbr', 'Sure %100 Kilidi', 'Tebâr, Tetbîr ve Mütetebbir (Sure 71 Nûh kilidi + 6 geçiş: 7:139, 17:7, 25:39, 71:28 parçalayıp un ufak ederek tamamen yıkıma uğratmak)'),
    ('drr', 'Sure %100 Kilidi', 'Midrâr ve Dürrî (Sure 71 Nûh kilidi + 4 geçiş: 6:6, 11:52, 24:35, 71:11 bolca ve kesintisiz akıp dökülen yağmur ve inci gibi parıldayan yıldız)'),
    ('srj', 'Sure %100 Kilidi', 'Sirâc (Sure 71 Nûh kilidi + 4 geçiş: 25:61, 33:46, 71:16, 78:13 karanlığı delen aydınlatıcı ve ısıtıcı ışık/kandil kaynağı)'),
    ('fjj', 'Sure %100 Kilidi', 'Fecc ve Ficâc (Sure 71 Nûh kilidi + 3 geçiş: 21:31, 22:27, 71:20 iki dağ arasından açılan geniş geçit ve uzak yol)'),
    ('SbE', 'Sure %100 Kilidi', 'Esâbi\' (Sure 71 Nûh kilidi + 2 geçiş: 2:19, 71:7 parmaklar — gerçeği duymamak için kulakları tıkama imgesi)'),
    ('nsr', 'Sure %100 Kilidi', 'Nesr (Sure 71 Nûh son kilidi: 71:23 Nûh kavminin akbaba/kartal simgeli geleneksel put/odağı)'),

    ('Swt', 'Sure %100 Kilidi', 'Savt ve Esvât (Sure 49 Hucurât kilidi + 8 geçiş: 17:64, 20:108, 31:19, 49:2, 49:3 titreşimle çıkan işitilir ses ve ses tonunu ölçülü tutmak)'),
    ('ndm', 'Sure %100 Kilidi', 'Nedâme ve Nâdimîn (Sure 49 Hucurât kilidi + 7 geçiş: 5:31, 5:52, 10:54, 23:40, 26:157, 34:33, 49:6 yanlış eylem sonrası içten kemiren yakıcı pişmanlık)'),
    ('Ent', 'Sure %100 Kilidi', 'Anet ve A\'nete (Sure 49 Hucurât kilidi + 5 geçiş: 2:220, 3:118, 4:25, 9:128, 49:7 kırık kemiğin yeniden incinmesi gibi ağır sıkıntı, darlık ve yıpranma)'),
    ('$Eb', 'Sure %100 Kilidi', 'Şuûb ve Şuab (Sure 49 Hucurât + Sure 77 Mürselât ortak kilidi + 2 geçiş: 49:13, 77:30 ana gövdeden ayrılıp kollara bölünen büyük halk toplulukları ve üç kollu gölge)'),
    ('jss', 'Sure %100 Kilidi', 'Tecessüs (Sure 49 Hucurât kilidi: 49:12 el yordamıyla yoklarcasına insanların gizli kusurlarını araştırıp gözetlemek)'),
    ('lqb', 'Sure %100 Kilidi', 'Elkâb (Sure 49 Hucurât kilidi | 1M: 49:11 insanları küçültücü/incitici takma adlarla damgalamak)'),
    ('lyt', 'Sure %100 Kilidi', 'Yelitküm (Sure 49 Hucurât kilidi: 49:14 bir kimsenin hak ettiği emeğin karşılığından zerre kadar eksiltmek)'),
    ('nbz', 'Sure %100 Kilidi', 'Tenâbüz (Sure 49 Hucurât son kilidi: 49:11 karşılıklı kötü lakaplar fırlatarak birbirini aşağılamak)'),

    ('stt', 'Sure %100 Kilidi', 'Sitte ve Sittîn (Sure 58 Mücâdele kilidi + 8 geçiş: 7:54, 10:3, 11:7, 25:59, 32:4, 50:38, 57:4, 58:4 altı sayısı — altı evre/gün ve altmış yoksulu doyurma ölçüsü)'),
    ('xms', 'Sure %100 Kilidi', 'Hamse, Hâmis ve Humus (Sure 58 Mücâdele kilidi + 8 geçiş: 3:125, 8:41, 18:22, 24:7, 24:9, 29:14, 58:7, 70:4 beş sayısı, beşinci ve beşte bir payı)'),
    ('sds', 'Sure %100 Kilidi', 'Sâdis ve Südüs (Sure 58 Mücâdele kilidi + 5 geçiş: 4:11, 4:12, 18:22, 58:7 altıncı ve miras paylaşımındaki altıda bir hisse)'),
    ('$kw', 'Sure %100 Kilidi', 'Şekvâ, Teştekî ve Mişkât (Sure 58 Mücâdele kilidi + 3 geçiş: 12:86, 24:35, 58:1 içindeki derdi/haksızlığı açıp yakarmak ve duvardaki ışık oyuğu)'),
    ('fsH', 'Sure %100 Kilidi', 'Tefessüh ve Fesh (Sure 58 Mücâdele kilidi + 3 geçiş: 58:11 darlığı giderip oturumda başkalarına yer açmak ve gönül genişliği)'),
    ('kbt', 'Sure %100 Kilidi', 'Kebt (Sure 58 Mücâdele kilidi + 3 geçiş: 3:127, 58:5 öfkeyle yüzüstü bastırıp bozguna ve alçalmaya uğratmak)'),
    ('Hw*', 'Sure %100 Kilidi', 'İstihvâz (Sure 58 Mücâdele kilidi + 2 geçiş: 4:141, 58:19 sürü güder gibi bütünüyle kuşatıp denetim altına almak)'),
    ('jls', 'Sure %100 Kilidi', 'Mecâlis (Sure 58 Mücâdele son kilidi: 58:11 topluca oturulup görüşülen toplantı/meclis alanları)'),

    ('Sfr', 'Sure %100 Kilidi', 'Safrâ, Musferr ve Sufr (Sure 77 Mürselât kilidi + 5 geçiş: 2:69, 30:51, 39:21, 57:20, 77:33 parlak sarı renk ve ekinin kuruyup sararması)'),
    ('nsf', 'Sure %100 Kilidi', 'Nesf (Sure 77 Mürselât kilidi + 5 geçiş: 20:97, 20:105, 77:10 kökünden söküp savurarak toz gibi dağıtmak)'),
    ('hnA', 'Sure %100 Kilidi', 'Henîen (Sure 77 Mürselât kilidi + 4 geçiş: 4:4, 52:19, 69:24, 77:43 zahmetsiz, gönül rahatlığı ve sindirim kolaylığıyla afiyetle yenen/alınan şey)'),
    ('mhn', 'Sure %100 Kilidi', 'Mehîn (Sure 77 Mürselât kilidi + 4 geçiş: 32:8, 43:52, 68:10, 77:20 zayıf, sıradan, gösterişsiz ve küçümsenen nitelik)'),
    ('frt', 'Sure %100 Kilidi', 'Furât (Sure 77 Mürselât kilidi + 3 geçiş: 25:53, 35:12, 77:27 susuzluğu anında kesen tatlı, berrak ve içimi rahat su)'),
    ('$mx', 'Sure %100 Kilidi', 'Şâmihât (Sure 77 Mürselât kilidi: 77:27 başını göğe doğru yüceltip yükselen ulu dağlar)'),
    ('kft', 'Sure %100 Kilidi', 'Kifât (Sure 77 Mürselât son kilidi: 77:25 dirileri ve ölüleri sinesinde derleyip toplayan yeryüzü)'),

    ('sry', 'Sure %100 Kilidi', 'Esrâ, Yesrî ve Seriyy (Sure 89 Fecr kilidi + 8 geçiş: 11:81, 15:65, 17:1, 19:24, 20:77, 26:52, 44:23, 89:4 geceleyin yola koyulup yürümek ve ince dere/akarsu)'),
    ('dkk', 'Sure %100 Kilidi', 'Dekk ve Dekke (Sure 89 Fecr kilidi + 7 geçiş: 7:143, 18:98, 69:14, 89:21 yüksek ve sert kütleyi dövüp parçalayarak yerle düzlemek)'),
    ('rSd', 'Sure %100 Kilidi', 'Rasad, İrsâd ve Mirsâd (Sure 89 Fecr kilidi + 6 geçiş: 9:5, 9:107, 72:9, 72:27, 78:21, 89:14 hedefi kesintisiz gözetleyen pusuda/gözetleme noktasında beklemek)'),
    ('Sbb', 'Sure %100 Kilidi', 'Sabb (Sure 89 Fecr kilidi + 5 geçiş: 22:19, 44:48, 80:25, 89:13 yukarıdan aşağıya güçlü ve kesintisiz akışla boşaltıp dökmek)'),
    ('lmm', 'Sure %100 Kilidi', 'Lemm ve Lemem (Sure 89 Fecr kilidi + 4 geçiş: 6:150, 33:18, 53:32, 89:19 dağınık olanı sıyırıp toplamak, ufak sürçmeler ve "haydi gelin" çağrısı)'),
    ('Sxr', 'Sure %100 Kilidi', 'Sahr ve Sahre (Sure 89 Fecr kilidi + 3 geçiş: 18:63, 31:16, 89:9 yekpare sert ve büyük kaya kütlesi)'),
    ('wtd', 'Sure %100 Kilidi', 'Evtâd (Sure 89 Fecr kilidi + 3 geçiş: 38:12, 78:7, 89:10 yere derinlemesine çakılıp sabitleyen kazık/direkler)'),
    ('wtr', 'Sure %100 Kilidi', 'Vetr, Tetrâ ve Yetireküm (Sure 89 Fecr kilidi + 3 geçiş: 23:44, 47:35, 89:3 tek/eşsiz sayı, birbiri ardınca gönderilmek ve hakkı eksiltmek)'),
    ('jmm', 'Sure %100 Kilidi', 'Cemm (Sure 89 Fecr kilidi: 89:20 kuyuda birikip taşan su gibi aşırı ve yığılı mal tutkusu)'),
    ('swT', 'Sure %100 Kilidi', 'Savt (Sure 89 Fecr son kilidi: 89:13 karışıp vuran şiddetli kırbaç/yaptırım darbesi — Sure 84–114 [son 31 sure] kesintisiz %100!)'),

    # Kategori 2: Kalan Tüm 4+ Açık Furûk Tepe Uçları (2 Kök -> 4+ açık Furûk = 0!)
    ('SEd', 'Açık Furûk Tepe Ucu', 'Saîd, Suûd ve Yes\'adu (4 açık Furûk ref + 1M! 9 geçiş: 3:153, 4:43, 5:6, 6:125, 18:8, 18:40, 35:10, 72:17, 74:17 yukarı tırmanıp yükselmek, düz toprak yüzeyi ve çetin yokuş)'),
    ('brq', 'Açık Furûk Tepe Ucu', 'Berk ve Berika (4 açık Furûk ref! 6 geçiş: 2:19, 2:20, 13:12, 24:43, 30:24, 75:7 ani parlayıp çakan şimşek ve gözün kamaşıp şaşkına dönmesi)'),

    # Kategori 3: Kalan Tüm 11 Geçişli Çekirdek Kökler (7 Kök — 11'likler %100 biter!) + İlk 10 Geçişli Kök (1 Kök -> 850 KÖK!)
    ('Enb', 'Yüksek Frekanslı Çekirdek', 'İneb ve A\'nâb (11 geçiş: 2:266, 6:99, 13:4, 16:11, 16:67, 17:91, 18:32, 23:19, 36:34, 78:32, 80:28 salkım salkım üzüm ve üzüm bağları)'),
    ('Trf', 'Yüksek Frekanslı Çekirdek', 'Tarf ve Etrâf (11 geçiş: 3:127, 11:114, 13:41, 14:43, 20:130, 21:44, 27:40, 37:48, 38:52, 42:45, 55:56 bir şeyin uç/kenar sınırı ve göz kırpım bakışı)'),
    ('fAy', 'Yüksek Frekanslı Çekirdek', 'Fie ve Fieteyn (11 geçiş: 2:249, 3:13, 4:88, 8:16, 8:19, 8:45, 8:48, 18:43, 28:81 bir bayrak/hedef etrafında toplanıp geri yaslanılan topluluk/bölük)'),
    ('gmm', 'Yüksek Frekanslı Çekirdek', 'Ğamm ve Ğamâm (11 geçiş: 2:57, 2:210, 3:153, 3:154, 7:160, 10:71, 20:40, 21:88, 22:22, 25:25 göğü örten beyaz bulut tabakası ve zihni kaplayıp daraltan keder/sıkıntı)'),
    ('sHb', 'Yüksek Frekanslı Çekirdek', 'Sehâb ve Yüshabûn (11 geçiş: 2:164, 7:57, 13:12, 24:40, 24:43, 27:88, 30:48, 35:9, 40:71, 52:44, 54:48 yüzey boyunca sürükleyip çekmek ve gökte sürüklenen bulutlar)'),
    ('sbb', 'Yüksek Frekanslı Çekirdek', 'Sebeb, Esbâb ve Sebb (11 geçiş: 2:166, 6:108, 18:84, 18:85, 18:89, 18:92, 22:15, 38:10, 40:36, 40:37 ulaştıran ip/vesile/yol ve bağı koparırcasına sövmek)'),
    ('wkA', 'Yüksek Frekanslı Çekirdek', 'Müttekiîn ve Ettevekkü (11 geçiş: 12:31, 18:31, 20:18, 36:56, 38:51, 43:34, 52:20, 55:54, 56:16, 76:13, 83:23 bir desteğe güven ve huzurla yaslanıp dayanmak)'),
    ('ASl', 'Yüksek Frekanslı Çekirdek', 'Asl, Usûl ve Asîl (10 geçiş | 2F: 7:205, 13:15, 14:24, 24:36, 25:5, 33:42, 37:64, 48:9, 59:5, 76:25 yere sağlam tutunan kök/temel ve günün ikindi-akşam ucu)'),
]


def generate_etap_3l():
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
    for etap_rank, (bw, category, rationale) in enumerate(ETAP_3L_ROOTS_SPEC, 1):
        if bw in seen_bw:
            raise ValueError(f"ETAP_3L_ROOTS_SPEC içinde mükerrer kök: {bw}")
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
            'etap_3l_rank': etap_rank,
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
        'package': 'Faz 1 - Etap 3L (+5 Sure %100 Tam Kilidi [Sure 71, 49, 58, 77, 89 -> 45 Sure], Kalan Tüm 4+ Açık Furûk Tepe Uçları ve 11–10 Geçişli Çekirdek Kökler — 50 Kök -> 850 Kök)',
        'target_count': len(items),
        'locked_count': locked_cnt,
        'total_tokens_in_package': total_tokens,
        'total_corpus_tokens': total_corpus_tokens,
        'current_coverage_pct': round(current_cov_pct, 2),
        'target_coverage_pct': round(target_cov_pct, 2),
        'etap_3l_roots': items,
    }
    json_path = os.path.join(DATA_DIR, 'etap_3l_key_roots.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    pct_now_str = f"{current_cov_pct:.2f}".replace('.', ',')
    pct_target_str = f"{target_cov_pct:.2f}".replace('.', ',')
    md_lines = [
        "# ETAP 3L: +5 SURE %100 TAM KİLİDİ (45 SURE), 4+ AÇIK FURÛK TEPE UÇLARI VE 11–10 GEÇİŞLİ ÇEKİRDEK KÖKLER (50 KÖK -> 850 KÖK)",
        "## Tabula Rasa Mesânî Çözümleme Sistemi (v3.0 — Faz 1 850 Kök, %95,94 Kapsam & 45 Tam Kilitli Sure Zırhı)",
        "",
        "> [!IMPORTANT]",
        f"> **HEDEF KAPSAM:** İlk 800 mühürlü kökten (`%95,43`) sonra, `5` sureyi daha `%100` kilitleyen `40` kök (Sure 71 Nûh, 49 Hucurât, 58 Mücâdele, 77 Mürselât, 89 Fecr → **45 tam kilitli sure**; Sure 60–66 ve Sure 84–114 [son 31 sure] kesintisiz `%100` kilit), kalan tüm `4+` açık Furûk tepe uçları (`2` kök: `ص-ع-د`, `ب-ر-ق`), kalan tüm `11` geçişli çekirdek kökler (`7` kök) ve `10` geçişli ilk çekirdek kök (`1` kök: `أ-ص-ل`) olmak üzere **50 kök** ({total_tokens} geçiş) mühürlenerek toplam sözlük **850 kilitli köke (`%{pct_target_str}` kümülatif kök kapsamı, tüm Kur'an kelimelerinin `%97,38`'i)** ulaştırılır.",
        f"> **Etap 3L İçinde Şu Ana Kadar Mühürlenen:** {locked_cnt} / {len(items)} Kök (Toplam Mühürlü: {len(locked_roots)} Kök | Güncel Kapsam: %{pct_now_str})",
        "",
        "| Etap Sıra | Kategori | Genel Sıra | Kök (Arapça) | Kök (Latin) | Geçiş | Ayet | Örnek | Stratejik Önemi / Kavram Durumu | Durum |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |",
    ]
    for it in items:
        badge = "✅ **MÜHÜRLÜ**" if it['is_locked'] else "⏳ *Bekliyor*"
        desc = it['concept_label'] if it['is_locked'] else it['rationale']
        md_lines.append(
            f"| {it['etap_3l_rank']} | {it['category']} | {it['global_rank']} | "
            f"`{it['root_arabic']}` | `{it['root_latin']}` | **{it['frequency']}** | {it['unique_ayahs']} | "
            f"{it['sample_ayah']} | {desc} | {badge} |"
        )
    md_lines.append("")

    md_path = os.path.join(DATA_DIR, 'ETAP_3L_KAVRAM.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(
        f"Etap 3L JSON üretildi: {json_path} "
        f"({locked_cnt}/{len(items)} mühürlü | Güncel: %{pct_now_str} -> Hedef 850 kök: %{pct_target_str})"
    )
    print(f"Etap 3L Markdown üretildi: {md_path}")


if __name__ == '__main__':
    generate_etap_3l()
