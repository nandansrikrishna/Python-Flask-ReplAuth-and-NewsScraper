from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import pandas as pd
from textblob import TextBlob

app = Flask('app')

@app.route('/')
def hello_world():
    print(request.headers) 
    return render_template(
        'index.html',
        user_id=request.headers['X-Replit-User-Id'],
        user_name=request.headers['X-Replit-User-Name'],
        user_roles=request.headers['X-Replit-User-Roles'],
      user_bio=request.headers['X-Replit-User-Bio'],
      user_profile_image=request.headers['X-Replit-User-Profile-Image'],
      user_teams=request.headers['X-Replit-User-Teams'],
      user_url=request.headers['X-Replit-User-Url']
    )

@app.route('/scrapebbc')
def bbcscraper():
  # Make a request to the BBC News website
  url = "https://www.bbc.com/news"
  response = requests.get(url)
  
  if response.status_code != 200:
      print('Error: Could not retrieve website')
      exit(1)
  
  # Parse the HTML content of the page with BeautifulSoup
  soup = BeautifulSoup(response.content, "html.parser")
  
  # Extract the text of the headlines from the HTML content
  headlines = []
  for item in soup.find_all('h3', class_='gs-c-promo-heading__title'):
      headlines.append(item.text.strip())
  
  # Perform sentiment analysis on the headlines
  num_positive = 0
  num_negative = 0
  sentiments = []
  for headline in headlines:
      blob = TextBlob(headline)
      sentiment = blob.sentiment.polarity
      if sentiment > 0:
        sentiments.append("Positive")
        num_positive += 1
      elif sentiment < 0:
        sentiments.append("Negative")
        num_negative += 1
      else:
        sentiments.append("Neutral")
  
  # Create a DataFrame and save it to a CSV file
  data = {'Headline': headlines, 'Sentiment': sentiments}
  df = pd.DataFrame(data)
  df.to_csv('news_headlines.csv', index=False)
  
  if (num_positive > num_negative):
    return "More Positive Today :)"
  elif (num_negative > num_positive):
    return ":("
  else:
    return "Pretty Neutral Day"

@app.route('/scrapenyt')
def nytscrapper():
  url = "https://www.nytimes.com/"
  response = requests.get(url)
  
  if response.status_code != 200:
      print('Error: Could not retrieve website')
      exit(1)
  
  soup = BeautifulSoup(response.content, "html.parser")
  
  headlines = []
  for item in soup.find_all('h2'):
      headline = item.get_text().strip()
      if len(headline) > 0:
          headlines.append(headline)
  
  num_positive = 0
  num_negative = 0
  sentiments = []
  for headline in headlines:
      blob = TextBlob(headline)
      sentiment = blob.sentiment.polarity
      if sentiment > 0:
          sentiments.append("Positive")
          num_positive += 1
      elif sentiment < 0:
          sentiments.append("Negative")
          num_negative += 1
      else:
          sentiments.append("Neutral")
  
  data = {'Headline': headlines, 'Sentiment': sentiments}
  df = pd.DataFrame(data)
  df.to_csv('nyt_headlines.csv', index=False)
  
  if (num_positive > num_negative):
      print("More Positive Today :)")
  elif (num_negative > num_positive):
      print(":(")
  else:
      print("Pretty Neutral Day")
  

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

