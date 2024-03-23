import requests
# define all the GET Method in this class
headers = {
            'x-api-key': YOUROWNKEY,
            'userId': YOURID,
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'PostmanRuntime/7.37.0',
            'Connection': 'keep-alive',
            }
class GET:
    def __init__(self):
        self.url = "https://www.notexponential.com/aip2pgaming/api/index.php"
        self.headers =headers # Dictionary to store headers
    # Function: Get My Teams 
    # Parameters: type=myTeams
    # Return Values: teams, comma separated.  Generally, this should be just one.
    def getmyTeams(self) -> None:
        self.url = 'https://www.notexponential.com/aip2pgaming/api/index.php?type=myTeams'
        
    # Parameters: type=myGames or myOpenGames 
    # Return Values:games, comma separated
    def getMyGames(self) ->None:
        self.url = 'https://www.notexponential.com/aip2pgaming/api/index.php?type=myGames'

    # Parameters: type=moves, gameId, Count of most recent of moves
    # Return Values: List of Moves, comma separated
    def getMoves(self, gameid: str, movescount: int) ->None:
        self.url = 'https://www.notexponential.com/aip2pgaming/api/index.php?type=boardMap&gameId='+ gameid+'&count='+ str(movescount)
    
    # Parameters: type=boardString, gameId
    # Return Values: Board, in form of a string of O,X,-
    def getBoardString(self, gameid: str) ->None:
        self.url = 'https://www.notexponential.com/aip2pgaming/api/index.php?type=boardString&gameId='+ gameid

    # Parameters: type=boardMap, gameId
    # Return Values: Board, in form of a string of O,X,-
    def getBoardMap(self, gameid: str) ->None:
        self.url = 'https://www.notexponential.com/aip2pgaming/api/index.php?type=boardMap&gameId='+ gameid
    

     
class POST:
    def __init__(self):
        self.url = "https://www.notexponential.com/aip2pgaming/api/index.php"
        self.headers = headers
        self.payload ={}

    # Parameters: type=team, name=$name
    # Return Values: Team ID.  Fails if team already exists, or team name is too short, or too long.
    def createTeam(self, teamname: str) -> None:
        self.payload = {'name': teamname, 'type': 'team'}

    # Parameter: type=member, teamId, userId
    # Return Values: OK. Fails if user is already in that team
    def addTeamMember(self, teamid: int) -> None:
        self.payload = {'type': 'member', 'teamId': teamid, 'userId': '3597'}
    
    # Parameters: 
    # type=game
    # teamId1
    # teamId2
    # gameType=TTT  // This is the only value supported this semester
    # Optionally:
    # boardSize=20
    # target=10 (Needs to be <= boardSize) 
    #  Default values are 12 and 6
    def createGame(self, team1: str, team2: str, boardSize: int = 12, target:int = 6) -> None:
        self.payload = {'type': 'game', 'teamId1': team1,'teamId2': team2,  'gameType': 'TTT','boardSize': boardSize, 'target': target }

    # Parameter: type=move, gameId, teamId, move
    # Return Value: Move ID. 
    # Fails in following cases:
    # If no such game
    # If the team is not a participant in the game
    # If it is not the move of the team making that move
    # If the move dimensions are negative or >= n.  (Move starts from 0,0.  That is, 0 - indexing]
    def makeMove(self, teamid, gameid, move) ->None:
        self.payload = {'type': 'move', 'gameId': gameid, 'move': move, 'teamId': teamid}


# examples to use the get operation 
# get_test = GET()
# get_test.getmyTeams()
# response = requests.request("GET", url = get_test.url, headers=get_test.headers)
# print(response.text)
        
# One example to use the post operation
# post_test = POST()
# post_test.createGame('1413', '1414')
# print(post_test.payload)
# response = requests.request("POST", url = post_test.url, headers=post_test.headers, data = post_test.payload)
# print(response.text)
        
# getop = GET()
# getop.getMoves('4687', 5)
# response = requests.request("GET", url = getop.url, headers=getop.headers)
# print(response.text)
        
# post_test = POST()
# post_test.makeMove('1413', '4687', '4,4')
# print(post_test.payload)
# response = requests.request("POST", url = post_test.url, headers=post_test.headers, data = post_test.payload)
# print(response.text)