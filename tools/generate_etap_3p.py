# -*- coding: utf-8 -*-
"""
Etap 3P Kilit Kavramlar (En Yüksek Frekanslı Kalan 50 Kök: Kalan Tüm 24 Adet 6 Geçişli Kök [≥6 Açık Kök = 0!]
ve En Yüksek Etkili 26 Adet 5 Geçişli Kök [8 Açık Mesânî + 18 Yaygın 5/5 Kök] — 50 Kök -> 1.050 Kilitli Kök!)
Tabula Rasa Mesânî Çözümleme Sistemi (v3.0)

İlk 1.000 mühürlü kökten sonra (%97,23 köklü / %98,21 tüm kelime kapsamı),
Kur'an'da kalan tüm 6 geçişli kökleri (24 kök / 144 geçiş -> ≥6 geçişli açık kök = 0!)
ve kalan 5 geçişli köklerin en yüksek öncelikli 26'sını (8'i mevcut kilitli köklerle doğrudan açık Mesânî bağı kuran,
18'i 5 farklı ayette geçen çekirdek kök — 130 geçiş) olmak üzere toplam 50 kökü (274 geçiş) indeksler;
sözlüğü 1.050 kilitli kök eşiğine (%97,78 köklü / %98,57 tüm Kur'an kelimesi kapsamı) ulaştırır.
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
ETAP_3P_ROOTS_SPEC = [
    # Kategori 1: Kalan Tüm 6 Geçişli Çekirdek Kökler (24 Kök / 144 Geçiş -> ≥6 geçişli açık kök = 0!)
    ('grm', '6 Geçişli Çekirdek', 'Ğarâm, Mağrem, Ğârimîn ve Muğramûn (6/6 + Açık Mesânî [أ-ج-ر]: yakayı bırakmayan borç yükü, zarar tazmini ve yapışkan azap)'),
    ('xlT', '6 Geçişli Çekirdek', 'Halt, İhtilât, Muhâlata ve Huletâ (6/6 + Açık Mesânî [ح-ص-ل]: birbirine karışıp kaynaşmak, ortaklık ve yetim malına karışmak)'),
    ('*rA', '6 Geçişli Çekirdek', 'Zerae (6/6: yeryüzünde ve yaratılışta çok sayıda canlıyı üretip yaymak)'),
    ('DwA', '6 Geçişli Çekirdek', 'Edâe ve Dıyâ (6/6: özünden güçlü ışık saçan parlak aydınlık, güneşin ışıması ve ateşin parlaması)'),
    ('Dyf', '6 Geçişli Çekirdek', 'Dayf ve Yudayyifû (6/6: konuk/misafir ve ağırlayıp konukseverlik göstermek)'),
    ('HSd', '6 Geçişli Çekirdek', 'Hasad, Hasâd ve Hasîd (6/6: olgunlaşan ekini biçmek ve biçilip kökü kazınmış yurtlar)'),
    ('Hss', '6 Geçişli Çekirdek', 'Ehasse, Tahussû, Tehassesû ve Hasîs (6/6: duyuyla kesin sezmek, kökten biçmek, iz aramak ve hafif hışırtı)'),
    ('bkm', '6 Geçişli Çekirdek', 'Bükm ve Ebkem (6/6: konuşma ve hakkı dile getirme yetisinden yoksun dilsizlik)'),
    ('dAb', '6 Geçişli Çekirdek', 'De\'b, Deeb ve Dâibeyn (6/6: kesintisiz sürüp giden alışkanlık, düzenli yörünge akışı ve azimli çalışma)'),
    ('drs', '6 Geçişli Çekirdek', 'Derese ve Dirâse (6/6: metni tekrar tekrar okuyup inceleyerek derinlemesine öğrenmek)'),
    ('fzE', '6 Geçişli Çekirdek', 'Fezia, Feza\' ve Füzzia (6/6: ansızın kaplayan şiddetli dehşet/telaş ve kalplerden o telaşın giderilmesi)'),
    ('kZm', '6 Geçişli Çekirdek', 'Kâzımîn, Kazîm ve Mekzûm (6/6: dolu tulumun ağzını bağlar gibi öfkeyi ve kederi içine hapsedip yutmak)'),
    ('khf', '6 Geçişli Çekirdek', 'Kehf (6/6: dağ içindeki geniş sığınak mağara — Ashâb-ı Kehf kıssası)'),
    ('krr', '6 Geçişli Çekirdek', 'Kerre (6/6: geri dönüp bir kez daha hamle yapmak / ikinci bir dönüş fırsatı)'),
    ('lHd', '6 Geçişli Çekirdek', 'Yülhidûn, İlhâd ve Mültehad (6/6: doğru eksenden yana eğilip sapmak ve sığınılacak yan kovuk)'),
    ('mrj', '6 Geçişli Çekirdek', 'Merece, Mercân, Merîc ve Mâric (6/6: salıverip kavuşturmak, karmaşık/karışık iş, dumansız yalın alev ve mercan)'),
    ('qmS', '6 Geçişli Çekirdek', 'Kamîs (6/6: bedeni saran gömlek — Yusuf kıssasının üç dönüm noktası kanıtı)'),
    ('Syd', '6 Geçişli Çekirdek', 'Sayd ve İstedû (6/5: av ve avlanmak — ihram yasakları ve deniz avı helalliği)'),
    ('sdd', '6 Geçişli Çekirdek', 'Sedd ve Sedîd (6/5: geçidi kapatan sağlam set ve gediksiz, dosdoğru söz)'),
    ('wTA', '6 Geçişli Çekirdek', 'Vat\', Yetaû, Yuvâtiû ve Mevtı\' (6/5: ayakla sağlamca basıp çiğnemek, gece kıyamında uyumlu basış ve sayı denkliği)'),
    ('zjr', '6 Geçişli Çekirdek', 'Zecr, Zecre, Zâcirât ve Müzdecer (6/5: sert uyarıyla engelleyip caydırmak, tek bir haykırış ve sürüp yönlendirenler)'),
    ('klb', '6 Geçişli Çekirdek', 'Kelb ve Mükellibîn (6/4: köpek ve av köpeklerini/yırtıcıları eğitip salmak)'),
    ('nzg', '6 Geçişli Çekirdek', 'Nezeğa ve Nezg (6/4: dürtükleyip kışkırtarak araya bozgun ve fitne sokmak)'),
    ('myl', '6 Geçişli Çekirdek', 'Meyl, Yemîlu ve Meyle (6/3: bir tarafa eğilip yönelmek, adaletten sapmak ve toplu saldırı — ≥6 geçişli açık kök = 0!)'),

    # Kategori 2: Açık Mesânî Bağı Olan 5 Geçişli Kökler (8 Kök / 40 Geçiş)
    ('*mm', '5 Geçişli Mesânî', 'Mezmûm ve Zimme (5/5 + Açık Mesânî [ح-م-د]: kınanıp yerilmiş olmak ve bozulmaması gereken güvence/ahd)'),
    ('mDy', '5 Geçişli Mesânî', 'Madâ ve Mudiyy (5/5 + Açık Mesânî [ر-ج-ع]: ileriye doğru geçip gitmek ve örnek/sünnetin gelip geçmesi)'),
    ('myd', '5 Geçişli Mesânî', 'Temîde ve Mâide (5/5 + Açık Mesânî [ر-س-و]: yerin sağa sola çalkalanıp sallanması ve üzerinde rızık sunulan sofra)'),
    ('qSw', '5 Geçişli Mesânî', 'Aksâ, Kusvâ ve Kasiyy (5/5 + Açık Mesânî [د-ن-و]: en uzak uç nokta, vadinin uzak yamacı ve ıssız uzak mekân)'),
    ('rfq', '5 Geçişli Mesânî', 'Refîk, Mirfak, Merâfik ve Mürtefak (5/5 + Açık Mesânî [ب-ط-ش]: yumuşak yoldaşlık, kolaylık, dirsekler ve dayanılıp dinlenilen yer)'),
    ('Twy', '5 Geçişli Mesânî', 'Tayy, Natvî, Matviyyât ve Tuvâ (5/4 + Açık Mesânî [ك-ت-ب]: göğü yazılı tomar gibi dürüp katlamak ve Tuvâ vadisi)'),
    ('xTw', '5 Geçişli Mesânî', 'Hutuvât (5/4 + Açık Mesânî [س-ل-م]: iki ayak arası adım ve şeytanın adım izlerine uymamak)'),
    ('$Tr', '5 Geçişli Mesânî', 'Şatr (5/3 + Açık Mesânî [ح-ي-ث]: belirli bir yön, taraf ve Mescid-i Harâm istikameti)'),

    # Kategori 3: En Yaygın (5/5 Ayet) 5 Geçişli Çekirdek Kökler (18 Kök / 90 Geçiş -> 1.050 Kök!)
    ('$hb', '5 Geçişli Çekirdek', 'Şihâb ve Şühüb (5/5: kor halinde parlayan alevli ateş parçası ve delici parlak ışık)'),
    ('Asf', '5 Geçişli Çekirdek', 'Esif, Esef ve Âsefû (5/5: derin kederle karışık yoğun öfke, üzüntü ve öfkelendirmek)'),
    ('ESb', '5 Geçişli Çekirdek', 'Usbe ve Asîb (5/5: birbirine sıkıca kenetlenmiş güçlü topluluk ve çetin, sıkışık gün)'),
    ('Evw', '5 Geçişli Çekirdek', 'Ta\'sev (5/5: yeryüzünde aşırıya kaçıp azgınca bozgunculuk yaymak)'),
    ('HSb', '5 Geçişli Çekirdek', 'Hâsıb ve Hasab (5/5: çakıl taşları savuran yıkıcı fırtına ve ateşe atılan tutuşturucu yakıt)'),
    ('HrS', '5 Geçişli Çekirdek', 'Harîs, Ahras ve Harastüm (5/5: bir şeye aşırı düşkünlük ve yoğun istek/özen göstermek)'),
    ('Hwt', '5 Geçişli Çekirdek', 'Hût (5/5: büyük balık — Yunus kıssası ve iki denizin kavuştuğu yerdeki balık)'),
    ('HyS', '5 Geçişli Çekirdek', 'Mahîs (5/5: yana sapıp kurtulacak kaçış yeri ve sığınak)'),
    ('Snm', '5 Geçişli Çekirdek', 'Esnâm (5/5: yontulup dikilen ve Allah\'tan başka yakarılan suretler/putlar)'),
    ('hll', '5 Geçişli Çekirdek', 'Ühille ve Ehille (5/5: kesimde Allah\'tan başkası adına ses yükseltmek ve vakit ölçüsü yeni aylar/hilaller)'),
    ('hzz', '5 Geçişli Çekirdek', 'İhtezzet ve Hüzzî (5/5: suyla canlanan toprağın harekete geçip kıpırdaması ve hurma gövdesini silkelemek)'),
    ('jvm', '5 Geçişli Çekirdek', 'Câsimîn (5/5: büyük sarsıntı ve çığlıkla yurtlarında dizüstü çöküp hareketsiz kalmak)'),
    ('kml', '5 Geçişli Çekirdek', 'Ekmeltü, Kâmile ve Kâmileyn (5/5: eksiği kalmaksızın bütünlük içinde tamamlanıp kemale ermek)'),
    ('ksw', '5 Geçişli Çekirdek', 'Kesâ ve Kisve (5/5: kemiklere et giydirmek, giyim-kuşam ihtiyacını karşılamak ve örtüyle giydirmek)'),
    ('lzm', '5 Geçişli Çekirdek', 'Elzeme ve Lizâm (5/5: ayrılmaz biçimde boyna/kişiye bağlayıp yapıştırmak ve kaçınılmaz kalıcı karşılık)'),
    ('mSr', '5 Geçişli Çekirdek', 'Mısr (5/5: sınırları belirli yerleşik şehir/ülke ve Mısır diyarı)'),
    ('mrd', '5 Geçişli Çekirdek', 'Merîd, Mârid, Meredû ve Mümerred (5/5: pürüzsüzce sıyrılıp azgınlıkta direten inatçı isyankâr ve pürüzsüz yüksek saray)'),
    ('nkl', '5 Geçişli Çekirdek', 'Nekâl, Tenkîl ve Enkâl (5/5: başkalarına caydırıcı ders olan ağır ceza ve bağlayıcı ağır bukağılar — 1.050. KÖK!)'),
]


def generate_etap_3p():
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
    for etap_rank, (bw, category, rationale) in enumerate(ETAP_3P_ROOTS_SPEC, 1):
        if bw in seen_bw:
            raise ValueError(f"ETAP_3P_ROOTS_SPEC içinde mükerrer kök: {bw}")
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
            'etap_3p_rank': etap_rank,
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
        'package': 'Faz 1 - Etap 3P (En Yüksek Frekanslı Kalan 50 Kök: Kalan Tüm 24 Adet 6 Geçişli Kök [≥6 Açık = 0!] + 26 Adet 5 Geçişli Çekirdek Kök — 1.050 Kök!)',
        'target_count': len(items),
        'locked_count': locked_cnt,
        'total_tokens_in_package': total_tokens,
        'total_corpus_tokens': total_corpus_tokens,
        'current_coverage_pct': round(current_cov_pct, 2),
        'target_coverage_pct': round(target_cov_pct, 2),
        'etap_3p_roots': items,
    }
    json_path = os.path.join(DATA_DIR, 'etap_3p_key_roots.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    pct_now_str = f"{current_cov_pct:.2f}".replace('.', ',')
    pct_target_str = f"{target_cov_pct:.2f}".replace('.', ',')
    md_lines = [
        "# ETAP 3P: EN YÜKSEK FREKANSLI KALAN 50 KÖK (TÜM 6 GEÇİŞLİLER + 26 ADET 5 GEÇİŞLİ — 1.050 KÖK!)",
        "## Tabula Rasa Mesânî Çözümleme Sistemi (v3.0 — Faz 1 1.050 Kök, %97,78 Kapsam & ≥6 Açık Kök = 0!)",
        "",
        "> [!IMPORTANT]",
        f"> **HEDEF KAPSAM:** İlk 1.000 mühürlü kökten (`%97,23`) sonra, Kur'an'da kalan **tüm 6 geçişli kökler** (`24` kök / `144` geçiş → `≥6` açık kök `0`!) ile en yüksek öncelikli **`26` adet 5 geçişli kök** (`8` açık Mesânî bağı + `18` yaygın `5/5` ayet kökü = `130` geçiş) olmak üzere **50 kök** (`{total_tokens}` geçiş) mühürlenerek toplam sözlük **1.050 kilitli köke (`%{pct_target_str}` kümülatif kök kapsamı, tüm Kur'an kelimelerinin `%98,57`'si)** ulaştırılır.",
        f"> **Etap 3P İçinde Şu Ana Kadar Mühürlenen:** {locked_cnt} / {len(items)} Kök (Toplam Mühürlü: {len(locked_roots)} Kök | Güncel Kapsam: %{pct_now_str})",
        "",
        "| Etap Sıra | Kategori | Genel Sıra | Kök (Arapça) | Kök (Latin) | Geçiş | Ayet | Örnek | Stratejik Önemi / Kavram Durumu | Durum |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |",
    ]
    for it in items:
        badge = "✅ **MÜHÜRLÜ**" if it['is_locked'] else "⏳ *Bekliyor*"
        desc = it['concept_label'] if it['is_locked'] else it['rationale']
        md_lines.append(
            f"| {it['etap_3p_rank']} | {it['category']} | {it['global_rank']} | "
            f"`{it['root_arabic']}` | `{it['root_latin']}` | **{it['frequency']}** | {it['unique_ayahs']} | "
            f"{it['sample_ayah']} | {desc} | {badge} |"
        )
    md_lines.append("")

    md_path = os.path.join(DATA_DIR, 'ETAP_3P_KAVRAM.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(
        f"Etap 3P JSON üretildi: {json_path} "
        f"({locked_cnt}/{len(items)} mühürlü | Güncel: %{pct_now_str} -> Hedef 1050 kök: %{pct_target_str})"
    )
    print(f"Etap 3P Markdown üretildi: {md_path}")


if __name__ == '__main__':
    generate_etap_3p()
