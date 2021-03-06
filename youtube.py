""" Simple Youtube Analytics """
from datetime import date
import requests
from database import Database
import helpers

class Youtube():
    """ A YouTube analytics object """
    def __init__(self):
        data_file = open("secrets/youtube.txt", "r")
        self.channel_id = data_file.readline()
        self.key = data_file.readline()
        self.database = Database()

    def create_table(self):
        """ Creates table in sqlite database for youtube """
        columns = [{"name": "subscribers", "type": "int"},
                   {"name": "date", "type": "datetime default current_timestamp"}]
        self.database.create_table("youtube", columns)

    def subscribers(self):
        """ Get number of subs, daily subs, print out """
        subscribers = self.get_subscribers()
        self.write_subscribers_to_db(subscribers)
        daily_subscriptions = self.daily_subscribers()
        daily_sub_string = helpers.pretty_num_to_s(daily_subscriptions)

        print("YouTube")
        print("{0} Subscribers ({1})".format(helpers.num_to_s(int(subscribers)), daily_sub_string))

    def get_subscribers(self):
        """ Get the number of subscribers to channel """
        payload = {"part": "statistics",
                   "channel": self.channel_id,
                   "key": self.key,
                   "forUsername": "MrFish235"}
        url = "https://www.googleapis.com/youtube/v3/channels"
        request = requests.get(url, params=payload)
        return request.json()["items"][0]["statistics"]["subscriberCount"]

    def write_subscribers_to_db(self, subscribers):
        """ Write the number of subscribers to the database """
        self.database.cursor.execute("INSERT INTO youtube (subscribers) VALUES({0})"\
                                     .format(subscribers))
        self.database.connection.commit()

    def daily_subscribers(self):
        """ Get the number of subscribers since midnight """
        daily_data = self.database.cursor\
                     .execute("SELECT * from youtube WHERE date >= '{0}'"\
                     .format(date.today())).fetchall()
        first = daily_data[0]
        last = daily_data[-1]
        return last[0] - first[0]

if __name__ == "__main__":
    YOUTUBE = Youtube()
    YOUTUBE.subscribers()
