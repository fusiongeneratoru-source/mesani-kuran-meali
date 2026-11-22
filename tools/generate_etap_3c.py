# -*- coding: utf-8 -*-
"""
Etap 3C Kilit Kavramlar (Son Mayın Temizliği, Hukuk-Ritüel-Kısa Sure Kilitleri
ve Açık Mesânî Zırhı — 48 Kök -> 400 Kilitli Kök) İndeks Üreticisi
Tabula Rasa Mesânî Çözümleme Sistemi (v3.0)

İlk 352 mühürlü kökten sonra (%83,08 kapsam), meal aşamasına (Faz 2) geçmeden önce
ceza-aile-ibadet hukuku, kısa sure kilitleri ve en çok açık Mesânî referansı taşıyan
48 kritik kökü indeksler ve toplam kilitli sözlüğü 400 köke tamamlar.
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
ETAP_3C_ROOTS_SPEC = [
    # Kategori 1: Hukuk, Ceza, Esir ve Ekonomi Düğümleri (10 kök: 3C-1 & 3C-2)
    ('qTE', 'Hukuk ve Ceza', 'Kat\' (5:38 hırsızlıkta el kesme / 12:31 çizme / 2:27 bağ ve ilişki koparma tek çekirdeği)'),
    ('srq', 'Hukuk ve Ceza', 'Serika ve Sârik (5:38 hırsızlık suçu ve 12:70-81 Yûsuf kıssasındaki hukuk çıpası)'),
    ('zny', 'Hukuk ve Ceza', 'Zinâ (24:2-3, 17:32 evlilik dışı cinsel ihlal, toplumsal sınır ve iftira koruma dengesi)'),
    ('jld', 'Hukuk ve Ceza', 'Cild ve Celde (24:2 kırbaç/deriye vurma cezası ve 41:20-22 derilerin tanıklığı tek kökte)'),
    ('rjm', 'Hukuk ve Ceza', 'Recm ve Racîm (taşlayıp kovma, 18:22 desteksiz zanla atma [رَجْمًۢا بِٱلْغَيْبِ] — Kur\'an\'da zina cezası değil!)'),
    ('mnn', 'Hukuk ve Ceza', 'Menn ve Memnûn (47:4 savaş esirini karşılıksız salıverme, 2:264 başa kakma yasağı ve kesintisiz lütuf)'),
    ('fdy', 'Hukuk ve Ceza', 'Fidye ve İftidâ (2:184 oruç fidyesi, 47:4 esir fidyesi ve 37:107 İbrâhîm kıssasındaki büyük kurtuluş bedeli)'),
    ('Eqd', 'Hukuk ve Ceza', 'Akd ve Ukûd (5:1 bağlayıcı sözleşmeler, 2:235-237 nikâh düğümü ve 113:4 düğümler tek çekirdekte)'),
    ('sHt', 'Hukuk ve Ceza', 'Suht (5:42, 5:62-63 kökünden kazıyıp tüketen haram kazanç, rüşvet ve hukuksuz sömürü)'),
    ('qrD', 'Hukuk ve Ceza', 'Karz-ı Hasen (18:17 makas gibi kesip geçme somut çıpası + toplum yararına karşılıksız dayanışma ödüncü)'),

    # Kategori 2: Aile, Mahremiyet ve Toplumsal İlişkiler (10 kök: 3C-3 & 3C-4)
    ('HyD', 'Aile ve Mahremiyet', 'Mahîd (2:222 pislik değil geçici rahatsızlık [أَذًى] ve 65:4 bekleme süresi hukuku)'),
    ('brj', 'Aile ve Mahremiyet', 'Teberrüc ve Bürûc (24:60, 33:33 gösterişli sergilenme vs gökteki yüksek kuleler/burçlar tek fizikte)'),
    ('gDD', 'Aile ve Mahremiyet', 'Gadd (24:30-31 erkek-kadın eşit bakış kısması ve 31:19 sesi alçaltıp kibar konuşma)'),
    ('jyb', 'Aile ve Mahremiyet', 'Ceyb ve Cüyûb (24:31 yaka/göğüs açıklığı + 27:12, 28:32 Mûsâ\'nın elini koynuna sokması çıpası)'),
    ('wEZ', 'Aile ve Mahremiyet', 'Va\'z ve Mev\'iza (4:34 ilk aşama öğüt + Kur\'an\'ın gönülleri yumuşatan uyarısı — 4:34 kilidini tamamlar)'),
    ('msk', 'Aile ve Mahremiyet', 'İmsâk (2:229-231 boşanmada iyilikle tutma, 35:2 rahmeti tutan yok — 3 açık Mesânî referansı!)'),
    ('srH', 'Aile ve Mahremiyet', 'Tesrîh (2:229, 2:231, 33:28, 33:49 boşanmada incitmeden güzellikle salıverme ve 16:6 sürüyü salma)'),
    ('rDE', 'Aile ve Mahremiyet', 'Radâa (2:233 iki yıl emzirme hakkı ve anne ücreti, 4:23 süt akrabalığı, 65:6 boşanma sonrası emzirme)'),
    ('$qq', 'Aile ve Mahremiyet', 'Şikâk ve Şakk (4:35 aile içi hakemli geçimsizlik çözümü, hizip yarılması ve toprağın yarılması)'),
    ('kfl', 'Aile ve Mahremiyet', 'Kefâlet ve Kifl (3:37 Meryem\'in himayesi, 4:85 iyi-kötü aracılık payı, 57:28 çift pay ve Zülkifl)'),

    # Kategori 3: İbadet, Ritüel ve Teoloji Düğümleri (10 kök: 3C-5 & 3C-6)
    ('gsl', 'İbadet ve Teoloji', 'Gasl (5:6 abdest yıkama ayeti, 4:43 boy abdesti, 38:42 soğuk yıkanma suyu ve 69:36 gıslîn)'),
    ('msH', 'İbadet ve Teoloji', 'Mesh (5:6 başı ve ayakları sıvazlama, 4:43 teyemmüm ve 38:33 Süleymân\'ın atlarını sıvazlaması)'),
    ('rhb', 'İbadet ve Teoloji', 'Rahb ve Ruhbâniyye (57:27 sonradan uydurulan ruhbanlık, 9:31 rahipler, 8:60 terör değil caydırıcılık)'),
    ('bdE', 'İbadet ve Teoloji', 'Bedî\' ve İbtidâ\' (2:117 benzersiz yaratış, 46:9 ilk elçi değilim, 57:27 ruhbanlık bid\'ati)'),
    ('ysr', 'İbadet ve Teoloji', 'Yüsr ve Meysir (94:5-6 kolaylık, 54:17 Kur\'an\'ın kolaylığı + 2:219/5:90 emeksiz kolay kazanç/kumar!)'),
    ('nSb', 'İbadet ve Teoloji', 'Nasîb, Ensâb ve Nasab (5:3,90 dikili put taşları, hak/miras payı ve 94:7 yeni işe dikilip emek verme)'),
    ('wzr', 'İbadet ve Teoloji', 'Vizr ve Vezîr (kimsenin başkasının yükünü taşımaması yasası, 20:29 yük ortağı yardımcı, 47:4 savaş yükü)'),
    ('skr', 'İbadet ve Teoloji', 'Sekr ve Seker (4:43 zihin bulanıkken salâta yaklaşmama, 15:15 göz bağlanması, 16:67 hurma/üzüm ürünü)'),
    ('qSr', 'İbadet ve Teoloji', 'Kasr ve Maksûrât (4:101 tehlikede salâtı kısaltma, 55:72 maksûrât eşler ve sağlam köşkler)'),
    ('*bH', 'İbadet ve Teoloji', 'Zebh (37:102-107 İbrâhîm\'in rüyası ve insan kurbanını reddeden büyük fidye, 2:67-71 inek kesimi)'),

    # Kategori 4: Kısa Sure Kilitleri, Zihin/Etik ve 113-114 Düğümleri (10 kök: 3C-7 & 3C-8)
    ('Hrj', 'Zihin, Etik ve Mesânî', 'Harac (22:78, 5:6, 4:65, 33:37-38 dinde darlık ve baskı yokluğu ilkesi — göğsün daralması çıpası)'),
    ('bht', 'Zihin, Etik ve Mesânî', 'Bühtân (2:258 şaşırıp donakalma somut çıpası + masumu şoke eden ağır iftira — İfk/Zûr/Kezib Furûku)'),
    ('njs', 'Kısa Sure ve Ritüel', 'Necs (9:28 tek geçiş: bedensel/ırksal değil, ortak koşmadan doğan inançsal-ahlaki kirlilik)'),
    ('nHr', 'Kısa Sure ve Ritüel', 'Nahr (108:2 tek geçiş: Kevser suresinde dik durup yönelme / kurban paylaşımı filolojik hakemliği)'),
    ('mEn', 'Kısa Sure ve Ritüel', 'Mâûn (107:7 tek geçiş: en temel komşuluk yardımı ve toplumsal dayanışmayı engelleme eleştirisi)'),
    ('nfv', 'Kısa Sure ve Ritüel', 'Nefs / Neffâsât (113:4 tek geçiş: düğümlere üfleyerek bağları ve anlaşmaları zehirleyen gizli fitne)'),
    ('Hqb', 'İbadet ve Teoloji', 'Hukub ve Ahkâb (18:60 uzun çağlar + 78:23 sonsuzluk değil uzun dönemler/çağlar boyu kalış!)'),
    ('lgw', 'Zihin, Etik ve Mesânî', 'Lağv (2:225 kasıtsız söz, 23:3/25:72 anlamsız boş sözden onurla yüz çevirme ve 41:26 gürültü çıkarma)'),
    ('lhw', 'Zihin, Etik ve Mesânî', 'Lehv (asıl amaçtan koparan oyalanma, 31:6 boş söz ticareti ve 62:11 ticaret-eğlenceye dağılma)'),
    ('lEb', 'Zihin, Etik ve Mesânî', 'Laib (ciddiyetsiz oyun — lehv vs laib aynı ayet içi Furûku: 6:32, 29:64, 47:36, 57:20)'),

    # Kategori 5: En Çok Açık Mesânî Referansı Taşıyan 8 Çekirdek Kök (3C-9 & 3C-10 -> 400 KÖK!)
    ('Ejl', 'Açık Mesânî Kilidi', 'Acel ve İcl (5 açık Mesânî ref! Sabır/Ecel zıttı acelecilik + buzağı [عِجْل] iki ayrı asıl hakemliği)'),
    ('trk', 'Açık Mesânî Kilidi', 'Terk (5 açık Mesânî ref! Alıkoyma/Sahiplenme zıttı olarak geride bırakmak, miras/iz bırakmak)'),
    ('bsT', 'Açık Mesânî Kilidi', 'Bast (4 açık Mesânî ref! Kadr/Daraltma zıttı: rızkı, eli ve bilgiyi genişletip açıp yaymak)'),
    ('mnE', 'Açık Mesânî Kilidi', 'Men\' (4 açık Mesânî ref! İ\'tâ/Verme zıttı: hayrı ve hakkı engellemek, cimrilik ve koruma)'),
    ('nqS', 'Açık Mesânî Kilidi', 'Naks (4 açık Mesânî ref! Ziyâde/Vefâ zıttı: ölçüde, emekte, ömürde ve hakta eksiltme)'),
    ('HDr', 'Açık Mesânî Kilidi', 'Hudûr ve Muhtazar (4 açık Mesânî ref! Gıyab zıttı: ölüm, vasiyet, hesap ve tanıklıkta hazır bulunmak)'),
    ('*ll', 'Açık Mesânî Kilidi', 'Züll ve Tezlîl (3 açık Mesânî ref! İzzet/Kibir zıttı: boyun eğdirilen doğa, anne-babaya tevazu kanadı ve alçalma)'),
    ('gwy', 'Açık Mesânî Kilidi', 'Gayy ve İğvâ (3 açık Mesânî ref! Rüşd zıttı: saptırıcı cazibeyle doğru istikameti yitirip çukura düşme)'),
]


def generate_etap_3c():
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
    total_corpus_tokens = sum(roots_count.values())

    # Exact baseline coverage of all currently locked roots outside 3C + 3C tokens
    items = []
    seen_bw = set()
    spec_bw_set = set()
    for etap_rank, (bw, category, rationale) in enumerate(ETAP_3C_ROOTS_SPEC, 1):
        if bw in seen_bw:
            raise ValueError(f"ETAP_3C_ROOTS_SPEC içinde mükerrer kök: {bw}")
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
            'etap_3c_rank': etap_rank,
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

    # Compute exact cumulative token coverage once all 3C roots are sealed
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
        'package': 'Faz 1 - Etap 3C (Son Mayın Temizliği, Hukuk-Ritüel-Kısa Sure Kilitleri ve Açık Mesânî Zırhı — 48 Kök)',
        'target_count': len(items),
        'locked_count': locked_cnt,
        'total_tokens_in_package': total_tokens,
        'total_corpus_tokens': total_corpus_tokens,
        'current_coverage_pct': round(current_cov_pct, 2),
        'target_coverage_pct': round(target_cov_pct, 2),
        'etap_3c_roots': items,
    }
    json_path = os.path.join(DATA_DIR, 'etap_3c_key_roots.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    pct_now_str = f"{current_cov_pct:.2f}".replace('.', ',')
    pct_target_str = f"{target_cov_pct:.2f}".replace('.', ',')
    md_lines = [
        "# ETAP 3C: SON MAYIN TEMİZLİĞİ, HUKUK-RİTÜEL-KISA SURE KİLİTLERİ VE AÇIK MESÂNÎ ZIRHI (48 KÖK -> 400 KÖK)",
        "## Tabula Rasa Mesânî Çözümleme Sistemi (v3.0 — Faz 2 Öncesi 400 Kök Tam Zırhı)",
        "",
        "> [!IMPORTANT]",
        f"> **HEDEF KAPSAM:** İlk 352 mühürlü kökten (`%83,08`) sonra, meal aşamasına geçmeden önce ceza-aile-ibadet hukuku düğümlerini, kısa sure kilitlerini ve en yüksek açık Mesânî referanslarını kapatan **48 kritik kök** ({total_tokens} geçiş) mühürlenerek toplam sözlük **400 kilitli köke (`%{pct_target_str}` kümülatif kapsam)** ulaştırılır.",
        f"> **Etap 3C İçinde Şu Ana Kadar Mühürlenen:** {locked_cnt} / {len(items)} Kök (Toplam Mühürlü: {len(locked_roots)} Kök | Güncel Kapsam: %{pct_now_str})",
        "",
        "| Etap Sıra | Kategori | Genel Sıra | Kök (Arapça) | Kök (Latin) | Geçiş | Ayet | Örnek | Stratejik Önemi / Kavram Durumu | Durum |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |",
    ]
    for it in items:
        badge = "✅ **MÜHÜRLÜ**" if it['is_locked'] else "⏳ *Bekliyor*"
        desc = it['concept_label'] if it['is_locked'] else it['rationale']
        md_lines.append(
            f"| {it['etap_3c_rank']} | {it['category']} | {it['global_rank']} | "
            f"`{it['root_arabic']}` | `{it['root_latin']}` | **{it['frequency']}** | {it['unique_ayahs']} | "
            f"{it['sample_ayah']} | {desc} | {badge} |"
        )
    md_lines.append("")

    md_path = os.path.join(DATA_DIR, 'ETAP_3C_KAVRAM.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(
        f"Etap 3C JSON üretildi: {json_path} "
        f"({locked_cnt}/{len(items)} mühürlü | Güncel: %{pct_now_str} -> Hedef 400 kök: %{pct_target_str})"
    )
    print(f"Etap 3C Markdown üretildi: {md_path}")


if __name__ == '__main__':
    generate_etap_3c()
