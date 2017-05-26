"""
A Skybeard moustache that shows spacecats on request

Adapted from work by LanceMaverick

"""
from os.path import basename
import random
import logging
from urllib.request import urlopen
from skybeard.beards import BeardChatHandler
from skybeard.predicates import regex_predicate


class PostCats(BeardChatHandler):
    __userhelp__ = """
    Say give me spacecats or show me spacecats if you want
    to, well, see cats in space."""

    __commands__ = [
        (regex_predicate('(give|show) me spacecats'), 'send_cat',
         "Sends a spacecat image"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def send_cat(self, msg):
        cat_photos = [
            'http://i.imgur.com/bJ043fy.jpg',
            'http://i.imgur.com/iFDXD5L.gif',
            'http://i.imgur.com/6r3cMsl.gif',
            'http://i.imgur.com/JpM5jcX.jpg',
            'http://i.imgur.com/r7swEJv.jpg',
            'http://i.imgur.com/vLVbiKu.jpg',
            'http://i.imgur.com/Yy0TCXA.jpg',
            'http://i.imgur.com/2eV7kmq.gif',
            'http://i.imgur.com/rnA769W.jpg',
            'http://i.imgur.com/08mxOAK.jpg',
            'http://i.imgur.com/Ct5GsQn.jpg',
        ]

        try:
            choice = random.choice(cat_photos)
            await self.sender.sendChatAction('upload_photo')
            await self.sender.sendPhoto(
                (basename(choice), urlopen(choice)))
        except Exception as e:
            logging.error(e)
            await self.sender.sendPhoto(
                ("cat_photo.jpg",
                 urlopen('http://cdn.meme.am/instances/500x/55452028.jpg')))
            raise e
