import os
from flask import Flask, redirect, render_template, request, session
from pymongo import MongoClient
import json

MONGODB_URI = os.environ.get('MONGODB_URI')
MONGODB_NAME = os.environ.get('MONGODB_NAME')

app = Flask(__name__)

@app.route('/')
def get_homepage():
   return render_template('index.html')
   
@app.route('/login', methods=['POST'])
def login(): 
    sport = request.form['sport']
    team = request.form['team']
    username = request.form['username']
    meet = request.form['meet']
    return redirect("/" + sport + "/" + team + "/" + username + "/" + meet) 

@app.route('/<sport>/<team>/<username>/<meet>')
def get_user_page(sport, team, username, meet):
    return render_template('timer_page.html', username = username, team = team, sport = sport, meet = meet)

@app.route('/<sport>/<team>/<username>/<meet>/new', methods = ['POST'])
def timer_setup(sport, team, username, meet):
    event = request.form['event']
    heat = request.form['heat']
    lanes = request.form['lanes']
    return redirect("/" + sport + "/" + team + "/" + username + "/" + meet + '/' + event + "/" + heat + "/" + lanes)

@app.route('/<sport>/<team>/<username>/<meet>/<event>/<heat>/<lanes>')
def timer_set(sport, team, username, meet, event, heat, lanes):
    return render_template('timer_page.html', username = username, team = team, sport = sport, meet = meet, event = event, heat = heat, lanes = lanes)

@app.route('/time', methods = ['POST'])
def time():
    meet = request.form['meet']
    event = request.form['event']
    heat = request.form['heat']
    lanes = request.form['lanes']
    
    print(lanes)
    print(heat)
    print(event)
    print(meet)
    
    time = request.form['final']
    split = request.form['splits']
    n = 9
    splits = [split[i:i+n] for i in range(0, len(split), n)]
    
    
    time_data = {
            meet : {
                event : {
                    heat : {
                        lanes : {
                            'final': time, 
                            'splits': splits,
                            }
                        }  
                    }
                }
            }

    
    with MongoClient(MONGODB_URI) as conn: 
        db = conn[MONGODB_NAME]
        coll = db['final-times']
        coll.insert(time_data)
        
    return "0"
    
if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug = True)