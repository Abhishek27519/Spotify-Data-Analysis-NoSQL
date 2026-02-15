# Spotify NoSQL Data Analysis

A Python-based data analysis tool that explores trends in music popularity, release timing, and track characteristics using a dataset of 10,000+ songs. This project was developed as part of a Master's Database Systems course.

## 🚀 Features

The application performs four key analysis tasks using MongoDB aggregation pipelines:

* **Trend Analysis:** Visualizes the relationship between song popularity, danceability, and energy.
* **Label Comparison:** Analyzes the top 10 record labels to compare "Energy & Rhythm" vs. "Vocal & Instrumental" characteristics.
* **Release Timing Impact:** Examines how the day of the week a song is released impacts its tempo and popularity.
* **Duration vs. Popularity:** Correlates track duration with popularity trends over the years.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Database:** MongoDB (NoSQL)
* **Libraries:** `pymongo`, `matplotlib`, `tkinter`, `Pillow`

## ⚙️ Database Setup (Required)

Since this project connects to a local MongoDB instance, you must import the dataset before running the script.

1.  **Install MongoDB:** Ensure you have MongoDB Community Server installed and running locally on port `27017`.
2.  **Open MongoDB Compass:** Connect to `mongodb://localhost:27017`.
3.  **Create Database:**
    * Click the **+** button to create a database.
    * **Database Name:** `Spotify`
    * **Collection Name:** `Songs`
4.  **Import Data:**
    * Navigate to the `Spotify` database and `Songs` collection.
    * Click the **Add Data** dropdown > **Import File**.
    * Select the file: `Dataset/Top 10000 Songs on Spotify 1960-Now.csv`.
    * Select **CSV** as the file type and click **Import**.

## 🚀 How to Run

Once the database is ready:

1.  Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the application:
    ```bash
    python spotify.py
    ```