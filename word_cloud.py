#!/bin/python3
import requests
import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import argparse

# A simple script for building a word cloud from your top artist on last.fm
# Hope you enjoy, let me know if you like using it @aircoolefe@infosec.exchange

parser = argparse.ArgumentParser(prog="Artist Wordcloud", description="Create a word cloud based upon your top artists from last.fm. Created by @aircooledcafe with love in Wales.")
parser.add_argument("-a", "--api_key", type=str, required=True, help="Your last.fm api key, reuqired. You can create one here https://www.last.fm/api/account/create.")
parser.add_argument("-u", "--user", type=str, required=True, help="Your last.fm username, required.")
parser.add_argument("-p", "--period", type=str, nargs='?', const="12month", help="The period you want to generate over, defaults to 12 months. Acceptable periods: overall | 7day | 1month | 3month | 6month | 12month")
parser.add_argument("-l", "--limit", type=int, nargs='?', const=200, help="Maximum number of artists to retreive, defaults to 200")
parser.add_argument("-m", "--mask", type=str, nargs='?', const="oval.png", help="Select a png file to use as a maks to change the output shape. There are sample masks in the 'masks' folder. Default os oval.png")
parser.add_argument("-c", "--colour", type=str, nargs='?', const="Reds_r", help="A colour for your text to appear in, defaults to red. Some useful values: Reds, Blues, Greens, Oranges, Greys, and Purples. Full list can be found in the colour_values.txt file.")

args = parser.parse_args()
api_key = args.api_key
user = args.user

period = "12month"
if args.period:
    period = args.period

limit = 200
if args.limit:
    limit = args.limit

mask_file = "masks/oval.png"
if args.mask:
    mask_file = args.mask

colour = "Reds_r"
if args.colour:
    colour = args.colour

cloud_mask = np.array(Image.open(mask_file))

def get_artists(api_key: str, user: str, period: str, limit: int):
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={user}&api_key={api_key}&period={period}&limit={limit}&format=json"
    
    response = requests.get(url)
    response.raise_for_status()
    
    return response.json()

def generate_dictionary(data):
    data_dict = {}
    
    for artist in data["topartists"]["artist"]:
        data_dict[artist["name"]] = int(artist["playcount"])
    return data_dict

def generate_wordcloud(data: dict, colour: str, mask: str):
    wordcloud = WordCloud(width=1800, height=1200, scale=2, min_font_size=10, prefer_horizontal=0.55, relative_scaling=1, colormap=colour, mask=mask).generate_from_frequencies(data)
    return wordcloud

# def generate_image(wordcloud):
#     plt.figure(figsize=(24,18))
#     plt.imshow(wordcloud, interpolation='bilinear')
#     plt.axis('off')
#     plt.savefig('artist_cloud.png', bbox_inches="tight", pad_inches=0.01)

def generate_image(wordcloud):
    fig = plt.figure(figsize=(24,18))
    ax = fig.add_subplot()
    plt.imshow(wordcloud)
    plt.axis('off')
    ax.text(0.95, 0.02, f"last.fm @{user}", verticalalignment='bottom', horizontalalignment='right', transform=ax.transAxes, color='grey', fontsize=20)
    plt.savefig('artist_cloud.png', bbox_inches="tight", pad_inches=0.01, dpi=300)

if __name__ == "__main__":
    response = get_artists(api_key, user, period, limit)
    
    artists_dict = generate_dictionary(response)
    
    wordcloud = generate_wordcloud(artists_dict, colour, cloud_mask)

    generate_image(wordcloud)
