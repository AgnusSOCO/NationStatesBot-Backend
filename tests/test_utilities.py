import pytest
from utilities import display_banner, get_user_input, extract_economy_data
from unittest.mock import patch, MagicMock

def test_display_banner(capsys):
    """Test that display_banner prints the expected banner"""
    display_banner()
    captured = capsys.readouterr()
    assert "NationStatesBot" in captured.out
    assert "https://discord.gg" in captured.out

def test_get_user_input():
    """Test get_user_input with mocked input"""
    with patch('builtins.input', side_effect=['test_nation', 'test_pass']):
        nation, password = get_user_input()
        assert nation == 'test_nation'
        assert password == 'test_pass'

@pytest.mark.asyncio
async def test_extract_economy_data(tmp_path):
    """Test economy data extraction with mocked browser"""
    mock_browser = MagicMock()
    mock_browser.execute_script.return_value = [100, 200, 300]
    
    with patch('utilities.browser', mock_browser), \
         patch('builtins.open', create=True) as mock_open:
        extract_economy_data('test_nation')
        mock_browser.get.assert_called_once()
        mock_browser.execute_script.assert_called_once()
        mock_open.assert_called_once()
