# TABULA RASA MESÂNÎ ÇÖZÜMLEME SİSTEMİ
## KÖK VE AYET ANALİZLERİ ZORUNLU KALİTE ANAYASASI (v3.0)

Bu kurallar, sistemdeki tüm kök analizlerinde (Faz 1) ve ayet blokları çözümlemelerinde (Faz 2) tavizsiz olarak uygulanacak mutlak doğrulama filtreleridir:

1. **Gereksiz Alt-Sayım Yasağı ve Morfoloji Sadakati:**
   - Kökün toplam geçiş sayısını tutturmak için tahmini alt-isim/mastar kovaları üretilmez.
   - İstatistikte yalnızca genel ölçek (toplam geçiş / ayet) ve anlamı doğrudan belirleyen **fiil babları (Form I, II, IV, X vb.)** ile **harf-i cer kalıpları** (`آمن بـ` vs `آمن لـ`, `صلى على` vs `صلى لـ`) esas alınır.

2. **İbn Fâris Birebir İktibas & Çoklu Asıl Kuralı:**
   - `ibn_faris_asl` alanına başka sözlüklerden (*Lisânü'l-Arab*, *es-Sıhâh* vb.) cümle karıştırılamaz ve yapay zeka şerhi eklenemez.
   - İbn Fâris kökte *"أصلان / أصول متباينة"* (birden fazla bağımsız asıl) sayıyorsa, bunlar tek asılmış gibi birleştirilemez; ayrı ayrı belirtilir. Metin içi atlamalar kesinlikle `...` ile gösterilir.

3. **Sami Dilleri Ses Yasası ve Dil Ayrımı Kuralı:**
   - Tezi desteklemek için Sami dilleri kelimelerine sözlüklerde olmayan veya zıt anlamlar yüklenemez.
   - Strong/BDB içindeki İbranice maddeler ile Kitâb-ı Mukaddes Aramicesi maddeleri birbirine karıştırılamaz.
   - Islıklı ünsüz (Proto-Sami sibilant) ses yasasına sadık kalınır:
     * Proto-Sami `*s₂` -> Arapça `ش` (š) = İbranice `שׂ` (ś) = Sebece `s₂` = Aramice `ס/שׂ`.
     * Proto-Sami `*s₁` -> Arapça `س` (s) = İbranice `שׁ` (š) = Sebece `s₁`.

4. **Kaynak ve Referans Disiplini:**
   - Canlı web aramasında birebir doğrulanmamış hiçbir CAD, BDB veya Mekâyîs cilt/sayfa numarası tahmini yazılamaz. Yalnızca eser adı ve doğrudan madde başlığı verilir.

5. **"Eşkökenlisi Yok / Semantik Ayrışma Var" Dürüstlüğü:**
   - Bir Sami dilinde paralel kelime yoksa veya kök farklı bir anlama kaymışsa boşluk zorlanamaz. Açıkça "doğrudan paralel tespit edilmedi" veya "sesçe eşkökenli ancak semantik ayrışma var" olarak kaydedilir.

6. **Tek Çekirdek ve Kök-Dal Zorunluluğu (`unified_core_mechanism`):**
   - 1 kavram birden fazla alakasız veya çelişen anlama gelemez. Kökün Kur'an'daki tüm geçişleri tek bir değişmez çekirdek mekanizma altında %100 sıfır çelişkiyle çalışmalıdır.
   - Bağlamdaki görünür farklar keyfî anlam değişimi değil; yalnızca fiil babı, harf-i cer ve özne/nesne ilişkisinden kaynaklanır.

7. **Çift Yönlü MesÂNî (Ters-Anlam) Stres Testi:**
   - Bir köke (A) verilen anlamın tam tersi alındığında, bu ters kavram Kur'an'ın kendi metin içi Mesânî zıttının (B) geçtiği diğer tüm ayetlerdeki kullanımlarıyla %100 örtüşmek zorundadır.
   - "B'nin tüm Kur'an kullanımlarının tam tersi, A tanımımı doğruluyor mu?" testi geçilmeden kök kilitlenemez.

8. **Aynı Ayet İçi Furûk Kuralı (Terâdüf / Eşanlamlılık Yasağı):**
   - Kur'an'da aynı ayette veya paralel yapılarda yan yana gelen yakın kavramların hiçbiri eşanlamlı değildir (`Şekk / Rayb`, `Halaka / Fatara`, `Adl / Kıst`, `Salât / Zekât`, `Afv / Mağfiret` vb.).
   - Aralarındaki mekanik fark açıkça ayrıştırılmalıdır.

9. **Rasm-ı Osmânî (Harekesiz İskelet) ve Alternatif Okuma Denetimi:**
   - Özgün metin noktasız ve harekesiz ünsüz iskeletidir. İskeletin izin verdiği alternatif okumalar (etken/edilgen, farklı vezinler) denetlenir; harekeleme Mesânî veya sentaksla çelişiyorsa iskeletin izin verdiği okuma kanıtlarıyla not edilir.

10. **Sözlükler Eleme ve Hakem Masası Kuralı (Sözlük Dogmatizmini Önleme):**
   - Hiçbir sözlük yazarının (İbn Fâris dahil) otoritesi dogmatize edilemez. *Mekâyîsü'l-Luğa*, *Kitâbü'l-Ayn*, *Lisânü'l-Arab*, *es-Sıhâh* ve *el-Müfredât* gibi klasik kaynakların iddiaları toplanır; Sami arkeolojisi, Çift Yönlü Mesânî, %100 Ayet Stres Testi ve harf-i cer vektör uyumu süzgecinden geçirilerek hakem masası kararı gerekçelendirilir.

11. **İki Yönlü Önyargı ve Anakronizm Kilidi:**
   - Geleneksel dinî kalıplardan kaçarken 21. yüzyıl teknoloji/bilimkurgu jargonu (`fabrika ayarı`, `kalibrasyon`, `yazılım`, `donanım`, `sinyal`, `kozmik görevli`) kullanılamaz; her zaman sade ve zamansız Türkçe tercih edilir.
   - Bir kökün nihai tanımında açıklanmamış başka dinî terimler döngüsel olarak bırakılamaz ve iki ayrı tarihsel kök (örn. `*m-l-k` ile `*l-ʾ-k`) morfoloji etiketi yüzünden zorla tek çekirdeğe sıkıştırılamaz.

12. **Otomatik Çift Yönlü Mesânî Simetri ve Sıfır Mükerrer Ayet Sigortası:**
   - Kilitli bir A kökü, kilitli başka bir B kökünü `mesani_opposite.roots` alanında zıt kutup olarak gösteriyorsa; B kökünde de A'nın karşılıklı referansı zorunlu olarak bulunur (`verify_project.py` %100 simetriyi doğrular).
   - Türkçe referans metninde (`data/quran-turkish.txt`) 6.236 ayetin tamamı birebir eşleşmek ve sıfır mükerrer ayet içermek zorundadır. Faz 2'de bu dosya değil, doğrudan Arapça Rasm + Kilitli Sözlük + Edat/Harf-i Cer Haritası esas alınır.

13. **Aşırı Mekanikleşme Yasağı ve Yaşayan Türkçe (Okunabilirlik ve Sentaks Doğallığı İlkesi):**
    - Tek çekirdek mekanizması ve Furûk ayrımları motamot/robotik bir kelime yığınına dönüştürülemez.
    - Türkçe cümle yapısı (özne-tümleç-yüklem akışı) korunmalı; okunduğunda yapay zeka çıktısı veya kuru teknik şema hissi veren mekanik dizilimler engellenmelidir.
    - Metin, parantez içi tefsir eklemelerine boğulmadan; mühürlü kavramın saf mekaniğini Türkçenin yaşayan, duru ve estetik gücüyle doğrudan yansıtmalıdır. Faz 2 ayet blokları hem %100 filolojik doğruluğu hem de %100 Türkçe okunabilirlik akıcılığını aynı anda sağlamak zorundadır.
