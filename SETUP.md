# NationStatesBot Setup Guide 🚀

This guide will help you set up and run both the NationStatesBot and its dashboard components.

## Prerequisites

Before starting, ensure you have:

- Python 3.12+
- Node.js 18+
- Chrome/Chromium browser (will be configured automatically)
- Git
- OpenAI API key (required for AI decision making)
- Discord bot token (optional)

## Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/AgnusSOCO/NationStatesBot-Backend.git
cd NationStatesBot-Backend
```

### 2. Bot Setup

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
1. Create a `.env` file in the root directory with your OpenAI API key and optional Discord token:
```env
OPENAI_API_KEY=your_api_key_here
DISCORD_TOKEN=your_discord_token  # Optional
```

2. Configure your bot settings:
```python
NATION_NAME = "your_nation"
PASSWORD = "your_password"
CHANNEL_ID = "your_discord_channel"  # Optional for Discord
```

Note: ChromeDriver will be installed and configured automatically.

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

### Bot Configuration (.env)
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_api_key_here  # Required for AI-powered decision making
DISCORD_TOKEN=your_discord_token   # Optional: for Discord integration
```

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
