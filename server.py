import assignment2_pb2_grpc
import assignment2_pb2
from concurrent import futures
import grpc
import time
import csv


class TweetService(assignment2_pb2_grpc.Assignment2Servicer):
    def GetTweet(self, request, context):
        tweets = open("training.1600000.processed.noemoticon.csv", 'r')

        for tweet in tweets:
            split_tweet = [x.replace("\"", "") for x in tweet.split('","')]
            tweet_object = assignment2_pb2.Tweet(target=int(split_tweet[0]), id=int(split_tweet[1]),
                                                 date=split_tweet[2], flag=split_tweet[3],
                                                 user=split_tweet[4], text=split_tweet[5])

            time.sleep(0.5)
            yield tweet_object

    def GetReddit(self, request, context):

        with open('reddit.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')

            first_line = True

            for row in reader:
                if not first_line:
                    reddit_data = assignment2_pb2.RedditData(id=str(row[0]), title=str(row[1]), score=int(row[2]),
                                                             author=str(row[3]))
                    time.sleep(1)
                    yield reddit_data

                else:
                    first_line = False
                    continue


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    assignment2_pb2_grpc.add_Assignment2Servicer_to_server(TweetService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


serve()
