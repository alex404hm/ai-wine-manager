# 🍷 Wine AI App

An intelligent wine collection management system powered by AI. Upload photos of your wine bottles, and let AI automatically identify and catalog them in your digital cellar.

## ✨ Features

- 📸 **Smart Image Upload** - Upload single bottles or entire wine shelves
- 🤖 **AI-Powered Recognition** - Automatically extracts wine details using OpenAI Vision API
- 📊 **Wine Collection Management** - View and organize your entire collection
- 🔄 **Auto-Refresh** - Real-time updates of your wine collection

## 🎯 What Information Does It Extract?

For each wine bottle, the AI identifies:
- Wine name
- Type (Red, White, Rosé, Sparkling)
- Vintage year
- Producer/Winery
- Grape variety or blend
- Classification (e.g., Grand Cru)
- Region/Country of origin

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/alex404hm/wine.git
   cd wine
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask pillow openai python-dotenv
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   DATA_FILE=src/data/data.json
   UPLOAD_FOLDER=src/uploads
   AI_MODEL=gpt-4-vision-preview
   ```

5. **Create required directories**
   ```bash
   mkdir -p src/data src/uploads
   echo "[]" > src/data/data.json
   ```

6. **Run the application**
   ```bash
   cd src
   python app.py
   ```

7. **Open your browser**
   
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
wine/
├── src/
│   ├── app.py                 # Flask application
│   ├── data/
│   │   └── data.json         # Wine collection database
│   ├── static/
│   │   ├── script.js         # Wine data display logic
│   │   ├── upload.js         # Upload handling
│   │   └── styles.css        # Custom styles (minimal)
│   ├── templates/
│   │   ├── landing.html      # Landing page
│   │   └── index.html        # Dashboard
│   └── uploads/              # Uploaded wine images
├── .env                      # Environment variables
├── .gitignore
├── README.md
└── TODO.md                   # Feature roadmap
```

## 🎨 Tech Stack

### Backend
- **Flask** - Web framework
- **OpenAI API** - AI vision for wine recognition
- **Pillow** - Image processing
- **Python-dotenv** - Environment management

### Frontend
- **Tailwind CSS** - Utility-first CSS framework
- **Vanilla JavaScript** - No framework needed
- **HTML5** - Semantic markup

## 🔧 Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-...` |
| `DATA_FILE` | Path to JSON database | `src/data/data.json` |
| `UPLOAD_FOLDER` | Directory for uploads | `src/uploads` |
| `AI_MODEL` | OpenAI model to use | `gpt-4-vision-preview` |

## 📖 Usage

### Upload a Wine Photo

1. Navigate to the dashboard at `/dashboard`
2. Click "Choose File" and select a wine bottle image
3. Click "Upload"
4. Wait for AI analysis (usually 5-10 seconds)
5. Your wine will appear in the collection table below

### View Your Collection

- All wines are displayed in a searchable table
- Auto-refreshes every 10 seconds
- Click on images for a larger view

## 🛣️ Roadmap

Check out our [TODO.md](TODO.md) for planned features:

- [ ] Search and filter functionality
- [ ] Pagination for large collections
- [ ] Location tracking (cellar position)
- [ ] User authentication
- [ ] Price lookup via external APIs
- [ ] Export collection to CSV/PDF

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## ⚠️ Important Notes

- **API Costs**: This app uses OpenAI's Vision API which incurs costs per image analysis
- **Image Quality**: Better quality photos lead to more accurate recognition
- **Privacy**: Images and data are stored locally on your machine

## 🐛 Troubleshooting

### Common Issues

**Problem**: "Import openai could not be resolved"
```bash
pip install --upgrade openai
```

**Problem**: Upload fails
- Check that `UPLOAD_FOLDER` directory exists
- Ensure file is JPG, PNG, or GIF format
- Check file size (recommended < 5MB)

**Problem**: AI returns incorrect data
- Use higher quality images
- Ensure wine label is clearly visible
- Try different lighting conditions

## 📧 Contact

Project maintained by [@alex404hm](https://github.com/alex404hm)

---

Made with ❤️ and 🍷 by the Wine AI Team