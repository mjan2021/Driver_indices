from flask import Flask, jsonify, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the data once when the app starts
try:
    driver_stats = pd.read_csv('driver_stats.csv')
    daily_data = pd.read_csv('daily_driving_data.csv', parse_dates=['date'])
except FileNotFoundError:
    print("Data files not found. Please run the data processing script first.")
    driver_stats = pd.DataFrame()
    daily_data = pd.DataFrame()

@app.route('/')
def index():
    return render_template('dash.html')

@app.route('/api/top_drivers')
def get_top_drivers():
    """Returns the top 5-10 drivers based on total duration."""
    if driver_stats.empty:
        return jsonify([])
    
    # Sort by total duration and select top 10
    top_drivers = driver_stats.sort_values(by='total_duration_minutes', ascending=False).head(10)
    
    # Convert minutes to hours for better readability
    top_drivers['total_duration_hours'] = round(top_drivers['total_duration_minutes'] / 60, 2)
    top_drivers['average_daily_duration_hours'] = round(top_drivers['average_daily_duration_minutes'] / 60, 2)
    
    return jsonify(top_drivers.to_dict('records'))

@app.route('/api/driver_data/<driver_id>')
def get_driver_data(driver_id):
    """Returns detailed daily data for a specific driver."""
    if daily_data.empty:
        return jsonify({})

    driver_daily_data = daily_data[daily_data['driver_id'] == int(driver_id)]
    if driver_daily_data.empty:
        return jsonify({})
    
    # Convert dates to string format for JSON
    driver_daily_data['date'] = driver_daily_data['date'].dt.strftime('%Y-%m-%d')
    
    return jsonify(driver_daily_data.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True)