import os
import pandas as pd
from moviepy.editor import VideoFileClip

def process_videos(main_folder='Y:\\VIDEOS'):
    """
    Scans video folders with the corrected structure and aggregates data.
    """
    all_data = []

    if not os.path.exists(main_folder):
        print(f"Main folder '{main_folder}' not found.")
        return pd.DataFrame(), pd.DataFrame()

    # Iterate through each driver ID folder
    for driver_id in os.listdir(main_folder):
        driver_path = os.path.join(main_folder, driver_id)
        if not os.path.isdir(driver_path):
            continue

        # Check for the 'Video' subfolder
        video_main_path = os.path.join(driver_path, 'Video')
        if not os.path.exists(video_main_path):
            continue

        # Iterate through each date folder (e.g., 2024-04-13)
        for date_folder in os.listdir(video_main_path):
            date_path = os.path.join(video_main_path, date_folder)
            if not os.path.isdir(date_path):
                continue
            
            # The date is the name of the folder
            try:
                video_date = pd.to_datetime(date_folder)
            except ValueError:
                print(f"Skipping invalid date folder name: {date_folder}")
                continue

            # Iterate through each video file
            for filename in os.listdir(date_path):
                if filename.endswith(('.asf', '.mp4', '.avi', '.mov')):
                    file_path = os.path.join(date_path, filename)
                    try:
                        clip = VideoFileClip(file_path)
                        duration_seconds = clip.duration
                        clip.close()

                        all_data.append({
                            'driver_id': driver_id,
                            'date': video_date,
                            'duration_minutes': duration_seconds / 60
                        })
                    except Exception as e:
                        print(f"Could not process {file_path}: {e}")

    if not all_data:
        print("No video data found in the specified path.")
        return pd.DataFrame(), pd.DataFrame()

    df = pd.DataFrame(all_data)
    
    # Calculate daily totals
    daily_df = df.groupby(['driver_id', 'date']).sum().reset_index()
    
    # Calculate key metrics
    driver_stats = daily_df.groupby('driver_id').agg(
        total_days_driven=('date', 'count'),
        total_duration_minutes=('duration_minutes', 'sum'),
        average_daily_duration_minutes=('duration_minutes', 'mean')
    ).reset_index()
    
    # Save to a file for later use by the Flask app
    driver_stats.to_csv('driver_stats.csv', index=False)
    daily_df.to_csv('daily_driving_data.csv', index=False)
    
    return driver_stats, daily_df

if __name__ == '__main__':
    print("Processing video data...")
    driver_stats_df, daily_data_df = process_videos('Y:/VIDEOS')
    if not driver_stats_df.empty:
        print("Data processing complete. Saved to driver_stats.csv and daily_driving_data.csv")
    else:
        print("No data processed.")