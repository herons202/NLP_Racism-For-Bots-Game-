## Credit DataSet From : https://github.com/okkyibrohim/id-multi-label-hate-speech-and-abusive-language-detection

# NLP Racism Detector — Informasi Model & Training

Dokumen ini menjelaskan detail teknis tentang model deteksi rasisme (NLP Racism Detection) yang dikembangkan untuk kebutuhan backend **Racist Bot Game**.

---

## 🎮 1. Tujuan Project (Untuk Bot Game)
Dalam konteks **Bot Game** (misalnya bot moderasi Discord, bot chat game, atau NPC interaktif), model ini berfungsi sebagai **filter & moderator otomatis**.
* **Fungsi Utama**: Mendeteksi secara *real-time* jika ada pemain yang mengirimkan chat bernada rasisme, ujaran kebencian berbasis SARA/ras, atau kata-kata makian rasis (seperti varian *N-word*, sebutan rasis lokal, dll.).
* **Output Bot**: Jika terdeteksi (`HS_Race = 1`), bot dalam game dapat melakukan tindakan seperti:
  * Melakukan sensor kata (*censorship*).
  * Memberikan peringatan (*warning*) kepada pemain.
  * Mengurangi poin reputasi/skor pemain di dalam game.
  * Melakukan *kick* atau *ban* otomatis bagi pelanggar berat.

---

## 📊 2. Dataset yang Digunakan
Model ini dilatih menggunakan penggabungan dua dataset:
1. **Dataset Utama (`re_dataset.csv`)**:
   * Dataset dari penelitian Muhammad Okky Ibrohim & Indra Budi (2019).
   * Berisi sekitar 13.000+ tweet dalam bahasa Indonesia dengan label multi-label (HS, Abusive, HS_Race, dll.).
2. **Dataset Tambahan (`racism_dataset_additional.csv`)**:
   * Dataset tambahan yang berfokus pada kata-kata sensitif rasisme (*obfuscated N-word*, hinaan rasial lokal, dll.) untuk menutupi kekurangan data minoritas pada dataset utama.

---

## 🧹 3. Preprocessing Teks (Pencegahan Obfuscation)
Pemain game sering kali menyamarkan kata rasis agar tidak terdeteksi oleh filter teks biasa (misal menulis `n1gg3r`, `n*gga`, `c1n0`). Model ini menggunakan regex pemetaan khusus sebelum teks dimasukkan ke model:
* Mengubah variasi tulisan tersamar (*obfuscated words*) kembali ke bentuk dasar kata rasis standar sehingga model BERT dapat memahaminya dengan baik.
* Menghapus karakter non-alfanumerik yang tidak perlu, username placeholder (`USER`), dan tautan (`URL`).

---

## 🧠 4. Arsitektur Model yang Digunakan
Model yang digunakan adalah **IndoBERT** (`indobenchmark/indobert-base-p1`):
* **Mengapa IndoBERT?**
  * IndoBERT adalah model berbasis transformer **BERT-base** yang dilatih secara khusus menggunakan korpus bahasa Indonesia berskala besar (~220 juta kata).
  * Sangat unggul dalam memahami nuansa bahasa Indonesia, termasuk bahasa gaul, singkatan, dan konteks lokal yang sering muncul dalam chat game/media sosial.
* **Konfigurasi Output**:
  * Menggunakan `AutoModelForSequenceClassification` dengan `num_labels=2` (Binary Classification):
    * **Label `0`**: Non-Rasisme (Normal / Aman).
    * **Label `1`**: Rasisme (Mengandung unsur rasisme/kebencian rasial).

---

## ⚙️ 5. Hyperparameter & Detail Training
Proses pelatihan model diatur dengan konfigurasi berikut:

| Parameter | Nilai | Penjelasan |
| :--- | :--- | :--- |
| **Model Pretrained** | `indobenchmark/indobert-base-p1` | Model dasar berbahasa Indonesia |
| **Max Sequence Length** | `128` token | Panjang maksimal kalimat chat yang diproses |
| **Batch Size** | `16` | Ukuran batch data per iterasi |
| **Epochs** | `5` | Jumlah iterasi pelatihan seluruh dataset |
| **Learning Rate (LR)** | `2e-5` | Kecepatan penyesuaian bobot model |
| **Optimizer** | `AdamW` (decay `0.01`) | Optimizer standar untuk fine-tuning BERT |
| **Scheduler** | `Linear with Warmup` | Mengatur kestabilan learning rate di awal epoch (10% warmup) |
| **Loss Function** | `Weighted CrossEntropyLoss` | Mengatasi *imbalanced dataset* dengan memberi bobot lebih besar pada kelas minoritas (`HS_Race=1`) |

---

## 💾 6. Output Penyimpanan Model
Setelah training selesai, file model akan disimpan dalam dua format:
1. **`best_racism_model.pt`**: Bobot model terbaik (`state_dict`) berdasarkan metrik F1-score pada data validasi.
2. **`saved_racism_model/`**: Folder lengkap berisi model (`model.safetensors`), tokenizer, dan konfigurasi agar siap di-load oleh backend bot game menggunakan library `transformers` Hugging Face.


# id-multi-label-hate-speech-and-abusive-language-detection

## About this data
Here we provide our dataset for multi-label hate speech and abusive language detection in the Indonesian Twitter. The main dataset can be seen at **re_dataset** with labels information as follows:
* **HS** : hate speech label;
* **Abusive** : abusive language label;
* **HS_Individual** : hate speech targeted to an individual;
* **HS_Group** : hate speech targeted to a group;
* **HS_Religion** : hate speech related to religion/creed;
* **HS_Race** : hate speech related to race/ethnicity;
* **HS_Physical** : hate speech related to physical/disability;
* **HS_Gender** : hate speech related to gender/sexual orientation;
* **HS_Gender** : hate related to other invective/slander;
* **HS_Weak** : weak hate speech;
* **HS_Moderate** : moderate hate speech;
* **HS_Strong** : strong hate speech.

For each label, `1` means `yes` (tweets including that label), `0` mean `no` (tweets are not included in that label). 

Due to Twitter's Terms of Service (now X), we do not provide the hydrated tweets (unfortunately, we forget to store the tweet ID when we collect the data). All usernames and URLs in this dataset are changed into USER and URL. 

For text normalization in our experiment, we built typo and slang words dictionaries named **new_kamusalay.csv**, that contain two columns (first columns are the typo and slang words, and the second one is the formal words). Here the examples of mapping:
* *beud --> banget*
* *jgn --> jangan*
* *loe --> kamu*

Furthermore, we also built abusive lexicon list named **abusive.csv** that can be used for feature extraction.

## More detail
If you want to know how this dataset was build (include the explanation of crawling and annotation technique) and how we did our experiment in multi-label hate speech and abusive language detection in Indonesian language using this dataset, you can read our paper in here: https://www.aclweb.org/anthology/W19-3506.pdf.

## How to cite us
This dataset and the other resource can be used for free, but if you want to publish paper/publication using this dataset, please cite this publication:

**Muhammad Okky Ibrohim and Indra Budi. 2019. Multi-label Hate Speech and Abusive Language Detection in Indonesian Twitter. In *ALW3: 3rd Workshop on Abusive Language Online, 46-57*.** (Every paper template may have different citation writting. For LaTex user, you can see **citation.bib**).

## License
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
