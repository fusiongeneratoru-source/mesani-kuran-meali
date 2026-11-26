# -*- coding: utf-8 -*-
"""
Etap 3M Kilit Kavramlar (+5 Sure %100 Tam Kilidi [Sure 83 Mutaffifîn, 80 Abese, 74 Müddessir, 75 Kıyâmet, 81 Tekvîr -> 50 Tam Kilitli Sure & Sure 80–114 Son 35 Sure Kesintisiz %100!]
ve Kalan Tüm 10 Geçişli Çekirdek Kökler — 50 Kök -> 900 Kilitli Kök)
Tabula Rasa Mesânî Çözümleme Sistemi (v3.0)

İlk 850 mühürlü kökten sonra (%95,94 köklü / %97,38 tüm kelime kapsamı),
5 sureyi daha %100 tam kilide geçiren 43 kökü (Sure 83 Mutaffifîn, 80 Abese, 74 Müddessir, 75 Kıyâmet, 81 Tekvîr
-> 50 tam kilitli sure; Sure 60–66 ve Sure 80–114 [son 35 sure] kesintisiz %100 kilit)
ve kalan tüm 10 geçişli çekirdek kökleri (7 kök: ط-و-ل, د-م-و, ج-ب-ر, ج-د-د, ز-ي-ل, م-ل-و, م-أ-ي — ≥10 geçişli açık kök = 0!)
olmak üzere toplam 50 kökü (190 geçiş) indeksler;
sözlüğü 900 kilitli köke (%96,32 köklü / %97,62 tüm Kur'an kelimesi kapsamı) ulaştırır.
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
ETAP_3M_ROOTS_SPEC = [
    # Kategori 1: Sure %100 Tam Kilidi (+5 Tam Sure: Sure 83, 80, 74, 75, 81 -> 50 Tam Kilitli Sure & Son 35 Sure Kesintisiz %100! — 43 Kök)
    ('DHk', 'Sure %100 Kilidi', 'Dahik, Edhake ve Dâhike (Sure 83 Mutaffifîn + Sure 80 Abese ortak kilidi + 10 geçiş: 9:82, 11:71, 23:110, 27:19, 43:47, 53:43, 53:60, 80:39, 83:29, 83:34 gülmek, sevinçle açılmak ve alaycı gülüş)'),
    ('Ark', 'Sure %100 Kilidi', 'Erâik (Sure 83 Mutaffifîn kilidi + 5 geçiş: 18:31, 36:56, 76:13, 83:23, 83:35 gölgelikli ve süslü oturma divanları/tahtlar)'),
    ('mzj', 'Sure %100 Kilidi', 'Mizâc (Sure 83 Mutaffifîn kilidi + 3 geçiş: 76:5, 76:17, 83:27 içeceğe katılan hoş koku ve tat karışımı)'),
    ('nDr', 'Sure %100 Kilidi', 'Nadra ve Nâdıra (Sure 83 Mutaffifîn + Sure 75 Kıyâmet ortak kilidi | 1M + 3 geçiş: 75:22, 76:11, 83:24 taze parlaklık, yüzdeki canlı ışık ve dirilik)'),
    ('rqm', 'Sure %100 Kilidi', 'Merkûm ve Rakîm (Sure 83 Mutaffifîn kilidi + 3 geçiş: 18:9, 83:9, 83:20 silinmez biçimde nakşedilip yazılmış kayıt/kitabe)'),
    ('Tff', 'Sure %100 Kilidi', 'Mutaffifîn (Sure 83 Mutaffifîn kilidi: 83:1 ölçü ve tartıda alırken tam, verirken ufak ufak kırpıp eksiltenler)'),
    ('gmz', 'Sure %100 Kilidi', 'Yetegâmezûn (Sure 83 Mutaffifîn kilidi: 83:30 yanlarından geçerken kaş-göz işaretiyle alaylı biçimde fısıldaşmak)'),
    ('rHq', 'Sure %100 Kilidi', 'Rahîk (Sure 83 Mutaffifîn kilidi: 83:25 tortusuz, katkısız ve saf içecek)'),
    ('ryn', 'Sure %100 Kilidi', 'Râne (Sure 83 Mutaffifîn kilidi: 83:14 işlenenlerin kalbin üzerini pas/kir tabakası gibi kaplayıp örtmesi)'),
    ('snm', 'Sure %100 Kilidi', 'Tesnîm (Sure 83 Mutaffifîn son kilidi: 83:27 yüksekten/doruktan akıp gelen seçkin kaynak — Sure 82–114 kesintisiz %100!)'),

    ('rhq', 'Sure %100 Kilidi', 'Rehak ve İrhâk (Sure 80 Abese + Sure 74 Müddessir ortak kilidi + 10 geçiş: 10:26, 10:27, 18:73, 18:80, 68:43, 70:44, 72:6, 72:13, 74:17, 80:41 kaplayıp bürümek ve dayanılması güç yükle bunaltmak)'),
    ('$An', 'Sure %100 Kilidi', 'Şe\'n (Sure 80 Abese kilidi + 4 geçiş: 10:61, 24:62, 55:29, 80:37 kişinin tüm dikkatini bağlayan önemli iş, hâl ve gündem)'),
    ('Ebs', 'Sure %100 Kilidi', 'Abese ve Abûs (Sure 80 Abese + Sure 74 Müddessir ortak kilidi + 3 geçiş: 74:22, 76:10, 80:1 yüzünü buruşturup kaşlarını çatmak)'),
    ('Hdq', 'Sure %100 Kilidi', 'Hadâik (Sure 80 Abese kilidi + 3 geçiş: 27:60, 78:32, 80:30 etrafı duvar/çitle çevrili bol ağaçlı bahçeler)'),
    ('Sdy', 'Sure %100 Kilidi', 'Tesaddâ ve Tasdiye (Sure 80 Abese kilidi + 2 geçiş: 8:35, 80:6 ses/el çırpma ve birine özellikle yüzünü çevirip yönelmek)'),
    ('Abb', 'Sure %100 Kilidi', 'Ebb (Sure 80 Abese kilidi: 80:31 hayvanların otlaması için yerden biten taze mera bitkisi)'),
    ('Sxx', 'Sure %100 Kilidi', 'Sâhha (Sure 80 Abese kilidi: 80:33 kulak zarını sarsıp sağır eden şiddetli çarpma/haykırış sesi)'),
    ('qDb', 'Sure %100 Kilidi', 'Kadb (Sure 80 Abese son kilidi: 80:28 biçilip tekrar yeşeren taze yeşil ot/yonca)'),

    ('tsE', 'Sure %100 Kilidi', 'Tis\'a ve Tis\'ûn (Sure 74 Müddessir kilidi + 7 geçiş: 17:101, 27:12, 27:48, 18:25, 38:23, 74:30 dokuz sayısı ve doksan dokuz)'),
    ('nqr', 'Sure %100 Kilidi', 'Nâkûr ve Nakîr (Sure 74 Müddessir kilidi + 4 geçiş: 4:53, 4:124, 74:8 delip oyarak vurmak, çekirdekteki küçücük oyuk ve ses borusu)'),
    ('rhn', 'Sure %100 Kilidi', 'Rahîn ve Rihân (Sure 74 Müddessir kilidi + 3 geçiş: 2:283, 52:21, 74:38 bir borca veya eyleme karşılık rehin/teminat tutulmak)'),
    ('bsr', 'Sure %100 Kilidi', 'Besere ve Bâsira (Sure 74 Müddessir + Sure 75 Kıyâmet ortak kilidi + 2 geçiş: 74:22, 75:24 yüzü asılıp kararmak, somurtmak)'),
    ('dvr', 'Sure %100 Kilidi', 'Müddessir (Sure 74 Müddessir kilidi: 74:1 üstüne dış örtüsünü/bürgüsünü sarınıp bürünen)'),
    ('qsr', 'Sure %100 Kilidi', 'Kasvera (Sure 74 Müddessir son kilidi: 74:51 yaban eşeklerini kaçıran güçlü aslan veya avcı)'),

    ('xsf', 'Sure %100 Kilidi', 'Hasf (Sure 75 Kıyâmet kilidi | 1M + 8 geçiş: 16:45, 17:68, 28:81, 28:82, 29:40, 34:9, 67:16, 75:8 yerin dibine geçirmek ve ayın ışığının tutulup sönmesi)'),
    ('rqy', 'Sure %100 Kilidi', 'Rukiyy, Terakkî ve Râk (Sure 75 Kıyâmet kilidi + 4 geçiş: 17:93, 38:10, 75:27 basamak basamak yukarı tırmanmak ve can boğazdayken şifa/okuma aramak)'),
    ('lff', 'Sure %100 Kilidi', 'İltifâf, Eltâf ve Lefîf (Sure 75 Kıyâmet kilidi + 3 geçiş: 17:104, 75:29, 78:16 birbirine dolanıp sarılmak ve sık sarmaşık/toplu hâlde gelmek)'),
    ('bnn', 'Sure %100 Kilidi', 'Benân (Sure 75 Kıyâmet kilidi + 2 geçiş: 8:12, 75:4 en ince detay olarak parmak uçları)'),
    ('Hrk', 'Sure %100 Kilidi', 'Tuharrik (Sure 75 Kıyâmet kilidi: 75:16 vahyi aceleyle yakalamak için dilini kıpırdatıp hareket ettirmek)'),
    ('mTw', 'Sure %100 Kilidi', 'Yetemattâ (Sure 75 Kıyâmet kilidi: 75:33 kibirle gerinip çalım satarak salına salına yürümek)'),
    ('trq', 'Sure %100 Kilidi', 'Terâkî (Sure 75 Kıyâmet son kilidi: 75:26 canın boğazdaki köprücük kemiklerine dayanma anı)'),

    ('zlf', 'Sure %100 Kilidi', 'Zülfâ, Zülef ve Üzlifet (Sure 81 Tekvîr kilidi | 1M + 10 geçiş: 11:114, 26:64, 26:90, 34:37, 38:25, 38:40, 39:3, 50:31, 67:27, 81:13 yaklaştırmak, yakınlık derecesi ve gecenin gündüze yakın saatleri)'),
    ('Afq', 'Sure %100 Kilidi', 'Ufuk ve Âfâk (Sure 81 Tekvîr kilidi + 3 geçiş: 41:53, 53:7, 81:23 gök ile yerin birleştiği açık çevre ufku ve dış evren sınırları)'),
    ('kwr', 'Sure %100 Kilidi', 'Tekvîr (Sure 81 Tekvîr kilidi | 1M + 3 geçiş: 39:5, 81:1 sarık sarar gibi geceyi gündüze dolamak ve güneşin ışığını dürüp sarmak)'),
    ('sjr', 'Sure %100 Kilidi', 'Tescîr ve Mescûr (Sure 81 Tekvîr kilidi + 3 geçiş: 40:72, 52:6, 81:6 alevlendirip tutuşturmak ve denizlerin taşıp tutuşması)'),
    ('ETl', 'Sure %100 Kilidi', 'Ta\'tîl ve Muattala (Sure 81 Tekvîr kilidi + 2 geçiş: 22:45, 81:4 bakımsız, sahipsiz ve işlevsiz bırakılmak)'),
    ('Dnn', 'Sure %100 Kilidi', 'Danîn (Sure 81 Tekvîr kilidi: 81:24 gayb bilgisi konusunda cimrilik edip bilgiyi saklayan)'),
    ('EsEs', 'Sure %100 Kilidi', 'As\'ase (Sure 81 Tekvîr kilidi: 81:17 gecenin karanlığını toplayıp sırtını dönerek çekilmesi/yönelmesi)'),
    ('k$T', 'Sure %100 Kilidi', 'Kuşitat (Sure 81 Tekvîr kilidi: 81:11 göğün bir deri/örtü gibi sıyrılıp açılması)'),
    ('kdr', 'Sure %100 Kilidi', 'İnkederet (Sure 81 Tekvîr kilidi | 1M: 81:2 yıldızların parlaklığını yitirip bulanarak dökülmesi)'),
    ('kns', 'Sure %100 Kilidi', 'Künnes (Sure 81 Tekvîr kilidi | 1M: 81:16 yörüngesinde akıp yuvasına/gözden uzağa çekilen gök cisimleri)'),
    ('wAd', 'Sure %100 Kilidi', 'Mev\'ûde (Sure 81 Tekvîr kilidi: 81:8 diri diri toprağa gömülerek öldürülen kız çocuğu)'),
    ('wH$', 'Sure %100 Kilidi', 'Vuhûş (Sure 81 Tekvîr son kilidi: 81:5 yabanıl hayvanların bir araya toplanması — Sure 80–114 [son 35 sure] kesintisiz %100 & 50. tam kilitli sure!)'),

    # Kategori 2: Kalan Tüm 10 Geçişli Çekirdek Kökler (7 Kök -> ≥10 geçişli açık kök = 0 & 900 KÖK!)
    ('Twl', 'Yüksek Frekanslı Çekirdek', 'Tûl, Tavl ve Tâle (10 geçiş: 4:25, 9:86, 17:37, 20:86, 21:44, 28:45, 40:3, 57:16, 73:7, 76:26 süre/boy uzunluğu ve el genişliği/imkân)'),
    ('dmw', 'Yüksek Frekanslı Çekirdek', 'Dem ve Dimâ\' (10 geçiş: 2:30, 2:84, 2:173, 5:3, 6:145, 7:133, 12:18, 16:115, 22:37 canın taşıyıcısı akan kan ve kan dökme yasağı)'),
    ('jbr', 'Yüksek Frekanslı Çekirdek', 'Cebbâr (10 geçiş | 1M + 2F: 5:22, 11:59, 14:15, 19:14, 19:32, 26:130, 28:19, 40:35, 50:45, 59:23 kırığı zorla onaran ve başkasına boyun eğdiren zorba/mutlak ıslah edici güç)'),
    ('jdd', 'Yüksek Frekanslı Çekirdek', 'Cedîd, Cüded ve Cedd (10 geçiş: 13:5, 17:49, 17:98, 32:10, 34:7, 35:16, 35:27, 50:15, 72:3 yeni/taze yaratılış, dağlardaki yol çizgileri ve yüce azamet)'),
    ('zyl', 'Yüksek Frekanslı Çekirdek', 'Lâ Yezâlü ve Tezeyyele (10 geçiş: 2:217, 5:13, 11:118, 13:31, 15:60, 21:15, 35:41, 48:25 ayrılıp kopmak ve olumsuzuyla kesintisiz sürmek)'),
    ('mlw', 'Yüksek Frekanslı Çekirdek', 'İmlâ ve Meliyy (10 geçiş: 2:282, 3:178, 7:183, 13:32, 19:46, 22:44, 22:48, 25:5, 47:25, 68:45 ipi/süreyi uzatmak, mühlet vermek ve yazdırıp dikte ettirmek)'),
    ('mAy', 'Yüksek Frekanslı Çekirdek', 'Mi\'e ve Mi\'eteyn (10 geçiş | 1M: 2:259, 2:261, 8:65, 8:66, 18:25, 24:2, 37:147 yüz sayısı ve iki yüz — ≥10 geçişli açık kök 0 & 900. Kök!)'),
]


def generate_etap_3m():
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
    for etap_rank, (bw, category, rationale) in enumerate(ETAP_3M_ROOTS_SPEC, 1):
        if bw in seen_bw:
            raise ValueError(f"ETAP_3M_ROOTS_SPEC içinde mükerrer kök: {bw}")
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
            'etap_3m_rank': etap_rank,
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
        'package': 'Faz 1 - Etap 3M (+5 Sure %100 Tam Kilidi [Sure 83, 80, 74, 75, 81 -> 50 Sure & Son 35 Sure Kesintisiz %100] ve Kalan Tüm 10 Geçişli Çekirdek Kökler — 50 Kök -> 900 Kök)',
        'target_count': len(items),
        'locked_count': locked_cnt,
        'total_tokens_in_package': total_tokens,
        'total_corpus_tokens': total_corpus_tokens,
        'current_coverage_pct': round(current_cov_pct, 2),
        'target_coverage_pct': round(target_cov_pct, 2),
        'etap_3m_roots': items,
    }
    json_path = os.path.join(DATA_DIR, 'etap_3m_key_roots.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    pct_now_str = f"{current_cov_pct:.2f}".replace('.', ',')
    pct_target_str = f"{target_cov_pct:.2f}".replace('.', ',')
    md_lines = [
        "# ETAP 3M: +5 SURE %100 TAM KİLİDİ (50 SURE / SON 35 SURE KESİNTİSİZ %100) VE KALAN TÜM 10 GEÇİŞLİ ÇEKİRDEK KÖKLER (50 KÖK -> 900 KÖK)",
        "## Tabula Rasa Mesânî Çözümleme Sistemi (v3.0 — Faz 1 900 Kök, %96,32 Kapsam & 50 Tam Kilitli Sure Zırhı)",
        "",
        "> [!IMPORTANT]",
        f"> **HEDEF KAPSAM:** İlk 850 mühürlü kökten (`%95,94`) sonra, `5` sureyi daha `%100` kilitleyen `43` kök (Sure 83 Mutaffifîn, 80 Abese, 74 Müddessir, 75 Kıyâmet, 81 Tekvîr → **50 tam kilitli sure**; Sure 60–66 ve Sure 80–114 [son 35 sure] kesintisiz `%100` kilit) ve kalan tüm `10` geçişli çekirdek kökler (`7` kök — `≥10` geçişli açık kök `0`!) olmak üzere **50 kök** ({total_tokens} geçiş) mühürlenerek toplam sözlük **900 kilitli köke (`%{pct_target_str}` kümülatif kök kapsamı, tüm Kur'an kelimelerinin `%97,62`'si)** ulaştırılır.",
        f"> **Etap 3M İçinde Şu Ana Kadar Mühürlenen:** {locked_cnt} / {len(items)} Kök (Toplam Mühürlü: {len(locked_roots)} Kök | Güncel Kapsam: %{pct_now_str})",
        "",
        "| Etap Sıra | Kategori | Genel Sıra | Kök (Arapça) | Kök (Latin) | Geçiş | Ayet | Örnek | Stratejik Önemi / Kavram Durumu | Durum |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |",
    ]
    for it in items:
        badge = "✅ **MÜHÜRLÜ**" if it['is_locked'] else "⏳ *Bekliyor*"
        desc = it['concept_label'] if it['is_locked'] else it['rationale']
        md_lines.append(
            f"| {it['etap_3m_rank']} | {it['category']} | {it['global_rank']} | "
            f"`{it['root_arabic']}` | `{it['root_latin']}` | **{it['frequency']}** | {it['unique_ayahs']} | "
            f"{it['sample_ayah']} | {desc} | {badge} |"
        )
    md_lines.append("")

    md_path = os.path.join(DATA_DIR, 'ETAP_3M_KAVRAM.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(
        f"Etap 3M JSON üretildi: {json_path} "
        f"({locked_cnt}/{len(items)} mühürlü | Güncel: %{pct_now_str} -> Hedef 900 kök: %{pct_target_str})"
    )
    print(f"Etap 3M Markdown üretildi: {md_path}")


if __name__ == '__main__':
    generate_etap_3m()
