# -*- coding: utf-8 -*-
"""
Etap 3K Kilit Kavramlar (+5 Sure %100 Tam Kilidi [Sure 84, 86, 90, 91, 45 -> 40 Tam Kilitli Sure!],
Kalan Tüm 2+ Açık Mesânî Tepe Uçları ve Kalan Tüm 12 Geçişli + En Yüksek 11 Geçişli Çekirdek Kökler — 50 Kök -> 800 Kilitli Kök)
Tabula Rasa Mesânî Çözümleme Sistemi (v3.0)

İlk 750 mühürlü kökten sonra (%94,81 köklü / %96,65 tüm kelime kapsamı),
5 sureyi daha %100 tam kilide geçiren 35 kökü (Sure 84 İnşikâk, 86 Târık, 90 Beled, 91 Şems, 45 Câsiye
-> 40 tam kilitli sure; Sure 60–66 ve Sure 90–114 [son 25 sure] kesintisiz %100 kilit),
kalan tüm 2+ açık Mesânî tepe uçlarını (2 kök: ل-ي-ن, ص-م-ت), kalan tüm 12 geçişli çekirdek kökleri (7 kök)
ve 11 geçişli açık Mesânî/Furûk çekirdek köklerini (6 kök) olmak üzere toplam 50 kökü (308 geçiş) indeksler;
sözlüğü 800 kilitli köke (%95,43 köklü / %97,05 tüm Kur'an kelimesi kapsamı) ulaştırır.
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
ETAP_3K_ROOTS_SPEC = [
    # Kategori 1: Sure %100 Tam Kilidi (+5 Tam Sure: Sure 84, 86, 90, 91, 45 -> 40 Tam Kilitli Sure! — 35 Kök)
    ('$fq', 'Sure %100 Kilidi', 'İşfâk, Müşfikûn ve Şefak (Sure 84 İnşikâk kilidi | 1M: ح-م-ل + 11 geçiş: 21:28, 21:49, 23:57, 33:72, 52:26, 84:16 akşam kızıllığı ve incelikle karışık derin sakınma/ürperti)'),
    ('wEy', 'Sure %100 Kilidi', 'Va\'y, Vâiye ve Viâ\' (Sure 84 İnşikâk kilidi + 7 geçiş: 12:76, 69:12, 70:18, 84:23 bir kapta toplayıp saklamak, bellemek ve içte biriktirmek)'),
    ('vbr', 'Sure %100 Kilidi', 'Sübûr ve Mesbûr (Sure 84 İnşikâk kilidi + 5 geçiş: 17:102, 25:13, 25:14, 84:11 çaresiz yıkım, bozgun ve hayırdan alıkonulmuş hâl)'),
    ('Tbq', 'Sure %100 Kilidi', 'Tıbâk ve Tabak (Sure 84 İnşikâk kilidi + 4 geçiş: 67:3, 71:15, 84:19 birbirine tam oturan katmanlar ve bir hâlden başka bir hâle geçiş)'),
    ('kdH', 'Sure %100 Kilidi', 'Kadh ve Kâdih (Sure 84 İnşikâk kilidi + 2 geçiş: 84:6 iz bırakıncaya dek yoğun çaba, emek ve didinme)'),
    ('wsq', 'Sure %100 Kilidi', 'Veseka ve İtteseka (Sure 84 İnşikâk son kilidi + 2 geçiş: 84:17, 84:18 gecenin örtüp derleyip toplaması ve ayın dolunay hâlinde bütünlenmesi)'),

    ('Trq', 'Sure %100 Kilidi', 'Tarîk, Tarâik ve Târık (Sure 86 Târık kilidi + 11 geçiş: 4:168, 20:63, 20:77, 23:17, 72:11, 86:1-2 ayakla/vuruşla çiğnenmiş yol ve geceleyin kapıyı çalar gibi beliren yıldız)'),
    ('Slb', 'Sure %100 Kilidi', 'Salb ve Sulb (Sure 86 Târık kilidi + 8 geçiş: 4:23, 4:157, 5:33, 7:124, 12:41, 20:71, 26:49, 86:7 sert omurga/bel kemiği ve asıp çarmıha germek)'),
    ('mhl', 'Sure %100 Kilidi', 'Mehl, Temhîl ve Mühl (Sure 86 Târık kilidi + 6 geçiş: 18:29, 44:45, 70:8, 73:11, 86:17 ağır/yavaş mühlet vermek ve erimiş maden tortusu)'),
    ('SdE', 'Sure %100 Kilidi', 'Sad\' ve Yessadda\'ûne (Sure 86 Târık kilidi + 5 geçiş: 15:94, 30:43, 56:19, 59:21, 86:12 sert yüzeyi yarıp açmak, baş çatlatmak ve hakikati açıkça ortaya koymak)'),
    ('vqb', 'Sure %100 Kilidi', 'Sâkıb (Sure 86 Târık kilidi + 2 geçiş: 37:10, 86:3 karanlığı delip geçen parlak ve keskin ışık)'),
    ('dfq', 'Sure %100 Kilidi', 'Dâfik (Sure 86 Târık kilidi: 86:6 ileri doğru güçlü basınçla atılıp dökülen su)'),
    ('hzl', 'Sure %100 Kilidi', 'Hezl (Sure 86 Târık son kilidi: 86:14 ciddi ölçünün karşıtı boş şaka ve ciddiyetsizlik)'),

    ('$Am', 'Sure %100 Kilidi', 'Meş\'eme (Sure 90 Beled kilidi | 1M: ي-م-ن + 3 geçiş: 56:9 [2x], 90:19 uğursuzluk ve olumsuz akıbet kanadı olan sol taraf)'),
    ('lbd', 'Sure %100 Kilidi', 'Lübed ve Libed (Sure 90 Beled kilidi + 2 geçiş: 72:19, 90:6 üst üste yığılıp sıkışmış yoğun kütle ve yığın mal)'),
    ('qHm', 'Sure %100 Kilidi', 'İktihâm ve Muktehim (Sure 90 Beled kilidi + 2 geçiş: 38:59, 90:11 zor ve dik geçide göğüs gererek atılıp dalmak)'),
    ('njd', 'Sure %100 Kilidi', 'Necdeyn (Sure 90 Beled kilidi: 90:10 açıkça seçilen iki yüksek yol / iki tepe geçidi)'),
    ('sgb', 'Sure %100 Kilidi', 'Mesğabe (Sure 90 Beled kilidi: 90:14 yorgunlukla birleşen şiddetli kıtlık ve açlık günü)'),
    ('$fh', 'Sure %100 Kilidi', 'Şefeteyn (Sure 90 Beled kilidi: 90:9 insanın sözünü ve nefesini biçimlendiren iki dudak)'),
    ('kbd', 'Sure %100 Kilidi', 'Kebed (Sure 90 Beled son kilidi: 90:4 insanın yaratılışındaki zorlu mücadele, direnç ve çetin sınav hâli)'),

    ('Eqr', 'Sure %100 Kilidi', 'Akr ve Âkır (Sure 91 Şems kilidi + 8 geçiş: 3:40, 7:77, 11:65, 19:5, 19:8, 26:157, 54:29, 91:14 sinirini/kökünü kesip devirmek ve doğurganlıktan kesilmiş kısır hâl)'),
    ('nwq', 'Sure %100 Kilidi', 'Nâka (Sure 91 Şems kilidi + 7 geçiş: 7:73, 7:77, 11:64, 17:59, 26:155, 54:27, 91:13 Semûd toplumuna sınama nişanesi kılınan dişi deve)'),
    ('xyb', 'Sure %100 Kilidi', 'Haybe ve Hâibîn (Sure 91 Şems kilidi + 5 geçiş: 3:127, 14:15, 20:61, 20:111, 91:10 umduğunu bulamayıp eli boş, hüsrana uğramış kalmak)'),
    ('THw', 'Sure %100 Kilidi', 'Tahâhâ (Sure 91 Şems kilidi: 91:6 yeryüzünü her yöne genişçe yayıp açmak)'),
    ('dmdm', 'Sure %100 Kilidi', 'Demdeme (Sure 91 Şems kilidi: 91:14 dört köklü: üstlerine kapatıp yerle bir ederek dümdüz etmek)'),
    ('dsw', 'Sure %100 Kilidi', 'Dessâhâ (Sure 91 Şems kilidi: 91:10 benliğini kötülüğe gömüp bastırarak karartmak)'),
    ('lhm', 'Sure %100 Kilidi', 'Elhemehâ (Sure 91 Şems son kilidi: 91:8 içine yuttururcasına yerleştirip sezgi ve ahlaki ayırt etme kabiliyeti vermek)'),

    ('nTq', 'Sure %100 Kilidi', 'Nutk ve Mantık (Sure 45 Câsiye kilidi + 12 geçiş: 21:63, 21:65, 23:62, 27:16, 41:21, 45:29, 51:23, 53:3, 77:35 açık ve anlaşılır sesli sözle konuşmak)'),
    ('Hyq', 'Sure %100 Kilidi', 'Hâka / Yahîku (Sure 45 Câsiye kilidi + 10 geçiş: 6:10, 11:8, 16:34, 21:41, 35:43, 39:48, 40:83, 45:33, 46:26 alay ve tuzağın dönüp dolaşıp sahibini çepeçevre kuşatması)'),
    ('rjz', 'Sure %100 Kilidi', 'Ricz ve Rucz (Sure 45 Câsiye kilidi + 10 geçiş: 2:59, 7:134, 7:135, 7:162, 8:11, 29:34, 34:5, 45:11, 74:5 sarsıcı bela, yıkıcı yaptırım ve kirli putperestlik)'),
    ('Srr', 'Sure %100 Kilidi', 'İsrâr ve Sır (Sure 45 Câsiye kilidi + 6 geçiş: 3:117, 3:135, 45:8, 56:46, 71:7, 68:25 sert düğüm gibi diretip ayak diremek ve yakıcı kavurucu rüzgâr)'),
    ('Etb', 'Sure %100 Kilidi', 'İsti\'tâb ve Mu\'tebîn (Sure 45 Câsiye kilidi + 5 geçiş: 16:84, 30:57, 41:24, 45:35 [2x] sitemi giderip özür dileyerek yeniden hoşnutluk kazanmak)'),
    ('jrH', 'Sure %100 Kilidi', 'Cerh, İctirâh ve Cevârih (Sure 45 Câsiye kilidi + 4 geçiş: 5:4, 6:60, 45:21, 5:45 yaralamak, avcı hayvanla kazanmak ve bilinçli eylem/kötülük işlemek)'),
    ('jvw', 'Sure %100 Kilidi', 'Câsiye ve Cisi (Sure 45 Câsiye kilidi + 3 geçiş: 19:68, 19:72, 45:28 dehşet ve hesap karşısında dizleri üstüne çökmüş hâl)'),
    ('dhr', 'Sure %100 Kilidi', 'Dehr (Sure 45 Câsiye son kilidi + 2 geçiş: 45:24, 76:1 uzun akıp giden zaman çağları ve tarihsel süre)'),

    # Kategori 2: Kalan Tüm 2+ Açık Mesânî Tepe Uçları (2 Kök -> 2+ açık Mesânî = 0!)
    ('lyn', 'Açık Mesânî Zırhı', 'Lîn ve Elyene (2 açık Mesânî ref: ق-ل-ب, خ-ش-ب + 2F! 5 geçiş: 3:159, 20:44, 34:10, 39:23, 59:5 sertliğin zıddı yumuşaklık, esneklik ve ince/yumuşak hurma fidanı)'),
    ('Smt', 'Açık Mesânî Zırhı', 'Sâmitûn (2 açık Mesânî ref: ق-و-ل, ض-ب-ح! 7:193 sesini kesip tam suskunluğa bürünmek)'),

    # Kategori 3: Kalan Tüm 12 Geçişli Çekirdek Kökler (7 Kök — 12'likler %100 biter!)
    ('ESw', 'Yüksek Frekanslı Çekirdek', 'Asâ (12 geçiş: 2:60, 7:107, 7:117, 7:160, 20:18, 20:66, 26:32, 26:44, 26:45, 26:63, 27:10, 28:31 dayanılan ve yönlendirilen sağlam değnek/asâ)'),
    ('Tyn', 'Yüksek Frekanslı Çekirdek', 'Tîn (12 geçiş: 3:49, 5:110, 6:2, 7:12, 17:61, 23:12, 28:38, 32:7, 37:11, 38:71, 38:76, 51:33 su ile yoğrulup biçim alan balçık/çamur)'),
    ('knn', 'Yüksek Frekanslı Çekirdek', 'Kinn, Eknân ve Meknûn (12 geçiş | 1M: ع-ر-ض + 2F: 2:235, 6:25, 16:81, 17:46, 18:57, 27:74, 28:69, 37:49, 41:5, 52:24, 56:23, 56:78 koruyucu örtü ve sığınak içinde gizleyip muhafaza etmek)'),
    ('lHm', 'Yüksek Frekanslı Çekirdek', 'Lahm ve Lühûm (12 geçiş | 1M: ع-ظ-م: 2:173, 2:259, 5:3, 6:145, 16:14, 16:115, 22:37, 23:14, 35:12, 49:12, 52:22, 56:21 kemiği örten kas/et dokusu ve yiyecek et)'),
    ('nTf', 'Yüksek Frekanslı Çekirdek', 'Nutfe (12 geçiş | 2F: 16:4, 18:37, 22:5, 23:13, 23:14, 35:11, 36:77, 40:67, 53:46, 75:37, 76:2, 80:19 süzülüp damlayan saf ve küçücük sıvı damlası)'),
    ('wdy', 'Yüksek Frekanslı Çekirdek', 'Vâdî, Evdiye ve Diye (12 geçiş: 4:92 [2x], 9:121, 13:17, 14:37, 20:12, 26:225, 27:18, 28:30, 46:24, 79:16, 89:9 suların aktığı vadi yatağı ve öldürmede ödenen tazminat/bedel)'),
    ('nyl', 'Yüksek Frekanslı Çekirdek', 'Neyl ve Yenâlu (12 geçiş: 2:124, 3:92, 5:94, 7:49, 9:120 [2x], 22:37, 24:11, 33:25, 60:2 [2x], 64:14 uzanıp elde etmek, erişmek ve payına ulaşmak)'),

    # Kategori 4: En Yüksek 11 Geçişli Açık Mesânî / Furûk Çekirdek Kökleri (6 Kök -> 800 KÖK!)
    ('wrd', 'Yüksek Frekanslı Çekirdek', 'Vürûd, Vârid ve Verîd (11 geçiş | 1M: ص-د-ر + 2F: 11:98 [2x], 12:19, 19:71, 19:86, 21:98, 21:99, 28:23, 50:16, 55:37 su başına inip varmak ve şahdamarı)'),
    ('gyZ', 'Yüksek Frekanslı Çekirdek', 'Ğayz ve Teğayyuz (11 geçiş | 1M: ع-ج-ب: 3:119 [2x], 3:134, 9:15, 9:120, 22:15, 25:12, 33:25, 48:29, 67:8 içte kabarıp taşan yakıcı öfke ve hınç)'),
    ('ymm', 'Yüksek Frekanslı Çekirdek', 'Yemm ve Teyemmüm (11 geçiş | 1M: أ-ر-ض: 2:267, 4:43, 5:6, 7:136, 20:39, 20:78, 20:97, 28:7, 28:40, 51:40 engin su/deniz ve bir yöne/temiz toprağa bilinçle yönelmek)'),
    ('jml', 'Yüksek Frekanslı Çekirdek', 'Cemîl, Cemâl, Cemel ve Cümle (11 geçiş | 3F: 7:40, 12:18, 12:83, 15:85, 16:6, 25:32, 33:28, 33:49, 70:5, 73:10, 77:33 derli toplu bütünlük, zarif güzellik ve iri deve)'),
    ('SEq', 'Yüksek Frekanslı Çekirdek', 'Sâika ve Saık (11 geçiş | 2F: 2:19, 2:55, 4:153, 7:143, 13:13, 39:68, 41:13 [2x], 41:17, 51:44, 52:45 gökten inen sarsıcı yıldırım ve bayılıp yığılmak)'),
    ('zbr', 'Yüksek Frekanslı Çekirdek', 'Zebûr, Zübür ve Züber (11 geçiş | 1F: 3:184, 4:163, 16:44, 17:55, 18:96, 21:105, 23:53, 26:196, 35:25, 54:43, 54:52 sert yüzeye kazınmış yazılı metin/kayıt ve sağlam demir bloklar)'),
]


def generate_etap_3k():
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
    for etap_rank, (bw, category, rationale) in enumerate(ETAP_3K_ROOTS_SPEC, 1):
        if bw in seen_bw:
            raise ValueError(f"ETAP_3K_ROOTS_SPEC içinde mükerrer kök: {bw}")
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
            'etap_3k_rank': etap_rank,
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
        'package': 'Faz 1 - Etap 3K (+5 Sure %100 Tam Kilidi [Sure 84, 86, 90, 91, 45 -> 40 Sure], Kalan Tüm 2+ Açık Mesânî Tepe Uçları ve 12–11 Geçişli Çekirdek Kökler — 50 Kök -> 800 Kök)',
        'target_count': len(items),
        'locked_count': locked_cnt,
        'total_tokens_in_package': total_tokens,
        'total_corpus_tokens': total_corpus_tokens,
        'current_coverage_pct': round(current_cov_pct, 2),
        'target_coverage_pct': round(target_cov_pct, 2),
        'etap_3k_roots': items,
    }
    json_path = os.path.join(DATA_DIR, 'etap_3k_key_roots.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    pct_now_str = f"{current_cov_pct:.2f}".replace('.', ',')
    pct_target_str = f"{target_cov_pct:.2f}".replace('.', ',')
    md_lines = [
        "# ETAP 3K: +5 SURE %100 TAM KİLİDİ (40 SURE), KALAN TÜM 2+ AÇIK MESÂNÎ TEPE UÇLARI VE 12–11 GEÇİŞLİ ÇEKİRDEK KÖKLER (50 KÖK -> 800 KÖK)",
        "## Tabula Rasa Mesânî Çözümleme Sistemi (v3.0 — Faz 1 800 Kök, %95+ Kapsam & 40 Tam Kilitli Sure Zırhı)",
        "",
        "> [!IMPORTANT]",
        f"> **HEDEF KAPSAM:** İlk 750 mühürlü kökten (`%94,81`) sonra, `5` sureyi daha `%100` kilitleyen `35` kök (Sure 84 İnşikâk, 86 Târık, 90 Beled, 91 Şems, 45 Câsiye → **40 tam kilitli sure**; Sure 60–66 ve Sure 90–114 [son 25 sure] kesintisiz `%100` kilit), kalan tüm `2+` açık Mesânî tepe uçları (`2` kök), kalan tüm `12` geçişli çekirdek kökler (`7` kök) ve `11` geçişli açık Mesânî/Furûk çekirdek kökleri (`6` kök) olmak üzere **50 kök** ({total_tokens} geçiş) mühürlenerek toplam sözlük **800 kilitli köke (`%{pct_target_str}` kümülatif kök kapsamı, tüm Kur'an kelimelerinin `%97,05`'i)** ulaştırılır.",
        f"> **Etap 3K İçinde Şu Ana Kadar Mühürlenen:** {locked_cnt} / {len(items)} Kök (Toplam Mühürlü: {len(locked_roots)} Kök | Güncel Kapsam: %{pct_now_str})",
        "",
        "| Etap Sıra | Kategori | Genel Sıra | Kök (Arapça) | Kök (Latin) | Geçiş | Ayet | Örnek | Stratejik Önemi / Kavram Durumu | Durum |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |",
    ]
    for it in items:
        badge = "✅ **MÜHÜRLÜ**" if it['is_locked'] else "⏳ *Bekliyor*"
        desc = it['concept_label'] if it['is_locked'] else it['rationale']
        md_lines.append(
            f"| {it['etap_3k_rank']} | {it['category']} | {it['global_rank']} | "
            f"`{it['root_arabic']}` | `{it['root_latin']}` | **{it['frequency']}** | {it['unique_ayahs']} | "
            f"{it['sample_ayah']} | {desc} | {badge} |"
        )
    md_lines.append("")

    md_path = os.path.join(DATA_DIR, 'ETAP_3K_KAVRAM.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(
        f"Etap 3K JSON üretildi: {json_path} "
        f"({locked_cnt}/{len(items)} mühürlü | Güncel: %{pct_now_str} -> Hedef 800 kök: %{pct_target_str})"
    )
    print(f"Etap 3K Markdown üretildi: {md_path}")


if __name__ == '__main__':
    generate_etap_3k()
