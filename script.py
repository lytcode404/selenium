from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the web driver
driver = webdriver.Chrome()  # Replace 'path_to_chrome_driver' with the actual path

# Open the YouTube video page
video_url = 'https://www.youtube.com/watch?v=ZDzy5JnAHsE'  # Replace 'your_video_id' with the actual video ID
driver.get(video_url)

# Wait for the comments section to load
comments_section = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="comments"]'))
)

# Scroll down to load more comments
while True:
    driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
    try:
        load_more_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#continuations yt-next-continuation button'))
        )
        driver.execute_script('arguments[0].click();', load_more_button)
    except:
        break

# Extract the comments
comment_authors = driver.find_elements(By.CSS_SELECTOR, '#author-text')
comment_texts = driver.find_elements(By.CSS_SELECTOR, '#content-text')

# Take only the top 10 comments
top_10_comments = []
for i in range(min(10, len(comment_authors))):
    author = comment_authors[i].text.strip()
    text = comment_texts[i].text.strip()
    comment = f'{author}: {text}'
    top_10_comments.append(comment)

# Write the comments to a text file
with open('comments.txt', 'w', encoding='utf-8') as file:
    for comment in top_10_comments:
        file.write(comment + '\n')

# Close the web driver
driver.quit()
