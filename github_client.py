import requests
from config import gh_token

#Loads the Oath Token in the request Headers.
class GithubClient:
    def __init__(self):
        self.token = gh_token()
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
#Returns a Python Dictionary with all the GitHub's account Data.
    def get_user(self):
        url="https://api.github.com/user"
        response=requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def contribution_streak(self,username:str=None):
        username=self.get_user()["login"]
        query = """
        query($user: String!){ 
          user(login: $user){ 
            contributionsCollection{ 
              contributionCalendar{ 
                totalContributions weeks{ 
                  contributionDays{ 
                    contributionCount date 
                  } 
                } 
              } 
            } 
          } 
        }
        """
        #GitHub specifically expects this python dictionary.
        payload={"query": query, "variables": {"user": username}} #username is $user from query.
        responce=requests.post("https://api.github.com/graphql", json=payload, headers=self.headers)
        responce.raise_for_status()
        return responce.json()["data"]["user"]["contributionsCollection"]["contributionCalendar"]

