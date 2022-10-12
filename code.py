from flask import json
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from pytube import YouTube
import time
from selenium.webdriver.common.by import By
import pandas as pd



app = Flask(__name__)
@app.route('/',methods=['GET'])  # route to display the home page
def greetings():
    return render_template("home.html")

@app.route('/home/search',methods=['POST'])
def search():
    if request.method == 'POST':
        # on the basis of search text...search on youtube
        search_text = request.form['search_text']
        url = "https://www.youtube.com/results?search_query="+search_text.replace(' ','+')

        # put that searching url into chrome driver with the help of selenium
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(url)
        time.sleep(7)

        # get channel details
        channel_section = driver.find_element(By.ID,"content-section")
        channel_details = channel_section.text.split("\n")
        channel_name = channel_details[0]
        channel_subscribers = channel_details[1].split(" ")[0]
        channel_desc = channel_details[2]
        no_of_videos = channel_details[1].split(" ")[1][12:]

        avtar = channel_section.find_element(By.XPATH,"//*[@id='avatar-section']/a")
        channel_url = avtar.get_attribute("href")
        img_section = channel_section.find_element(By.ID,"img")
        channel_avtar_url = img_section.get_attribute("src")

        driver.quit()
        #data = []
        data =  {"no_of_videos": no_of_videos,"channel_avtar_url": channel_avtar_url, "channel_url": channel_url}
        #data.append(my_dict)
        return render_template('Home.html',data = data)
        #return jsonify(my_dict)


@app.route('/home/search/top-videos',methods=['POST'])
def top_videos():
    if request.method == 'POST':
        channel_avtar_url = request.form['channel_avtar_url']
        no_of_videos = request.form['no_of_videos']
        channel_url = request.form['channel_url']

        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(channel_url)
        channel_name = driver.find_elements(By.ID, "text-container")[0].text
        channel_subscribers = driver.find_elements(By.ID, "subscriber-count")[0].text

        no_of_videos=20
        count = 0
        while True:
            driver.execute_script("window.scrollBy(0,1000)", "")
            time.sleep(3)
            video_sections = driver.find_elements(By.ID, "thumbnail")[1:21]
            if len(video_sections) >= no_of_videos:
                break
            count = count + 1

        video_links = []
        for i in video_sections:
            if i not in video_links:
                video_links.append(i.get_attribute("href"))
        print(video_links)

        video_titles = []
        for i in video_links:
            yt = YouTube(i)
            video_titles.append(yt.title)
        print(video_titles)

        video_thumbnail_urls = []
        for i in video_links:
            yt = YouTube(i)
            video_thumbnail_urls.append(yt.thumbnail_url)
        print(video_thumbnail_urls)

        driver.quit()

        #data1 = []
        result = {"video_thumbnail_urls": video_thumbnail_urls,"video_titles": video_titles , "video_links":video_links}
        #data1.append(mydict1)
        return render_template('Table.html',data = result)



if __name__ == "__main__":
    app.run(port = 5002,debug=True)