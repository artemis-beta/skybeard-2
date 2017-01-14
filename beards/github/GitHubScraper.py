#!/usr/bin/env python

from lxml import html
import requests
import json
import re
import parser
import datetime
from bs4 import BeautifulSoup

class GitHubScraper:
   def __init__(self, user, repo, reqBranch='master'):
      self.user = user
      self.repo = repo
      self.url = 'https://github.com/{}/{}'.format(user, repo)
      self.pull_req = []
      self.proj = []
      self.branches = self.getBranches()
      self.contr = []
      self.branch = reqBranch
      self.commits = self.getCommitsAsDict()   

   def getCommitsAsDict(self):
      url = '{}/commits/{}'.format(self.url, self.branch)
      webpage_content = requests.get(url).content.decode('utf-8')
      string = BeautifulSoup(webpage_content, 'html.parser')
      titles = [i.next_element for i in string.find_all('a', attrs={'class' : 'message'})]
      a_ref = [i.get('href') for i in string.find_all('a')]
      commit_id = [i for i in a_ref if('{}/commit/'.format(self.repo) in i)]
      commit_id = [i.split('commit/')[1] for i in commit_id]
      author_id = [i for i in a_ref if('{}/commits/{}?author='.format(self.repo, self.branch) in i)]
      author_id = [i.split('author=')[1] for i in author_id]
    
      out_dict = {}
      for title, com_id, author in zip(titles, commit_id, author_id):
         out_dict[com_id] = {'description' : title, 'author' : author}
      return out_dict
 
   def getBranches(self):
       url = '{}/branches/all'.format(self.url)
       webpage_content = requests.get(url).content.decode('utf-8')
       string = BeautifulSoup(webpage_content, 'html.parser')
       s_ref = string.find_all('div')
       s_ref = [i.get('data-branch-name') for i in s_ref if i.get('data-branch-name')!= None]
       print(s_ref)
       return s_ref

   def stringBranches(self):
       out_str = 'Branches in: {}/{}\n\n'.format(self.user, self.repo)
       for branch in self.branches:
           out_str += '- {}\n'.format(branch)
       return out_str
     
   def stringCommits(self):
        out_str = 'Commits for Branch: {}/{}/{}\n\n'.format(self.user, self.repo, self.branch)
        for key in self.commits:
         out_str += '{}... {}\n{}\n\n'.format(key[:5], self.commits[key]['author'], self.commits[key]['description'])
        return out_str
 
if __name__ == "__main__":
  
  gitHub = GitHubScraper('artemis-beta', 'skybeard-2', 'natrailplugin')
      
