# Football Scrapper

Download and merge into one video the highlights of a match at Fit Five Brussels.

To use it:
  1. Clone repository
  2. pip install -r requirements.txt
  3. python scrap.py
  4. Fill in date and field number as requested by the program

Note:
  When merging the videos, a warning like this is normal:
        OpenCV: FFMPEG: tag 0x5634504d/'MP4V' is not supported with codec id 12 and format 'mp4 / MP4 (MPEG-4 Part 14)'
        OpenCV: FFMPEG: fallback to use tag 0x7634706d/'mp4v'
    But if it says:
        Could not find encoder for codec id {}: Encoder not found
    it will not create the merged video.
