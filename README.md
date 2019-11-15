# Football Scrapper

**Description**

Download and merge into one video the highlights of a match at Fit Five Brussels.

**Installation**
  1. Install FFmpeg for [Windows](https://m.wikihow.com/Install-FFmpeg-on-Windows) or [Linux](https://linuxize.com/post/how-to-install-ffmpeg-on-ubuntu-18-04/). This will be used to compress the final output.
  2. Clone repository and access root directory  
  ```git clone https://github.com/eltrujo/football_scrapper.git```  
  ```cd football_scrapper```
  3. Create virtual environment and activate it  
  ```conda create -n football_scrapper python=3.7```  
  ```conda activate football_scrapper```
  4. Install Python dependencies  
  ```pip install -r requirements.txt```

**Usage**
  1. With the environment active, run ```python scrap.py```
  2. Fill in date, time and field number as requested by the program.

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
