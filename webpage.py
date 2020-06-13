from flask import Flask
import redis

app = Flask(__name__)


@app.route('/')
def print_logs():
    output = ""
    conn = redis.StrictRedis(host="redis", port=6379)
    total = conn.get('total.words')
    shortest = conn.get('shortest.tweet')
    total_metric = conn.get('metric.characters')
    shortest_tweet_user = conn.get('shortest.tweet.user')

    total_chars = conn.get('title.characters')
    shortest_title = conn.get('shortest.title')
    metric_title = conn.get('metric.title')
    shortest_author = conn.get('shortest.title.author')

    output += "<div style=\"color:blue;text-align:center;\">"

    if total is not None and metric_title is not None and shortest_tweet_user is not None and shortest is not None and total_metric is not None and total_chars is not None and shortest_title is not None and shortest_author is not None:
        return output + "Total number of characters so far: " + str(
            total.decode()) + "</div></br><div style=\"color:blue;text-align:center;\">Shortest tweet so far: " + str(
            shortest_tweet_user.decode()) + " \" " + str(
            shortest.decode()) + "\"</div><br><div style=\"color:blue;text-align:center;\">Total number of characters in the last 3 minutes: " + str(
            total_metric.decode()) + "</div>" + "<br><div style=\"color:blue;text-align:center;\">" + "Total number of characters so far for the title: " + str(
            total_chars.decode()) + "</div></br><div style=\"color:blue;text-align:center;\">Shortest title so far: " + str(
            shortest_title.decode()) + " \" " + str(
            shortest_author.decode()) + "\"</div><br><div style=\"color:blue;text-align:center;\">Total number of characters in the last 3 minutes: " + str(
            metric_title.decode()) + "</div>"

    else:
        return output


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
