# NationStatesBot 🌐

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB.svg)](https://reactjs.org)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.3.2-7289DA.svg)](https://discordpy.readthedocs.io/)

An automated bot for NationStates.net that uses AI for strategic decision-making. Features include automated dilemma resolution, activity monitoring, and a real-time dashboard interface.

## 🚀 Features

- **AI-Powered Decision Making**: Utilizes advanced AI models to make strategic decisions for your nation
- **Automated Dilemma Resolution**: Automatically handles nation dilemmas with intelligent choices
- **Real-Time Dashboard**: Monitor and control your bot through a modern web interface
- **Activity Logging**: Comprehensive logging of all bot actions and decisions
- **Discord Integration**: Optional notifications and controls through Discord

## 📊 Dashboard

The NationStatesBot now includes a modern web dashboard for real-time monitoring and control:

- **Live Status**: Monitor bot status, version, and current nation
- **Action Logs**: View detailed logs of dilemmas, decisions, and navigation
- **Control Panel**: Start/stop the bot and configure settings
- **Dark Mode**: Comfortable viewing in any lighting condition

## 🛠 Prerequisites

- Python 3.12+
- Node.js 18+ (for dashboard)
- Chrome/Chromium browser
- Discord bot token (optional)

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/AgnusSOCO/NationStatesBot-Backend.git
cd NationStatesBot-Backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install dashboard dependencies:
```bash
cd dashboard/bot-dashboard-ui
npm install
```

## ⚙️ Configuration

1. Configure your bot settings in `config.py`:
```python
NATION_NAME = "your_nation"
PASSWORD = "your_password"
DISCORD_TOKEN = "your_discord_token"  # Optional
```

2. Start the backend server:
```bash
cd dashboard/bot-dashboard
uvicorn app.main:app --reload
```

3. Start the dashboard:
```bash
cd dashboard/bot-dashboard-ui
npm run dev
```

## 🏗 Project Architecture

```
NationStatesBot-Backend/
├── main.py              # Bot entry point
├── web_automation.py    # Web interaction logic
├── utilities.py         # Helper functions
├── config.py           # Configuration
├── discord_bot.py      # Discord integration
├── dashboard/          # Web dashboard
│   ├── bot-dashboard/  # FastAPI backend
│   └── bot-dashboard-ui/ # React frontend
└── tests/             # Test suite
```

## 🔒 Security Note

- Keep your credentials secure
- Don't share your config.py
- Use environment variables for sensitive data
- Follow NationStates.net ToS

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- NationStates.net for the platform
- The Discord.py community
- All contributors to this project
