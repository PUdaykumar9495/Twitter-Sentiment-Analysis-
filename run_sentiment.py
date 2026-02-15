import argparse
from sentiment_v2 import SentimentAnalysisV2


def main():
    parser = argparse.ArgumentParser(description="Run SentimentAnalysisV2 on a search term (Twitter + Reddit)")
    parser.add_argument("term", help="Search term to query (string)")
    parser.add_argument("-n", "--num", type=int, default=50, help="Number of posts/tweets to fetch (int)")
    args = parser.parse_args()

    sa = SentimentAnalysisV2()
    result = sa.DownloadData(args.term, args.num)
    print(result)


if __name__ == "__main__":
    main()
