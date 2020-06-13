import redis
import assignment2_pb2_grpc
import assignment2_pb2
import grpc
import datetime
import time

with grpc.insecure_channel('server:50051') as channel:
    stub = assignment2_pb2_grpc.Assignment2Stub(channel)
    response = stub.GetTweet(assignment2_pb2.Empty())

    total_characters = 0
    avg_characters = 0
    num_tweets = 0
    max_tweet = 280
    metric_time = None
    total_metric_characters = 0

    for tweet in response:
        print("TWEET" + tweet.text)

        total_characters += len(tweet.text)

        print("TOTAL CHARACTERS: " + str(total_characters))

        conn = redis.StrictRedis(host="redis", port=6379)
        conn.set("total.words", str(total_characters))

        if len(tweet.text) < max_tweet:
            shortest_tweet = tweet.text
            shortest_tweet_user = tweet.user
            max_tweet = len(shortest_tweet)
            conn.set("shortest.tweet", str(shortest_tweet))
            conn.set("shortest.tweet.user", str(shortest_tweet_user))
            print("USER: " + shortest_tweet_user)

        if metric_time is None or time.time() >= (metric_time + 180):
            metric_time = time.time()

            total_metric_characters += len(tweet.text)

            conn.set("metric.characters", total_metric_characters)
