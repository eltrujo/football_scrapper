#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 16:09 2019

@author: eltrujo
"""
import os
import requests
import cv2
from glob import glob
import subprocess
from inputimeout import inputimeout, TimeoutOccurred
from time import time


def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def save_video_from_bytes(bytes_str, video_path):
    with open(video_path, 'wb') as f:
        f.write(bytes_str)


def prompt_yes_no_question(question):
    while True:
        try:
            proceed = inputimeout(prompt=f"{question} (y/n)? ", timeout=5)
            if proceed == 'y' or proceed == '':
                return True
            elif proceed == 'n':
                return False
        except TimeoutOccurred:
            return 'y'


# Create directory to save the videos if it doesn't exist
data_path = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'videos'
create_directory(data_path)

# Input parameters
proceed = False
while not proceed:
    params = {
        'field': input('Field number [1-5]? '),  # field or terrain number
        # date of the match in format YYYYMMDD
        'date': input('Year [YYYY]? ') + input('Month [MM]? ') + input('Day [DD]? '),
        'time': input('Time [hh]? '),  # time of the match in format hh
    }

    # Verify answer is correct or re-input parameters
    print(params)
    proceed = prompt_yes_no_question('Proceed')

# Start counting time
tic = time()

# Download highlights
download = prompt_yes_no_question('Download highlights')
if download:
    print('Downloading highlights...')
    # Define url
    url = 'http://fitfive.inowys.com/VIDEO/'

    # Create directory inside data_path to save this date's videos
    down_data_path = data_path + os.sep + params['date']
    create_directory(down_data_path)

    # Array with all quarters of hour and the first quarter of the next hour
    quarters = [params['time'] + mm for mm in ['00', '15', '30', '45']]
    quarters += [str(int(params['time']) + 1) + '00']

    # Loop through every quarter and downlowad its highlights
    video_counter = 0
    for t in quarters:
        q_counter = 0
        while True:
            q_counter += 1
            video_name = f"FitFive_{params['date']}_{t}_Buzz{q_counter}_1"
            this_url = url + params['field'] + '/' + \
                params['date'] + '/' + video_name + '.mp4'
            resp = requests.get(this_url)
            if resp.status_code == 200:
                video_counter += 1
                save_video_from_bytes(
                    resp.content, f'{down_data_path}{os.sep}{video_counter:02d}.mp4')
                print(f"Video {video_counter:02d} saved")
            else:
                break

    print(
        f"Videos from {params['date'][-2:]}/{params['date'][4:6]}/{params['date'][:4]} downloaded.")

# Merge highlights
merge = prompt_yes_no_question('Merge donwloaded videos')
if merge:
    print("Merging videos...")
    # Create directory if it doesn't exist
    merged_data_path = data_path + os.sep + 'merged'
    create_directory(merged_data_path)

    # List video files and sort them
    videos = sorted(
        glob(data_path + os.sep + params['date'] + os.sep + '*.mp4'))

    # Load first video and get its properties
    i = 0
    cap = cv2.VideoCapture(videos[i])
    width, height = int(cap.get(3)), int(cap.get(4))
    w_small = 640
    h_small = int(float(height) * w_small / width)
    print(f"Output video resolution: {w_small} x {h_small}")
    fps = cap.get(5)
    # fourcc = int(cap.get(6))
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')

    # Start output video
    out_path = merged_data_path + os.sep + params['date'] + '.mp4'
    out = cv2.VideoWriter(out_path, fourcc, fps, (w_small, h_small))
    while True:
        # Read next frame
        _, frame = cap.read()

        # If end is reached, switch to next video
        if frame is None:
            print(f"Video {videos[i]} added")
            i += 1

            # Break if all videos have been merged
            if i >= len(videos):
                break

            # Load next video and read first frame
            cap = cv2.VideoCapture(videos[i])
            _, frame = cap.read()

        # Reduce size
        frame = cv2.resize(frame, (w_small, h_small))

        # Write frame to output video
        out.write(frame)

    cap.release()
    out.release()
    print(f"Merged video saved to: \n{out_path}")

# Compress video
compress = prompt_yes_no_question('Compress video')
if compress:
    print('Compressing video...')
    # CRF (Constant Rate Factor) can range from 18 to 24
    # CRF = 24 will compress the video to the smallest size
    subprocess.call(f"ffmpeg -i \"{out_path}\" -vcodec libx264 -crf 24 \"{out_path.replace('.mp4', '_compr.mp4')}\"", shell=True)

    # Delete uncompressed video
    delete = prompt_yes_no_question('Delete uncompressed video')
    if delete:
        os.remove(out_path)
    
# Delete individual videos
delete = prompt_yes_no_question('Delete individual video files')
if delete:
    # List video files and sort them
    videos = glob(data_path + os.sep + params['date'] + os.sep + '*.mp4')

    # Delete all of them one by one
    for video_path in videos:
        os.remove(video_path)

    # Delete directory (only works if it's empty)
    os.rmdir(data_path + os.sep + params['date'])

elapsed_t = time() - tic
print('Finished')
print(f"Total time elapsed: {elapsed_t // 60} minutes & {elapsed_t % 60} seconds")

"""
Examples of links to download videos:
    http://fitfive.inowys.com/VIDEO/5/20191106/FitFive_20191106_2130_Buzz1_1.mp4
    http://fitfive.inowys.com/VIDEO/5/20191106/FitFive_20191106_2130_Buzz2_1.mp4
    http://fitfive.inowys.com/VIDEO/5/20191106/FitFive_20191106_2100_Buzz1_1.mp4
    http://fitfive.inowys.com/VIDEO/5/20191106/FitFive_20191106_2115_Buzz1_1.mp4
    http://fitfive.inowys.com/VIDEO/5/20191106/FitFive_20191106_2115_Buzz4_1.mp4
    http://fitfive.inowys.com/VIDEO/5/20191106/FitFive_20191106_2115_Buzz5_1.mp4
"""
