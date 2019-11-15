# Football Scrapper

Download and merge into one video the highlights of a match at Fit Five Brussels.

**Usage**
  1. Clone repository and access project's root directory
  2. Create virtual environment ```conda create -n football_scrapper python=3.5```
  3. Activate environment ```conda activate football_scrapper```
  4. Install dependencies ```pip install -r requirements.txt```
  5. Run program ```python scrap.py```
  6. Fill in date, time and field number as requested by the program

**Notes**
When merging the videos, it's normal to have a warning like this:
```
OpenCV: FFMPEG: tag 0x5634504d/'MP4V' is not supported with codec id 12 and format 'mp4 / MP4 (MPEG-4 Part 14)'
OpenCV: FFMPEG: fallback to use tag 0x7634706d/'mp4v'
```    
but if it says:
```
Could not find encoder for codec id {}: Encoder not found
```
it will not create the merged video.
