# -*- coding: utf-8 -*-
"""
Etap 3H Kilit Kavramlar (Sure %100 Tam Kilit Genişletmesi [20->25 Sure: 60, 64, 65, 85, 87],
3+ Açık Mesânî/Furûk Tepe Uçları ve 650. Kök Yüksek Frekanslı Çekirdek Zırh Paketi — 50 Kök -> 650 Kilitli Kök)
Tabula Rasa Mesânî Çözümleme Sistemi (v3.0)

İlk 600 mühürlü kökten sonra (%91,77 köklü / %94,79 tüm kelime kapsamı),
5 sureyi daha %100 kilitleyen 20 kökü (Sure 60 Mümtehine, 64 Teğâbün, 65 Talâk, 85 Bürûc, 87 A'lâ -> 25 tam kilitli sure),
4, 3 ve 2 açık Mesânî/Furûk referanslı 10 kritik tepe eşleniğini ve kalan en yüksek frekanslı 20 çekirdek kökü
(50 kök / 704 geçiş) indeksler; toplam sözlüğü 650 köke (%93,18 köklü / %95,69 tüm kelime) ulaştırır.
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
ETAP_3H_ROOTS_SPEC = [
    # Kategori 1: Sure %100 Kilidi I (Sure 65 Talâk, Sure 60 Mümtehine ve Sure 87 A'lâ -> +3 Tam Kilitli Sure!)
    ('HSy', 'Sure %100 Kilidi', 'İhsâ\' (Sure 65 Talâk kilidi + 11 geçiş: 14:34, 18:49, 36:12, 65:1, 72:28, 78:29 tek tek sayıp kayda geçirerek kuşatmak)'),
    ('klf', 'Sure %100 Kilidi', 'Teklîf ve Tekellüf (Sure 65 Talâk kilidi + 8 geçiş: 2:233, 2:286, 6:152, 38:86, 65:7 güç ve kapasite ölçüsünde sorumluluk yüklemek)'),
    ('wbl', 'Sure %100 Kilidi', 'Vebâl, Vebîl ve Vâbil (Sure 65 Talâk son kilidi & Sure 64 Teğâbün kilidi + 8 geçiş: 2:264-265 sağanak yağmur ve 59:15, 64:5, 65:9 ağır sonuç)'),
    ('ESm', 'Sure %100 Kilidi', 'İsmet, İ\'tisâm ve Asım (Sure 60 Mümtehine kilidi | 1M+1F + 13 geçiş: 3:103, 4:146, 11:43, 60:10 sımsıkı tutunup korunmak ve bağlar)'),
    ('Asw', 'Sure %100 Kilidi', 'Üsve ve Teessî (Sure 60 Mümtehine kilidi + 7 geçiş: 7:93, 12:84, 33:21, 60:4, 60:6 örnek alınan sağlam model ve içten üzülmek)'),
    ('vqf', 'Sure %100 Kilidi', 'Sakf ve Teskîf (Sure 60 Mümtehine kilidi | 1F + 6 geçiş: 2:191, 3:112, 8:57, 33:61, 60:2 ele geçirip kıskıvrak yakalamak)'),
    ('mHn', 'Sure %100 Kilidi', 'İmtihân (Sure 60 Mümtehine son kilidi + 49:3: 49:3, 60:10 kalbi ve iddiayı eritip sınayarak özünü ortaya çıkarmak)'),
    ('Avr', 'Sure %100 Kilidi', 'Eser, Âsâr ve Îsâr (Sure 87 A\'lâ kilidi | 1M+2F + 21 geçiş: 20:84, 30:50, 36:12, 59:9, 79:38, 87:16 geride bırakılan izler ve tercih etmek)'),
    ('rEy', 'Sure %100 Kilidi', 'Ra\'y, Mer\'â ve Riâyet (Sure 87 A\'lâ kilidi + 10 geçiş: 2:104, 20:54, 23:8, 28:23, 79:31, 87:4 otlatmak, otlak ve emaneti gözetip korumak)'),
    ('Hwy', 'Sure %100 Kilidi', 'Ahvâ ve Havâyâ (Sure 87 A\'lâ kilidi + 6:146: 87:5 yemyeşil otlağın kuruyup siyaha çalan koyu renge dönmesi ve 6:146 bağırsaklar)'),

    # Kategori 2: Sure %100 Kilidi II (Sure 87 A'lâ Sonu, Sure 64 Teğâbün ve Sure 85 Bürûc -> 25 Tam Kilitli Sure!)
    ('gvw', 'Sure %100 Kilidi', 'Güsâ\' (Sure 87 A' + "'" + 'lâ son kilidi + 23:41: 23:41, 87:5 selin sürüklediği kuru çerçöp ve köpük)'),
    ('H*r', 'Sure %100 Kilidi', 'Hazer, Hذر ve Mahzûr (Sure 64 Teğâbün kilidi + 21 geçiş: 2:19, 2:243, 4:71, 4:102, 24:63, 63:4, 64:14 tehlikeye karşı uyanık ve tetikte olmak)'),
    ('zEm', 'Sure %100 Kilidi', 'Za\'m (Sure 64 Teğâbün & 62 Cum\'a kilidi + 17 geçiş: 6:22, 6:136, 17:56, 18:48, 62:6, 64:7 delilsiz zan ve mesnetsiz iddiada bulunmak)'),
    ('SfH', 'Sure %100 Kilidi', 'Safh (Sure 64 Teğâbün kilidi + 8 geçiş: 2:109, 15:85, 24:22, 43:5, 64:14 yüzünü başa kakmadan çevirip hoşgörüyle sayfasını kapatmak)'),
    ('gbn', 'Sure %100 Kilidi', 'Teğâbün (Sure 64 Teğâbün son kilidi: 64:9 kâr-zarar hesabında kimin aldanıp açıkta kaldığının ortaya çıktığı gün)'),
    ('wqd', 'Sure %100 Kilidi', 'Vukûd, Îkâd ve Mûkade (Sure 85 Bürûc & 104 Hümeze kilidi + 11 geçiş: 2:17, 2:24, 5:64, 24:35, 85:5, 104:6 ateş tutuşturmak ve çıra/yakıt)'),
    ('bT$', 'Sure %100 Kilidi', 'Batş ve Batşe (Sure 85 Bürûc kilidi + 10 geçiş: 7:195, 26:130, 28:19, 44:16, 54:36, 85:12 sıkıca kavrayıp ezici güçle yakalamak)'),
    ('Hrq', 'Sure %100 Kilidi', 'Hark ve Harîk (Sure 85 Bürûc kilidi + 9 geçiş: 2:266, 3:181, 20:97, 21:68, 29:24, 85:10 ateşle yakıp kavurmak)'),
    ('mjd', 'Sure %100 Kilidi', 'Mecîd (Sure 85 Bürûc kilidi + 4 geçiş: 11:73, 50:1, 85:15, 85:21 şan, cömertlik ve yücelikte genişlik sahibi)'),
    ('xdd', 'Sure %100 Kilidi', 'Uhdûd ve Hadd (Sure 85 Bürûc son kilidi + 31:18: 85:4 yerde yarılan derin hendek ve 31:18 kibirle yüz/yanak çevirmek)'),

    # Kategori 3: 4, 3 ve 2 Açık Mesânî/Furûk Referanslı Tepe Eşlenikler (10 Kök)
    ('dfE', 'Açık Mesânî Zırhı', 'Def\' ve Dâfi\' (4 açık ref: 2M+2F! و-ق-ع zıddı 10 geçiş: 2:251, 4:6, 22:38, 23:96, 52:8, 70:2 itip savuşturmak ve hakkını teslim etmek)'),
    ('$rq', 'Açık Mesânî Zırhı', 'Meşrık, İşrâk ve Şarkıyye (3 açık ref: 2M+1F! غ-ر-ب zıddı 17 geçiş: 2:115, 2:142, 2:258, 24:35, 38:18, 39:69 güneşin doğup parlaması ve doğu)'),
    ('rsw', 'Açık Mesânî Zırhı', 'Revâsî ve Mürsâ (3 açık ref: 2M+1F! س-ي-ر ve م-و-د zıddı 14 geçiş: 7:187, 11:41, 13:3, 16:15, 79:32 demir atıp sabitlenmek ve sabit dağlar)'),
    ('Ebr', 'Açık Mesânî Zırhı', 'İbret, İ\'tibâr ve Âbirî (3 açık ref: 1M+2F! 9 geçiş: 3:13, 4:43, 12:43, 12:111, 24:44, 59:2 bir yakadan diğerine geçmek, yorumlamak ve ders çıkarmak)'),
    ('qtr', 'Açık Mesânî Zırhı', 'Katr, Katere veMukter (3 açık ref: 1M+2F! س-ر-ف ve ب-س-ط zıddı 5 geçiş: 2:236, 17:100, 25:67, 42:27, 80:41 eli sıkıp kısmak ve koyu is/toz)'),
    ('gTw', 'Açık Mesânî Zırhı', 'Gıtâ\' ve Ağtâ (3 açık ref: 2M+1F! ك-ش-ف ve ض-ح-و zıddı 2 geçiş: 18:101, 50:22 gözün ve gecenin üzerine çekilen koyu örtü/perde)'),
    ('jmd', 'Açık Mesânî Zırhı', 'Câmide (3 açık ref: 2M+1F! م-ر-ر doğrudan zıddı 27:88: dağların donmuş gibi hareketsiz ve sabit sanılması)'),
    ('wqt', 'Açık Mesânî Zırhı', 'Vakt ve Mîkât (2 açık Mesânî ref! ح-ي-ن ve أ-ن-ي eşleniği 13 geçiş: 4:103, 7:142, 15:38, 44:40, 77:11, 78:17 sınırları belirlenmiş vakit)'),
    ('njm', 'Açık Mesânî Zırhı', 'Necm ve Nücûm (2 açık ref: 1M+1F! ش-ج-ر eşleniği 13 geçiş: 6:97, 16:16, 53:1, 55:6, 56:75, 86:3 doğup beliren yıldız ve gövdesiz bitki)'),
    ('byD', 'Açık Mesânî Zırhı', 'Ebyad, Beydâ\' ve İbyadda (2 açık Mesânî ref! س-و-د zıddı 12 geçiş: 2:187, 3:106-107, 7:108, 12:84, 35:27, 37:46-49 beyaz olmak ve yumurta)'),

    # Kategori 4: En Yüksek Frekanslı Çekirdek Kökler I (20-24 Geçiş — Kalan Tüm 20+ Kökler!)
    ('kwd', 'Yüksek Frekanslı Çekirdek', 'Kâde ve Yekâdü (24 geçiş — #1 kalan kök! 2:20, 2:71, 14:17, 24:35, 24:43, 67:8 bir işin gerçekleşmeye ramak kalması: "neredeyse / az kalsın")'),
    ('vmr', 'Yüksek Frekanslı Çekirdek', 'Semer ve Semerât (24 geçiş — #2 kalan kök! 2:22, 2:266, 6:99, 6:141, 14:37, 16:67, 18:34 ağacın ve emeğin olgunlaşmış meyvesi/ürünü)'),
    ('grq', 'Yüksek Frekanslı Çekirdek', 'Gark, İğrâk ve Garkâ (23 geçiş | 1M — #3 kalan kök! 2:50, 7:136, 8:54, 10:90, 11:43, 79:1 suya batıp boğulmak ve derinliğine dalmak)'),
    ('srE', 'Yüksek Frekanslı Çekirdek', 'Serî\', Sür\'at ve Müsâraa (23 geçiş — #4 kalan kök! 2:202, 3:114, 3:133, 5:41, 21:90, 23:61 hızla koşup yarışmak ve hesabı çabuk görmek)'),
    ('m$y', 'Yüksek Frekanslı Çekirdek', 'Meşy ve Meşşâ\' (23 geçiş — #5 kalan kök! 2:20, 17:37, 20:128, 24:45, 25:63, 57:28, 67:15, 68:11 adım adım yürümek ve laf gezdirmek)'),
    ('trb', 'Yüksek Frekanslı Çekirdek', 'Türâb, Etrâb ve Matrabe (22 geçiş — #6 kalan kök + Sure 90 Beled! 3:59, 13:5, 22:5, 30:20, 56:37, 78:40, 90:16 toprak, yaşıtlar ve yoksulluk)'),
    ('rbE', 'Yüksek Frekanslı Çekirdek', 'Erbaa, Râbi\', Rubu\' ve Rubâ\' (22 geçiş | 1M+1F — #7 kalan kök! 2:226, 2:260, 4:3, 4:12, 4:15, 24:4, 35:1, 41:10, 58:7 dört sayısı ve dörtte bir)'),
    ('tmm', 'Yüksek Frekanslı Çekirdek', 'Temâm ve İtmâm (22 geçiş — #8 kalan kök! 2:124, 2:187, 5:3, 6:115, 7:142, 9:32, 61:8 eksiği kalmayacak şekilde tamama erdirmek)'),
    ('nxl', 'Yüksek Frekanslı Çekirdek', 'Nahl ve Nahîl (20 geçiş | 1F — #9 kalan kök! 2:266, 6:99, 6:141, 13:4, 16:11, 19:23-25, 50:10, 54:20, 55:11, 69:7 hurma ağacı ve hurmalıklar)'),
    ('snw', 'Yüksek Frekanslı Çekirdek', 'Sene, Sinîn ve Senâ (20 geçiş — #10 kalan kök! 2:96, 7:130, 10:5, 12:47, 17:12, 24:43, 29:14 kuraklık/bolluk yılı, yıllar ve şimşeğin parıltısı)'),

    # Kategori 5: En Yüksek Frekanslı Çekirdek Kökler II (18-20 Geçiş -> 650 KÖK & %93,18 KÖK KAPSAMI!)
    ('SnE', 'Yüksek Frekanslı Çekirdek', 'Sun\', San\'at ve Masâni\' (20 geçiş | 1F: 7:137, 11:37, 18:104, 20:39, 20:41, 21:80, 26:129, 27:88 maharet ve özenle işleyip imal etmek)'),
    ('mry', 'Yüksek Frekanslı Çekirdek', 'Mirye, İmtirâ\' ve Temârî (20 geçiş | 1F: 2:147, 6:114, 11:17, 15:63, 18:22, 41:54, 53:12, 54:36 sağa-sola çekerek kuşku ve çekişmeye düşmek)'),
    ('Hzb', 'Yüksek Frekanslı Çekirdek', 'Hizb ve Ahzâb (20 geçiş | 1M+1F: 5:56, 11:17, 18:12, 33:20-22, 38:11-13, 40:30, 58:19-22 ortak bir tavır ve çıkar etrafında kümelenmiş taraf/grup)'),
    ('fkh', 'Yüksek Frekanslı Çekirdek', 'Fâkihe, Fekihîn ve Tefekküh (19 geçiş: 23:19, 36:55, 36:57, 43:73, 44:27, 52:18, 55:11, 56:65, 83:31 meyve, neşeyle tat almak ve şaşkınca söylenmek)'),
    ('vmn', 'Yüksek Frekanslı Çekirdek', 'Semen, Semâniye, Sâmin ve Sümün (19 geçiş | 1M+1F: 2:41, 4:12, 6:143, 12:20, 18:22, 28:27, 39:6, 69:7 değer/bedel, sekiz sayısı ve sekizde bir)'),
    ('dbb', 'Yüksek Frekanslı Çekirdek', 'Dâbbe ve Devâbb (18 geçiş | 1F: 2:164, 6:38, 8:22, 11:6, 16:49, 24:45, 27:82, 34:14, 42:29 yeryüzünde kımıldayıp yürüyen her canlı varlık)'),
    ('ldn', 'Yüksek Frekanslı Çekirdek', 'Ledün (18 geçiş | 1M: 3:8, 3:38, 4:40, 4:75, 11:1, 17:80, 18:2, 18:65, 27:6 bir zatın tam yanı başı, öz katı ve doğrudan huzuru)'),
    ('rAs', 'Yüksek Frekanslı Çekirdek', 'Re\'s ve Ruûs (18 geçiş: 2:196, 2:279, 5:6, 7:150, 12:36, 14:43, 17:51, 19:4, 20:94, 32:12, 37:65 baş, saç, doruk ve ana sermaye)'),
    ('xSm', 'Yüksek Frekanslı Çekirdek', 'Hasm, Husûmet ve Tehâsum (18 geçiş | 1F: 2:204, 3:44, 4:105, 22:19, 36:49, 38:21-22, 38:64, 43:58, 50:28 karşılıklı dava ve çekişmeye girmek)'),
    ('nfr', 'Yüksek Frekanslı Çekirdek', 'Nefr, Nefîr ve Nüfûr (18 geçiş | 1M: 4:71, 9:38-41, 9:122, 17:41, 18:34, 19:73, 67:21, 71:6, 74:50 topluca harekete geçmek, insan grubu ve ürküp kaçmak)'),
]


def generate_etap_3h():
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
    for etap_rank, (bw, category, rationale) in enumerate(ETAP_3H_ROOTS_SPEC, 1):
        if bw in seen_bw:
            raise ValueError(f"ETAP_3H_ROOTS_SPEC içinde mükerrer kök: {bw}")
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
            'etap_3h_rank': etap_rank,
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
        'package': 'Faz 1 - Etap 3H (Sure %100 Tam Kilit Genişletmesi [25 Sure], 3+ Açık Mesânî/Furûk Tepe Uçları ve 650. Kök Çekirdek Zırh Paketi — 50 Kök)',
        'target_count': len(items),
        'locked_count': locked_cnt,
        'total_tokens_in_package': total_tokens,
        'total_corpus_tokens': total_corpus_tokens,
        'current_coverage_pct': round(current_cov_pct, 2),
        'target_coverage_pct': round(target_cov_pct, 2),
        'etap_3h_roots': items,
    }
    json_path = os.path.join(DATA_DIR, 'etap_3h_key_roots.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    pct_now_str = f"{current_cov_pct:.2f}".replace('.', ',')
    pct_target_str = f"{target_cov_pct:.2f}".replace('.', ',')
    md_lines = [
        "# ETAP 3H: SURE %100 TAM KİLİT GENİŞLETMESİ (25 SURE), 3+ AÇIK MESÂNÎ/FURÛK TEPE UÇLARI VE 650. KÖK ÇEKİRDEK PAKETİ (50 KÖK -> 650 KÖK)",
        "## Tabula Rasa Mesânî Çözümleme Sistemi (v3.0 — Faz 1 650 Kök & 25 Tam Kilitli Sure Zırhı)",
        "",
        "> [!IMPORTANT]",
        f"> **HEDEF KAPSAM:** İlk 600 mühürlü kökten (`%91,77`) sonra, 5 sureyi daha `%100` kilitleyen kökler (Sure 60 Mümtehine, 64 Teğâbün, 65 Talâk, 85 Bürûc, 87 A'lâ → **25 tam kilitli sure**), 4, 3 ve 2 açık Mesânî/Furûk referanslı tepe uçlar (10 kök) ve kalan en yüksek frekanslı çekirdek kökler (20 kök, 18–24 geçiş) olmak üzere **50 kök** ({total_tokens} geçiş) mühürlenerek toplam sözlük **650 kilitli köke (`%{pct_target_str}` kümülatif kök kapsamı, tüm Kur'an kelimelerinin `%95,69`'u)** ulaştırılır.",
        f"> **Etap 3H İçinde Şu Ana Kadar Mühürlenen:** {locked_cnt} / {len(items)} Kök (Toplam Mühürlü: {len(locked_roots)} Kök | Güncel Kapsam: %{pct_now_str})",
        "",
        "| Etap Sıra | Kategori | Genel Sıra | Kök (Arapça) | Kök (Latin) | Geçiş | Ayet | Örnek | Stratejik Önemi / Kavram Durumu | Durum |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |",
    ]
    for it in items:
        badge = "✅ **MÜHÜRLÜ**" if it['is_locked'] else "⏳ *Bekliyor*"
        desc = it['concept_label'] if it['is_locked'] else it['rationale']
        md_lines.append(
            f"| {it['etap_3h_rank']} | {it['category']} | {it['global_rank']} | "
            f"`{it['root_arabic']}` | `{it['root_latin']}` | **{it['frequency']}** | {it['unique_ayahs']} | "
            f"{it['sample_ayah']} | {desc} | {badge} |"
        )
    md_lines.append("")

    md_path = os.path.join(DATA_DIR, 'ETAP_3H_KAVRAM.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(
        f"Etap 3H JSON üretildi: {json_path} "
        f"({locked_cnt}/{len(items)} mühürlü | Güncel: %{pct_now_str} -> Hedef 650 kök: %{pct_target_str})"
    )
    print(f"Etap 3H Markdown üretildi: {md_path}")


if __name__ == '__main__':
    generate_etap_3h()
