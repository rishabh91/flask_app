import os
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
	url = "http://api.pearson.com/v2/dictionaries/ldoce5/entries?headword="+word+"&limit=2"
	r = requests.get(url)
	code = r.status_code
	if code==200:
		data = r.json()
		results = data['results']
		if len(results)>0:
			values =[]
			for result in results:
				value = result['senses']
				value = value[0]
				try:
					value = value['subsenses']
					value = value[0]
					value = value['definition']
					values.append(value)
				except:
					value = value['definition']
					values.append(value)
		else:
			return render_template('form_nodata.html')
	else:
		return render_template('form_nodata.html')
	

	return render_template('form_action.html', meaning=values)

# Run the app :)
if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
