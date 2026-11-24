# -*- coding: utf-8 -*-
"""
Web XHigh -> PC Antigravity Tek Komutluk Mühürleme ve Sıradaki Kök Brifing Motoru.

Kullanım:
  1) Sıradaki mühürsüz kök(ler) için kesin korpus brifingi üret:
       python tools/seal_from_web.py --next-brief
       python tools/seal_from_web.py --next-brief 2

  2) Web XHigh'tan gelen [WEB SEAL JSON] paketini denetle, mühürle, doğrula (ve isteğe bağlı GitHub'a gönder):
       python tools/seal_from_web.py --seal data/web_inbox.json
       python tools/seal_from_web.py --seal data/web_inbox.json --push
"""

import argparse
import importlib
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quran_analyzer import DATA_DIR, QuranCorpus
from tabula_rasa import find_forbidden_terms


STAGE_CONFIGS = [
    ('İkinci 100', 'second_100_roots.json', 'second_100_roots', 'second_100_rank'),
    ('Etap 2.5', 'etap_2_5_key_roots.json', 'etap_2_5_roots', 'etap_2_5_rank'),
    ('Etap 3', 'etap_3_key_roots.json', 'etap_3_roots', 'etap_3_rank'),
    ('Etap 3C', 'etap_3c_key_roots.json', 'etap_3c_roots', 'etap_3c_rank'),
    ('Etap 3D', 'etap_3d_key_roots.json', 'etap_3d_roots', 'etap_3d_rank'),
    ('Etap 3E', 'etap_3e_key_roots.json', 'etap_3e_roots', 'etap_3e_rank'),
    ('Etap 3F', 'etap_3f_key_roots.json', 'etap_3f_roots', 'etap_3f_rank'),
    ('Etap 3G', 'etap_3g_key_roots.json', 'etap_3g_roots', 'etap_3g_rank'),
]


def load_all_stage_roots():
    by_ar = {}
    active_stage = None
    for label, fname, list_key, rank_key in STAGE_CONFIGS:
        path = os.path.join(DATA_DIR, fname)
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        items = data.get(list_key, [])
        for r in items:
            by_ar[r['root_arabic']] = r
        unlocked = [r for r in items if not r.get('is_locked')]
        if unlocked and active_stage is None:
            active_stage = (label, unlocked, rank_key)
    return by_ar, active_stage


def print_next_brief(count=1):
    _, active_stage = load_all_stage_roots()
    if not active_stage:
        print("Tüm aktif etaplar (600 kök) mühürlendi! Yeni Faz 1 etabı tanımlanabilir.")
        return

    etap_label, roots, rank_key = active_stage
    corpus = QuranCorpus()
    targets = roots[:count]
    print(f"=== {etap_label.upper()} SIRADAKİ KÖK BRİFİNGİ ===")
    for item in targets:
        ar = item['root_arabic']
        lat = item['root_latin']
        bw = item['buckwalter']
        etap = item[rank_key]
        grank = item['global_rank']
        tier_info = f" [{item['tier']} - {item['category']}]" if 'tier' in item else ""
        wg = corpus.get_root_word_groups(bw)
        suras = len(set(s for (s, a, w), _ in wg))
        stats = corpus.get_root_stats(bw)

        lem_counts = Counter()
        lem_ayahs = defaultdict(list)
        pos_counts = Counter()
        for (s, a, w), segs in wg:
            stem = next((sg for sg in segs if 'STEM' in sg['features']), segs[0])
            lem = stem['lem']
            lem_counts[lem] += 1
            ref = f"{s}:{a}"
            if ref not in lem_ayahs[lem]:
                lem_ayahs[lem].append(ref)
            pos_counts[stem['tag']] += 1

        lem_summary = ", ".join(f"{l} ({c})" for l, c in lem_counts.most_common())
        vf_summary = ", ".join(f"{k}:{v}" for k, v in sorted(stats['verb_forms'].items())) if stats['verb_forms'] else "0 fiil"
        print(
            f"{etap_label} Sıra {etap}{tier_info} / Genel Sıra {grank}: {ar} ({lat} / Buckwalter: {bw})\n"
            f"- Kesin Korpus: {stats['total_occurrences']} geçiş / {stats['unique_ayahs_count']} ayet / {suras} sure\n"
            f"- Lemmalar: {lem_summary}\n"
            f"- Fiil Babları: {vf_summary} | POS: {dict(pos_counts)}\n"
            f"- Örnek Lemmalara Göre Ayetler: "
            + " | ".join(f"{l}: {','.join(lem_ayahs[l][:6])}" for l, _ in lem_counts.most_common(6))
        )


