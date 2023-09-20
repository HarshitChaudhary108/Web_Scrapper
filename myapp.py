from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import logging
import requests
from flask_cors import CORS, cross_origin
logging.basicConfig(filename="scrapper.log", level=logging.INFO)

app = Flask("__main__")

@app.route("/", methods = ["GET"])
def homepage():
    return render_template("index.html")

@app.route("/review", methods = ["GET", "POST"])
def reviews():
    if method == "POST":
        try :
            searchSting = request.form["content"].replace(" ", "")
            Flipcart_link = "https://www.flipkart.com/" + searchSting
            openpage = urlopen(Flipcart_link)
            readed_page = openpage.read()
            openpage.close()
            bs_page = bs(readed_page, "html.parser")
            bigboxes = bs_page.find_all("div", {"class":"_1AtVbE col-12-12"})
            box = bigboxes[0]
            product_link = "https://www.flipkart.com" + box.div.div.div.a["href"]
            product_page = requests.get(product_link)
            product_page.encoding='utf-8'
            productpage = bs(product_page.text, "html.parser")
            print(product_page)
            commentboxes = productpage.find_all("div", {"class", "col _2wzgFH"})

            filename = searchSting + ".csv"
            fw = open(filename, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write("headers")
            review = []
            for i in commentboxes:
                try :
                    name = i.find("div", {"class": "row _3n8db9"}).p.text
                except :
                    print("NOT FOUND")
                
                try :
                    ratings = i.div.div.div.div.text
                except :
                    print("NOT FOUND")
                
                try :
                    heading = i.find("div", {"class": "t-ZTKy"}).text
                except :
                    print("NOT FOUND")

                try :
                    comment = i.find("div", {"class": "t-ZTKy"}).text
                except:
                    print("NOT FOUND")

                my_dict = {"product":searchSting, "Customer Name":name, "Rating":ratings, "Heading":heading, "Comment":comment}
                review.append(my_dict)
            logging.info("log my final result {}").format(review)
            return render_template("result.html", reviews=review[0:len(review)-1])
        
        except Exception as e:
            return "Something is wrong {}".format(e)
    
    else :
        return render_template("index.html")

if __name__=="__main__":
    app.run(host="0.0.0.0")
