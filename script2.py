import time
from bs4 import BeautifulSoup
from selenium import webdriver

# Initialize ChromeDriver
driver = webdriver.Chrome()

# Open YouTube page
driver.get('https://www.youtube.com/watch?v=a6Xs2Ir40OI')

# Scroll and load more comments
SCROLL_PAUSE_TIME = 2

def end_of_comments():
    # Add your logic here to determine if all comments have been loaded
    # For example, check if a "Load more" button is present or if the scroll position has reached the bottom
    return True

while True:
    # Scroll to the bottom of the page
    driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')

    # Wait for some time to let the comments load
    time.sleep(SCROLL_PAUSE_TIME)

    # Check if all comments have been loaded
    if end_of_comments():
        break

# Get the page source
page_source = driver.page_source

# Create a BeautifulSoup object
soup = BeautifulSoup(page_source, 'html.parser')

# Extract the comments using appropriate CSS selectors
comments = soup.select('yt-formatted-string#content-text span')

# Process and display the top 10 comments
for comment in comments[:10]:
    print("Comment:", comment.text)

# Open a file for writing
with open('comments.txt', 'w', encoding='utf-8') as file:
    # Write each comment to the file
    for comment in comments[:10]:
        file.write(comment.text + '\n')

# Notify the user that the comments are saved
print('Comments saved to comments.txt')

# Close the browser
driver.quit()
