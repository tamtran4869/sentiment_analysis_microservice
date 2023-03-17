
# sentiment_analysis_microservice

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/tamtran4869/sentiment_analysis_microservice">
  </a>

  <h3 align="center">Sentiment Analysis Microservice</h3>

  <p align="center">
This is a small project to practice preprocessing data for sentiment analysis with the roBERTa pre-trained model and build a simple microservice with Flask which helps to classify sentiment labels for comments in a Facebook post or a tweet. It is beneficial to know overall reviews about a brand, a movie or a product in a post/tweet from public pages.
    <br />
    <br />
    <a href="https://github.com/tamtran4869/sql_challenge/issues">Report Bug</a>
    ·
    <a href="https://github.com/tamtran4869/sql_challenge/issues">Request Feature</a>
  </p>
</div>


<!-- CONTEXT -->
## About the service
### Scraping 
Using tweepy and facebook _scraper library to get comments and replies from the post/tweet. Facebook_scapper does not require a key, while the tweepy library needs a bearer key to scrape Twitter data using API.
The bearer key for Twitter can get from https://developer.twitter.com/en.

<!-- GETTING STARTED -->
### Preprocessing

The step includes removing user names, links, punctuations, and stopwords; drop NA, drop duplicates and lemmatization for removing tenses and transforming words into their original form.

### Translation and sentiment analysis
Using googletrans to translate non-English comments into English.
The microservice utilises the Twitter-roBERTa-base (https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment) to classify comments and return the results into an HTML template.

<!-- USAGE EXAMPLES -->
## Usage
To run microservice, go to the project direction

```sh
python3 sentiment_predict.py
```
After loading the microservice, open the given link

![image](https://user-images.githubusercontent.com/114192113/225885812-a45c5258-a201-4994-8418-e8621fed70a8.png)

![image](https://user-images.githubusercontent.com/114192113/225885875-0516a410-a234-4f11-a20e-94adf9c2513b.png)


Note: The translation and social networks API may limit the number of requests. 
<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/tamtran4869/sentiment_analysis_microservice.svg?style=for-the-badge
[contributors-url]: https://github.com/tamtran4869/sql_challenge/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/tamtran4869/sentiment_analysis_microservice.svg?style=for-the-badge
[forks-url]: https://github.com/tamtran4869/sql_challenge/network/members
[stars-shield]: https://img.shields.io/github/stars/tamtran4869/sentiment_analysis_microservice.svg?style=for-the-badge
[stars-url]: https://github.com/tamtran4869/sql_challenge/stargazers
[issues-shield]: https://img.shields.io/github/issues/tamtran4869/sentiment_analysis_microservice.svg?style=for-the-badge
[issues-url]: https://github.com/tamtran4869/sql_challenge/issues
