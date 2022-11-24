import flask from Flask

app=Flask(__name__)
@app.route("/"))
def root():
	return "Hello World!"

if __name__=="__main__":
	app.run(debug=True, port=5000)
