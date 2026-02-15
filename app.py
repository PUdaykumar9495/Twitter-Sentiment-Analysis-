
from flask import Flask, render_template, request
from sentiment_v2 import SentimentAnalysisV2
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    chart_path = None
    query = None

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        try:
            requested = int(request.form.get("count", 50))
        except (TypeError, ValueError):
            requested = 50

        sa = SentimentAnalysisV2()
        if requested > sa.max_tweets:
            requested = sa.max_tweets

        result = sa.DownloadData(query, requested)
        chart_path = "/static/chart.png"

    return render_template("index.html", result=result, chart_path=chart_path, query=query)


if __name__ == "__main__":
    app.run(debug=True)
