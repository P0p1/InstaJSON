# Instagram Likes Analyzer

A Python script to analyze your Instagram liked posts from a JSON data export.

## Features
- Counts likes per account/person
- Shows top most-liked accounts
- Saves results to JSON
- Handles errors gracefully

## How to Use

1. **Export your Instagram data:**
   - Go to Instagram Settings → Privacy and Security → Data Download
   - Request "Liked Posts" data
   - Download and extract when ready

2. **Run the analyzer:**
   ```bash
   # Copy your liked_posts.json to this folder
   python main.py
   
   # Or specify the path
   python main.py "path/to/your/liked_posts.json"