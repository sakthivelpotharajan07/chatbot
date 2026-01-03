# Agentic AI Chatbot

A powerful, multi-agent AI system built with FastAPI that intelligently routes user queries to specialized agents. The system features a **brand new, premium web-based chat interface** and supports document analysis, meeting scheduling, weather checking, and database queries.

## 🚀 Features

### 🤖 Intelligent Agents
- **Document Analysis Agent**:
    - Upload **PDF** or **TXT** files.
    - Ask questions about the content with high accuracy.
    - Automatic fallback to **Web Search** (DuckDuckGo) if the answer is completely missing from the document.
- **Meeting Agent**:
    - Schedule meetings using natural language (e.g., "Book a meeting in Delhi tomorrow").
    - **Smart Conflict Resolution**: Checks **Weather** conditions before scheduling to warn about bad weather.
    - Prevents double-booking.
- **Weather Agent**:
    - Real-time weather information for any city using OpenWeatherMap.
    - Understands relative dates like "today", "tomorrow", and "yesterday".
- **Database Agent**:
    - Query your scheduled meetings (e.g., "Do I have any meetings next week?").

### 🎨 Modern Interface (New!)
- **Premium Design**: A completely overhauled UI with a soft Indigo/Slate color palette and Glassmorphism effects.
- **Interactive Experience**: "Typing..." indicators, message badges, and smooth animations.
- **Responsive**: Fully optimized for different screen sizes.

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: HTML5, CSS3 (Modern Variables & Flexbox), Vanilla JavaScript
- **Key Libraries**:
    - `pypdf` for robust document text extraction
    - `duckduckgo-search` for privacy-focused web browsing
    - `requests` for API interactions

## 📋 Prerequisites

- Python 3.8+
- An API Key from [OpenWeatherMap](https://openweathermap.org/api)

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd agent-ai
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn python-multipart python-dotenv pypdf duckduckgo-search requests
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the root directory and add your OpenWeatherMap API key:
   ```env
   OPENWEATHER_API_KEY=your_api_key_here
   ```


## 📸 Screenshots

![Screenshot 1](screenshots/Screenshot%20(8).png)
![Screenshot 2](screenshots/Screenshot%20(9).png)

## 🏃‍♂️ Usage

1. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the application**
   Open your browser and navigate to:
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 📂 Project Structure

```
agent-ai/
├── app/
│   ├── agents/          # Agent logic (Chat router, Document, Meeting, Weather, DB)
│   ├── schemas/         # Pydantic models
│   ├── static/          # Frontend assets (HTML, CSS, JS) - SERVED AT /static
│   ├── tools/           # External tool implementations (PDF reader, Search, API calls)
│   ├── utils/           # Helper utilities (NLP, City Extraction)
│   ├── config.py        # Configuration & Env Loading
│   └── main.py          # FastAPI application entry point
├── uploads/             # Directory for user-uploaded documents
└── .env                 # Environment variables
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
