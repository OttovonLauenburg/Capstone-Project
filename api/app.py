from flask import Flask, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import request
import Market
import Information
import Leaderboard
import Quiz
import Concentration_Game

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


db = firestore.client()
user_accounts = db.collection("users")
app = Flask(__name__)

def dummy_add_db(user_account = user_accounts):
    data = {'username':'ChunkyMan','password':'Chunky123','firstName':'Chunky','lastName':'Man','wallet':[{'crypto':"Bitcoin",'amount_owned':400,'purchase_price':37},{'crypto':"Ethereum",'amount_owned':300,'purchase_price':23}],'profit':50,'currency':20}
    user_account.document().set(data)
    
@app.route("/Home")
def get_home_page():
    return {'home':"This is the Home Page"}
    
@app.route("/Information",methods = ['GET','POST'])
def get_information_page():
    """If buy/sell form is completed the transaction is then processed on the 
    back-end by talking to the database and adjusting the user's wallet according
    to the amount of crypto purchased with virtual currency."""
    if(request.method == 'GET'):
        """retrieves the amount of virtual currency so front-end
        can display a slider with min to max of tradable virtual currency"""
        #print("inside retrive vc get")
        return {'info': Information.retrieve_virtual_currency(user_accounts, request.args.get("uid"), request.get("coin_name"))}
    if(request.method == 'POST'):
        #print("Before transaction")
        try:
            Information.process_transaction(user_accounts, request.json["trade"])
            return {'info_trade' : 'Successfully traded'}
        except:
            return {'info_trade' : 'Unsuccessfully traded'}


@app.route("/Leaderboard")
def get_leaderboard_page():
    uid = request.args['uid']
    ans = Leaderboard.generate_leaderboard(user_accounts,uid)
    return {'leaderboard':ans}
    
@app.route("/Market")
def get_market_page():
    return {'Market':Market.checking()}

@app.route("/News")
def get_news_page():
    return {'news':"This is the News Page"}
        
@app.route("/Wallet")
def get_wallet_page():
    return {'Wallet':"This is the Wallet Page"}

@app.route("/Quiz",methods = ["GET","POST"])
def get_quiz_game():
    if request.method == "GET":
        return {"quiz_data":Quiz.send_questions()}
    elif request.method == "POST":
        return {"score":Quiz.generate_score(request.json["responses"])}

@app.route("/ConcentrationGame", methods = ["GET", "POST"])
def get_concentration_game():
    if(request.method == "GET"):
        return {"concentration_data": Concentration_Game.retrieve_images()}
    elif(request.method == "POST"):
        return {"concentation_data": Concentration_Game.update_user_vc(user_accounts, request.args.get("uid"), request.json["game_reward"])}