def seal_package(json_path, do_push=False):
    with open(json_path, 'r', encoding='utf-8') as f:
        raw = f.read().strip()

    # Markdown ```json ... ``` bloğu içinde yapıştırıldıysa temizle
    if raw.startswith("```"):
        lines = raw.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines).strip()

    pkg = json.loads(raw)
    delta = pkg.get('locked_roots_delta')
    if not delta:
        raise ValueError("JSON içinde 'locked_roots_delta' anahtarı bulunamadı.")

    specs_in = pkg.get('kavram_build_spec', {})

    # 1. Tabula Rasa yasaklı terim denetimi
    forbidden = find_forbidden_terms(json.dumps(pkg, ensure_ascii=False))
    if forbidden:
        raise ValueError(f"TABULA RASA İHLALİ! JSON içinde yasaklı geleneksel terim tespit edildi: {sorted(set(forbidden))}")

    idx_by_ar, _ = load_all_stage_roots()
    corpus = QuranCorpus()

    locked_path = os.path.join(DATA_DIR, 'locked_roots.json')
    with open(locked_path, 'r', encoding='utf-8') as f:
        locked_json = json.load(f)

    specs_path = os.path.join(DATA_DIR, 'root_build_specs.json')
    if os.path.exists(specs_path):
        with open(specs_path, 'r', encoding='utf-8') as f:
            all_specs = json.load(f)
    else:
        all_specs = {}

    sealed_roots = []
    for ar_root, entry in delta.items():
        idx_info = idx_by_ar.get(ar_root)
        if 'rank' not in entry or entry['rank'] is None:
            if idx_info:
                entry['rank'] = idx_info['global_rank']
            else:
                raise ValueError(f"{ar_root} için 'rank' alanı eksik ve aktif indekslerde bulunamadı.")

        spec = specs_in.get(ar_root)
        if spec:
            if 'buckwalter' not in spec and idx_info:
                spec['buckwalter'] = idx_info['buckwalter']
            all_specs[ar_root] = spec
            bw = spec['buckwalter']
        elif idx_info:
            bw = idx_info['buckwalter']
        else:
            raise ValueError(f"{ar_root} için 'kavram_build_spec' eksik.")

        # Korpus frekans doğrulaması
        stats = corpus.get_root_stats(bw)
        expected_prefix = f"{stats['total_occurrences']} geçiş / {stats['unique_ayahs_count']} ayet"
        mr = entry.setdefault('morphology_and_rasm', {})
        af = mr.get('approx_frequency', '')
        if not af.startswith(expected_prefix):
            print(f"[UYARI] {ar_root} approx_frequency korpusla hizalandı: '{af}' -> '{expected_prefix} (referans amaçlı)'")
            mr['approx_frequency'] = f"{expected_prefix} (referans amaçlı)"

        locked_json['locked_roots'][ar_root] = entry
        sealed_roots.append((ar_root, entry['rank'], entry.get('root_latin', '')))

    # Çift yönlü Mesânî simetrisini otomatik senkronize et
    locked_map = locked_json['locked_roots']
    for r_key, r_val in list(locked_map.items()):
        for target in r_val.get('mesani_opposite', {}).get('roots', []):
            if target in locked_map:
                t_roots = locked_map[target].setdefault('mesani_opposite', {}).setdefault('roots', [])
                if r_key not in t_roots:
                    t_roots.append(r_key)

    total_locked = len(locked_json['locked_roots'])
    e3g_locked = max(0, total_locked - 550)
    locked_json['phase'] = (
        f"Faz 1 - Top 100 (100/100) + 5 Çekirdek + İkinci 100 (100/100) + Etap 2.5 (16/16) "
        f"+ Etap 3 (131/131) + Etap 3C (48/48) + Etap 3D (50/50) + Etap 3E (50/50) "
        f"+ Etap 3F (50/50) + Etap 3G ({e3g_locked}/50 — Toplam {total_locked} Kök Mühürlü)"
    )

    with open(locked_path, 'w', encoding='utf-8') as f:
        json.dump(locked_json, f, ensure_ascii=False, indent=2)
    with open(specs_path, 'w', encoding='utf-8') as f:
        json.dump(all_specs, f, ensure_ascii=False, indent=2)

    # Dinamik spec'leri yükleyip kavram dosyasını üret
    import build_kavramlar
    importlib.reload(build_kavramlar)
    for ar_root, _, _ in sealed_roots:
        build_kavramlar.build_root(ar_root, corpus=corpus, locked_roots_data=locked_json)

    # İndeks ve özet betiklerini çalıştır
    tools_dir = os.path.dirname(os.path.abspath(__file__))
    for script in [
        'generate_top_100.py',
        'generate_second_100.py',
        'generate_etap_2_5.py',
        'generate_etap_3.py',
        'generate_etap_3c.py',
        'generate_etap_3d.py',
        'generate_etap_3e.py',
        'generate_etap_3f.py',
        'generate_etap_3g.py',
        'generate_compact_roots.py',
        'verify_project.py',
    ]:
        subprocess.run([sys.executable, os.path.join(tools_dir, script)], check=True)

    if do_push:
        repo_root = os.path.dirname(tools_dir)
        names = ", ".join(f"Sira {rk} {ar}" for ar, rk, _ in sealed_roots)
        env = os.environ.copy()
        env['GIT_TERMINAL_PROMPT'] = '0'
        subprocess.run(['git', 'add', 'data/', 'tools/', 'README.md'], cwd=repo_root, check=True, env=env)
        subprocess.run(
            ['git', 'commit', '-m', f"Etap 3 muhurleme: {names} ({total_locked} kok sifir hata)"],
            cwd=repo_root, check=True, env=env
        )
        subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_root, check=True, env=env)
        print("GitHub push tamamlandı!")

    print("\n--- SIRADAKİ KÖK ---")
    print_next_brief(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--next-brief', nargs='?', const=1, type=int, help='Sıradaki N mühürsüz kökün korpus brifingini yazdır')
    parser.add_argument('--seal', type=str, help='Web XHigh JSON paket dosya yolu')
    parser.add_argument('--push', action='store_true', help='Sıfır hata sonrası GitHub commit+push yap')
    args = parser.parse_args()

    if args.seal:
        seal_package(args.seal, do_push=args.push)
    else:
        print_next_brief(args.next_brief or 1)
