# Optimine Machine Learning Project Readme <br>

# Team Profile <br>

**Tim ID Capstone Project : A25-CS123** <br> 

**Anggota Tim** 
- M891D5X0843 - Imelda Margaret Kristiani - Machine Learning
- M891D5X0496 - Dinda Maulidiyah - Machine Learning
- F891D5Y1288 - Muhammad Hatta Yudia Gymnastiar - Front-End Web & Back-End with AI
- F891D5X1671 - Regina Ayuningrum- Front-End Web & Back-End with AI
- F891D5X1961 - Windi Dwi Astuti- Front-End Web & Back-End with AI <br>

**Optimine Machine Learning Project** <br>

**Arsitektur Sistem Portal Aplikasi** 
Di dalam portal, Machine Learning berperan sebagai engine untuk prediksi dan rekomendasi. Alur ML di sistem ini adalah :
1. Data dikumpulkan dari berbagai bagian operasional (produksi, cuaca, fleet, logistik).
2. Tim ML membersihkan dan melakukan feature engineering lalu melatih 2 model:
    - Model prediksi produksi (Main Planner)
    - Model prediksi loading kapal (Shipping Planner)
3. Model disimpan dalam format .joblib dan di-deploy melalui FastAPI.
4. Portal frontend (dibuat oleh tim FEBE) memanggil endpoint ini setiap planner memilih minggu tertentu.
5. Agentic AI menerima hasil prediksi model → melakukan reasoning → mengubahnya menjadi rekomendasi operasional.
6. UI menampilkan prediksi dan rekomendasi kepada planner.

**Model Al dan pendekatan Agentic Al**
Tim ML membangun dua model utama:
1. Model Prediksi Produksi (Main Planner) -> Model yang digunakan: Random Forest Regressor
2. Hasil Model Truck-to-Ship (Shipping Planner) -> Model: Random Forest + TimeSeriesSplit
Agentic AI Reasoning :
1. Mengambil output model ML
2. Mengidentifikasi risiko operasional
3. Memberikan rekomendasi actionable (misal: alokasi alat, prioritas hauling, dll)

**Dataset yang Dipakai** 




