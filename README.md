# Project Menggunakan Streamlite (Belajar Analisis Data dengan Python)

## Project Analisis Data

Repository ini berisi proyek data analytics yang saya kerjakan. Deployment in **Streamlit**

## Deskripsi

Proyek ini bertujuan untuk menganalisis data pada Air Quality Dataset. Tujuan akhirnya adalah untuk menghasilkan wawasan dan informasi yang berguna dari data yang dianalisis.

## Struktur Direktori

- **/dataset**: Direktori ini berisi data mentah yang digunakan dalam proyek, dalam format .csv .
- **/dashboard**: Direktori ini berisi main.py yang digunakan untuk membuat dashboard hasil analisis data.
- **/dashboard/data**: Berisi data-data dari setiap stasiun dalam format .csv.
- **notebook.ipynb**: File ini yang digunakan untuk melakukan analisis data.
- **url.txt**: Berisi link deploy ke steamlite.

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir air-quality-analysis
cd air-quality-analysis
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Instalasi

1. Clone repository ini ke komputer lokal Anda menggunakan perintah berikut:

   ```shell
   git clone https://github.com/alkifani/air-quality-analysis.git
   ```

2. Pastikan Anda memiliki lingkungan Python yang sesuai dan pustaka-pustaka yang diperlukan. Anda dapat menginstal pustaka-pustaka tersebut dengan menjalankan perintah berikut:

    ```shell
    pip install streamlit
    pip install -r requirements.txt
    ```

## Penggunaan
1. Masuk ke direktori proyek (Local):

    ```shell
    cd air-quality-analysis
    cd dashboard
    streamlit run dashboard.py
    ```
    Atau bisa dengan kunjungi website ini [Project Data Analytics](https://mufadhdhal-air-quality-analysis.streamlit.app/)

## Kontribusi
Anda dapat berkontribusi pada proyek ini dengan melakukan pull request. Pastikan untuk menjelaskan perubahan yang Anda usulkan secara jelas dan menyeluruh.


