"""
Contains all the functions for scraping 
""" 
import requests
from collections import defaultdict

def get_repos(username): 
    """ given a valid git username, get all the repos in a list 
    Args: 
        username (str): username of github user
    Returns: 
        repos (list): list of repos as strings
    """
    url = f'https://api.github.com/users/{username}/repos'
    data = requests.get(url).json()
    
    # automatically skips over private repos
    repos = [repo['name'] for repo in data]
  
    return repos

def get_lang_stats(username, repo): 
    """ given a user and a repo, get all the lang stats 
    Args: 
        username (str): github user 
        repo (str): repo name 
    Returns: 
        stats (dct): stats in num of bytes 
    """
    url = f'https://api.github.com/repos/{username}/{repo}/languages'
    stats = requests.get(url).json()
    
    return stats

def get_total_stats(username): 
    """ gets the language stats of a given user 
    Args: 
        username (str): username of github user 
    Returns: 
        stats (dict): Lang stats as a percent
    """
    repos = get_repos(username)

    byte_stats = defaultdict(int)
    total = 0
    # get each repo stat and add it. 
    for repo in repos: 
        curr_stats = get_lang_stats(username, repo) # returns a dct
        for lang, bytes_ in curr_stats.items(): # go thru the dct and add to stats
            byte_stats[lang] += bytes_
            total += bytes_

    # convert the bytes stats into percentages 
    stats = {}
    for lang, bytes_ in byte_stats.items(): 
        stats[lang] = bytes_ / total
    
    print(f"{username}'s GitHub Stats: {stats}") # for debugging 
    return stats

# example (don't have a main func for utils please)
alex_stats = get_total_stats('kloafe')

