
from flask import Flask ,jsonify ,make_response
from flask_restful import Resource ,Api ,reqparse 
import requests
import xml.etree.ElementTree as ET
import Config

app = Flask(__name__)
api = Api(app)


Data={
    'city':'Pune',
    'out-format':'json'
}  

post_args = reqparse.RequestParser()
post_args.add_argument('city',type=str,help="City is required",required=True)
post_args.add_argument('out-format',type=str,help="Out-format is json/xml required ",required=True)

class CurrentWeather(Resource):

    def get(self):
        return jsonify(Data)
    
    def post(self):
        args = post_args.parse_args()
        # Make a request to a weather API (replace with your desired weather API)
        
        url = 'https://weatherapi-com.p.rapidapi.com/current.json'

        querystring = {"q":f"{args['city']}"}

        headers = {
        "X-RapidAPI-Key": f"{Config.api_key}",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        
        # Parse the response JSON from the weather API
        weather_data = response.json()
        
        # Extract the relevant weather information
        temperature = weather_data['current']['temp_c']
        latitude = weather_data['location']['lat']
        longitude = weather_data['location']['lon']
        city_name = weather_data['location']['name']
    
        #Construct the response based on the output format
        if args['out-format'] == 'json':
            response_data = {
                'Weather': f'{temperature} C',
                'Latitude': str(latitude),
                'Longitude': str(longitude),
                'City': city_name
            }
            return response_data
        
        elif args['out-format'] == 'xml':
            response_data = ET.Element('response')
            weather = ET.SubElement(response_data, 'Weather')
            weather.text = f'{temperature} C'
            latitude_elem = ET.SubElement(response_data, 'Latitude')
            latitude_elem.text = str(latitude)
            longitude_elem = ET.SubElement(response_data, 'Longitude')
            longitude_elem.text = str(longitude)
            city_elem = ET.SubElement(response_data, 'City')
            city_elem.text = city_name
            response_content = ET.tostring(response_data)
            response = make_response(response_content)
            response.headers['Content-Type'] = 'application/xml'
            return response

        else:
            print('response-',response)
            return 'Invalid output format. Please specify either "json" or "xml" .'
            

api.add_resource(CurrentWeather, '/CurrentWeather')



if __name__=='__main__':
    app.run(debug=True,use_reloader=True)