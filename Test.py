from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from bs4 import BeautifulSoup
import eplinkgenerator as eplink
import requests
app = Flask(__name__)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kittu2001",
    database="flask"
)
print('connected')
db = mydb.cursor()


@app.route('/')
def hello_world():
    print(request)
    return render_template('index.html')


@app.route('/addemployee', methods=['POST', 'GET'])
def addemp():
    if request.method == 'GET':
        return render_template('addemp.html')
    if request.method == 'POST':
        print(type(request.form["empid"]))
        q = f"insert into emp values (%s,%s,%s)"
        v = (int(request.form["empid"]), request.form["empname"],
             request.form["empage"])
        # print(q)
        db.execute(q, v)
        mydb.commit()
        # print(q)
        return redirect(url_for('getallemp'))


@app.route('/updateemp', methods=['GET', 'POST'])
def updateemp():
    if request.method == 'GET':
        return render_template('updateemp.html')
    if request.method == 'POST':
        que = "update emp set empname=%s,empage=%s where empid=%s"
        fq = (request.form["empname"],
              request.form["empage"], request.form["empid"])
        db.execute(que, fq)
        mydb.commit()
        return redirect(url_for('getallemp'))


@app.route('/deleteemp', methods=['GET', 'POST'])
def deleteemp():
    if request.method == 'GET':
        return render_template('deleteemp.html')
    if request.method == 'POST':
        q = f"delete from emp where empid={request.form['empid']}"
        db.execute(q)
        mydb.commit()
        return redirect(url_for('getallemp'))


@app.route('/delete/<int:empid>', methods=['POST'])
def delete(empid):
    # print(empid)
    return empid


@app.route('/getallemp')
def getallemp():
    db.execute("select * from emp")
    result = db.fetchall()
    emp = []
    for i in result:
        emp.append(i)
        # print(emp)
    return render_template('allemp.html', data=emp)


@app.route('/anime', methods=['POST', 'GET'])
def anime():
    if request.method == 'POST':
        anime = request.form['anime']
        ep = request.form['ep']
        anime = anime.replace(' ', '-')
        url = f'https://ww.gogoanimes.org/watch/{anime}-episode-{ep}'
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        ifr = soup.find_all('iframe')[0]
        attr = ifr['src']
        return render_template('anime.html', link=attr)
    if request.method == 'GET':
        return render_template('anime.html', link=None)


@app.route('/animehome')
def animehome():
    html = requests.get('https://animixplay.to/')
    soup = BeautifulSoup(html.content, "html.parser")
    return str(soup)


@app.route('/animix', methods=['GET', 'POST'])
def animix():
    if request.method == 'POST':
        anime = request.form['anime']
        ep = request.form['ep']
        # eplink.getiframepage()
        # linkep = eplink.getiframepage(anime, ep)
        animix = eplink.animix()
        lik = animix.getiframepage(anime, ep)
        animix.webd.quit()
        return render_template('anime.html', link=lik)
    if request.method == 'GET':
        return render_template('anime.html', link=None)


@app.route('/searchanime', methods=['POST', 'GET'])
def searchanime():
    if request.method == 'GET':
        return render_template('home.html')
    if request.method == 'POST':
        aniname = request.form['animename']
        searchres = eplink.gogoscrap()
        return searchres.search(aniname)


if __name__ == '__main__':
    app.run(debug=True)
