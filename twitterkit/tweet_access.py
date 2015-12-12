from tweepy.streaming import StreamListener


class TweetStreamer(StreamListener):

    def on_error(self, status_code):
        import pdb; pdb.set_trace()  # XXX BREAKPOINT
        return False


class StdoutStreamer(TweetStreamer):

    def on_data(self, data):
        print data
        return True


class TsvStreamer(TweetStreamer):
    def __init__(self, *args, **kwargs):
        self.filename = kwargs.pop('filename')
        TweetStreamer.__init__(self, *args, **kwargs)

    def on_data(self, data):
        with open(self.filename, 'a') as f:
            f.write(data)
        return True
