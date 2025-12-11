<h1 align="center">Optimine Portal Machine Learning</h1> <br>
Sistem Prediksi Produksi dan Optimasi Distribusi Material untuk Mining Value Chain Optimization (Optimine)

# Tim Profile <br>

**Tim ID Capstone Project : A25-CS123** <br> 

**Anggota Tim** 
- M891D5X0843 - Imelda Margaret Kristiani - Machine Learning
- M891D5X0496 - Dinda Maulidiyah - Machine Learning
- F891D5Y1288 - Muhammad Hatta Yudia Gymnastiar - Front-End Web & Back-End with AI
- F891D5X1671 - Regina Ayuningrum- Front-End Web & Back-End with AI
- F891D5X1961 - Windi Dwi Astuti- Front-End Web & Back-End with AI <br>

# **📌 Deskripsi** <br> 
Machine Learning pada proyek Mining Value Chain Optimization bertujuan untuk menyediakan prediksi operasional mingguan yang membantu dua peran utama :
- Main Planner → prediksi produksi mingguan
- Shipping Planner → prediksi suplai truck ke jetty <br>
Model dibangun menggunakan dataset (produksi, fleet, cycle time, cuaca, logistik) dan menghasilkan prediksi akurat yang nantinya dipakai oleh Agentic AI Portal untuk menjawab pertanyaan dan memberikan insight lintas proses tambang. <br>

# **📌 Tools & Frameworks** <br>
- Python 3.12
- Scikit-Learn
- Pandas & NumPy
- Joblib
- TimeSeriesSplit
- Matplotlib <br>

# **📌 Development Environment**
- Google Colabortory
- Visual Studio Code <br>

# **📌 Struktur Project** <br>
```
OptiMine/
│
├── all_dataset/
│   ├── clean_dataset/          # Dataset hasil pembersihan (cleaned data)
│   ├── feature_dataset/        # Dataset setelah feature engineering
│   ├── merge_dataset/          # Dataset gabungan siap modelling
│   ├── models/                 # Model .joblib hasil training
│   └── raw_dataset/            # Dataset mentah hasil scrapping
│
├── feature_engineering/        # Script untuk pembuatan fitur 
│
├── modeling/                   # Script training model (production & shipping)
│
├── system/                     # File terkait integrasi dengan FE/BE 
│
├── data_celaning.ipynb         # Notebook pembersihan data (EDA + preprocessing)
├── Datasets_raw.ipynb          # Notebook untuk eksplorasi dataset mentah
```

<br>

# **📌 Dataset** <br>
Link Dataset : [Dataset Optimine](https://github.com/ldya9/capstone/tree/fafdb9e65e8cb6234b4e79cbbf2c1ebdf4c0155a/all_dataset/raw_dataset). 
- Fleet
- Heavy Equipment
- Production
- Road
- Ship Schedule
- Stockpile
- Truck to Ship
- Weather <br>

# **📌 How to Use** <br>
- pip install -r requirements.txt
- Download datasets on datasets link : [Dataset Optimine](https://github.com/ldya9/capstone/tree/63a53f67435540177436f65220ce772da615e3ca/all_dataset/merge_dataset).
- Open .ipynb dengan Google Colab <br>
```
[Production] RMSE: 609.66 | R²: 0.9037

=== Production Top-10 Features ===
target_ton              : 0.556003
progress_ratio          : 0.334496
differential            : 0.054442
...

[Truck-to-Ship] Avg RMSE: 636.11 | Avg R²: 0.8953

=== Truck-to-Ship Top-10 Features ===
weekly_ship_demand_ton  : 0.2891
weekly_trips_total      : 0.2530
...
``` 







