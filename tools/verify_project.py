# -*- coding: utf-8 -*-
"""
Tabula Rasa Mesânî Çözümleme Sistemi - Sıfır Hata Doğrulama Motoru
PROMPT.md §9.3 kapsamında tüm JSON şemalarını, morfoloji sayımlarını,
Rasm-ı Osmânî kelime hizalamalarını ve Tabula Rasa temizliğini doğrular.
"""

import os
import re
import sys
import json
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quran_analyzer import DATA_DIR, QuranCorpus, extract_ayah_words, strip_tashkeel, load_verses, to_arabic_root
from tabula_rasa import find_forbidden_terms, purify_tabula_rasa
from build_kavramlar import ROOT_CONFIG

REQUIRED_LOCKED_KEYS = [
    'root_latin',
    'arabic',
    'rank',
    'morphology_and_rasm',
    'physical_core',
    'ibn_faris_asl',
    'dictionary_arbitration',
    'semitic_cognates',
    'mesani_opposite',
    'same_ayah_furuk',
    'anchor_ayahs',
    'unified_core_mechanism',
    'grammar_and_branch_rules',
    'derivatives',
]

REQUIRED_KAVRAM_KEYS = [
    'root',
    'root_latin',
    'concept_name',
    'rank',
    'total_occurrences',
    'unique_ayahs_count',
    'unified_core_mechanism',
    'physical_core',
    'dictionary_arbitration',
    'semitic_cognates',
    'mesani_opposite',
    'same_ayah_furuk',
    'anchor_ayahs',
    'grammar_and_branch_rules',
    'derivatives',
    'ayah_occurrences',
]


