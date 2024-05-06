"""
Contains all the functions for scraping 

- please keep note that theres a limit of 60 api calls per hour per IP address (unathorized API calls)
- how to do authorized API calls? 

# example.... How to get token???
login = requests.get('https://api.github.com/search/repositories?q=github+api', auth=(username,token))


""" 
import requests
from collections import defaultdict
import time 

def get_repos(username): 
    """ given a valid git username, get all the repos in a list 
    Args: 
        username (str): username of github user
    Returns: 
        repos (dict): dict of repos with the owner as the value
    """
    url = f'https://api.github.com/users/{username}/repos'
    data = requests.get(url).json()
    
    # automatically skips over private repos
    repos = {repo['name']: repo['owner']['login'] for repo in data}

    return repos

def get_repo_shas(owner, repo, user): 
    """ gets the SHAs from a given repo and stores in a list. 
    get_repo_shas
    """
    time.sleep(1)
    url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    commits_log = requests.get(url).json()

    shas = []
    for commit in commits_log: 
        try: 
            if commit['author']['login'] == user: # cross checks against our user
                shas.append(commit['sha']) # appends if correct user
        except: 
            pass # am getting a nonetype error here, if someone could look at it that would be great
    return shas


def get_commit_files(owner, repo, user): 
    shas = get_repo_shas(owner, repo, user)

    file_types = defaultdict(int)
    for sha in shas: 
        time.sleep(1)
        url = f'https://api.github.com/repos/{owner}/{repo}/commits/{sha}'
        data = requests.get(url).json()
        
        for file in data['files']: 
            end = file['filename'].split('.')[-1].lower() # gets the end of a file 
            file_types[end] += file['additions'] + file['deletions'] # gets the bytes adjusted 
    
    return dct_to_percents(file_types) # convert the final dct to percents at the end

# test for getting stats thru commits...
test = get_repos('agonzalez22')
for key, value in test.items(): 
    get_commit_files(value, key, 'agonzalez22')
    break 

""" GETTING GITHUB STATS THRU REPO STATS """
def dct_to_percents(dct): 
    """ takes a dict and converts it's contents to percent values...
    """
    total = sum(list(dct.values())) # calculate the toal 
    return {key: val/total for key, val in dct.items()} # return new dct 
        
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
    stats = dct_to_percents(byte_stats)
    
    print(f"{username}'s GitHub Stats: {stats}") # for debugging 
    return stats

# example (don't have a main func for utils please)
# alex_stats = get_total_stats('Dao-Ho')


