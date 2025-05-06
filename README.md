# TRAVEL-CAR-RENTAL-RECOMMENDER-SYSTEM
Capstone Project
![image](https://github.com/user-attachments/assets/1519cb22-5520-43ed-bcf4-85d81f23a002)
# Travel and Car Rental Recommender System

## 🚀 Project Overview

This is a dual-system web application that includes:

- **🌍 Travel Recommender**: Suggests attractions, hotels, and restaurants based on user preferences.
- **🚗 Car Rental System**: Allows users to browse and book rental cars.

Both modules are powered by Flask and use structured datasets for recommendations and inventory.

---

## 📦 Setup Instructions

### ✅ Prerequisites
-Python 3.10+
- `pip` (Python package installer)
- Git (optional for cloning)

### 📥 Installation Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/Joshita1306/TRAVEL-CAR-RENTAL-RECOMMENDER-SYSTEM.git
   
2.Navigate to the project folder:
   ```bash
   cd TRAVEL-CAR-RENTAL-RECOMMENDER-SYSTEM
   ```
3.Install dependencies:
flask, pandas, openpyxl

## 📝 File Explanation
Travel Recommender
- data/: Contains Excel and CSV files for attractions, hotels, and restaurants.
- templates/: HTML pages for user interaction (search, results, payment, confirmation).
- app.py: Main backend logic using Flask to serve and process recommendations.

Car Rental System
- data/: CSV file with car listings and details.
- templates/: HTML pages for vehicle search, details, and confirmation.
- app.py: Flask backend for handling car rental logic.

## 4. Running the Projects
## Travel Recommender:
Navigate to the folder:
```bash
cd travelRecommender
```
Run the app:
```bash
python app.py
```
Access at:
```bash
http://localhost:5000
```
## Car Rental System:
Navigate to the folder:
```bash
cd car_rental_system
```
Run the app (change port if needed):
```bash
python app.py --port 5001
```
Access at:
```bash
http://localhost:5001
```
