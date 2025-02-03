# NationStatesBot Setup Guide 🚀

This guide will help you set up and run both the NationStatesBot and its dashboard components.

## Prerequisites

Before starting, ensure you have:

- Python 3.12+
- Node.js 18+
- Chrome/Chromium browser
- Git
- Discord bot token (optional)

## Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/AgnusSOCO/NationStatesBot-Backend.git
cd NationStatesBot-Backend
```

### 2. Bot Setup

#### Ubuntu/Linux-Specific Notes
- Install required system packages:
```bash
sudo apt-get update
sudo apt-get install -y python3-dev python3-setuptools build-essential python3-distutils
```

- If you encounter a "No module named 'distutils'" error:
  1. Ensure setuptools is installed: `pip install setuptools`
  2. Install Python development packages: `sudo apt-get install python3-dev`
  3. For Python 3.12+, the distutils module is provided by setuptools

#### Windows-Specific Notes
- Install Python 3.12+ from python.org (not Microsoft Store version)
- Use `.\venv\Scripts\activate` instead of `source venv/bin/activate`
- The bot will automatically handle ChromeDriver installation
- Browser-based AI provider will be used with automatic fallback

#### Create Python Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

#### Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Configure the Bot
Create a `.env` file in the root directory:
```env
# Required settings
NATION_NAME=your_nation
PASSWORD=your_password

# Optional Discord integration (remove if not using Discord)
DISCORD_TOKEN=your_discord_token
DISCORD_CHANNEL_ID=your_channel_id
```

Note: 
- Discord integration is completely optional. The bot can run without Discord and will use console logging instead.
- ChromeDriver will be installed and configured automatically. For Windows users, the bot will use a browser-based AI provider with automatic fallback to other providers if needed.

### 3. Dashboard Setup

#### Backend Setup
```bash
cd dashboard/bot-dashboard
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend Setup
```bash
cd ../bot-dashboard-ui
npm install
```

## Running the Application

### 1. Start the Bot
In the root directory:
```bash
source venv/bin/activate
python main.py
```

### 2. Start the Dashboard Backend
In `dashboard/bot-dashboard`:
```bash
source venv/bin/activate
uvicorn app.main:app --reload --port 8001
```

### 3. Start the Dashboard Frontend
In `dashboard/bot-dashboard-ui`:
```bash
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8001
- API Documentation: http://localhost:8001/docs

## Environment Variables

### Frontend (.env)
Create a `.env` file in `dashboard/bot-dashboard-ui`:
```env
VITE_API_URL=http://localhost:8001
```

## Testing

### Backend Tests
```bash
cd dashboard/bot-dashboard
pytest
```

### Frontend Tests
```bash
cd dashboard/bot-dashboard-ui
npm test
```

## Production Deployment

### Backend Deployment
1. Ensure all dependencies are in `requirements.txt`
2. Set up environment variables
3. Deploy using a production ASGI server like Uvicorn or Gunicorn

### Frontend Deployment
1. Build the frontend:
```bash
cd dashboard/bot-dashboard-ui
npm run build
```

2. The built files will be in the `dist` directory, ready for deployment

## Common Issues & Troubleshooting

### Bot Issues
- Ensure Chrome/Chromium and ChromeDriver versions match
- Verify NationStates.net credentials
- Check network connectivity

### Dashboard Issues
- Verify API URL in frontend .env file
- Ensure all ports are available
- Check CORS settings if accessing from different domains

## Security Notes

- Never commit sensitive credentials
- Use environment variables for secrets
- Keep your Discord bot token private
- Follow NationStates.net ToS
- Review AI decisions in production

## Support

If you encounter any issues:
1. Check the troubleshooting section
2. Review the logs
3. Open an issue on GitHub
4. Contact the maintainers

Remember to always pull the latest changes before starting development:
```bash
git pull origin main
```
