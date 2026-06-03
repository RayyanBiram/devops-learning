# app.py

from flask import Flask
import redis
import os

app = Flask(__name__)          
cache = redis.Redis(
    host=os.getenv("REDIS_HOST", "redisdb"),
    port=int(os.getenv("REDIS_PORT", "6379"))
)

@app.route('/')
def welcome():
    return 'Welcome to my project built using Docker & Flask!'               

@app.route('/count')
def increment():
    visits = cache.incr('visits')
    return f'This page has been visited {visits} times.'

if __name__ == '__main__':     
    app.run(host='0.0.0.0', port=5000)

