# KUR'AN EDAT, HARF-İ CER VE KÖKSÜZ TEMEL KAVRAMLAR HARİTASI
## Tabula Rasa Mesânî Çözümleme Sistemi (v3.0 — Faz 2 Hazırlık Omurgası)

> [!IMPORTANT]
> Kur'an morfoloji korpusundaki 77.429 kelimenin **%35,5'i** üçlü Arapça kök etiketi (`ROOT:`) taşımaz. Bu katman; cümlenin yönünü, fail-mef'ûl dengesini, şart olasılığını ve fiillerin anlam eksenini belirleyen **harf-i cerler, bağlaçlar, edatlar ve köksüz özel/ödünç kavramlardan** oluşur. Faz 2'de ayetler doğrudan Arapça iskelet metinden sıfırdan çözümlenirken bu harita `locked_roots.json` ile birlikte temel referans olarak kullanılır.

---

### 1. Temel Harf-i Cerlerin (Yön Vektörlerinin) Mekaniği

| Harf-i Cer | Çekirdek Vektör | Mekanik İşlevi ve Mesânî Karşıtı | Çıpa Ayetler |
| :---: | :--- | :--- | :--- |
| **`بِـ`** | Bitişme, araç, bedel | Eylemin hangi araçla, dayanakla veya bedelle yapışık gerçekleştiğini belirler (`ذَهَبَ` gitti vs `ذَهَبَ بِـ` götürdü). | `1:1`, `2:3`, `2:17` |
| **`فِي`** | İçerme, alan kuşatması | Mekân, zaman veya durumun iç sınırlarını çizer. | `2:2`, `2:11`, `2:179` |
| **`عَلَى`** | Üstten basma, yükümlülük, aleyh | Fiziksel üstünlük, sorumluluk yükü ve aleyhe dönüş (`لِـ` ile tam zıt vektör). | `2:286`, `2:183`, `33:56` |
| **`لِـ`** | Tahsis, aidiyet, lehine, amaç | Bir hakkın/eylemin kime tahsis edildiğini ve kimin yararına işlediğini gösterir (`عَلَى` zıttı). | `1:2`, `2:286`, `51:56` |
| **`إِلَى`** | Varış noktası, hedef ucu | Hareketin veya sürenin uzanıp ulaştığı hedef sınır (`مِنْ` başlangıç vektörünün eşleniği). | `2:156`, `2:187`, `5:6` |
| **`مِنْ`** | Çıkış noktası, parça alma, cins | Başlangıç kaynağı, bütünden parça seçimi (`مِمَّا رَزَقْنَٰهُمْ`) ve olumsuzda kesin genelleme. | `2:3`, `17:1`, `11:6` |
| **`عَنْ`** | Ayrılma, uzaklaşma, yerine geçme | Merkezden kopma, yüz çevirme, savuşturma veya birinin yerine bedel ödeme. | `2:48`, `2:130`, `6:153` |
| **`كَـ`** | Benzetme ve nitelik denkliği | İki olgu arasında ortak özellik köprüsü kurar. | `2:17`, `2:74`, `42:11` |
| **`حَتَّى`** | Son sınır ve kırılma eşiği | Bir sürecin hangi kesin eşiğe kadar sürdüğünü ve nerede kırıldığını belirtir. | `2:187`, `13:11`, `97:5` |
| **`مَعَ`** | Eşzamanlı birliktelik | Aynı saf, aynı zaman ve destek birlikteliğini kodlar. | `2:43`, `2:153`, `94:5` |

---

### 2. Bağlaç, Şart ve Olumsuzlama Furûku (Eşanlamlılık Yasağı)

* **`وَ` / `فَـ` / `ثُمَّ`:** `وَ` sırasız birliktelik, `فَـ` arada boşluksuz anlık ardışıklık veya doğrudan neden-sonuç, `ثُمَّ` ise belirgin zaman/aşama aralığı koyar (`80:21-22`).
* **`إِذَا` / `إِنْ` / `لَوْ`:** `إِذَا` kesin veya olağan beklenen durum (`5:6` kalktığınızda), `إِنْ` belirsiz/ender olasılık (`5:6` eğer hasta olursanız), `لَوْ` ise gerçekleşmemiş varsayım (`21:22` olsaydı) kurar.
* **`إِنَّمَا` / `مَا ... إِلَّا`:** Hükmü yalnızca belirtilen odağa hapseder ve dışındaki tüm ihtimalleri eler (`49:10`).
* **`بَلْ`:** Önceki yanlış sanıyı boşa çıkarıp doğrudan gerçeğe çevirir (`2:154`, `21:18`).
* **`لَا` / `مَا` / `لَمْ` / `لَنْ`:** `لَمْ` geçmişi kesin sıfırlar, `لَنْ` geleceği kesin kapatır (`2:24` yapamadınız ve asla yapamayacaksınız).

---

### 3. Korpusta Kök Etiketi Taşımayan 5 Anahtar Kavram

| Kavram | Geçiş | Etimoloji ve Dilsel Köken | Tabula Rasa Çekirdek Anlamı |
| :---: | :---: | :--- | :--- |
| **`جَهَنَّم`** | **77** | İbranice *Gê-Hinnôm* / Süryanice *Gēhannā* + Arapça *bihr-i cihinnâm* (derin çukur) | Kasıtlı yıkım ve kibir seçimleriyle sürüklenecek derin, yakıcı karşılık çukuru (`2:206`, `67:6-8`). |
| **`تَوْرَاة`** | **18** | İbranice *Tōrāh* (`ي-ر-ه`: yol göstermek, öğretmek, yasa koymak) | Mûsâ'ya ve İsrailoğullarına verilen önceki yazılı yasa ve yön gösterici öğreti (`3:3`, `5:44`). |
| **`إِنْجِيل`** | **12** | Yunanca *euangélion* -> Süryanice/Habeşçe ('iyi haber, müjde') | Îsâ'ya verilen, önceki yasayı doğrulayan aydınlatıcı iyi haber metni (`3:3`, `5:46`). |
| **`وَيْل`** | **40** | Klasik Arapça `و-ي-ل` ('şiddetli yıkım ve çöküş ünlemi') | Gerçeği çarpıtan ve haksızlık edenleri bekleyen ağır yıkım uyarısı (`2:79`, `83:1`, `107:4`). |
| **`ذُو / ذَات`** | **116** | Proto-Sami `*ḏū` ('sahip olan, üzerinde taşıyan') | Bir niteliği, hakkı veya öz-içeriği bizzat üzerinde taşıyan (`ذُو ٱلْفَضْلِ`, `ذَاتِ ٱلصُّدُورِ`). |
