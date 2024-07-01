import requests
from datetime import datetime

def get_forecast(longitude, latitude):
    # using API for data
    url = f"https://api.weather.gov/points/{latitude},{longitude}"
    response = requests.get(url)
    data = response.json()

    forecast_url = data['properties']['forecast']
    
    # getting data
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()
    
    forecast_list = forecast_data['properties']['periods']
    forecasts = []

    for period in forecast_list:
        date = period['startTime']
        day_name = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').strftime('%A')
        temp = period['temperature']
        short_forecast = period['shortForecast']
        wind_speed = period['windSpeed']
        wind_direction = period['windDirection']
        forecasts.append((date, day_name, temp, short_forecast, wind_speed, wind_direction))

    # Saving file 
    with open('forecast.txt', 'w') as f:
        for forecast in forecasts:
            f.write(f"{forecast[0]}, {forecast[1]}, {forecast[2]}, {forecast[3]}, {forecast[4]}, {forecast[5]}\n")

def generate_html():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Weather Forecast</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-image: url('BG IMAGE.jpg'); 
                background-size: cover;
                background-position: center;
                margin: 0;
                padding: 20px;
            }
            h1 {
                text-align: center;
                color: #fff;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
            table {
                width: 80%;
                margin: 0 auto;
                border-collapse: collapse;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                background-color: rgba(255, 255, 255, 0.9);
            }
            th, td {
                padding: 12px;
                text-align: center;
                border: 1px solid #ddd;
                color: #333;
            }
            th {
                background-color: #4CAF50;
                color: white;
                text-transform: uppercase;
            }
            tr:nth-child(even) {
                background-color: rgba(240, 240, 240, 0.9);
            }
            tr:hover {
                background-color: rgba(220, 220, 220, 0.9);
            }
        </style>
    </head>
    <body>
        <h1>Weather Forecast</h1>
        <table>
            <tr>
                <th>Date</th>
                <th>Day</th>
                <th>Temperature (°F)</th>
                <th>Forecast</th>
                <th>Wind Speed</th>
                <th>Wind Direction</th>
            </tr>
    """

    # add file to the HTML
    with open('forecast.txt', 'r') as file:
        for line in file:
            date, day_name, temp, short_forecast, wind_speed, wind_direction = line.strip().split(', ')
            html_content += f"""
            <tr>
                <td>{date}</td>
                <td>{day_name}</td>
                <td>{temp}</td>
                <td>{short_forecast}</td>
                <td>{wind_speed}</td>
                <td>{wind_direction}</td>
            </tr>
            """

    html_content += """
        </table>
    </body>
    </html>
    """

    with open('forecast.html', 'w') as file:
        file.write(html_content)

def main():
    longitude = input("Enter longitude: ")
    latitude = input("Enter latitude: ")
    
    get_forecast(longitude, latitude)
    generate_html()
    print("Weather forecast has been saved to forecast.html")

if __name__ == "__main__":
    main()