def verify_all():
    errors = []
    corpus = QuranCorpus()
    corpus_ar_roots = {to_arabic_root(bw): bw for bw in corpus.roots_map.keys()}

    # 1. Tüm 6.236 ayette kelime sayısı hizalamasını doğrula
    ayah_max_w = defaultdict(int)
    with open(corpus.morphology_file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.startswith('('):
                continue
            tab = line.find('\t')
            m = re.match(r'\((\d+):(\d+):(\d+):', line[:tab])
            if m:
                s, a, w = map(int, m.groups())
                if w > ayah_max_w[(s, a)]:
                    ayah_max_w[(s, a)] = w

    for (s, a), txt in corpus.ayahs_uthmani.items():
        words = extract_ayah_words(txt, s, a)
        if len(words) != ayah_max_w[(s, a)]:
            errors.append(f"Kelime hizalama hatası {s}:{a}: uthmani={len(words)}, corpus={ayah_max_w[(s, a)]}")

    # 2. Tüm 6.236 Türkçe ayette birebir eşleşme, mükerrer ayet ve Tabula Rasa arındırma kontrolü
    raw_tr = load_verses(os.path.join(DATA_DIR, 'quran-turkish.txt'))
    if len(raw_tr) != 6236:
        errors.append(f"Türkçe ayet sayısı 6236 değil: {len(raw_tr)}")
    prev_tr_ref = None
    prev_tr_txt = None
    for (s, a) in sorted(raw_tr.keys()):
        txt = raw_tr[(s, a)]
        if prev_tr_txt is not None and txt == prev_tr_txt:
            errors.append(f"Mükerrer/birleşik Türkçe ayet hatası ({prev_tr_ref[0]}:{prev_tr_ref[1]} == {s}:{a})")
        prev_tr_ref = (s, a)
        prev_tr_txt = txt
        hits = find_forbidden_terms(purify_tabula_rasa(txt))
        if hits:
            errors.append(f"Tabula Rasa kalıntısı ({s}:{a}): {hits}")

    # 3. locked_roots.json v3.0 şema, korpus, anakronizm, döngüsel terim ve Çift Yönlü Mesânî simetri kontrolü
    with open(os.path.join(DATA_DIR, 'locked_roots.json'), 'r', encoding='utf-8') as f:
        locked_json = json.load(f)
    locked_roots = locked_json.get('locked_roots', {})

    anachronism_re = re.compile(
        r'\b(?:fabrika ayarı|kalibrasyon|yazılım(?!lı)|donanım|kırmızı dur sinyali|yön sinyali|doğa sinyali|kozmik görevli\w*)\b',
        re.IGNORECASE | re.UNICODE,
    )
    circular_re = re.compile(
        r'\b(?:secde\w*|mescid\w*|rük[uû]\w*|tevhid\w*|fıtrat\w*|ahiret\w*|tevbe\w*|tövbe\w*|hidayet\w*|vesvese\w*|infak\w*|sal[aâ]t\w*|helal\w*|haram\w*)\b',
        re.IGNORECASE | re.UNICODE,
    )
    root_ref_re = re.compile(r'[\u0621-\u064a]-[\u0621-\u064a]-[\u0621-\u064a](?:-[\u0621-\u064a])?')

    for ar_root, entry in locked_roots.items():
        for k in REQUIRED_LOCKED_KEYS:
            if k not in entry:
                errors.append(f"locked_roots[{ar_root}] eksik anahtar: {k}")

        if entry.get('rank') is None:
            errors.append(f"locked_roots[{ar_root}] rank alanı boş (None)")

        entry_dump = json.dumps(entry, ensure_ascii=False)
        anach_hits = anachronism_re.findall(entry_dump)
        if anach_hits:
            errors.append(f"locked_roots[{ar_root}] 21. yüzyıl jargonu tespit edildi: {sorted(set(anach_hits))}")

        for fld in ('unified_core_mechanism', 'derivatives', 'physical_core'):
            fld_str = json.dumps(entry.get(fld, ''), ensure_ascii=False)
            if fld in ('unified_core_mechanism', 'derivatives'):
                f_hits = find_forbidden_terms(fld_str)
                if f_hits:
                    errors.append(f"locked_roots[{ar_root}].{fld} yasaklı geleneksel terim içeriyor: {sorted(set(f_hits))}")
            c_hits = circular_re.findall(fld_str.replace('İ', 'i').replace('I', 'ı').lower())
            if c_hits:
                errors.append(f"locked_roots[{ar_root}].{fld} döngüsel dinî terim içeriyor (PROMPT.md §4.6): {sorted(set(c_hits))}")

        # Çift Yönlü Mesânî Simetri Kilidi ve Kanonik Kök İmlası Kontrolü (A -> B varsa B -> A zorunlu)
        mo_roots = entry.get('mesani_opposite', {}).get('roots', [])
        mentioned_opps = set(root_ref_re.findall(json.dumps(mo_roots, ensure_ascii=False))) - {ar_root}
        for opp_root in sorted(mentioned_opps):
            if opp_root not in corpus_ar_roots:
                errors.append(f"Mesânî alanında standart dışı/geçersiz kök imlası: {ar_root} -> {opp_root}")
            if opp_root in locked_roots:
                opp_mo = json.dumps(locked_roots[opp_root].get('mesani_opposite', {}).get('roots', []), ensure_ascii=False)
                if ar_root not in opp_mo:
                    errors.append(f"Mesânî tek yönlü simetri ihlali: {ar_root} -> {opp_root} (tersi eksik)")

        fu_roots = entry.get('same_ayah_furuk', {}).get('paired_concepts', [])
        for fp_root in sorted(set(root_ref_re.findall(json.dumps(fu_roots, ensure_ascii=False))) - {ar_root}):
            if fp_root not in corpus_ar_roots:
                errors.append(f"Furûk alanında standart dışı/geçersiz kök imlası: {ar_root} -> {fp_root}")

        cfg = ROOT_CONFIG.get(ar_root)
        if not cfg:
            errors.append(f"ROOT_CONFIG içinde eksik kök: {ar_root}")
            continue

        bw = cfg['buckwalter']
        stats = corpus.get_root_stats(bw)
        approx_freq = entry.get('morphology_and_rasm', {}).get('approx_frequency', '')
        expected_prefix = f"{stats['total_occurrences']} geçiş / {stats['unique_ayahs_count']} ayet"
        if not approx_freq.startswith(expected_prefix):
            errors.append(
                f"locked_roots[{ar_root}] frekans uyumsuzluğu: '{approx_freq}' != '{expected_prefix}...'"
            )

        # Fiil babı gerçeği kontrolü (ör. أ-ل-ه içinde fiil yoksa Form I yazılmamalı)
        vf_str = " ".join(entry.get('morphology_and_rasm', {}).get('verb_forms_used', []))
        if not stats['verb_forms'] and 'Form I' in vf_str:
            errors.append(f"locked_roots[{ar_root}] fiil formu hatası: korpusta fiil yok ama '{vf_str}' yazılmış")

        # 4. data/kavramlar/<slug>.json kontrolü
        kavram_path = os.path.join(DATA_DIR, 'kavramlar', f"{cfg['slug']}.json")
        if not os.path.exists(kavram_path):
            errors.append(f"Eksik kavram dosyası: {kavram_path}")
            continue

        with open(kavram_path, 'r', encoding='utf-8') as kf:
            kd = json.load(kf)

        for k in REQUIRED_KAVRAM_KEYS:
            if k not in kd:
                errors.append(f"{cfg['slug']}.json eksik anahtar: {k}")

        occs = kd.get('ayah_occurrences', [])
        if kd.get('total_occurrences') != stats['total_occurrences'] or len(occs) != stats['total_occurrences']:
            errors.append(
                f"{cfg['slug']}.json toplam geçiş uyumsuz: json={len(occs)} / {kd.get('total_occurrences')}, corpus={stats['total_occurrences']}"
            )
        if kd.get('unique_ayahs_count') != stats['unique_ayahs_count']:
            errors.append(
                f"{cfg['slug']}.json ayet sayısı uyumsuz: json={kd.get('unique_ayahs_count')}, corpus={stats['unique_ayahs_count']}"
            )

        for occ in occs:
            s, a, w = occ['surah'], occ['ayah'], occ['word_position']
            expected_words = extract_ayah_words(corpus.ayahs_uthmani.get((s, a), ''), s, a)
            expected_word = expected_words[w - 1]
            if occ['target_word_uthmani'] != expected_word:
                errors.append(f"{cfg['slug']}.json {s}:{a} w={w} kelime uyumsuz: {occ['target_word_uthmani']} != {expected_word}")
            if occ['target_word_rasm'] != strip_tashkeel(expected_word):
                errors.append(f"{cfg['slug']}.json {s}:{a} w={w} rasm uyumsuz")
            if occ['target_word_literal_irab'] == 'Kavramın sentaktik / irablı konumu':
                errors.append(f"{cfg['slug']}.json {s}:{a} w={w} genel irab şablonuna düştü")

            for field in [
                'context_snippet_turkish_tabula_rasa',
                'ayah_text_turkish_tabula_rasa_full',
                'target_word_literal_irab',
                'contextual_meaning',
            ]:
                hits = find_forbidden_terms(occ.get(field, ''))
                if hits:
                    errors.append(f"{cfg['slug']}.json {s}:{a} {field} yasaklı terim içeriyor: {hits}")

    # 5. top_100_roots.json ve TOP_100_KAVRAM.md tutarlılığı
    with open(os.path.join(DATA_DIR, 'top_100_roots.json'), 'r', encoding='utf-8') as f:
        top100 = json.load(f)
    top100_locked = [r for r in top100['top_100_roots'] if r['is_locked']]
    expected_top100_locked = [r for r in top100['top_100_roots'] if r['root_arabic'] in locked_roots]
    if len(top100_locked) != len(expected_top100_locked) or top100['locked_in_top_100'] != len(expected_top100_locked):
        errors.append("top_100_roots.json mühür sayısı locked_roots.json ile uyumsuz")

    with open(os.path.join(DATA_DIR, 'TOP_100_KAVRAM.md'), 'r', encoding='utf-8') as f:
        md_text = f.read()
    expected_badge_line = f"**Şu Ana Kadar Mühürlenen Kökler (Faz 1):** {len(locked_roots)} Kök (Top 100 içinde: {len(expected_top100_locked)} Kök)"
    if expected_badge_line not in md_text:
        errors.append(f"TOP_100_KAVRAM.md özet satırı güncel değil: '{expected_badge_line}' bekleniyordu")

    # 6. second_100_roots.json ve SECOND_100_KAVRAM.md tutarlılığı
    second100_path = os.path.join(DATA_DIR, 'second_100_roots.json')
    if os.path.exists(second100_path):
        with open(second100_path, 'r', encoding='utf-8') as f:
            second100 = json.load(f)
        s2_locked = [r for r in second100['second_100_roots'] if r['is_locked']]
        expected_s2_locked = [r for r in second100['second_100_roots'] if r['root_arabic'] in locked_roots]
        if len(s2_locked) != len(expected_s2_locked) or second100['locked_in_second_100'] != len(expected_s2_locked):
            errors.append("second_100_roots.json mühür sayısı locked_roots.json ile uyumsuz")

        s2_md_path = os.path.join(DATA_DIR, 'SECOND_100_KAVRAM.md')
        if not os.path.exists(s2_md_path):
            errors.append(f"Eksik indeks dosyası: {s2_md_path}")
        else:
            with open(s2_md_path, 'r', encoding='utf-8') as f:
                s2_md_text = f.read()
            expected_s2_line = (
                f"**İkinci 100 İçinde Şu Ana Kadar Mühürlenen:** "
                f"{len(expected_s2_locked)} / 100 Kök (Toplam Mühürlü: {len(locked_roots)} Kök)"
            )
            if expected_s2_line not in s2_md_text:
                errors.append(f"SECOND_100_KAVRAM.md özet satırı güncel değil: '{expected_s2_line}' bekleniyordu")

    # 7. etap_2_5_key_roots.json ve ETAP_2_5_KAVRAM.md tutarlılığı
    etap25_path = os.path.join(DATA_DIR, 'etap_2_5_key_roots.json')
    if os.path.exists(etap25_path):
        with open(etap25_path, 'r', encoding='utf-8') as f:
            etap25 = json.load(f)
        e25_locked = [r for r in etap25['etap_2_5_roots'] if r['is_locked']]
        expected_e25_locked = [r for r in etap25['etap_2_5_roots'] if r['root_arabic'] in locked_roots]
        if len(e25_locked) != len(expected_e25_locked) or etap25['locked_count'] != len(expected_e25_locked):
            errors.append("etap_2_5_key_roots.json mühür sayısı locked_roots.json ile uyumsuz")

        e25_md_path = os.path.join(DATA_DIR, 'ETAP_2_5_KAVRAM.md')
        if not os.path.exists(e25_md_path):
            errors.append(f"Eksik indeks dosyası: {e25_md_path}")
        else:
            with open(e25_md_path, 'r', encoding='utf-8') as f:
                e25_md_text = f.read()
            expected_e25_line = (
                f"**Etap 2.5 İçinde Şu Ana Kadar Mühürlenen:** "
                f"{len(expected_e25_locked)} / {len(etap25['etap_2_5_roots'])} Kök "
                f"(Toplam Mühürlü: {len(locked_roots)} Kök)"
            )
            if expected_e25_line not in e25_md_text:
                errors.append(f"ETAP_2_5_KAVRAM.md özet satırı güncel değil: '{expected_e25_line}' bekleniyordu")

    # 8. etap_3_key_roots.json ve ETAP_3_KAVRAM.md tutarlılığı
    etap3_path = os.path.join(DATA_DIR, 'etap_3_key_roots.json')
    if os.path.exists(etap3_path):
        with open(etap3_path, 'r', encoding='utf-8') as f:
            etap3 = json.load(f)
        e3_locked = [r for r in etap3['etap_3_roots'] if r['is_locked']]
        expected_e3_locked = [r for r in etap3['etap_3_roots'] if r['root_arabic'] in locked_roots]
        if len(e3_locked) != len(expected_e3_locked) or etap3['locked_count'] != len(expected_e3_locked):
            errors.append("etap_3_key_roots.json mühür sayısı locked_roots.json ile uyumsuz")

        e3_md_path = os.path.join(DATA_DIR, 'ETAP_3_KAVRAM.md')
        if not os.path.exists(e3_md_path):
            errors.append(f"Eksik indeks dosyası: {e3_md_path}")
        else:
            with open(e3_md_path, 'r', encoding='utf-8') as f:
                e3_md_text = f.read()
            expected_e3_line = (
                f"**Etap 3 İçinde Şu Ana Kadar Mühürlenen:** "
                f"{len(expected_e3_locked)} / {len(etap3['etap_3_roots'])} Kök "
                f"(Toplam Mühürlü: {len(locked_roots)} Kök)"
            )
            if expected_e3_line not in e3_md_text:
                errors.append(f"ETAP_3_KAVRAM.md özet satırı güncel değil: '{expected_e3_line}' bekleniyordu")

    # 8b. etap_3c_key_roots.json ve ETAP_3C_KAVRAM.md tutarlılığı
    etap3c_path = os.path.join(DATA_DIR, 'etap_3c_key_roots.json')
    if os.path.exists(etap3c_path):
        with open(etap3c_path, 'r', encoding='utf-8') as f:
            etap3c = json.load(f)
        e3c_locked = [r for r in etap3c['etap_3c_roots'] if r['is_locked']]
        expected_e3c_locked = [r for r in etap3c['etap_3c_roots'] if r['root_arabic'] in locked_roots]
        if len(e3c_locked) != len(expected_e3c_locked) or etap3c['locked_count'] != len(expected_e3c_locked):
            errors.append("etap_3c_key_roots.json mühür sayısı locked_roots.json ile uyumsuz")

        e3c_md_path = os.path.join(DATA_DIR, 'ETAP_3C_KAVRAM.md')
        if not os.path.exists(e3c_md_path):
            errors.append(f"Eksik indeks dosyası: {e3c_md_path}")
        else:
            with open(e3c_md_path, 'r', encoding='utf-8') as f:
                e3c_md_text = f.read()
            expected_e3c_prefix = (
                f"**Etap 3C İçinde Şu Ana Kadar Mühürlenen:** "
                f"{len(expected_e3c_locked)} / {len(etap3c['etap_3c_roots'])} Kök "
                f"(Toplam Mühürlü: {len(locked_roots)} Kök"
            )
            if expected_e3c_prefix not in e3c_md_text:
                errors.append(f"ETAP_3C_KAVRAM.md özet satırı güncel değil: '{expected_e3c_prefix}...' bekleniyordu")

    # 8c. etap_3d_key_roots.json ve ETAP_3D_KAVRAM.md tutarlılığı
    etap3d_path = os.path.join(DATA_DIR, 'etap_3d_key_roots.json')
    if os.path.exists(etap3d_path):
        with open(etap3d_path, 'r', encoding='utf-8') as f:
            etap3d = json.load(f)
        e3d_locked = [r for r in etap3d['etap_3d_roots'] if r['is_locked']]
        expected_e3d_locked = [r for r in etap3d['etap_3d_roots'] if r['root_arabic'] in locked_roots]
        if len(e3d_locked) != len(expected_e3d_locked) or etap3d['locked_count'] != len(expected_e3d_locked):
            errors.append("etap_3d_key_roots.json mühür sayısı locked_roots.json ile uyumsuz")

        e3d_md_path = os.path.join(DATA_DIR, 'ETAP_3D_KAVRAM.md')
        if not os.path.exists(e3d_md_path):
            errors.append(f"Eksik indeks dosyası: {e3d_md_path}")
        else:
            with open(e3d_md_path, 'r', encoding='utf-8') as f:
                e3d_md_text = f.read()
            expected_e3d_prefix = (
                f"**Etap 3D İçinde Şu Ana Kadar Mühürlenen:** "
                f"{len(expected_e3d_locked)} / {len(etap3d['etap_3d_roots'])} Kök "
                f"(Toplam Mühürlü: {len(locked_roots)} Kök"
            )
            if expected_e3d_prefix not in e3d_md_text:
                errors.append(f"ETAP_3D_KAVRAM.md özet satırı güncel değil: '{expected_e3d_prefix}...' bekleniyordu")

    # 8d. etap_3e_key_roots.json ve ETAP_3E_KAVRAM.md tutarlılığı
    etap3e_path = os.path.join(DATA_DIR, 'etap_3e_key_roots.json')
    if os.path.exists(etap3e_path):
        with open(etap3e_path, 'r', encoding='utf-8') as f:
            etap3e = json.load(f)
        e3e_locked = [r for r in etap3e['etap_3e_roots'] if r['is_locked']]
        expected_e3e_locked = [r for r in etap3e['etap_3e_roots'] if r['root_arabic'] in locked_roots]
        if len(e3e_locked) != len(expected_e3e_locked) or etap3e['locked_count'] != len(expected_e3e_locked):
            errors.append("etap_3e_key_roots.json mühür sayısı locked_roots.json ile uyumsuz")

        e3e_md_path = os.path.join(DATA_DIR, 'ETAP_3E_KAVRAM.md')
        if not os.path.exists(e3e_md_path):
            errors.append(f"Eksik indeks dosyası: {e3e_md_path}")
        else:
            with open(e3e_md_path, 'r', encoding='utf-8') as f:
                e3e_md_text = f.read()
            expected_e3e_prefix = (
                f"**Etap 3E İçinde Şu Ana Kadar Mühürlenen:** "
                f"{len(expected_e3e_locked)} / {len(etap3e['etap_3e_roots'])} Kök "
                f"(Toplam Mühürlü: {len(locked_roots)} Kök"
            )
            if expected_e3e_prefix not in e3e_md_text:
                errors.append(f"ETAP_3E_KAVRAM.md özet satırı güncel değil: '{expected_e3e_prefix}...' bekleniyordu")

    # 8e. etap_3f_key_roots.json ve ETAP_3F_KAVRAM.md tutarlılığı
    etap3f_path = os.path.join(DATA_DIR, 'etap_3f_key_roots.json')
    if os.path.exists(etap3f_path):
        with open(etap3f_path, 'r', encoding='utf-8') as f:
            etap3f = json.load(f)
        e3f_locked = [r for r in etap3f['etap_3f_roots'] if r['is_locked']]
        expected_e3f_locked = [r for r in etap3f['etap_3f_roots'] if r['root_arabic'] in locked_roots]
        if len(e3f_locked) != len(expected_e3f_locked) or etap3f['locked_count'] != len(expected_e3f_locked):
            errors.append("etap_3f_key_roots.json mühür sayısı locked_roots.json ile uyumsuz")

        e3f_md_path = os.path.join(DATA_DIR, 'ETAP_3F_KAVRAM.md')
        if not os.path.exists(e3f_md_path):
            errors.append(f"Eksik indeks dosyası: {e3f_md_path}")
        else:
            with open(e3f_md_path, 'r', encoding='utf-8') as f:
                e3f_md_text = f.read()
            expected_e3f_prefix = (
                f"**Etap 3F İçinde Şu Ana Kadar Mühürlenen:** "
                f"{len(expected_e3f_locked)} / {len(etap3f['etap_3f_roots'])} Kök "
                f"(Toplam Mühürlü: {len(locked_roots)} Kök"
            )
            if expected_e3f_prefix not in e3f_md_text:
                errors.append(f"ETAP_3F_KAVRAM.md özet satırı güncel değil: '{expected_e3f_prefix}...' bekleniyordu")

    # 8f. etap_3g_key_roots.json ve ETAP_3G_KAVRAM.md tutarlılığı
    etap3g_path = os.path.join(DATA_DIR, 'etap_3g_key_roots.json')
    if os.path.exists(etap3g_path):
        with open(etap3g_path, 'r', encoding='utf-8') as f:
            etap3g = json.load(f)
        e3g_locked = [r for r in etap3g['etap_3g_roots'] if r['is_locked']]
        expected_e3g_locked = [r for r in etap3g['etap_3g_roots'] if r['root_arabic'] in locked_roots]
        if len(e3g_locked) != len(expected_e3g_locked) or etap3g['locked_count'] != len(expected_e3g_locked):
            errors.append("etap_3g_key_roots.json mühür sayısı locked_roots.json ile uyumsuz")

        e3g_md_path = os.path.join(DATA_DIR, 'ETAP_3G_KAVRAM.md')
        if not os.path.exists(e3g_md_path):
            errors.append(f"Eksik indeks dosyası: {e3g_md_path}")
        else:
            with open(e3g_md_path, 'r', encoding='utf-8') as f:
                e3g_md_text = f.read()
            expected_e3g_prefix = (
                f"**Etap 3G İçinde Şu Ana Kadar Mühürlenen:** "
                f"{len(expected_e3g_locked)} / {len(etap3g['etap_3g_roots'])} Kök "
                f"(Toplam Mühürlü: {len(locked_roots)} Kök"
            )
            if expected_e3g_prefix not in e3g_md_text:
                errors.append(f"ETAP_3G_KAVRAM.md özet satırı güncel değil: '{expected_e3g_prefix}...' bekleniyordu")

    # 8g. etap_3h_key_roots.json ve ETAP_3H_KAVRAM.md tutarlılığı
    etap3h_path = os.path.join(DATA_DIR, 'etap_3h_key_roots.json')
    if os.path.exists(etap3h_path):
        with open(etap3h_path, 'r', encoding='utf-8') as f:
            etap3h = json.load(f)
        e3h_locked = [r for r in etap3h['etap_3h_roots'] if r['is_locked']]
        expected_e3h_locked = [r for r in etap3h['etap_3h_roots'] if r['root_arabic'] in locked_roots]
        if len(e3h_locked) != len(expected_e3h_locked) or etap3h['locked_count'] != len(expected_e3h_locked):
            errors.append("etap_3h_key_roots.json mühür sayısı locked_roots.json ile uyumsuz")

        e3h_md_path = os.path.join(DATA_DIR, 'ETAP_3H_KAVRAM.md')
        if not os.path.exists(e3h_md_path):
            errors.append(f"Eksik indeks dosyası: {e3h_md_path}")
        else:
            with open(e3h_md_path, 'r', encoding='utf-8') as f:
                e3h_md_text = f.read()
            expected_e3h_prefix = (
                f"**Etap 3H İçinde Şu Ana Kadar Mühürlenen:** "
                f"{len(expected_e3h_locked)} / {len(etap3h['etap_3h_roots'])} Kök "
                f"(Toplam Mühürlü: {len(locked_roots)} Kök"
            )
            if expected_e3h_prefix not in e3h_md_text:
                errors.append(f"ETAP_3H_KAVRAM.md özet satırı güncel değil: '{expected_e3h_prefix}...' bekleniyordu")

    # 8h. etap_3i_key_roots.json ve ETAP_3I_KAVRAM.md tutarlılığı
    etap3i_path = os.path.join(DATA_DIR, 'etap_3i_key_roots.json')
    if os.path.exists(etap3i_path):
        with open(etap3i_path, 'r', encoding='utf-8') as f:
            etap3i = json.load(f)
        e3i_locked = [r for r in etap3i['etap_3i_roots'] if r['is_locked']]
        expected_e3i_locked = [r for r in etap3i['etap_3i_roots'] if r['root_arabic'] in locked_roots]
        if len(e3i_locked) != len(expected_e3i_locked) or etap3i['locked_count'] != len(expected_e3i_locked):
            errors.append("etap_3i_key_roots.json mühür sayısı locked_roots.json ile uyumsuz")

        e3i_md_path = os.path.join(DATA_DIR, 'ETAP_3I_KAVRAM.md')
        if not os.path.exists(e3i_md_path):
            errors.append(f"Eksik indeks dosyası: {e3i_md_path}")
        else:
            with open(e3i_md_path, 'r', encoding='utf-8') as f:
                e3i_md_text = f.read()
            expected_e3i_prefix = (
                f"**Etap 3I İçinde Şu Ana Kadar Mühürlenen:** "
                f"{len(expected_e3i_locked)} / {len(etap3i['etap_3i_roots'])} Kök "
                f"(Toplam Mühürlü: {len(locked_roots)} Kök"
            )
            if expected_e3i_prefix not in e3i_md_text:
                errors.append(f"ETAP_3I_KAVRAM.md özet satırı güncel değil: '{expected_e3i_prefix}...' bekleniyordu")

    # 8i. etap_3j_key_roots.json ve ETAP_3J_KAVRAM.md tutarlılığı
    etap3j_path = os.path.join(DATA_DIR, 'etap_3j_key_roots.json')
    if os.path.exists(etap3j_path):
        with open(etap3j_path, 'r', encoding='utf-8') as f:
            etap3j = json.load(f)
        e3j_locked = [r for r in etap3j['etap_3j_roots'] if r['is_locked']]
        expected_e3j_locked = [r for r in etap3j['etap_3j_roots'] if r['root_arabic'] in locked_roots]
        if len(e3j_locked) != len(expected_e3j_locked) or etap3j['locked_count'] != len(expected_e3j_locked):
            errors.append("etap_3j_key_roots.json mühür sayısı locked_roots.json ile uyumsuz")

        e3j_md_path = os.path.join(DATA_DIR, 'ETAP_3J_KAVRAM.md')
        if not os.path.exists(e3j_md_path):
            errors.append(f"Eksik indeks dosyası: {e3j_md_path}")
        else:
            with open(e3j_md_path, 'r', encoding='utf-8') as f:
                e3j_md_text = f.read()
            expected_e3j_prefix = (
                f"**Etap 3J İçinde Şu Ana Kadar Mühürlenen:** "
                f"{len(expected_e3j_locked)} / {len(etap3j['etap_3j_roots'])} Kök "
                f"(Toplam Mühürlü: {len(locked_roots)} Kök"
            )
            if expected_e3j_prefix not in e3j_md_text:
                errors.append(f"ETAP_3J_KAVRAM.md özet satırı güncel değil: '{expected_e3j_prefix}...' bekleniyordu")

    # 8j. etap_3k_key_roots.json ve ETAP_3K_KAVRAM.md tutarlılığı
    etap3k_path = os.path.join(DATA_DIR, 'etap_3k_key_roots.json')
    if os.path.exists(etap3k_path):
        with open(etap3k_path, 'r', encoding='utf-8') as f:
            etap3k = json.load(f)
        e3k_locked = [r for r in etap3k['etap_3k_roots'] if r['is_locked']]
        expected_e3k_locked = [r for r in etap3k['etap_3k_roots'] if r['root_arabic'] in locked_roots]
        if len(e3k_locked) != len(expected_e3k_locked) or etap3k['locked_count'] != len(expected_e3k_locked):
            errors.append("etap_3k_key_roots.json mühür sayısı locked_roots.json ile uyumsuz")

        e3k_md_path = os.path.join(DATA_DIR, 'ETAP_3K_KAVRAM.md')
        if not os.path.exists(e3k_md_path):
            errors.append(f"Eksik indeks dosyası: {e3k_md_path}")
        else:
            with open(e3k_md_path, 'r', encoding='utf-8') as f:
                e3k_md_text = f.read()
            expected_e3k_prefix = (
                f"**Etap 3K İçinde Şu Ana Kadar Mühürlenen:** "
                f"{len(expected_e3k_locked)} / {len(etap3k['etap_3k_roots'])} Kök "
                f"(Toplam Mühürlü: {len(locked_roots)} Kök"
            )
            if expected_e3k_prefix not in e3k_md_text:
                errors.append(f"ETAP_3K_KAVRAM.md özet satırı güncel değil: '{expected_e3k_prefix}...' bekleniyordu")

    # 8k. etap_3l_key_roots.json ve ETAP_3L_KAVRAM.md tutarlılığı
    etap3l_path = os.path.join(DATA_DIR, 'etap_3l_key_roots.json')
    if os.path.exists(etap3l_path):
        with open(etap3l_path, 'r', encoding='utf-8') as f:
            etap3l = json.load(f)
        e3l_locked = [r for r in etap3l['etap_3l_roots'] if r['is_locked']]
        expected_e3l_locked = [r for r in etap3l['etap_3l_roots'] if r['root_arabic'] in locked_roots]
        if len(e3l_locked) != len(expected_e3l_locked) or etap3l['locked_count'] != len(expected_e3l_locked):
            errors.append("etap_3l_key_roots.json mühür sayısı locked_roots.json ile uyumsuz")

        e3l_md_path = os.path.join(DATA_DIR, 'ETAP_3L_KAVRAM.md')
        if not os.path.exists(e3l_md_path):
            errors.append(f"Eksik indeks dosyası: {e3l_md_path}")
        else:
            with open(e3l_md_path, 'r', encoding='utf-8') as f:
                e3l_md_text = f.read()
            expected_e3l_prefix = (
                f"**Etap 3L İçinde Şu Ana Kadar Mühürlenen:** "
                f"{len(expected_e3l_locked)} / {len(etap3l['etap_3l_roots'])} Kök "
                f"(Toplam Mühürlü: {len(locked_roots)} Kök"
            )
            if expected_e3l_prefix not in e3l_md_text:
                errors.append(f"ETAP_3L_KAVRAM.md özet satırı güncel değil: '{expected_e3l_prefix}...' bekleniyordu")

    # 8l. etap_3m_key_roots.json ve ETAP_3M_KAVRAM.md tutarlılığı
    etap3m_path = os.path.join(DATA_DIR, 'etap_3m_key_roots.json')
    if os.path.exists(etap3m_path):
        with open(etap3m_path, 'r', encoding='utf-8') as f:
            etap3m = json.load(f)
        e3m_locked = [r for r in etap3m['etap_3m_roots'] if r['is_locked']]
        expected_e3m_locked = [r for r in etap3m['etap_3m_roots'] if r['root_arabic'] in locked_roots]
        if len(e3m_locked) != len(expected_e3m_locked) or etap3m['locked_count'] != len(expected_e3m_locked):
            errors.append("etap_3m_key_roots.json mühür sayısı locked_roots.json ile uyumsuz")

        e3m_md_path = os.path.join(DATA_DIR, 'ETAP_3M_KAVRAM.md')
        if not os.path.exists(e3m_md_path):
            errors.append(f"Eksik indeks dosyası: {e3m_md_path}")
        else:
            with open(e3m_md_path, 'r', encoding='utf-8') as f:
                e3m_md_text = f.read()
            expected_e3m_prefix = (
                f"**Etap 3M İçinde Şu Ana Kadar Mühürlenen:** "
                f"{len(expected_e3m_locked)} / {len(etap3m['etap_3m_roots'])} Kök "
                f"(Toplam Mühürlü: {len(locked_roots)} Kök"
            )
            if expected_e3m_prefix not in e3m_md_text:
                errors.append(f"ETAP_3M_KAVRAM.md özet satırı güncel değil: '{expected_e3m_prefix}...' bekleniyordu")

    # 8m. etap_3n_key_roots.json ve ETAP_3N_KAVRAM.md tutarlılığı
    etap3n_path = os.path.join(DATA_DIR, 'etap_3n_key_roots.json')
    if os.path.exists(etap3n_path):
        with open(etap3n_path, 'r', encoding='utf-8') as f:
            etap3n = json.load(f)
        e3n_locked = [r for r in etap3n['etap_3n_roots'] if r['is_locked']]
        expected_e3n_locked = [r for r in etap3n['etap_3n_roots'] if r['root_arabic'] in locked_roots]
        if len(e3n_locked) != len(expected_e3n_locked) or etap3n['locked_count'] != len(expected_e3n_locked):
            errors.append("etap_3n_key_roots.json mühür sayısı locked_roots.json ile uyumsuz")

        e3n_md_path = os.path.join(DATA_DIR, 'ETAP_3N_KAVRAM.md')
        if not os.path.exists(e3n_md_path):
            errors.append(f"Eksik indeks dosyası: {e3n_md_path}")
        else:
            with open(e3n_md_path, 'r', encoding='utf-8') as f:
                e3n_md_text = f.read()
            expected_e3n_prefix = (
                f"**Etap 3N İçinde Şu Ana Kadar Mühürlenen:** "
                f"{len(expected_e3n_locked)} / {len(etap3n['etap_3n_roots'])} Kök "
                f"(Toplam Mühürlü: {len(locked_roots)} Kök"
            )
            if expected_e3n_prefix not in e3n_md_text:
                errors.append(f"ETAP_3N_KAVRAM.md özet satırı güncel değil: '{expected_e3n_prefix}...' bekleniyordu")

    # 8n. etap_3o_key_roots.json ve ETAP_3O_KAVRAM.md tutarlılığı
    etap3o_path = os.path.join(DATA_DIR, 'etap_3o_key_roots.json')
    if os.path.exists(etap3o_path):
        with open(etap3o_path, 'r', encoding='utf-8') as f:
            etap3o = json.load(f)
        e3o_locked = [r for r in etap3o['etap_3o_roots'] if r['is_locked']]
        expected_e3o_locked = [r for r in etap3o['etap_3o_roots'] if r['root_arabic'] in locked_roots]
        if len(e3o_locked) != len(expected_e3o_locked) or etap3o['locked_count'] != len(expected_e3o_locked):
            errors.append("etap_3o_key_roots.json mühür sayısı locked_roots.json ile uyumsuz")

        e3o_md_path = os.path.join(DATA_DIR, 'ETAP_3O_KAVRAM.md')
        if not os.path.exists(e3o_md_path):
            errors.append(f"Eksik indeks dosyası: {e3o_md_path}")
        else:
            with open(e3o_md_path, 'r', encoding='utf-8') as f:
                e3o_md_text = f.read()
            expected_e3o_prefix = (
                f"**Etap 3O İçinde Şu Ana Kadar Mühürlenen:** "
                f"{len(expected_e3o_locked)} / {len(etap3o['etap_3o_roots'])} Kök "
                f"(Toplam Mühürlü: {len(locked_roots)} Kök"
            )
            if expected_e3o_prefix not in e3o_md_text:
                errors.append(f"ETAP_3O_KAVRAM.md özet satırı güncel değil: '{expected_e3o_prefix}...' bekleniyordu")

    # 8o. etap_3p_key_roots.json ve ETAP_3P_KAVRAM.md tutarlılığı
    etap3p_path = os.path.join(DATA_DIR, 'etap_3p_key_roots.json')
    if os.path.exists(etap3p_path):
        with open(etap3p_path, 'r', encoding='utf-8') as f:
            etap3p = json.load(f)
        e3p_locked = [r for r in etap3p['etap_3p_roots'] if r['is_locked']]
        expected_e3p_locked = [r for r in etap3p['etap_3p_roots'] if r['root_arabic'] in locked_roots]
        if len(e3p_locked) != len(expected_e3p_locked) or etap3p['locked_count'] != len(expected_e3p_locked):
            errors.append("etap_3p_key_roots.json mühür sayısı locked_roots.json ile uyumsuz")

        e3p_md_path = os.path.join(DATA_DIR, 'ETAP_3P_KAVRAM.md')
        if not os.path.exists(e3p_md_path):
            errors.append(f"Eksik indeks dosyası: {e3p_md_path}")
        else:
            with open(e3p_md_path, 'r', encoding='utf-8') as f:
                e3p_md_text = f.read()
            expected_e3p_prefix = (
                f"**Etap 3P İçinde Şu Ana Kadar Mühürlenen:** "
                f"{len(expected_e3p_locked)} / {len(etap3p['etap_3p_roots'])} Kök "
                f"(Toplam Mühürlü: {len(locked_roots)} Kök"
            )
            if expected_e3p_prefix not in e3p_md_text:
                errors.append(f"ETAP_3P_KAVRAM.md özet satırı güncel değil: '{expected_e3p_prefix}...' bekleniyordu")

    # 9. particles_and_prepositions.json Tabula Rasa ve JSON bütünlüğü
    particles_path = os.path.join(DATA_DIR, 'particles_and_prepositions.json')
    if os.path.exists(particles_path):
        with open(particles_path, 'r', encoding='utf-8') as f:
            particles_data = json.load(f)
        for sec_name in ('prepositions_harf_i_cer', 'logical_and_structural_particles', 'rootless_core_concepts_in_corpus'):
            sec = particles_data.get(sec_name, {})
            for k_item, v_item in sec.items():
                p_hits = find_forbidden_terms(json.dumps(v_item, ensure_ascii=False))
                if p_hits:
                    errors.append(f"particles_and_prepositions.json[{sec_name}][{k_item}] yasaklı terim içeriyor: {sorted(set(p_hits))}")

    if errors:
        print(f"DOĞRULAMA BAŞARISIZ! Toplam {len(errors)} hata bulundu:")
        for err in errors[:30]:
            print("  -", err)
        return 1

    print(
        f"SIFIR HATA DOĞRULANDI! 6236 ayet hizalaması, {len(locked_roots)} kilitli kök v3.0 şeması, "
        f"tüm kavram JSON dosyaları, Edat/Köksüz haritası ve Top 100 / İkinci 100 / Etap 2.5 / Etap 3 / Etap 3C / Etap 3D / Etap 3E / Etap 3F / Etap 3G / Etap 3H / Etap 3I / Etap 3J / Etap 3K / Etap 3L / Etap 3M / Etap 3N / Etap 3O / Etap 3P indeksleri %100 tutarlı ve Tabula Rasa arınmış."
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(verify_all())
