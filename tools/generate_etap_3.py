# -*- coding: utf-8 -*-
"""
Etap 3 Kilit Kavramlar (Faz 2 Öncesi Kafa Karıştıran ve Anlamı Doğrudan Belirleyen
131 Kök — 3A Çekirdek 55 + 3B Genişletilmiş 76) İndeks Üreticisi
Tabula Rasa Mesânî Çözümleme Sistemi (v3.0)

İlk 221 mühürlü kökten sonra (%77,12 kapsam), ayet çözümlemesine (Faz 2) geçmeden
önce geleneksel algıda en çok anlam kaymasına uğrayan kavramları ve locked_roots.json /
PROMPT.md içinde açıkta kalan Mesânî & Furûk eşleniklerini indeksler.
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_kavramlar import ROOT_CONFIG
from quran_analyzer import DATA_DIR, to_arabic_root, to_latin_root

# (buckwalter, tier, category, rationale)
ETAP_3_ROOTS_SPEC = [
    # =========================================================================
    # ETAP 3A — ÇEKİRDEK 55 KAFA KARIŞTIRICI VE AÇIK MESÂNÎ/FURÛK KİLİDİ
    # =========================================================================
    # Kategori 1: Teoloji, İlahi Sıfatlar, Metafizik ve Otorite (11 çekirdek)
    ('Tgy', '3A', 'Teoloji ve Otorite', 'Tâğût ve Tuğyân (sınırı aşan zorba sistem ve taşkın otorite; 3 kilitli kökün Mesânî zıttı)'),
    ('$fE', '3A', 'Teoloji ve Otorite', 'Şefâat ve Şefî (çiftlemek, omuz vermek ve destek/aracılık sınırları)'),
    ('Er$', '3A', 'Teoloji ve Otorite', 'Arş (çardak/çatı kurma kökünden evrensel yönetim ve egemenlik merkezi)'),
    ('slT', '3A', 'Teoloji ve Otorite', 'Sultân (kesin kanıt, delile dayalı yetki ve hüküm geçerliliği)'),
    ('brk', '3A', 'Teoloji ve Otorite', 'Bereket, Tebâreke ve Mübârek (sarsılmaz sabitlik, kalıcılık ve kesintisiz verimlilik)'),
    ('brA', '3A', 'Teoloji ve Otorite', 'Bâri ve Berâet (pürüzsüz yaratış [Halaka/Fatara Furûku] ve sorumluluktan/bağdan temize çıkma)'),
    ('xlS', '3A', 'Teoloji ve Otorite', 'İhlâs, Muhlis ve Muhlas (yabancı karışımdan tamamen arındırıp saf ve katıksız kılma)'),
    ('Smd', '3A', 'Teoloji ve Otorite', 'Samed (İhlâs suresinin çekirdek sıfatı: her şeyin yöneldiği, boşluğu olmayan mutlak dayanak)'),
    ('krs', '3A', 'Teoloji ve Otorite', 'Kürsî (2:255 ve 38:34: bilgi, hâkimiyet ve egemenlik kaidesi)'),
    ('mkr', '3A', 'Teoloji ve Otorite', 'Mekr (gizli plan ve karşı-strateji mekaniği; Keyd ile Furûk)'),
    ('sxr', '3A', 'Teoloji ve Otorite', 'Teshîr ve Suhriye (doğa yasalarının hizmete sunulması ile alay edip küçümseme tek kökte)'),

    # Kategori 2: Vahiy, Metin Kavramları ve İnanç Kimliği (9 çekirdek)
    ('SrT', '3A', 'Vahiy ve Kimlik', 'Sırât (Fâtiha omurgası: geniş ana cadde; Sebîl ve Şerîat ile Furûk)'),
    ('$bh', '3A', 'Vahiy ve Kimlik', 'Müteşâbih, Teşâbüh ve Şübbihe (3:7 muhkem-müteşâbih ayrımı ve 4:157 benzetilme ayeti)'),
    ('Hnf', '3A', 'Vahiy ve Kimlik', 'Hanîf (eğrilikten ve sapmadan doğruluk eksenine kesin yöneliş)'),
    ('mll', '3A', 'Vahiy ve Kimlik', 'Millet (yazdırılan ve izlenen yaşam yolu/sistemi; İbrâhîm yolu)'),
    ('$Er', '3A', 'Vahiy ve Kimlik', 'Şuûr, Şâir ve Şeâir (ince farkındalık, şiir ve ortak semboller/nişaneler tek kökte)'),
    ('Hdv', '3A', 'Vahiy ve Kimlik', 'Hadîs (yeni ortaya çıkan söz ve anlatı; Kur\'an\'ın kendisine Ahsenü\'l-Hadîs demesi)'),
    ('qSS', '3A', 'Vahiy ve Kimlik', 'Kıssa ve Kısâs (iz sürmek ve birebir denklikle takip etmek — anlatı ile hukuk tek kökte)'),
    ('flH', '3A', 'Vahiy ve Kimlik', 'Felâh ve Müflihûn (toprağı yarıp filizlendirmek gibi çabayla sonuç ve kurtuluş hasat etmek)'),
    ('Hrf', '3A', 'Vahiy ve Kimlik', 'Tahrîf ve Harf (sözü bağlamından/ucundan kaydırıp saptırmak ve kıyıda durmak)'),

    # Kategori 3: Açık Mesânî ve Aynı Ayet İçi Furûk Kutupları (16 çekirdek)
    ('nsy', '3A', 'Mesânî ve Furûk Kilidi', 'Nisyân (11 Mesânî ref! Zikir zıttı: unutkanlık ile bilinçli terk edip önemsememe)'),
    ('Edl', '3A', 'Mesânî ve Furûk Kilidi', 'Adl (9 Mesânî ref! Kıst ile Furûk: denk yükleme, denge ve eşdeğer karşılık)'),
    ('qsT', '3A', 'Mesânî ve Furûk Kilidi', 'Kıst (Adl ile Furûk: hak payı dağıtımı; Muksit [âdil] vs Kâsıt [sapmış] zıtlığı)'),
    ('qEd', '3A', 'Mesânî ve Furûk Kilidi', 'Kuûd (8 Mesânî ref! Kıyâm ana zıttı: ataletle oturup sorumluluktan geri kalma)'),
    ('bTl', '3A', 'Mesânî ve Furûk Kilidi', 'Bâtıl (7 Mesânî ref! Hakk ana zıttı: boş, dayanaksız ve hükümsüz kalan)'),
    ('Efw', '3A', 'Mesânî ve Furûk Kilidi', 'Afv (7 Mesânî ref! Mağfiret Furûku ve İntikam zıttı + 2:219 ihtiyaç fazlası)'),
    ('krh', '3A', 'Mesânî ve Furûk Kilidi', 'İkrâh ve Kerh (6 Mesânî ref! Tav\'/Meşîet zıttı ve 2:256 zorlama yasağı)'),
    ('hwy', '3A', 'Mesânî ve Furûk Kilidi', 'Hevâ ve Hâviye (5 Mesânî ref! Uçurumdan savrulma, boş arzu ve 101:9 Hâviye tek kökte)'),
    ('Ejz', '3A', 'Mesânî ve Furûk Kilidi', 'Acz ve Mu\'ciz (5 Mesânî ref! Gücü yetmemek, geri kalmak ve kaçıp kurtulamamak)'),
    ('blw', '3A', 'Mesânî ve Furûk Kilidi', 'Belâ ve İbtilâ (Fitne ile Furûk: hem iyilikle hem zorlukla sınayıp açığa çıkarma)'),
    ('ryb', '3A', 'Mesânî ve Furûk Kilidi', 'Rayb (Şekk ile Furûk: 2:2 huzursuz edici, suçlayıcı kuşku)'),
    ('x$y', '3A', 'Mesânî ve Furûk Kilidi', 'Haşyet (Rank 207! Havf ve Vikâye ile Furûk: bilgiye dayalı derin ürperti ve saygı)'),
    ('jnH', '3A', 'Mesânî ve Furûk Kilidi', 'Cünâh ve Cenâh (İsm/Zenb/Cünâh Furûk üçlüsü: eğilme, kanat ve hukuki sakınca)'),
    ('fjr', '3A', 'Mesânî ve Furûk Kilidi', 'Fücûr ve Fecr (91:8 Vikâye zıttı: yarıp taşmak — şafak, pınar ve ahlaki sınır yıkımı)'),
    ('Afk', '3A', 'Mesânî ve Furûk Kilidi', 'İfk (İfk/İftirâ/Zûr/Kezib Furûku: gerçeği tersyüz edip baş aşağı çevirme)'),
    ('xtm', '3A', 'Mesânî ve Furûk Kilidi', 'Hatm ve Hâtem (kalplerin mühürlenmesi mekaniği + 33:40 Hâtemü\'n-Nebiyyîn)'),

    # Kategori 4: Hukuk, Ekonomi, Aile, Örtünme ve Toplumsal Düzen (11 çekirdek)
    ('rbw', '3A', 'Hukuk ve Toplumsal Düzen', 'Ribâ (katlayıp şişiren haksız artış; 30:39 Zekâ [arınma/gelişme payı] zıttı ve toprağın kabarması)'),
    ('nkH', '3A', 'Hukuk ve Toplumsal Düzen', 'Nikâh (evlilik sözleşmesi ve hukuki birleşme akdi)'),
    ('n$z', '3A', 'Hukuk ve Toplumsal Düzen', 'Nüşûz (4:34 ve 4:128: hem kadın hem erkek için evlilik bağından baş kaldırıp kopma)'),
    ('HSn', '3A', 'Hukuk ve Toplumsal Düzen', 'Muhsanât ve Hısn (korunaklı kale; bağlama göre evli, özgür veya korunmuş kadınlar)'),
    ('qnt', '3A', 'Hukuk ve Toplumsal Düzen', 'Kunût ve Kânitât (4:34 dahil Kur\'an boyunca Allah\'a sürekli, huşulu bağlılık)'),
    ('xmr', '3A', 'Hukuk ve Toplumsal Düzen', 'Hamr ve Humur (24:31 örtü ile aklı örten sarhoş edicinin tek çekirdeği: örtmek)'),
    ('Hjb', '3A', 'Hukuk ve Toplumsal Düzen', 'Hicâb (Kur\'an boyunca giysi değil ayırıcı perde ve fiziksel/mecazi engel)'),
    ('jlb', '3A', 'Hukuk ve Toplumsal Düzen', 'Cilbâb (33:59 dış örtü ve 17:64 kök bağlantısı arkeolojisi)'),
    ('wzn', '3A', 'Hukuk ve Toplumsal Düzen', 'Mîzân ve Vezn (kozmik ve hukuki denge, ölçü ve ağırlık sistemi)'),
    ('mlA', '3A', 'Hukuk ve Toplumsal Düzen', 'Mele\' (göz dolduran yönetici seçkinler ve toplumsal iktidar zümresi)'),
    ('wsT', '3A', 'Hukuk ve Toplumsal Düzen', 'Vasat (2:143 Ümmeten Vasatan: merkezî, dengeli ve örnek tanık topluluk)'),

    # Kategori 5: İnsan Zihni, Kalp Organları ve Akletme Ekosistemi (4 çekirdek)
    ('dbr', '3A', 'Zihin ve Akletme', 'Tedebbür ve Dübür (arka/sonuç; sözün arkasına, sonucuna ve bütünlüğüne bakmak)'),
    ('fqh', '3A', 'Zihin ve Akletme', 'Fıkıh (derindeki inceliği yarıp kavrama ve keskin idrak)'),
    ('Sdr', '3A', 'Zihin ve Akletme', 'Sadr (Kalp ile Furûk: dış giriş/göğüs kafesi, iç sesin ilk karşılandığı ön alan)'),
    ('lbb', '3A', 'Zihin ve Akletme', 'Elbâb (kabuğu soyulmuş saf çekirdek ve arı öz sahipleri)'),

    # Kategori 6: Zaman, Kıyamet, Diriliş ve Ahiret Mekaniği (4 çekirdek)
    ('swE', '3A', 'Zaman ve Ahiret', 'Sâat (Rank 205 en sık açık kök! Yevm ile Furûk: kopuş/kırılma eşiği ve belirleyici an)'),
    ('H$r', '3A', 'Zaman ve Ahiret', 'Haşr (Ba\'s ve Nüşûr ile Furûk: sürülüp tek merkezde toplanma, dünya sürgünü dahil)'),
    ('Hwr', '3A', 'Zaman ve Ahiret', 'Hûr, Havârî ve Muhâvere (parlaklık/saflık, arı destekçiler ve karşılıklı diyalog tek kökte)'),
    ('vwb', '3A', 'Zaman ve Ahiret', 'Mesâbe, Siyâb ve Geri Dönen Karşılık (hem olumlu hem 83:36 olumsuz geri dönüş + giysi + güvenli merkez)'),

    # =========================================================================
    # ETAP 3B — TAM MESÂNÎ, FURÛK, HUKUK, ZİHİN VE AHİRET ZIRHI (76 KÖK)
    # =========================================================================
    # Kategori 1 Devamı (4 kök)
    ('kyd', '3B', 'Teoloji ve Otorite', 'Keyd (ince plan ve karşı hamle; Mekr ile aynı ayet içi Furûk)'),
    ('qds', '3B', 'Teoloji ve Otorite', 'Kuddûs ve Mukaddes (her türlü kirden ve eksiklikten arı, berrak alan)'),
    ('bls', '3B', 'Teoloji ve Otorite', 'İblâs (ümitsizliğe gömülüp şaşkınlıkla susakalmak; İblîs bağlantısı)'),
    ('wsws', '3B', 'Teoloji ve Otorite', 'Vesvese ve Vesvâs (Nâs suresi ve 50:16: zihinde yinelenen sinsi iç ses/dürtü)'),

    # Kategori 2 Devamı (11 kök)
    ('fSl', '3B', 'Vahiy ve Kimlik', 'Fasl ve Tafsîl (ayırıp netleştirme, metnin kendi kendini açıklaması ve ayrım günü)'),
    ('Twf', '3B', 'Vahiy ve Kimlik', 'Tavâf ve Tâife (etrafında dönme, gezinme ve belirli grup/kesim)'),
    ('hjr', '3B', 'Vahiy ve Kimlik', 'Hicret ve Hecr (göç, 4:34 uzaklaşma ve 25:30 Kur\'an\'ı terk edilmiş bırakma)'),
    ('Emr', '3B', 'Vahiy ve Kimlik', 'Ömür, Umre ve İmâr (yaşam süresi, bayındırlık/inşa ve ziyaret tek kökte)'),
    ('nsk', '3B', 'Vahiy ve Kimlik', 'Nüsük ve Mensek (adanmış düzenli uygulama yöntemi ve yaşam disiplini)'),
    ('sTr', '3B', 'Vahiy ve Kimlik', 'Esâtîr, Satır ve Müsaytır (satır satır yazılmış eski kayıtlar ve baskı/denetim kuran)'),
    ('brhn', '3B', 'Vahiy ve Kimlik', 'Burhân (Sultân ve Beyyine ile Furûk: tartışmayı bitiren somut ve rasyonel kanıt)'),
    ('HfZ', '3B', 'Vahiy ve Kimlik', 'Hıfz, Hafîz ve Mahfûz (korumak, gözetmek ve zayi etmemek)'),
    ('lwH', '3B', 'Vahiy ve Kimlik', 'Levh ve Elvâh (Mûsâ\'nın levhaları, gemi tahtaları ve 85:22 korunan kayıt)'),
    ('sbt', '3B', 'Vahiy ve Kimlik', 'Sebt ve Sübât (kesinti, çalışma arası ve 78:9 dinlenme uykusu tek kökte)'),
    ('hwd', '3B', 'Vahiy ve Kimlik', 'Hâdû ve Hûd (7:156 yönelip dönme eylemi ve tarihsel topluluk adlandırması)'),

    # Kategori 3 Devamı (26 kök)
    ('gfl', '3B', 'Mesânî ve Furûk Kilidi', 'Gaflet (7 Mesânî ref! Zikir/İlim zıttı: işaretlere kasten kapanma ve aymazlık)'),
    ('ktm', '3B', 'Mesânî ve Furûk Kilidi', 'Ketm (6 Mesânî ref! 3:187 Beyân zıttı: açık bilgiyi saklayıp gizleme)'),
    ('xfy', '3B', 'Mesânî ve Furûk Kilidi', 'İhfâ (6 Mesânî ref! Zuhûr zıttı: örtüp görünmez kılma; Ketm ile Furûk)'),
    ('nqD', '3B', 'Mesânî ve Furûk Kilidi', 'Nakz (6 Mesânî ref! Ahid/Mîsâk/Kıyâm zıttı: örülü bağı çözüp bozmak)'),
    ('bdl', '3B', 'Mesânî ve Furûk Kilidi', 'Tebdîl ve İstibdâl (6 Mesânî ref! Değiştirip yerine başkasını koyma; Nesh ile Furûk)'),
    ('ESy', '3B', 'Mesânî ve Furûk Kilidi', 'İsyân (5 Mesânî ref! Tav\'/İtaat zıttı: sopa gibi dikilip boyun eğmeme)'),
    ('Emy', '3B', 'Mesânî ve Furûk Kilidi', 'Amâ (5 Mesânî ref! Basar zıttı: fiziksel ve bilinç düzeyinde körlük)'),
    ('bxl', '3B', 'Mesânî ve Furûk Kilidi', 'Buhl (5 Mesânî ref! İnfâk/İtâ zıttı: kaynağı elde tutup dolaşımdan esirgeme)'),
    ('jhl', '3B', 'Mesânî ve Furûk Kilidi', 'Cehl ve Câhiliye (4 Mesânî ref! İlim ve Hilm zıttı: dürtüsel ve ölçüsüz tepki)'),
    ('Smm', '3B', 'Mesânî ve Furûk Kilidi', 'Samem (3 Mesânî ref! Sem\' zıttı: işitmeye ve kanıta kapanmış sağırlık)'),
    ('knz', '3B', 'Mesânî ve Furûk Kilidi', 'Kenz (9:34 İnfâk ana zıttı: serveti yığıp toplumun dolaşımından tıkama)'),
    ('nkr', '3B', 'Mesânî ve Furûk Kilidi', 'Münker (Ma\'rûf ana zıttı: aklın ve vicdanın yadırgayıp reddettiği yabancı/çirkin fiil)'),
    ('fH$', '3B', 'Mesânî ve Furûk Kilidi', 'Fahşâ ve Fâhişe (ölçüyü aşıp çirkinleşen her türlü ağır taşkınlık; Münker/Bağy Furûku)'),
    ('srf', '3B', 'Mesânî ve Furûk Kilidi', 'İsrâf (Tebzîr ile Furûk: yalnızca harcamada değil her alanda ölçüyü ve sınırı aşma)'),
    ('b*r', '3B', 'Mesânî ve Furûk Kilidi', 'Tebzîr (İsrâf ile Furûk: 17:26-27 tohum gibi rastgele saçıp savurma)'),
    ('$kk', '3B', 'Mesânî ve Furûk Kilidi', 'Şekk (Rayb ile Furûk: zihnin iki ihtimal arasında dengeli tereddüdü)'),
    ('zwr', '3B', 'Mesânî ve Furûk Kilidi', 'Zûr (İfk/İftirâ/Zûr/Kezib Furûku: gerçekten sapmış eğri tanıklık ve sahte söz)'),
    ('TbE', '3B', 'Mesânî ve Furûk Kilidi', 'Tab\' (Hatm ile Furûk: tekrarlanan seçimler sonucu kalbin katılaşıp damgalanması)'),
    ('Hlm', '3B', 'Mesânî ve Furûk Kilidi', 'Hilm, Halîm ve Hulum (Cehl zıttı: öfkeye kapılmayan dingin denge ve akıl olgunluğu)'),
    ('nqm', '3B', 'Mesânî ve Furûk Kilidi', 'İntikâm (5:95 Afv zıttı: ağır suç karşısında kesin yaptırım ve karşılık)'),
    ('krm', '3B', 'Mesânî ve Furûk Kilidi', 'Kerem ve İkrâm (Rank 211! 89:15-16 İhânet zıttı: onurlu değer, cömertlik ve saygınlık)'),
    ('hwn', '3B', 'Mesânî ve Furûk Kilidi', 'Hevn ve İhânet (89:15-16 İkrâm zıttı: alçaltma/horluk ile 25:63 sükûnetli yürüyüş)'),
    ('zyg', '3B', 'Mesânî ve Furûk Kilidi', 'Zeyğ (Kıyâm zıttı ve 3:7: doğru eksenden bilinçli meyil ve kayma)'),
    ('Ewj', '3B', 'Mesânî ve Furûk Kilidi', 'İvec (18:1-2 Kayyim zıttı: yapısal çarpıklık, eğrilik ve tutarsızlık)'),
    ('Aby', '3B', 'Mesânî ve Furûk Kilidi', 'İbâ (Rükû zıttı ve 2:34: inatla direnip reddetme)'),
    ('Etw', '3B', 'Mesânî ve Furûk Kilidi', 'Utuvv (Rükû zıttı: haddini aşıp sertleşerek diklenme)'),

    # Kategori 4 Devamı (21 kök)
    ('zyn', '3B', 'Hukuk ve Toplumsal Düzen', 'Zînet ve Tezyîn (24:31 görünen güzellik/süs ile kötü eylemlerin süslü gösterilmesi)'),
    ('Ewr', '3B', 'Hukuk ve Toplumsal Düzen', 'Avret (24:31, 24:58, 33:13: korunmasız açıklık, gedik ve mahremiyet aralığı)'),
    ('frj', '3B', 'Hukuk ve Toplumsal Düzen', 'Ferc (77:9 yarılma/açıklık ile 23:5 mahremiyet koruma tek çekirdeği)'),
    ('Tlq', '3B', 'Hukuk ve Toplumsal Düzen', 'Talâk ve İntilâk (bağdan çözüp salıverme: boşanma hukuku ve serbestçe yola koyulma)'),
    ('byE', '3B', 'Hukuk ve Toplumsal Düzen', 'Bey\' ve Bîat (ticari alışveriş ile toplumsal/siyasal bağlılık akdinin ortak kökü)'),
    ('rqb', '3B', 'Hukuk ve Toplumsal Düzen', 'Rekabe ve Rakîb (boyunduruk/kölelik çözme hukuku ve dikkatle gözetleme)'),
    ('Asr', '3B', 'Hukuk ve Toplumsal Düzen', 'Esîr ve Esr (savaş esirleri hukuku ve bedensel eklem bağı)'),
    ('Hdd', '3B', 'Hukuk ve Toplumsal Düzen', 'Hudûd ve Hadîd (koruyucu sınır çizgileri, demir ve keskinlik)'),
    ('wrv', '3B', 'Hukuk ve Toplumsal Düzen', 'Mîrâs ve Vâris (miras hukuku ve yeryüzüne/kitaba mirasçı kılınma sorumluluğu)'),
    ('wSy', '3B', 'Hukuk ve Toplumsal Düzen', 'Vasiyet ve Tavsiye (bağlayıcı miras bildirimi ve nesiller arası ahlaki emanet)'),
    ('Hrb', '3B', 'Hukuk ve Toplumsal Düzen', 'Harb ve Mihrâb (silahlı çatışma ile korunaklı sığınma/yöneliş odası tek kökte)'),
    ('gnm', '3B', 'Hukuk ve Toplumsal Düzen', 'Ganîmet ve Ganem (savaş kazanımı ve sürü/varlık)'),
    ('nfl', '3B', 'Hukuk ve Toplumsal Düzen', 'Enfâl ve Nâfile (savaş fazlası kamu geliri, ek gönüllü eylem ve torun)'),
    ('fyA', '3B', 'Hukuk ve Toplumsal Düzen', 'Fey\' (geri dönmek: çatışmasız kamu geliri ve gölgelerin dönüşü)'),
    ('$wr', '3B', 'Hukuk ve Toplumsal Düzen', 'Şûrâ (ortak danışma ve toplumsal karar meşruiyeti)'),
    ('trf', '3B', 'Hukuk ve Toplumsal Düzen', 'Mütrefîn (toplumları yozlaştıran şımarık aşırı refah sınıfı)'),
    ('ytm', '3B', 'Hukuk ve Toplumsal Düzen', 'Yetîm (tek/korunmasız kalmış birey ve toplumsal dayanışma sorumluluğu)'),
    ('fqr', '3B', 'Hukuk ve Toplumsal Düzen', 'Fakîr (bel kemiği kırılmış/muhtaç; 9:60 Miskîn Furûku ve varoluşsal muhtaçlık)'),
    ('xbv', '3B', 'Hukuk ve Toplumsal Düzen', 'Habîs (Tayyib zıttı: bozuk, çürük, zararlı ve kirli olan)'),
    ('rjs', '3B', 'Hukuk ve Toplumsal Düzen', 'Rics (Tahâret zıttı: zihinsel, ahlaki ve maddi karmaşa/pislik)'),
    ('Erb', '3B', 'Hukuk ve Toplumsal Düzen', 'Arabî, A\'râb ve Urûb (apaçık duru ifade dili, göçebe topluluk ve 56:37)'),

    # Kategori 5 Devamı (8 kök)
    ('fkr', '3B', 'Zihin ve Akletme', 'Tefekkür (Akl, Tedebbür ve Fıkıh ile Furûk: zihinde derin çözümleme)'),
    ('fAd', '3B', 'Zihin ve Akletme', 'Fuâd (Kalp ve Sadr ile Furûk: ateşlenip duygulanan, algılayan canlı iç bilinç)'),
    ('Hjr', '3B', 'Zihin ve Akletme', 'Hicr ve Hacer (taş, koruma/yasak sınırı ve 89:5 frenleyici akıl)'),
    ('yqn', '3B', 'Zihin ve Akletme', 'Yakîn (Zann ve Rayb zıttı: durulup netleşmiş kesin bilgi ve 15:99)'),
    ('r$d', '3B', 'Zihin ve Akletme', 'Rüşd (Gayy zıttı: olgunlaşmış doğruluk, isabetli yönetim ve erginlik)'),
    ('sfh', '3B', 'Zihin ve Akletme', 'Sefâhat ve Sefîh (hafiflik, tutarsızlık ve zihinsel/ekonomik dengesizlik)'),
    ('lsn', '3B', 'Zihin ve Akletme', 'Lisân (dil, ifade sistemi ve toplumsal söz/anlatı)'),
    ('Tmn', '3B', 'Zihin ve Akletme', 'İtminân ve Mutmainne (Rayb zıttı: çalkantıdan durulup güvenle yatışmak)'),

    # Kategori 6 Devamı (6 kök)
    ('n$r', '3B', 'Zaman ve Ahiret', 'Nüşûr ve İnşâr (dürülü olanı yayıp açma: rüzgâr, kayıt defteri ve diriliş)'),
    ('Swr', '3B', 'Zaman ve Ahiret', 'Sûr, Sûret ve Musavvir (biçimlendirme ve 6:73 kıyamette üflenen Sûr)'),
    ('nfx', '3B', 'Zaman ve Ahiret', 'Nefh (üfleme: insana diriltici soluk aktarımı, 3:49 ve Sûr\'a üflenmesi)'),
    ('jHm', '3B', 'Zaman ve Ahiret', 'Cahîm (yakıcı karşılık çukuru ve Nâr ile Furûk: yoğun tutuşmuş kor alev)'),
    ('sEr', '3B', 'Zaman ve Ahiret', 'Saîr ve Suur (çılgınca harlanan ateş ve 54:24 zihinsel sarsıntı)'),
    ('lbs', '3B', 'Zaman ve Ahiret', 'Libâs ve Lebs (örtü/giysi ile 2:42 gerçeği bâtıla karıştırıp bulanıklaştırma)'),
]


def generate_etap_3():
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
    for etap_rank, (bw, tier, category, rationale) in enumerate(ETAP_3_ROOTS_SPEC, 1):
        if bw in seen_bw:
            raise ValueError(f"ETAP_3_ROOTS_SPEC içinde mükerrer kök: {bw}")
        seen_bw.add(bw)
        ar_root = to_arabic_root(bw)
        is_locked = ar_root in locked_roots
        top_lemmas = [lem for lem, _ in roots_lemmas[bw].most_common(4)]
        concept_desc = (
            ROOT_CONFIG[ar_root]['concept_name']
            if (is_locked and ar_root in ROOT_CONFIG)
            else f"Analiz Bekliyor ({', '.join(top_lemmas)})"
        )
        items.append({
            'etap_3_rank': etap_rank,
            'tier': tier,
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

    locked_cnt = sum(1 for i in items if i['is_locked'])
    locked_3a = sum(1 for i in items if i['tier'] == '3A' and i['is_locked'])
    total_3a = sum(1 for i in items if i['tier'] == '3A')
    locked_3b = sum(1 for i in items if i['tier'] == '3B' and i['is_locked'])
    total_3b = sum(1 for i in items if i['tier'] == '3B')
    total_tokens = sum(i['frequency'] for i in items)
    tokens_3a = sum(i['frequency'] for i in items if i['tier'] == '3A')
    tokens_3b = sum(i['frequency'] for i in items if i['tier'] == '3B')

    out_json = {
        'package': 'Faz 1 - Etap 3 (Faz 2 Öncesi Kafa Karıştıran ve Anlamı Doğrudan Belirleyen 131 Kök)',
        'target_count': len(items),
        'locked_count': locked_cnt,
        'tier_3a_target': total_3a,
        'tier_3a_locked': locked_3a,
        'tier_3b_target': total_3b,
        'tier_3b_locked': locked_3b,
        'total_tokens_in_package': total_tokens,
        'tokens_3a': tokens_3a,
        'tokens_3b': tokens_3b,
        'total_corpus_tokens': total_corpus_tokens,
        'etap_3_roots': items,
    }
    json_path = os.path.join(DATA_DIR, 'etap_3_key_roots.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    md_lines = [
        "# ETAP 3: FAZ 2 ÖNCESİ KAFA KARIŞTIRAN VE ANLAMI DOĞRUDAN BELİRLEYEN 131 KÖK HARİTASI",
        "## Tabula Rasa Mesânî Çözümleme Sistemi (v3.0 — 3A Çekirdek 55 + 3B Tam Zırh 76)",
        "",
        "> [!IMPORTANT]",
        f"> **HEDEF KAPSAM:** İlk 221 kök (`100` Top 100 + `5` Çekirdek + `100` İkinci 100 + `16` Etap 2.5 = **%77,12**) mühürlendikten sonra, Faz 2 ayet çözümlemesine geçmeden önce geleneksel algıda en çok anlam kaymasına uğrayan kavramları ve açık Mesânî/Furûk eşleniklerini kapatan **131 kök** ({total_tokens} geçiş) iki aşamada mühürlenir:",
        f"> - **⭐ Etap 3A (Çekirdek Kafa Karıştırıcılar):** {locked_3a} / {total_3a} Kök ({tokens_3a} geçiş -> **%80,14** kümülatif kapsam)",
        f"> - **Etap 3B (Tam Mesânî, Furûk, Hukuk ve Zihin Zırhı):** {locked_3b} / {total_3b} Kök ({tokens_3b} geçiş -> **%83,08** kümülatif kapsam)",
        f"> **Etap 3 İçinde Şu Ana Kadar Mühürlenen:** {locked_cnt} / {len(items)} Kök (Toplam Mühürlü: {len(locked_roots)} Kök)",
        "",
        "| Etap Sıra | Paket | Kategori | Genel Sıra | Kök (Arapça) | Kök (Latin) | Geçiş | Ayet | Örnek | Stratejik Önemi / Kavram Durumu | Durum |",
        "| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |",
    ]
    for it in items:
        badge = "✅ **MÜHÜRLÜ**" if it['is_locked'] else "⏳ *Bekliyor*"
        tier_tag = "⭐ **3A**" if it['tier'] == '3A' else "3B"
        desc = it['concept_label'] if it['is_locked'] else f"{it['rationale']}"
        md_lines.append(
            f"| {it['etap_3_rank']} | {tier_tag} | {it['category']} | {it['global_rank']} | "
            f"`{it['root_arabic']}` | `{it['root_latin']}` | **{it['frequency']}** | {it['unique_ayahs']} | "
            f"{it['sample_ayah']} | {desc} | {badge} |"
        )
    md_lines.append("")

    md_path = os.path.join(DATA_DIR, 'ETAP_3_KAVRAM.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(
        f"Etap 3 JSON üretildi: {json_path} "
        f"({locked_cnt}/{len(items)} mühürlü | 3A: {locked_3a}/{total_3a}, 3B: {locked_3b}/{total_3b})"
    )
    print(f"Etap 3 Markdown üretildi: {md_path}")


if __name__ == '__main__':
    generate_etap_3()
