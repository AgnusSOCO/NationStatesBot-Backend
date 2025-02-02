from web_automation import browser
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.common.exceptions import TimeoutException  

def display_banner():
    banner = """                                            
       NationStatesBot
       https://discord.gg/8enej9h8
    """
    print(banner)
    print("\nStarting...\n")

# Get user input for nation name and password
def get_user_input() -> tuple[str, str]:
    print("Login to NationStatesBot")
    nation_name = input("Nation Name: ")
    password = input("Password: ")
    return nation_name, password

def extract_economy_data(nation_name):
    url = f"https://www.nationstates.net/nation={nation_name}/detail=trend"
    browser.get(url)

    # Wait for the Highcharts object to be defined
    try:
        WebDriverWait(browser, 10).until(
            lambda driver: driver.execute_script("return typeof Highcharts !== 'undefined';")
        )
    except TimeoutException:
        print("Highcharts library did not load in time.")
        return

    y_values_script = """
    var seriesData = Highcharts.charts[0].series[1].data;
    var yValues = [];
    for (var i = 0; i < seriesData.length; i++) {
        yValues.push(seriesData[i].y);
    }
    return yValues;
    """
    
    try:
        economy_data = browser.execute_script(y_values_script)
        with open("economy_data.txt", "a") as file:
            for data in economy_data:
                file.write(f"{nation_name}: {data}\n")
    except Exception as e:
        print(f"Error extracting economy data: {e}")
