#show spacecats test plugin
# Adapted from work by LanceMaverick
import telepot
import telepot.aio
from skybeard.beards import BeardChatHandler, regex_predicate
from skybeard.decorators import onerror
from . import GitHubScraper
import re

class GitHubInfo(BeardChatHandler):
    __userhelp__ = """
    The following commands are available:
     """

    __commands__ = [
        ("commits", "checkCommits", "Displays commits for a given repository.\nBranch can be specified, default is 'master'"),
        ("branches", "checkBranches", "Displays branches for a given repository."),
    ]

    @onerror
    async def checkBranches(self, msg):
       Input = msg['text'].replace('/branches ','')
       x = re.findall(r'([\w\d\-]', Input)
       user, repo = x
       gitHubReq =  GitHubScraper.GitHubScraper(user, repo, branch)
       await self.sender.sendMessage(gitHubReq.stringBranches())
  
    async def checkCommits(self, msg):
        Input = msg['text'].replace('/commits ', '')
        x = re.findall(r'([\w\d\-]+)', Input)
        branch = 'master'
        if len(x) == 3:
          user, repo, branch = x
        else:
          user, repo = x
        gitHubReq = GitHubScraper.GitHubScraper(user, repo, branch)
        await self.sender.sendMessage(gitHubReq.stringCommits())
