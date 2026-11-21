# -*- coding: utf-8 -*-
"""
Etap 2.5 Kilit Kavramlar (Top 200 Dışında Kalan Omurga Kökler) İndeks Üreticisi
Tabula Rasa Mesânî Çözümleme Sistemi (v3.0)

Frekans sırası 204'ün altında kaldığı için Top 200'e giremeyen, ancak Faz 2 ayet
çözümlemesi için hayati olan 16 kilit kavramı (`ث-ن-ي [Mesânî]`, `أ-ث-م`, `ع-ه-د`,
`ل-ع-ن`, `ج-ه-د`, `ذ-ن-ب`, `و-ث-ق`, `ح-ج-ج`, `ق-س-م`, `ب-ر-ر`, `ط-ه-ر`, `ف-ط-ر`,
`خ-ش-ع`, `ص-و-م`, `ش-ر-ع`, `ن-س-خ`) indeksler.
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_kavramlar import ROOT_CONFIG
from quran_analyzer import DATA_DIR, to_arabic_root, to_latin_root

ETAP_2_5_BUCKWALTER = [
    ('vny', 'Mesânî sisteminin kendi kökü (çiftleme, karşılıklı eşleştirme, ikiye katlama)'),
    ('Avm', 'İsm (ağır kusur / Furûk: Zenb ve Cünâh farkı)'),
    ('Ehd', 'Ahid (bağlayıcı sözleşme ve taahhüt)'),
    ('lEn', 'La\'net (koruma ve esenlik alanından uzaklaştırma)'),
    ('jhd', 'Cehd / Cihâd (var gücüyle çabalama ve direnç emeği)'),
    ('*nb', 'Zenb (iz bırakan hata/suç / Furûk: İsm farkı)'),
    ('wvq', 'Mîsâk / Vesâk (sağlam bağla düğümleme ve kopmaz sözleşme)'),
    ('Hjj', 'Hacc / Hüccet (kanıtla yönelme, delil sunma ve büyük yöneliş toplanması)'),
    ('qsm', 'Kasem / Kısmet (paylaştırma ve bağlayıcı and / Furûk: Ahid ve Half farkı)'),
    ('brr', 'Birr / Berr (genişlik, dürüstlük ve kapsamlı iyilik)'),
    ('Thr', 'Tahâret / Tathîr (kirden arınma / Furûk: Zekât farkı)'),
    ('fTr', 'Fıtrat / Fâtır (ilk kez yarma, özgün yaratılış yapısı)'),
    ('x$E', 'Huşû (alçalıp yatışma, içsel saygı ve dinginlik)'),
    ('Swm', 'Savm / Sıyâm (tutma, durma, öz denetim ve sakınma)'),
    ('$rE', 'Şer\' / Şerîat (suya inen açık yol, açık hukuk güzergâhı)'),
    ('nsx', 'Nesh / İstinsâh (izini silip aktarma, kayıt çıkarma ve yürürlük değişimi)'),
]


def generate_etap_2_5():
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

    items = []
    for etap_rank, (bw, rationale) in enumerate(ETAP_2_5_BUCKWALTER, 1):
        ar_root = to_arabic_root(bw)
        is_locked = ar_root in locked_roots
        top_lemmas = [lem for lem, _ in roots_lemmas[bw].most_common(4)]
        concept_desc = (
            ROOT_CONFIG[ar_root]['concept_name']
            if (is_locked and ar_root in ROOT_CONFIG)
            else f"Analiz Bekliyor ({', '.join(top_lemmas)})"
        )
        items.append({
            'etap_2_5_rank': etap_rank,
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

    locked_cnt = sum(1 for i in items if i['is_locked'])
    total_tokens = sum(i['frequency'] for i in items)

    out_json = {
        'package': 'Faz 1 - Etap 2.5 (Top 200 Dışında Kalan 16 Kilit Kavram)',
        'target_count': len(items),
        'locked_count': locked_cnt,
        'total_tokens_in_package': total_tokens,
        'etap_2_5_roots': items,
    }
    json_path = os.path.join(DATA_DIR, 'etap_2_5_key_roots.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    md_lines = [
        "# ETAP 2.5: TOP 200 DIŞINDA KALAN 16 KİLİT KAVRAM HARİTASI",
        "## Tabula Rasa Mesânî Çözümleme Sistemi (v3.0 — Faz 2 Öncesi Kapsam Tamamlama)",
        "",
        "> [!IMPORTANT]",
        f"> **HEDEF KAPSAM:** İlk 205 kök (`100` Top 100 + `5` Çekirdek + `100` İkinci 100) mühürlendikten sonra, frekansı 49'un altında kaldığı için listeye giremeyen ancak Faz 2 ayet çözümlemesi için omurga niteliğindeki **16 kilit kavram** ({total_tokens} geçiş) ve köksüz edat/harf-i cer haritası (`data/EDAT_VE_HARFICER_HARITASI.md`) bu etapta tamamlanır.",
        f"> **Etap 2.5 İçinde Şu Ana Kadar Mühürlenen:** {locked_cnt} / {len(items)} Kök (Toplam Mühürlü: {len(locked_roots)} Kök)",
        "",
        "| Etap Sıra | Genel Sıra | Kök (Arapça) | Kök (Latin) | Geçiş | Ayet | Örnek Ayet | Stratejik Önemi / Kavram Durumu | Durum |",
        "| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |",
    ]
    for it in items:
        badge = "✅ **MÜHÜRLÜ**" if it['is_locked'] else "⏳ *Bekliyor*"
        desc = it['concept_label'] if it['is_locked'] else f"{it['rationale']} — *{it['concept_label']}*"
        md_lines.append(
            f"| {it['etap_2_5_rank']} | {it['global_rank']} | `{it['root_arabic']}` | `{it['root_latin']}` | "
            f"**{it['frequency']}** | {it['unique_ayahs']} | {it['sample_ayah']} | {desc} | {badge} |"
        )
    md_lines.append("")

    md_path = os.path.join(DATA_DIR, 'ETAP_2_5_KAVRAM.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(f"Etap 2.5 JSON üretildi: {json_path} ({locked_cnt}/{len(items)} mühürlü)")
    print(f"Etap 2.5 Markdown üretildi: {md_path}")


if __name__ == '__main__':
    generate_etap_2_5()
