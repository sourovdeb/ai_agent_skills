# Audio, Video & Banner Tools: Complete Free Setup

## For ELT Content, Podcasts, and Blog Banners

---

## Banner & Image Tools

### Canva (Recommended Starting Point)
- **Website:** canva.com
- **Free tier:** Generous — most templates, unlimited designs
- **Best for:** Blog post banners, Pinterest pins, social media cards
- **ELT use:** Create a consistent banner template (your colour, font, logo) then duplicate it for each post, changing only the title text
- **Time to create one banner:** 3 minutes once you have a template

### Photopea (Browser Photoshop)
- **Website:** photopea.com
- **Cost:** Completely free, runs in browser, no download
- **Opens:** PSD files, PNG, JPG, AI, XCF, Sketch files
- **Best for:** Editing existing images, removing backgrounds, advanced adjustments

### GIMP (Professional, Open Source)
- **Website:** gimp.org
- **Cost:** Free forever
- **Best for:** Complex image editing, batch processing
- **Batch banner creation script:**
```python
# Install: pip install Pillow
from PIL import Image, ImageDraw, ImageFont

def create_banner(title, output_path, template='banner_template.png'):
    img = Image.open(template).copy()
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('fonts/Roboto-Bold.ttf', 48)
    # Centre the text
    bbox = draw.textbbox((0,0), title, font=font)
    x = (img.width - (bbox[2]-bbox[0])) // 2
    y = img.height // 2
    draw.text((x, y), title, fill='white', font=font)
    img.save(output_path)
    print(f'Banner saved: {output_path}')

# Create banners for all posts in a folder
import os
for filename in os.listdir('drafts'):
    if filename.endswith('.md'):
        with open(f'drafts/{filename}') as f:
            title = f.readline().lstrip('#').strip()
        create_banner(title, f'banners/{filename.replace(".md",".png")}')
```

### AI Image Generation (Free)
- **DALL-E 3 via ChatGPT:** Free tier gives 2 images/day — enough for 2 blog banners
- **Stable Diffusion (local):** Completely free, unlimited, runs on your computer
  - Install via Automatic1111: github.com/AUTOMATIC1111/stable-diffusion-webui
  - Requires 4GB+ GPU or runs (slowly) on CPU
- **Bing Image Creator:** Free, uses DALL-E 3, 15 free boosts/day

---

## Audio Tools

### Audacity (Recording and Editing)
- **Website:** audacityteam.org
- **Cost:** Free, open source
- **Best for:** Recording your own voice, editing podcast audio, noise removal
- **ELT use:** Record yourself doing pronunciation exercises, create listening activities

**Basic recording workflow:**
1. Open Audacity
2. Click the red Record button
3. Speak your content
4. Click Stop
5. Use **Effect → Noise Reduction** to clean background noise
6. **File → Export → Export as MP3**

### ElevenLabs (AI Voice — Free Tier)
- **Website:** elevenlabs.io
- **Free tier:** 10,000 characters/month (~7 minutes of audio)
- **Best for:** Creating audio versions of your blog posts without recording yourself
- **Voices:** Dozens of natural-sounding voices
- **ELT use:** Create listening exercises from your written texts

**Workflow:**
1. Copy your blog post text
2. Go to elevenlabs.io → Voice Lab
3. Paste text, choose a voice
4. Click Generate → Download MP3
5. Upload the MP3 to your WordPress post as an audio file
6. Add `[audio src="URL"]` shortcode to your post

### Whisper (Free Transcription)
- **GitHub:** github.com/openai/whisper
- **Cost:** Completely free (runs locally)
- **Best for:** Transcribing audio to text, creating subtitles
- **ELT use:** Transcribe existing audio lessons into blog post text

```bash
pip install openai-whisper
whisper audio.mp3 --model medium --language English
# Outputs: audio.txt, audio.srt (subtitles), audio.vtt
```

---

## Video Tools

### DaVinci Resolve (Professional, Free)
- **Website:** blackmagicdesign.com/products/davinciresolve
- **Cost:** Free tier is extremely capable (colour grading, editing, audio)
- **Best for:** Editing video content for YouTube, polished ELT video lessons
- **Learning curve:** Medium (but many free YouTube tutorials)

### OBS Studio (Screen Recording)
- **Website:** obsproject.com
- **Cost:** Free, open source
- **Best for:** Recording your screen + webcam for video lessons, tutorials
- **ELT use:** Record yourself explaining grammar with a whiteboard visible

**Simple OBS setup for ELT videos:**
1. Download and open OBS
2. In **Sources** click `+` → **Display Capture** (your screen)
3. Click `+` again → **Video Capture Device** (your webcam)
4. Resize webcam to a small corner box
5. Click **Start Recording** → teach your lesson → **Stop Recording**
6. File is saved to your Videos folder

### Kdenlive (Open Source Video Editor)
- **Website:** kdenlive.org
- **Cost:** Free, open source
- **Best for:** Simpler editing than Resolve, good for blog intro videos

### Handbrake (Video Compression)
- **Website:** handbrake.fr
- **Cost:** Free
- **Use:** Compress large video files before uploading to WordPress
- **Settings for web:** H.264, 720p, 2000kbps

---

## Complete Content Production Workflow

### For a Blog Post with Audio

```
Day 1: Write the post in Logseq or Google Docs (500 words)
Day 2: Add it to your Google Sheet queue (Status: queued)
        → Apps Script publishes as draft automatically
        → While waiting, generate the audio with ElevenLabs
Day 3: Log into WordPress, add the audio file to the draft, publish
```

### For a Blog Post with Banner

```
1. Have a Canva template with your site colours and font
2. Duplicate it
3. Change only the title text
4. Download as PNG (1200x628px for social sharing)
5. Upload to WordPress Media Library
6. Set as Featured Image on your post
Time: 3 minutes per banner
```

### Batch Create 10 Banners at Once (Python + Pillow)

See the GIMP/Pillow script above. Run it weekly to create banners for the upcoming week's posts. Store them in a `banners/` folder, then upload them to WordPress in one batch via Media → Add New.
