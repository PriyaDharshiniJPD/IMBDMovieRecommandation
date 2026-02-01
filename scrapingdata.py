from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


# Set up the WebDriver (you can use Chrome or Firefox)
driver = webdriver.Chrome()  # Or use webdriver.Firefox() if you prefer Firefox
# Open the IMDb page
driver.get("https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31")

# Wait for the page to load
time.sleep(3)
# Define a function to click the "Load More" button
def click_load_more():#//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[2]/div/span/button/span/span
    try:#://*[@class="ipc-see-more sc-d3761d38-0 izLQkx single-page-see-more-button"]/span[2]
        # Locate the "Load More" button//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[2]/div/span/button/span/span
        load_more_button = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[2]/div/span/button/span/span')

        # Scroll to the "Load More" button to make sure it's in view
        ActionChains(driver).move_to_element(load_more_button).perform()

        # Click the button
        load_more_button.click()

        # Wait for new content to load
        time.sleep(3)
        return True
    except Exception as e:
        print("Error clicking 'Load More' button:", e)
        return False

# Click "Load More" until the button is no longer available
while click_load_more():
    print("Clicked 'Load More' button")

# Once the loop ends, we assume there is no more content to load
print("No more content to load.")

import pandas as pd
# //*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul/li[1]/div/div/div/div[1]/div[2]/div[1]/a/h3
# Initialize lists to store the scraped data
titles = []
story_lines = []

# Loop through all movie items on the page
movie_items = driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul/li')#'//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul/li')
# //*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul/li[1]/div/div/div/div[1]/div[2]/div[1]/a/h3
for movie_item in movie_items:#//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul/li[1]/div/div/div/div[1]/div[2]/span/div/span/span[2]
    try:
        # Extract the movie title//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul/li[2]/div/div/div/div[1]/div[2]/div[1]/a/h3
        title = movie_item.find_element(By.XPATH, './div/div/div/div[1]/div[2]/div[1]/a/h3').text
        
        story_line = movie_item.find_element(By.XPATH, './div/div/div/div[2]/div/div').text



        # Append the data to the lists
        titles.append(title)
        story_lines.append(story_line)

    except Exception as e:
        # If any element is not found, skip this movie and print an error message
        print(f"Error extracting data for a movie: {e}")
        continue

# Create a DataFrame using the extracted data
df = pd.DataFrame({
    'Title': titles,
    'Story_line' : story_lines
})


 # Save the DataFrame to a CSV file (optional)
df.to_csv('imdb_movies_2024(1).csv', index=False)

# Close the browser
driver.quit()