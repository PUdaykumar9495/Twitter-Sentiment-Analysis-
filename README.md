

---

# 🐦 Twitter Sentiment Analysis Web App

This project is a **Twitter Sentiment Analysis Web Application** built using **Flask**.
It fetches real-time tweets using the Twitter API and analyzes their sentiment (Positive, Negative, or Neutral) using Natural Language Processing (NLP).

The results are displayed in both textual and graphical format.

---

## 🚀 Features

* Fetch real-time tweets using Twitter API
* Perform sentiment analysis using **TextBlob**
* Clean and preprocess tweet text
* Display sentiment distribution
* Visualize results using **Matplotlib**
* Progress tracking using **tqdm**
* Secure API key handling using **.env file**

---

## 🛠️ Tech Stack

* Python
* Flask
* Tweepy
* TextBlob
* NLTK
* Matplotlib
* dotenv

---

## 📦 Requirements

Install the following dependencies:

```
Flask>=2.2.0
tweepy>=4.14.0
textblob>=0.17.1
matplotlib>=3.7.0
tqdm>=4.65.0
nltk>=3.8.1
python-dotenv>=1.0.0
```

Or install using:

```bash
pip install -r requirements.txt
```

---

## 🔑 Twitter API Setup (Important)

⚠️ You must use **your own Twitter API keys**.

This project does NOT include API keys for security reasons.

### Step 1: Create Twitter Developer Account

1. Go to: [https://developer.twitter.com/](https://developer.twitter.com/)
2. Apply for a Developer Account
3. Create a new Project & App
4. Generate the following credentials:

   * API Key
   * API Secret Key
   * Bearer Token
   * Access Token
   * Access Token Secret

---

### Step 2: Create a `.env` File

In your project root directory, create a file named:

```
.env
```

Add your API credentials like this:

```
API_KEY=your_api_key_here
API_SECRET_KEY=your_api_secret_key_here
BEARER_TOKEN=your_bearer_token_here
ACCESS_TOKEN=your_access_token_here
ACCESS_TOKEN_SECRET=your_access_token_secret_here
```

⚠️ Make sure `.env` is added to your `.gitignore` file so your keys are not uploaded to GitHub.

---


---

## 📊 Output

* Shows number of Positive, Negative, and Neutral tweets
* Displays graphical sentiment distribution using Matplotlib
* Provides cleaned tweet text analysis

---

## 📁 Project Structure (Example)

```
twitter-sentiment-analysis/
│
├── app.py
├── requirements.txt
├── .env
├── templates/
├── static/
└── README.md
```

---

## 🧠 How Sentiment Analysis Works

* Tweets are fetched using **Tweepy**
* Text is cleaned (remove URLs, mentions, hashtags, etc.)
* TextBlob calculates polarity:

  * Polarity > 0 → Positive
  * Polarity < 0 → Negative
  * Polarity = 0 → Neutral
* Results are visualized using Matplotlib

---

## 🔒 Security Note

Never commit your `.env` file to GitHub.

Add this line to `.gitignore`:

```
.env
```

---

## 📌 Future Improvements

* Add database support
* Deploy on cloud (Heroku / Render / AWS)
* Add user authentication
* Add advanced NLP models (BERT)

---

Just tell me 👍
