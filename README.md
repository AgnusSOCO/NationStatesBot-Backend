# NationStatesBot-Backend

An automated bot for NationStates.net that uses AI to make strategic decisions and Discord integration for monitoring.

## Features
- AI-powered decision making for nation dilemmas
- Discord bot integration for monitoring and control
- Automated web navigation with human-like behavior
- Economic data tracking and analysis

## Prerequisites
- Python 3.11+
- Chrome/Chromium browser
- Discord bot token and permissions
- NationStates.net account

## Installation
1. Clone the repository
```bash
git clone https://github.com/AgnusSOCO/NationStatesBot-Backend.git
cd NationStatesBot-Backend
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure the bot
- Update Chrome/Chromium path in `config.py`
- Set up Discord bot token in `main.py`
- Configure Discord channel ID in `config.py`

## Configuration
Key configuration files:

### config.py
- `binary_location`: Path to Chrome/Chromium binary
- `driver_path`: Path to ChromeDriver
- `channel_id`: Discord channel for bot notifications

### main.py
- `bot_token`: Your Discord bot token

## Usage
1. Start the bot:
```bash
python main.py
```

2. Follow the prompts to enter:
- Nation name
- Password

The bot will then:
- Log into your NationStates account
- Monitor for dilemmas
- Make AI-powered decisions
- Send updates via Discord
- Track economic data

## Architecture
- `main.py`: Entry point and main loop
- `web_automation.py`: Browser automation and AI decision making
- `config.py`: Configuration settings
- `utilities.py`: Helper functions
- `discord_bot.py`: Discord integration

## Security Note
- Never share your NationStates credentials
- Keep your Discord bot token private
- Review AI decisions before implementing in production

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.
