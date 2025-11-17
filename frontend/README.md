# 🎨 AI Tutor Frontend

Simple HTML/JavaScript chat interface for the AI Tutor RAG System.

## 📁 Files

```
frontend/
├── index.html       # Main HTML structure
├── styles.css       # Beautiful, modern styling
├── app.js          # JavaScript logic & API calls
└── README.md       # This file
```

## 🚀 How to Run

### Method 1: Using Python HTTP Server (Recommended)

```bash
# From the frontend directory
python -m http.server 5500
```

Then open: http://localhost:5500

### Method 2: Using VS Code Live Server

1. Install "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

### Method 3: Direct File

Simply double-click `index.html` (may have CORS issues)

## ⚙️ Configuration

The frontend connects to the backend at: `http://localhost:8000`

If your backend runs on a different port, edit `app.js`:

```javascript
const API_BASE_URL = 'http://localhost:YOUR_PORT';
```

## 🧪 Testing

1. **Start Backend** (in backend folder):
   ```bash
   python main.py
   ```

2. **Start Frontend**:
   ```bash
   python -m http.server 5500
   ```

3. **Open Browser**: http://localhost:5500

4. **Ask Questions**:
   - "How does a bell produce sound?"
   - "What are vocal cords?"
   - "Explain compression and rarefaction"

## ✨ Features

- ✅ Clean, modern chat interface
- ✅ Real-time status indicator
- ✅ Automatic image display with answers
- ✅ Smooth animations
- ✅ Loading indicators
- ✅ Error handling
- ✅ Responsive design (mobile-friendly)
- ✅ Keyboard shortcuts (Enter to send)

## 🎨 Design

- Modern gradient header
- Clean message bubbles
- Inline image display
- Smooth scrolling
- Professional typography
- Accessible colors

## 🐛 Troubleshooting

**"Server Offline" Status:**
- Make sure backend is running: `python main.py`
- Check backend is on port 8000

**Images Not Showing:**
- Make sure `pics/` folder is in the project root
- Check image filenames match metadata

**CORS Errors:**
- Use Python HTTP server (Method 1)
- Backend already has CORS enabled

**Blank Page:**
- Check browser console for errors
- Make sure all files are in `frontend/` folder

## 📱 Mobile Support

The interface is fully responsive:
- Adapts to small screens
- Touch-friendly buttons
- Optimized layout

## 🎯 Next Steps

After testing:
1. ✅ Verify backend connection
2. ✅ Test chat functionality
3. ✅ Check image display
4. 🎬 Record demo video
5. 📝 Update main README

---

**Enjoy your AI Tutor!** 🚀

