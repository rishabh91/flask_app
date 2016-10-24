import requests
from flask import Flask, render_template, request, url_for



# Initialize the Flask application
app = Flask(__name__)

# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return render_template('form_submit.html')

# Define a route for the action of the form, for example '/dictionary/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/dictionary/', methods=['POST'])
def dictionary():
	#getting the word from the user to search meaning from pearson API
	word=request.form['word']
	#building the URL for making the API call
	url = "http://api.pearson.com/v2/dictionaries/ldoce5/entries?headword=" + word + "&limit=1"
	r = requests.get(url) # making a get call to the API to fetch the JSON values
	data = r.json()
	value = data['results']
	value = value[0]
	value = value['senses']
	value = value[0]
	try:
		value = value['subsenses']
		value = value[0]
		value = value['definition']
	except:
		value = value['definition']
	

	return render_template('form_action.html', meaning=value)

# Run the app :)
if __name__ == '__main__':
	app.run()