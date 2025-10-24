# Wine AI App Configuration

## Project Structure
```
wine/
├── main.py              # Main entry point to run the app
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (not in git)
├── .gitignore          # Git ignore rules
├── README.md           # Project documentation
├── TODO.md             # Feature roadmap
└── src/                # Source code directory
    ├── app.py          # Flask application
    ├── data/           # Data storage
    │   └── data.json   # Wine collection database
    ├── uploads/        # Uploaded images
    ├── static/         # Static assets
    │   ├── script.js   # Wine display logic
    │   ├── upload.js   # Upload handler
    │   └── styles.css  # Custom CSS
    └── templates/      # HTML templates
        ├── landing.html
        └── index.html
```

## Running the App

### Option 1: From project root (Recommended)
```bash
python main.py
```

### Option 2: From src directory
```bash
cd src
python app.py
```

## Environment Variables

The `.env` file should contain:
- `OPENAI_API_KEY` - Your OpenAI API key
- `DATA_FILE` - Path to JSON database (relative to src/)
- `UPLOAD_FOLDER` - Path to uploads folder (relative to src/)
- `AI_MODEL` - OpenAI model to use (e.g., gpt-4o)

## Notes

- All paths in .env are relative to the `src/` directory
- The app automatically creates required folders
- Data file is automatically initialized if it doesn't exist
