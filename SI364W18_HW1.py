## HW 1
## SI 364 W18
## 1000 points

#################################

## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".
#RESOURCES:
#https://github.com/ahazhou/HW1
#https://developer.yahoo.com/weather/
#https://sunrise-sunset.org/api
#https://maps-apis.googleblog.com/2010/03/introducing-new-google-geocoding-web.html
#http://maps.google.com/maps/api/geocode/json?address=4665%20squirrel%20hill%20dr.&sensor=false
#http://maps.google.com/maps/api/geocode/json?latlng=38.8961582,-77.0384882&sensor=false
#https://source.unsplash.com/
#https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/#searching
#https://www.programmableweb.com/category/all/apis?keyword=No%20Authentication
#https://www.programmableweb.com/api/metno-weather
#https://news.ycombinator.com/item?id=7546040


from flask import Flask, request
import requests
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_to_you():
    return 'Hello!'

## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and 
##go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"

#PROBLEM 1 SOLUTION:
@app.route('/class')
def class_route():
    return "Welcome to SI 364!"

## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 'http://localhost:5000/movie/<name-of-movie-here-one-word>' 
##you see a big dictionary of data on the page. For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', 
##you should see something like the data shown in the included file sample_ratatouille_data.txt, which contains data about 
##the animated movie Ratatouille. However, if you go to the url http://localhost:5000/movie/titanic, you should get different 
##data, and if you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:

# {
#  "resultCount":0,
#  "results": []
# }

## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!

#PROBLEM 2 SOLUTION:
@app.route('/movie/<name>')
def movie_route(name):
    itunesMovieResponse = "https://itunes.apple.com/search?term=" + name + "&entity=movie"
    response = requests.get(itunesMovieResponse)
    movies = []
    for var in response.json()["results"]:
        movies.append(var)
    if(response.json()["resultCount"] == 0):
        return "<pre>{<br>\t\"resultCount\":0,<br>\t\"results\": []<br>}<pre>"
    return '<p>{}<p>'.format(response.json())
    
## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, 
#you see a form that asks you to enter your favorite number.

## Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>". 
#For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.

#PROBLEM 3 SOLUTION:
def is_float(val):
    try:
        float(val)
        return True
    except ValueError:
        return False
def is_int(val):
    try:
        int(val)
        return True
    except ValueError:
        return False

@app.route('/question', methods = ['POST', 'GET'])
def ask_fav_number():
    question = """<!DOCTYPE html>
                <html>
                <body>
                <form method="POST" action="/question">
                What's your favorite number?:<br>
                <input type="text" name="number" value="0">
                <br>
                <input type="submit" value="Submit">
                </form>
                </body>
                </html>"""
    if request.method == 'POST':
        number = request.form["number"]
        if(is_int(number)):
            return """<p>Double your number {} is {}</p>
                    <a href="/question"><button>Try Again</button></a>""".format(number, int(number)*2)
        elif(is_float(number)):
            return """<p>Double your number {} is {}</p>
                    <a href="/question"><button>Try Again</button></a>""".format(number, float(number)*2)
        else:
            return """<h3>You input: \"{}\"</h3>
                    <br>
                    <p>That is not a number. Try again.</p>
                    <a href="/question"><button>Click</button></a> """.format(number)
    return question

## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and 
#build it into the above code for a Flask application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the 
#submission form and is readable by humans (more readable than e.g. the data you got in Problem 2 of this HW). 
#The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully 
#writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do 
#not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user 
#will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable 
#number; if your form asks the user to select a checkbox, you can assume they will do that.)

#PROBLEM 4 SOLUTION:
def picture(location):
    pictureResponse = "https://source.unsplash.com/400x225/?" + location
    return """<img src="{}">""".format(pictureResponse)
def astronomical(location):
    googleMapResponse = "http://maps.google.com/maps/api/geocode/json?address=" + location + "&sensor=false"
    googleResponseLatLong = requests.get(googleMapResponse).json()["results"][0]["geometry"]["location"]

    sunrisesunsetResponse = "https://api.sunrise-sunset.org/json?lat=" + str(googleResponseLatLong["lat"]) + "&lng=" + str(googleResponseLatLong["lng"]) + "&date=today"
    response = requests.get(sunrisesunsetResponse)
    results = response.json()["results"]
    return """<h3>Astronomical Information</h3>
                <p><b>*Using Coordinated Universal Time (UTC)</b><br>
                <b>Sunrise:</b> {}<br>
                <b>Sunset:</b> {}<br>
                <b>Solar Noon:</b> {}<br>
                <b>Day Length:</b> {} HR:MIN:S<br>
                <b>Beginning of Civil Twilight:</b> {}<br>
                <b>Ending of Civil Twilight:</b> {}<br>
                <b>Beginning of Nautical Twilight:</b> {}<br>
                <b>Ending of Nautical Twilight:</b> {}<br>
                <b>Beginning of Astronomical Twilight:</b> {}<br>
                <b>Ending of Astronomical Twilight:</b> {}<p>
                <a href="sunrise-sunset.org">Using Sunrise-Sunset</a> """.format(results["sunrise"], results["sunset"], results["solar_noon"], results["day_length"], results["civil_twilight_begin"], results["civil_twilight_end"], results["nautical_twilight_begin"], results["nautical_twilight_end"], results["astronomical_twilight_begin"], results["astronomical_twilight_end"])
