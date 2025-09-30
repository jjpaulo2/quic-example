from quart import Quart

app = Quart(__name__)

@app.route("/hello")
async def hello():
    return "hello world"