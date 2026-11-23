# -*- coding: utf-8 -*-
"""
Etap 3D Kilit Kavramlar (Fâtiha & Kısa Sure Tam Kilidi, Açık Mesânî Zırhı
ve Yüksek Frekanslı Çekirdek Kavramlar — 50 Kök -> 450 Kilitli Kök) İndeks Üreticisi
Tabula Rasa Mesânî Çözümleme Sistemi (v3.0)

İlk 400 mühürlü kökten sonra (%84,51 kapsam), meal aşamasına (Faz 2) geçmeden önce
Fâtiha suresinin %100'ünü, kısa surelerin (93-114) kalan anahtar düğümlerini,
3+ açık Mesânî referansı taşıyan tüm kökleri ve en yüksek frekanslı mühürsüz
çekirdek kavramları (50 kök / 1.205 geçiş) indeksler ve toplam kilitli sözlüğü
450 köke (%86,92 kapsam) tamamlar.
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
ETAP_3D_ROOTS_SPEC = [
    # Kategori 1: Fâtiha, İstiâze ve Kısa Surelerin (93-114) Çekirdek Kilitleri (10 kök: 3D-1 & 3D-2)
    ('Ewn', 'Fâtiha ve Kısa Sure Kilidi', 'İstiâne ve Teâvün (1:5 Fâtiha "yalnızca senden yardım isteriz" kilidi ve 5:2 iyilik-takvâ üzere yardımlaşma)'),
    ('gDb', 'Fâtiha ve Kısa Sure Kilidi', 'Gadab ve Mağdûb (1:7 Fâtiha "üzerlerine gazap/öfke çökmüş olanlar" kilidi ve 3:134/42:37 öfkeyi dizginleme)'),
    ('Ew*', 'Fâtiha ve Kısa Sure Kilidi', 'İstiâze ve Maâz (113:1 Felak, 114:1 Nâs ve 16:98 sığınma/korunma kalesi)'),
    ('$rr', 'Fâtiha ve Kısa Sure Kilidi', 'Şerr ve Şerer (113:2-5, 114:4, 99:8, 77:32 kıvılcım saçmak -> zarar saçan kötülük; خ-ي-ر kökünün 2 açık Mesânî ref!)'),
    ('Hsd', 'Fâtiha ve Kısa Sure Kilidi', 'Hased ve Hâsid (113:5 Felak suresi kilidi ve 4:54 başkasındaki nimeti kemiren yıkıcı kıskançlık)'),
    ('Elq', 'Fâtiha ve Kısa Sure Kilidi', 'Alak, Alaka ve Muallaka (96:2 Alak suresi tutunan/asılı embriyo ve 4:129 askıda bırakılan eş)'),
    ('qlm', 'Fâtiha ve Kısa Sure Kilidi', 'Kalem ve Aklâm (96:4 Alak suresi, 68:1 Kalem suresi ve 31:27 yontulmuş kayıt/yazı kalemi)'),
    ('Esr', 'Fâtiha ve Kısa Sure Kilidi', 'Usr ve Usre (94:5-6 İnşirâh suresi, 2:185, 65:7 sıkışık zorluk — ي-س-ر [Yüsr] kökünün doğrudan Mesânî zıttı!)'),
    ('$rH', 'Fâtiha ve Kısa Sure Kilidi', 'Şerh-i Sadr (94:1 İnşirâh, 6:125, 20:25, 39:22 göğsü açıp ferahlatmak — ض-ي-ق ve ح-ر-ج Mesânî zıttı!)'),
    ('Alf', 'Fâtiha ve Kısa Sure Kilidi', 'Îlâf, Te\'lîf ve Elf (106:1-2 Kureyş suresi güvenlik-uzlaşı bağı, 3:103 kalpleri kaynaştırma ve bin sayısı)'),

    # Kategori 2: Kısa Sure (93-114) Kozmoloji, Denge ve Toplumsal Dayanışma Kilitleri (10 kök: 3D-3 & 3D-4)
    ('wDE', 'Kısa Sure ve Kozmik Denge', 'Vad\' ve Mevzı\' (94:2 İnşirâh yükü indirme, 55:7 mîzânı koyma, 3:96 ilk kurulan ev ve 4:46 sözü bağlamından kaydırma)'),
    ('rfE', 'Kısa Sure ve Kozmik Denge', 'Ref\' ve Merfû\' (94:4 İnşirâh, 55:7 göğü yükseltme, 2:127 temelleri yükseltme — و-ض-ع ve خ-ف-ض zıttı, 2 açık Mesânî ref!)'),
    ('sfl', 'Kısa Sure ve Kozmik Denge', 'Esfel-i Sâfilîn ve Süflâ (95:5 Tîn suresi kilidi, 4:145, 9:40 en alt tabaka — ع-ل-و zıttı, 2 açık Mesânî ref!)'),
    ('vql', 'Kısa Sure ve Kozmik Denge', 'Miskâl, Sakîl ve Sekalân (99:7-8 Zilzâl, 101:6 Kâria ağır tartılar, 73:5 ağır söz — خ-ف-ف zıttı, 2 açık Mesânî ref!)'),
    ('*rr', 'Kısa Sure ve Kozmik Denge', 'Zerre ve Zürriyet (99:7-8 Zilzâl zerre ağırlığı, 4:40 ve 7:172 saçılıp yayılan soy/kuşaklar tek çekirdekte!)'),
    ('ETw', 'Kısa Sure ve Kozmik Denge', 'İ\'tâ ve Atâ\' (108:1 Kevser, 92:5 Leyl, 93:5 Duhâ el uzatıp bolca vermek — م-ن-ع ve ب-خ-ل Mesânî zıttı!)'),
    ('xTA', 'Kısa Sure ve Kozmik Denge', 'Hata ve Hatîe (96:16 Alak suçlu perçem, 2:286, 4:92 hedefi şaşıran kasıtsız hata vs yerleşik suç kuşatması)'),
    ('dry', 'Kısa Sure ve Kozmik Denge', 'Dirâyet ve Edra (97:2 Kadr, 101:3 Kâria, 104:5 Hümeze, 90:12 Beled "sana bildiren nedir?" kavrayış anahtarı)'),
    ('qhr', 'Kısa Sure ve Kozmik Denge', 'Kahr ve Kahhâr (93:9 Duhâ yetimi ezmeme buyruğu ve mutlak boyun eğdirici üstünlük sıfatı el-Kahhâr)'),
    ('tbb', 'Kısa Sure ve Kozmik Denge', 'Tebb ve Tetbîb (111:1 Tebbet suresi kilidi, 11:101, 40:37 kesintisiz kayıp, hüsran ve çöküş)'),

    # Kategori 3: En Yüksek Açık Mesânî Referansı Taşıyan Çekirdek Kökler (10 kök: 3D-5 & 3D-6)
    ('TEm', 'Açık Mesânî Kilidi', 'Taâm ve İt\'âm (5 açık Mesânî ref! 107:3 Mâûn, 90:14 Beled, 106:4 Kureyş, 76:8-9 yoksulu doyurmak ve tatmak)'),
    ('frr', 'Açık Mesânî Kilidi', 'Firâr ve Meferr (5 açık Mesânî ref! 51:50 Allah\'a kaçış vs 80:34, 75:10, 62:8 sorumluluktan ve ölümden kaçış)'),
    ('fwq', 'Açık Mesânî Kilidi', 'Fevk, Fevâk ve İfâka (4 açık Mesânî ref! ت-ح-ت ve س-ف-ل zıttı üstte olmak, 7:143 ayılıp kendine gelmek)'),
    ('A*y', 'Açık Mesânî Kilidi', 'Ezâ ve İyzâ\' (4 açık Mesânî ref! 2:222 geçici rahatsızlık, 2:262-264 başa kakıp incitme, 33:58 haksız eziyet)'),
    ('Hzn', 'Açık Mesânî Kilidi', 'Hüzün ve Hazen (3 açık Mesânî ref! 2:38 korku ve üzüntü yokluğu — ف-ر-ح zıttı ve خ-و-ف aynı ayet Furûku)'),
    ('bdw', 'Açık Mesânî Kilidi', 'Büduvv, İbdâ\' ve Bâdî (3 açık Mesânî ref! خ-ف-ي ve ك-ت-م zıttı: gizlenen şeyin çöl açıklığı gibi ortaya çıkması)'),
    ('nzE', 'Açık Mesânî Kilidi', 'Nez\' ve Tenâzü\' (3 açık Mesânî ref! 79:1-2 yerinden söküp çıkarmak, 3:26 gücü çekip almak ve 8:46 çekişip ihtilafa düşmek)'),
    ('bdA', 'Açık Mesânî Kilidi', 'Bed\' ve İbdâ\' (3 açık Mesânî ref! ع-و-د [İâde] kökünün doğrudan Mesânî eşleniği: yaratılışı ilk kez başlatmak)'),
    ('wSl', 'Açık Mesânî Kilidi', 'Vasl ve Vasîle (3 açık Mesânî ref! ق-ط-ع kökünün doğrudan Mesânî zıttı: 2:27, 13:21,25 bağları birleştirip ulaştırmak)'),
    ('frd', 'Açık Mesânî Kilidi', 'Ferd ve Furâdâ (3 açık Mesânî ref! 6:94, 19:80,95, 21:89 topluluk/şefaat zıttı: tek başına bireysel hesap)'),

    # Kategori 4: Ahit, Sabitlik, Özgürlük ve Kalıcılık Mesânî Kilitleri (10 kök: 3D-7 & 3D-8)
    ('qdm', 'Ahit, Sabitlik ve Özgürlük', 'Takdîm, Kadem ve İstikdâm (2 açık Mesânî ref! أ-خ-ر zıttı: 82:5, 75:13 önden göndermek ve sağlam duruş adımı)'),
    ('jwb', 'Ahit, Sabitlik ve Özgürlük', 'İsticâbe ve Cevâb (2 açık Mesânî ref! 89:9 kayayı delip oymak somut çıpası + 2:186, 8:24 çağrıya karşılık vermek)'),
    ('sbq', 'Ahit, Sabitlik ve Özgürlük', 'Sebk, Sâbikûn ve İstibâk (2 açık Mesânî ref! 56:10, 35:32, 23:61 hayırda ve sorumlulukta öne geçip yarışmak)'),
    ('wdd', 'Ahit, Sabitlik ve Özgürlük', 'Meveddet ve Vedûd (2 açık Mesânî ref! ع-د-و ve ب-غ-ض zıttı: 30:21, 60:7, 85:14 kazık gibi köklü sevgi ve dostluk bağı)'),
    ('bqy', 'Ahit, Sabitlik ve Özgürlük', 'Bakâ, Bâkî ve Bâkıyât (2 açık Mesânî ref! ف-ن-ي ve ن-ف-د zıttı: 16:96, 18:46, 55:27 yok olmayıp geride kalıcı olan)'),
    ('vbt', 'Ahit, Sabitlik ve Özgürlük', 'Sebât ve Tesbît (2 açık Mesânî ref! ز-ل-ل ve ز-ي-غ zıttı: 14:27, 2:250, 47:7 sarsılmaz biçimde yerinde sabitlenmek)'),
    ('gll', 'Ahit, Sabitlik ve Özgürlük', 'Gıll, Gulûl ve Ağlâl (2 açık Mesânî ref! 7:157 boyundaki pranga/boyunduruk, 59:10 kalpteki gizli kin ve 3:161 kamu malı ihaneti)'),
    ('Hrr', 'Ahit, Sabitlik ve Özgürlük', 'Hürr, Tahrîr ve Harr (2 açık Mesânî ref! 90:13, 4:92, 5:89 boyunduruktan özgürleştirme/köle azadı, 3:35 adanmış özgür kul)'),
    ('nkv', 'Ahit, Sabitlik ve Özgürlük', 'Neks ve Enkâs (2 açık Mesânî ref! 16:92 bükülmüş ipi çözüp dağıtmak somut çıpası + 48:10, 9:12 verilen ahdi bozmak)'),
    ('qnT', 'Ahit, Sabitlik ve Özgürlük', 'Kunût ve Kânit (2 açık Mesânî ref! ر-ج-و ve ط-م-ع zıttı: 39:53, 15:56, 30:36 rahmetten tamamen umut kesip kurumak)'),

    # Kategori 5: Yüksek Frekanslı Çekirdek Eylem, Kapasite ve Hukuk Kavramları (10 kök: 3D-9 & 3D-10 -> 450 KÖK!)
    ('srr', 'Yüksek Frekanslı Çekirdek', 'Sırr, İsrâr, Mesrûr ve Sürür (1 açık Mesânî ref! ع-ل-ن ve ج-ه-ر zıttı gizlemek/sır + içten parlayan sevinç ve tahtlar)'),
    ('qwy', 'Yüksek Frekanslı Çekirdek', 'Kuvvet, Kaviyy ve Mukvîn (1 açık Mesânî ref! ض-ع-ف [Za\'f] kökünün doğrudan Mesânî zıttı: bükülmüş halat sağlamlığı ve güç)'),
    ('Sdd', 'Yüksek Frekanslı Çekirdek', 'Sadd ve Sudûd (1 açık Mesânî ref! 4:61, 22:25 hak yoldan ve ortak mabedden geri çevirip engellemek ve yüz çevirmek)'),
    ('qrr', 'Yüksek Frekanslı Çekirdek', 'Karâr, Müstekarr ve İkrâr (1 açık Mesânî ref! 6:98 yerleşip durulma yeri, 25:74 göz aydınlığı ve 2:84 ahdi onaylamak)'),
    ('ftH', 'Yüksek Frekanslı Çekirdek', 'Feth, Fettâh ve Mefâtih (1 açık Mesânî ref! 7:89, 26:118 kilitli düğümü hak ile açıp hüküm vermek ve 6:59 gaybın anahtarları)'),
    ('mrA', 'Yüksek Frekanslı Çekirdek', 'Mer\', İmru\' ve İmra\'e (4:4 boğazdan rahat geçen afiyetli pay [هَنِيٓـًٔا مَّرِيٓـًٔا] + birey/kişi sorumluluğu ve eş/kadın)'),
    ('jnb', 'Yüksek Frekanslı Çekirdek', 'Cenb, İctinâb ve Cünüb (1 açık Mesânî ref! yan/kenar, 4:36 komşu, 16:36/22:30 pislik ve tâğûttan uzak durmak ve 4:43/5:6 cünüplük)'),
    ('wsE', 'Yüksek Frekanslı Çekirdek', 'Vüs\'at ve Vâsi\' (2:286, 65:7 kimseye kapasitesinin/gücünün [وُسْعَهَا] üstünde yük yüklenmemesi yasası ve kuşatıcı genişlik)'),
    ('sEy', 'Yüksek Frekanslı Çekirdek', 'Sa\'y (53:39 "insan için yalnızca kendi çabası vardır" yasası, 2:205, 62:9 bilinçli ve kararlı emek yürüyüşü)'),
    ('fwz', 'Yüksek Frekanslı Çekirdek', 'Fevz ve Fâizûn (خ-س-ر [Hüsrân] kökünün doğrudan Mesânî eşleniği: yıkımdan kurtulup büyük başarıya ve esenliğe ulaşmak)'),
]


def generate_etap_3d():
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

    items = []
    seen_bw = set()
    spec_bw_set = set()
    for etap_rank, (bw, category, rationale) in enumerate(ETAP_3D_ROOTS_SPEC, 1):
        if bw in seen_bw:
            raise ValueError(f"ETAP_3D_ROOTS_SPEC içinde mükerrer kök: {bw}")
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
            'etap_3d_rank': etap_rank,
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
        'package': 'Faz 1 - Etap 3D (Fâtiha & Kısa Sure Tam Kilidi, Açık Mesânî Zırhı ve Yüksek Frekanslı Çekirdek Kavramlar — 50 Kök)',
        'target_count': len(items),
        'locked_count': locked_cnt,
        'total_tokens_in_package': total_tokens,
        'total_corpus_tokens': total_corpus_tokens,
        'current_coverage_pct': round(current_cov_pct, 2),
        'target_coverage_pct': round(target_cov_pct, 2),
        'etap_3d_roots': items,
    }
    json_path = os.path.join(DATA_DIR, 'etap_3d_key_roots.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    pct_now_str = f"{current_cov_pct:.2f}".replace('.', ',')
    pct_target_str = f"{target_cov_pct:.2f}".replace('.', ',')
    md_lines = [
        "# ETAP 3D: FÂTİHA & KISA SURE TAM KİLİDİ, AÇIK MESÂNÎ ZIRHI VE YÜKSEK FREKANSLI ÇEKİRDEK KAVRAMLAR (50 KÖK -> 450 KÖK)",
        "## Tabula Rasa Mesânî Çözümleme Sistemi (v3.0 — Faz 2 Öncesi 450 Kök Tam Zırhı)",
        "",
        "> [!IMPORTANT]",
        f"> **HEDEF KAPSAM:** İlk 400 mühürlü kökten (`%84,51`) sonra, meal aşamasına geçmeden önce Fâtiha suresinin tamamını, kısa surelerin (93-114) kalan çekirdek düğümlerini, 3+ açık Mesânî referanslarını ve en yüksek frekanslı mühürsüz kavramları kapatan **50 kritik kök** ({total_tokens} geçiş) mühürlenerek toplam sözlük **450 kilitli köke (`%{pct_target_str}` kümülatif kapsam)** ulaştırılır.",
        f"> **Etap 3D İçinde Şu Ana Kadar Mühürlenen:** {locked_cnt} / {len(items)} Kök (Toplam Mühürlü: {len(locked_roots)} Kök | Güncel Kapsam: %{pct_now_str})",
        "",
        "| Etap Sıra | Kategori | Genel Sıra | Kök (Arapça) | Kök (Latin) | Geçiş | Ayet | Örnek | Stratejik Önemi / Kavram Durumu | Durum |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |",
    ]
    for it in items:
        badge = "✅ **MÜHÜRLÜ**" if it['is_locked'] else "⏳ *Bekliyor*"
        desc = it['concept_label'] if it['is_locked'] else it['rationale']
        md_lines.append(
            f"| {it['etap_3d_rank']} | {it['category']} | {it['global_rank']} | "
            f"`{it['root_arabic']}` | `{it['root_latin']}` | **{it['frequency']}** | {it['unique_ayahs']} | "
            f"{it['sample_ayah']} | {desc} | {badge} |"
        )
    md_lines.append("")

    md_path = os.path.join(DATA_DIR, 'ETAP_3D_KAVRAM.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(
        f"Etap 3D JSON üretildi: {json_path} "
        f"({locked_cnt}/{len(items)} mühürlü | Güncel: %{pct_now_str} -> Hedef 450 kök: %{pct_target_str})"
    )
    print(f"Etap 3D Markdown üretildi: {md_path}")


if __name__ == '__main__':
    generate_etap_3d()