def weather(location):
    yahooWeatherAPI = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22" + location + "%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
    response = requests.get(yahooWeatherAPI)
    information = response.json()["query"]["results"]["channel"]
    wind = information["wind"]
    atmosphere = information["atmosphere"]
    condition = information["item"]
    summary = information["item"]["description"][:-201]

    windText = """<p><b>Wind:</b><br>Chill: {}<br>Direction: {}<br>Speed: {}<br></p>""".format(wind["chill"], wind["direction"], wind["speed"])
    atmosphereText = """<p><b>Atmosphere:</b><br>Humidity: {}<br>Pressure: {}<br>Rising: {}<br>Visibility: {}<br></p>""".format(atmosphere["humidity"], atmosphere["pressure"], atmosphere["rising"], atmosphere["visibility"])
    conditionText = """<h3>Weather {}:</h3><p><b>Temperature:</b><br>{}°F<br>""".format(condition["title"], condition["condition"]["temp"])

    return conditionText + summary + windText + atmosphereText + """<a href="https://www.yahoo.com/?ilc=401" target="_blank"> <img src="https://poweredby.yahoo.com/purple.png" width="134" height="29"/> </a>"""
def locationtype(location):
    googleMapResponse = "http://maps.google.com/maps/api/geocode/json?address=" + location + "&sensor=false"
    response = requests.get(googleMapResponse)
    locationtype = response.json()["results"][0]["types"]
    latlong = response.json()["results"][0]["geometry"]["location"]

    locationtypeText = """<p>""".format()
    latlongText = """<p><b>Type of location:</b> {}<br><b>Latitude:</b> {}<br><b>Longitude:</b> {}</p><br>""".format(locationtype, latlong["lat"], latlong["lng"])
    return "<h3>Location Information</h3>" + locationtypeText + latlongText

@app.route('/problem4form', methods = ['POST', 'GET'])
def show_location_information():
    prompt = """
        <!DOCTYPE html>
        <html>
            <body>
                <form method="POST" action="/problem4form">
                    <p>What type of details do you want for your location?</p>
                    <input type="checkbox" id="picture" name="interest" value="picture"/>
                    <label for="picture">Provide picture</label><br>
                    <input type="checkbox" id="locationtype" name="interest" value="locationtype"/>
                    <label for="subscribeNews">Location details (what type of place is it?)</label><br>
                    <input type="checkbox" id="weather" name="interest" value="weather"/>
                    <label for="weather">Current weather details</label><br>
                    <input type="checkbox" id="astronomical" name="interest" value="astronomical"/>
                    <label for="astronomical">Astronomical details</label><br>
                    <br>
                    Enter a location name<br>
                    <input type="text" name="location">
                    <br>
                    <input type="submit" value="Submit">
                </form>
            </body>
        </html>
    """
    if request.method == 'POST':
        location = request.form["location"]
        details = request.form.getlist("interest")

        bodyText = ""

        readableDetails = ""
        if(details == []):
            readableDetails = "\"none\""
        if "picture" in details:
            if(len(readableDetails) != 1):
                readableDetails += ", "
            bodyText += picture(location)
            readableDetails += "Picture Information"
        if "locationtype" in details:
            if(len(readableDetails) != 1):
                readableDetails += ", "
            bodyText += locationtype(location)
            readableDetails += "Type of Location Information"
        if "weather" in details:
            if(len(readableDetails) != 1):
                readableDetails += ", "
            bodyText += weather(location)
            readableDetails += "Weather Information"
        if "astronomical" in details:
            if(len(readableDetails) != 1):
                readableDetails += ", "
            bodyText += astronomical(location)
            readableDetails += "Astronomical Information"
        
        if readableDetails[0] == ',':
            readableDetails = readableDetails[2:]

        header = """<p>You entered the location [{}] with fields [{}]</p>""".format(location, readableDetails)

        
        return header + bodyText + prompt

    return prompt



if __name__ == '__main__':
    app.run()

# Points will be assigned for each specification in the problem.
