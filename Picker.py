import requests
import urllib.request
import os
import base64
import glob
import argparse as parser
from tqdm import tqdm
from bs4 import BeautifulSoup as Bs
from time import sleep
from urllib.parse import urlparse, unquote

joyreactor_headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

other_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'img0.pornreactor.cc',
    'Referer': 'http://pornreactor.cc/post/4447487',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36 OPR/62.0.3331.105'
    }


def is_valid(url):
    parsed = urlparse(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/32.0.1700.107 Safari/537.36'}
    code = requests.get(url, headers=headers).status_code
    return bool(parsed.netloc) and bool(parsed.scheme) and bool(code == 200)


def get_pages_count(url):
    soup = Bs(requests.get(url).content, "html.parser")
    count = 0
    for tags in tqdm(soup.find_all("a"), ascii=True, desc="Counting pages"):
        tag_class = tags.attrs.get("class")
        if type(tag_class) is list and len(tag_class) > 0:
            if tag_class[0] == "next":
                count = tags.attrs.get("href").split("/")[3]
        sleep(0.01)
    return int(count)


def get_page_articles(url, page_num):
    soup = Bs(requests.get(url).content, "html.parser")
    links = []
    for tags in tqdm(soup.find_all("a", string="ссылка"), ascii=True, desc="Getting articles from page " + str(page_num)):
        if tags.attrs.get("title") == "ссылка на пост":
            links.append(urlparse(url).scheme + "://" + urlparse(url).netloc + tags.attrs.get("href"))
        sleep(0.1)
    return links


def get_images(url, directory):
    global joyreactor_headers
    try:
        post_dir = directory + "\\" + url.rsplit('/', 1)[1]
        if not os.path.exists(post_dir):
            os.mkdir(post_dir)

        if not os.path.exists(post_dir + "\\" + "Photo"):
            os.mkdir(post_dir + "\\" + "Photo")

        page_content = requests.get(url, joyreactor_headers).content
        soup = Bs(page_content, "html.parser")
        long = soup.find("div", {"class": ["post_content", "allow_long"]})
        if long is not None and soup is not None:
            all_images = []
            if len(long) == 0:
                all_images.clear()
                all_tags = long.findAll("div", {"class": "image"})
                for test_tag in all_tags:
                    result = test_tag.findChild()
                    if result.name == 'a':
                        all_images.append(result['href'])
                    elif result.name == 'img':
                        all_images.append(result['src'])
            else:
                all_images.clear()
                all_tags = long.findAll("div", {"class": "image"})
                for test_tag in all_tags:
                    result = test_tag.findChild()
                    if result.name == 'a':
                        all_images.append(result['href'])
                    elif result.name == 'img':
                        all_images.append(result['src'])
            for img in all_images:
                if (".jpeg" or ".png" in img) and ("-gif-" and ".gif" not in img):
                    if not os.path.exists(post_dir + "\\" + "Photo" + "\\" + unquote(img.rsplit('/', 1)[1])):
                        f = open(post_dir + "\\" + "Photo" + "\\" + unquote(img.rsplit('/', 1)[1]), 'wb')
                        other_headers['Referer'] = url
                        other_headers['Host'] = urlparse(img).netloc
                        file_content = requests.get(img, headers=other_headers).content
                        f.write(file_content)
                        f.close()
                        print("Image: " + unquote(img.rsplit('/', 1)[1]) + " downloaded!")
                    else:
                        print("Image " + unquote(img.rsplit('/', 1)[1]) + " is already downloaded!")
                sleep(0.5)
        else:
            print("Error occured while processing this url: " + url)
    except Exception as e:
        print(e)


def get_gif(url, directory):
    post_dir = directory + "\\" + url.rsplit('/', 1)[1]
    if not os.path.exists(post_dir):
        os.mkdir(post_dir)

    if not os.path.exists(post_dir + "\\" + "Gif"):
        os.mkdir(post_dir + "\\" + "Gif")

    soup = Bs(requests.get(url).content, "html.parser")
    long = soup.find("div", {"class": ["post_content", "allow_long"]})
    if long is not None and soup is not None:
        if len(long) == 0:
            tags = [elm["href"] for elm in soup.select('a.video_gif_source') if "comment" not in elm["href"]]
        else:
            tags = [elm["href"] for elm in soup.select('a.video_gif_source') if "comment" not in elm["href"]]
        for gif in tags:
            if ".gif" in gif:
                if not os.path.exists(post_dir + "\\" + "Gif" + "\\" + unquote(gif.rsplit('/', 1)[1])):
                    f = open(post_dir + "\\" + "Gif" + "\\" + unquote(gif.rsplit('/', 1)[1]), 'wb')
                    other_headers['Referer'] = url
                    other_headers['Host'] = urlparse(gif).netloc
                    file_content = requests.get(gif, headers=other_headers).content
                    f.write(file_content)
                    f.close()
                    print("Gif: " + unquote(gif.rsplit('/', 1)[1]) + " downloaded!")
                else:
                    print("This gif is already downloaded!")
            sleep(0.5)
    else:
        print("Error occured while processing this url: " + url)
        

def get_coub(url, directory):
    post_dir = directory + "\\" + url.rsplit('/', 1)[1]
    if not os.path.exists(post_dir):
        os.mkdir(post_dir)
    if not os.path.exists(post_dir + "\\" + "Coub"):
        os.mkdir(post_dir + "\\" + "Coub")

    soup = Bs(requests.get(url).content, "html.parser")
    long = soup.find("div", {"class": ["post_content", "allow_long"]})
    if long is not None and soup is not None:
        if len(long) != 0:
            tags = [elm["src"] for elm in soup.select('div.image iframe[src]') if "youtube" not in elm["src"]]
        else:
            tags = [elm["src"] for elm in long.select('div.image iframe[src]') if "youtube" not in elm["src"]]
        for coub_tag in tags:
            if "coub" in coub_tag:
                link = coub_tag.split('?', 1)[0].replace("embed", "view")
                files = glob.glob(post_dir + "\\" + "Coub" + "\\*" + link.rsplit('/', 1)[1] + "*")
                if len(files) == 0:
                    video = coub.video(link, post_dir + "\\" + "Coub" + "\\")
                    audio = coub.audio(link, post_dir + "\\" + "Coub" + "\\")
                    if "not found" in audio:
                        print("Coub audio: " + audio)
                    else:
                        print("Coub audio: " + audio + " downloaded!")

                    if "not found" in video:
                        print("Coub video: " + video)
                    else:
                        print("Coub video: " + video + " downloaded!")
                else:
                    print("This coub is already downloaded!")
            sleep(0.5)
    else:
        print("Error occured while processing this url: " + url)


def process_posts(links, directory):
    if not os.path.exists(directory):
        os.mkdir(directory)
    for link in links:
        get_coub(link, directory)
        get_gif(link, directory)
        get_images(link, directory)
        print("======================||Post " + link.rsplit('/', 1)[1] + " successfully processed!||======================")


def decode_url(text):
    message_bytes = base64.b64decode(text)
    message = message_bytes.decode('ascii')
    return message


def replace_forbidden_symbs(text):
    chars = ['\\', '/', '"', '*', ':', '<', '>', '|', '?']
    for c in chars:
        if c in text:
            text = text.replace(c, "_")
    return text


def main(url, path, type):
    if is_valid(url):
        main_dir = urlparse(url).netloc
        if not os.path.exists(main_dir):
            os.mkdir(main_dir)
        if type == "post":
            if not os.path.exists(os.getcwd() + "\\" + main_dir + "\\" + "Posts"):
                os.mkdir(os.getcwd() + "\\" + main_dir + "\\" + "Posts")
            get_coub(url, os.getcwd() + "\\" + main_dir + "\\" + "Posts")
            get_gif(url, os.getcwd() + "\\" + main_dir + "\\" + "Posts")
            get_images(url, os.getcwd() + "\\" + main_dir + "\\" + "Posts")
            print("======================||Post " + url.rsplit('/', 1)[1] + " successfully processed!||======================")
        elif type == "tag":
            if not os.path.exists(os.getcwd() + "\\" + main_dir + "\\" + "Tags"):
                os.mkdir(os.getcwd() + "\\" + main_dir + "\\" + "Tags")
            print("Oh, category")
            count = get_pages_count(url) + 1
            posts = get_page_articles(url, count)
            process_posts(posts, os.getcwd() + "\\" + main_dir + "\\" + "Tags\\" + path)
            count -= 1
            while count > 0:
                posts = get_page_articles(url + "/" + str(count), count)
                process_posts(posts, os.getcwd() + "\\" + main_dir + "\\" + "Tags\\" + path)
                print("=========||Page " + str(count) + " successfully processed! Continuing...||=========")
                count -= 1
    else:
        print("\n===============\nI have found nothing on this link!\nCheck your link, bro!\n===============\n")


class Coub:

    def connect(self, url):
        url = url.replace("https://coub.com/view/", "http://coub.com//api/v2/coubs/")
        data = requests.get(url).json()
        return data

    def dl(self, directlink, fn):
        opener = urllib.request.build_opener()
        opener.addheaders = [("User-agent", "Mozilla/5.0")]
        dldata = opener.open(directlink)
        self.saveData(dldata, fn)

    def saveData(self, dldata, fn):
        if fn[-3:] == 'mp4':
            with open(fn, 'wb') as f:
                f.write(b'\x00\x00' + dldata.read()[2:])
        if fn[-3:] == 'mp3':
            with open(fn, 'wb') as f:
                f.write(dldata.read())

    def fileName(self, data, ftype, addlink):
        if addlink == True:
            fn = data["title"] + '-' + data["permalink"] + '.' + ftype
        else:
            fn = data["title"] + data["permalink"] + '.' + ftype

        if addlink == "no utf-8":
            fn = 'coub-' + data["permalink"] + '.' + ftype
        return replace_forbidden_symbs(fn)

    def video(self, url, path, addlink=True, audio=False):
        if audio == True:
            formt = "audio"
        else:
            formt = "video"
        try:
            data = self.connect(url)
            if type(data) is dict:
                if 'error' in data.keys():
                    return(data['error'])
                else:
                    try:
                        directlink = data["file_versions"]["html5"][formt]["high"]["url"]
                    except:
                        directlink = data["file_versions"]["html5"][formt]["med"]["url"]

                    fn = self.fileName(data, directlink[-3:], addlink)
                    self.dl(directlink, path + fn)

                    if fn is not None:
                        return fn
                    else:
                        return "get an error"
        except:
            if not data['has_sound']:
                return None
            print("Error. Check internet connection and check coub.com link")

    def audio(self, url, addlink=True):
        name = self.video(url, addlink, audio=True)
        if name is not None:
            return name
        else:
            return "get an error"


if __name__ == "__main__":
    url_type = ""
    coub = Coub()

    args = parser.ArgumentParser(description="This script downloads all images from a posts and categories in"
                                                 "joyreactor.cc")
    args.add_argument("url", help="The URL of the article/category you want to download images")
    args.add_argument("-p", "--path",
                        help="The Directory you want to store your images, default is the script folder with new"
                             " directory called with post/category name")

    arguments = args.parse_args()
    url = arguments.url
    path = arguments.path

    if not path:
        url_type = urlparse(url).path.split("/")
        decode = unquote(url_type[2])

        if url_type[2] != decode:
            url_type[2] = decode

        path = url_type[2]

    main(url, path, url_type[1])
