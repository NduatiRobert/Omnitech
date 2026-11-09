HOME PAGE BACKGROUND VIDEO

Upload the video here as:   hero.mp4      (optionally also hero.webm)

Recommended:
- 10-20 seconds, loops smoothly, no sound needed (it plays muted)
- 1920x1080 or 1280x720, H.264 MP4
- Under 8 MB, ideally 3-5 MB, so the page loads fast
- Calm footage works best behind text: cameras, technicians at work, cabling,
  server racks, city or office scenes

The video plays on tablets and computers. Phones show the hero photo
(site/assets/img/hero/home.jpg) instead, to save visitors' mobile data.
Until a video is added, the hero photo is shown with a slow zoom.

Compress a large video with ffmpeg (free) before uploading:
  ffmpeg -i input.mp4 -vf "scale=1920:-2,fps=25" -c:v libx264 -crf 28 -preset slow -an -movflags +faststart hero.mp4
