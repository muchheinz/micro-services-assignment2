import grpc
import datetime
import time
import redis

import assignment2_pb2
import assignment2_pb2_grpc

with grpc.insecure_channel('server:50051') as channel:
    stub = assignment2_pb2_grpc.Assignment2Stub(channel)
    response = stub.GetReddit(assignment2_pb2.Empty())

    total_characters = 0
    avg_characters = 0
    num_tweets = 0
    max_data = 280
    metric_time = None
    total_metric_characters = 0

    for data in response:
        print("RESULT" + data.title)

        total_characters += len(data.title)

        print("TOTAL TITLE CHARACTERS: " + str(total_characters))

        conn = redis.StrictRedis(host="redis", port=6379)
        conn.set("title.characters", str(total_characters))

        if len(data.title) < max_data:
            shortest_data = data.title
            shortest_data_author = data.author
            max_tweet = len(shortest_data)
            conn.set("shortest.title", str(shortest_data))
            conn.set("shortest.title.author", str(shortest_data_author))
            print("USER: " + shortest_data_author)

        if metric_time is None or time.time() >= (metric_time + 180):
            metric_time = time.time()

            total_metric_characters += len(data.title)

            conn.set("metric.title", total_metric_characters)
