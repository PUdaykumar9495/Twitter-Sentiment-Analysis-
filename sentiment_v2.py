import os, sys, csv, re, logging, requests
from textblob import TextBlob
import matplotlib.pyplot as plt
from tqdm import tqdm
from dotenv import load_dotenv
import tweepy


class SentimentAnalysisV2:
    def __init__(self):
        load_dotenv()

        
        self.bearer_token = os.getenv("TW_BEARER_TOKEN")
        try:
            self.max_tweets = int(os.getenv("TW_MAX_TWEETS", "500"))
        except ValueError:
            self.max_tweets = 500

        if not self.bearer_token:
            logging.error("Missing TW_BEARER_TOKEN.")
            sys.exit(1)

        self.client = tweepy.Client(bearer_token=self.bearer_token, wait_on_rate_limit=True)

    
    def DownloadData(self, searchTerm: str, NoOfTerms: int):
        csv_path = f"result_{re.sub(r'\\s+', '_', searchTerm)}.csv"

        polarity = 0.0
        positive = wpositive = spositive = 0
        negative = wnegative = snegative = neutral = 0

        if NoOfTerms <= 0:
            NoOfTerms = 10

        if NoOfTerms > self.max_tweets:
            NoOfTerms = self.max_tweets

        tweets = self.fetch_twitter(searchTerm, NoOfTerms)

        
        reddits = self.fetch_reddit_pushshift(searchTerm, NoOfTerms)

        
        all_posts = tweets + reddits

        
        with open(csv_path, "w", newline="", encoding="utf-8") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(["Source", "Text"])

            for source, text in tqdm(all_posts, total=len(all_posts), desc="Processing Sentiment"):
                writer.writerow([source, text])

                p = TextBlob(text).sentiment.polarity
                polarity += p

                if p == 0:
                    neutral += 1
                elif 0 < p <= 0.3:
                    wpositive += 1
                elif 0.3 < p <= 0.6:
                    positive += 1
                elif 0.6 < p <= 1:
                    spositive += 1
                elif -0.3 < p < 0:
                    wnegative += 1
                elif -0.6 < p <= -0.3:
                    negative += 1
                elif -1 <= p <= -0.6:
                    snegative += 1

        total = len(all_posts)

        
        result = {
            "positive": self.percentage(positive, total),
            "wpositive": self.percentage(wpositive, total),
            "spositive": self.percentage(spositive, total),
            "negative": self.percentage(negative, total),
            "wnegative": self.percentage(wnegative, total),
            "snegative": self.percentage(snegative, total),
            "neutral": self.percentage(neutral, total),
            "polarity": round(polarity / total, 2) if total else 0.0
        }

        
        self.plotPieChart(result, searchTerm, total)

        
        negatives = self.extract_negative_texts(all_posts)
        issues = self.extract_issues(negatives)
        suggestions = self.get_improvement_suggestions(issues)
        trending = self.sample_topics(all_posts)
        most_pos, most_neg = self.find_extreme_comments(all_posts)
        detailed_summary = self.generate_sentiment_report(result)

        return {
            "sentiments": result,
            "summary": detailed_summary,
            "trending": trending,
            "issues": issues,
            "suggestions": suggestions,
            "most_positive": most_pos,
            "most_negative": most_neg
        }

    
    def fetch_twitter(self, searchTerm, limit):
        query = f"{searchTerm} lang:en -is:retweet"
        data = []
        try:
            tweets = tweepy.Paginator(
                self.client.search_recent_tweets,
                query=query,
                tweet_fields=["text", "lang"],
                max_results=100,
            ).flatten(limit=limit)

            for tweet in tweets:
                data.append(("Twitter", self.clean_text(tweet.text)))

        except tweepy.TooManyRequests:
            print("⚠ Twitter rate limit exceeded → Using only Reddit data.")
            return []
        except Exception as e:
            print("⚠ Twitter error:", e)
            return []

        return data

    
    def fetch_reddit_pushshift(self, searchTerm, limit):
        url = f"https://api.pullpush.io/reddit/search?query={searchTerm}&size={limit}"
        try:
            response = requests.get(url, timeout=10).json()
            posts = response.get("data", [])
        except:
            print("⚠ Reddit fetch error.")
            return []

        data = []
        for post in posts:
            text = self.clean_text(post.get("title", "") + " " + post.get("selftext", ""))
            if text.strip():
                data.append(("Reddit", text))

        return data

    
    def clean_text(self, text):
        text = re.sub(r"https?://\S+", "", text)
        text = re.sub(r"@[A-Za-z0-9_]+", "", text)
        text = re.sub(r"#[A-Za-z0-9_]+", "", text)
        text = re.sub(r"[^0-9A-Za-z \t]", " ", text)
        return " ".join(text.split())

    
    def percentage(self, part, whole):
        return round(100 * float(part) / float(whole), 2) if whole else 0

    
    def plotPieChart(self, result, searchTerm, total):
        labels = [
            f'Positive [{result["positive"]}%]',
            f'Weakly Positive [{result["wpositive"]}%]',
            f'Strongly Positive [{result["spositive"]}%]',
            f'Neutral [{result["neutral"]}%]',
            f'Negative [{result["negative"]}%]',
            f'Weakly Negative [{result["wnegative"]}%]',
            f'Strongly Negative [{result["snegative"]}%]'
        ]
        sizes = [
            result["positive"], result["wpositive"], result["spositive"],
            result["neutral"], result["negative"], result["wnegative"], result["snegative"]
        ]
        colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(labels, loc="best", fontsize=8)
        plt.title(f"Sentiment Analysis (Twitter + Reddit) for '{searchTerm}' | {total} posts")
        plt.axis("equal")
        plt.tight_layout()
        plt.savefig("static/chart.png")
        plt.close()

    

    
    def extract_negative_texts(self, posts):
        return [text for _, text in posts if TextBlob(text).sentiment.polarity <= 0.1]

    
    def extract_issues(self, texts):
        issue_keywords = {}
        problem_words = ["issue", "problem", "error", "bug", "slow", "crash", "bad",
                         "difficult", "confusing", "expensive", "lag", "poor",
                         "not", "missing", "hate", "fail"]

        for t in texts:
            for w in t.lower().split():
                if w in problem_words:
                    issue_keywords[w] = issue_keywords.get(w, 0) + 1

        return [w for w, _ in sorted(issue_keywords.items(), key=lambda x: x[1], reverse=True)[:10]]

    
    def get_improvement_suggestions(self, issues):
        suggestions = []
        mapping = {
            "slow": "Improve performance and optimize speed.",
            "expensive": "Lower pricing or add cheaper options.",
            "confusing": "Enhance UI/UX for better clarity.",
            "crash": "Fix stability and crashing issues.",
            "bug": "Fix reported bugs.",
            "missing": "Add important missing features.",
            "error": "Improve error handling.",
            "poor": "Enhance product quality."
        }
        for i in issues:
            suggestions.append(mapping.get(i, f"Investigate and improve issues related to '{i}'."))
        return suggestions

    
    def sample_topics(self, posts, limit=10):
        words = {}
        for _, text in posts:
            for w in text.lower().split():
                if len(w) > 4:
                    words[w] = words.get(w, 0) + 1
        return [w for w, _ in sorted(words.items(), key=lambda x: x[1], reverse=True)[:limit]]

    
    def find_extreme_comments(self, posts):
        if not posts:
            return ("No data", "No data")

        best = max(posts, key=lambda x: TextBlob(x[1]).sentiment.polarity)
        worst = min(posts, key=lambda x: TextBlob(x[1]).sentiment.polarity)
        return best[1], worst[1]

    
    def generate_sentiment_report(self, r):
        summary = []
        if r["polarity"] > 0.2:
            summary.append("Overall sentiment is positive. People show support and optimism.")
        elif r["polarity"] < -0.2:
            summary.append("Overall sentiment is negative. People express frustration or complaints.")
        else:
            summary.append("Overall sentiment is mixed with no strong polarity.")

        summary.append(f"Neutral posts are {r['neutral']}%, showing many factual or non-emotional discussions.")

        if r["spositive"] > 5:
            summary.append("There is a noticeable amount of highly positive excitement.")
        if r["snegative"] > 5:
            summary.append("Strong negative opinions suggest major concerns among users.")

        return " ".join(summary)
