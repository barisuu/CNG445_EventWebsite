from flask import *
import sqlite3
import re

app = Flask(__name__)
app.secret_key = "ced428fab82a18422645f3e5"

def validatePassword(password):
    #Regex expression of password criteria.
    expression = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"

    pattern = re.compile(expression)

    valid = re.search(pattern,password)

    if valid:
        return True
    else:
        return False


@app.route("/")
@app.route("/index")
def index(errorMsg=None):
    # Getting the info of cities to display as table titles.
    conn = sqlite3.connect("eventwebsite.db")
    c = conn.cursor()
    c.execute("SELECT * FROM city ORDER BY cityID")
    rows = c.fetchall()

    cities = {}
    for nameTuple in rows:
        cities[nameTuple[0]] = {
            "cityName": str(nameTuple[1]),
            "noOfEvents": 0,
            "events": []
        }

    c.execute("SELECT event.* FROM event JOIN city c on c.cityID = event.cityID")
    rows = c.fetchall()

    for tupleInfo in rows:
        if tupleInfo[8] in cities:
            cities[tupleInfo[8]]["noOfEvents"] += 1
            cities[tupleInfo[8]]["events"].append({
                "eventid":tupleInfo[0],
                "name":tupleInfo[1],
                "description":tupleInfo[2],
                "price":tupleInfo[3],
                "date":tupleInfo[4],
                "time":tupleInfo[5],
                "isActive":1,
                "location":tupleInfo[7],
            })
    #If username is in session that info will be sent during rendering as well.
    if 'username' in session:
        return render_template("index.html", username=session['username'],cityInfo=cities)
    else:
        if errorMsg:
            return render_template("index.html", cityInfo=cities,errorMsg=errorMsg)
        else:
            return render_template("index.html",cityInfo=cities)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/applyregister", methods=["GET","POST"])
def applyregister():
    if request.method == "POST":
        # Getting the values from submitted form.
        username = str(escape(request.form["username"]))
        password = str(escape(request.form["password"]))
        fname = str(escape(request.form["fname"]))
        lname = str(escape(request.form["lname"]))
        email = str(escape(request.form["email"]))
        conn = sqlite3.connect("eventwebsite.db")

        #Checking if username is unique
        c = conn.cursor()
        c.execute("SELECT username FROM user WHERE username=?",(username,))
        result=c.fetchone()

        # If result is not NONE then username exists.
        if result:
            errorMsg="Username already exists! Choose a different username"
            return render_template('register.html',errorMsg=errorMsg)
        # Checking if password fits the criteria
        elif validatePassword(password) == False:
            errorMsg = "Password must be at least eight digits and must include at least one upper case, one lower case and one digit."
            return render_template('register.html', errorMsg=errorMsg)
        else:
            c.execute("INSERT INTO user VALUES(?,?,?,?,?)", (username,password,fname,lname,email))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    elif request.method =="GET":
        pass
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = escape(request.form["username"])
        password = escape(request.form["password"])
        conn = sqlite3.connect("eventwebsite.db")
        c = conn.cursor()
        c.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password))
        row = c.fetchone()
        conn.close()
        if row != None:
            session["username"] = username
        else:
            errorMsg = "Username or password not found"
            return index(errorMsg)  # Calling the index method to display error msg. Don't know if this is bad practice.
        return redirect(url_for('index'))

    elif request.method == "GET":
        pass

@app.route("/logout")
def logout():
    session.pop("username",None)
    return redirect(url_for("index"))

@app.route("/newevent")
def newEvent():
    if "username" in session:
        # Getting the info of cities to use in combo box.
        conn = sqlite3.connect("eventwebsite.db")
        c = conn.cursor()
        c.execute("SELECT * FROM city ORDER BY cityID")
        cities = c.fetchall()


        return render_template("newEvent.html",cityInfo=cities)
    return redirect(url_for("index"))

@app.route("/addevent", methods=["GET", "POST"])
def addEvent():
    if (request.method == "POST" and "username" in session):

        eventName = str(escape(request.form["eventname"]))
        desc = str(escape(request.form["description"]))
        location = str(escape(request.form["location"]))
        city = str(escape(request.form["cities"]))
        price = str(escape(request.form["price"]))
        date = str(escape(request.form["date"]))
        time = str(escape(request.form["time"]))
        user = session["username"]

        conn = sqlite3.connect("eventwebsite.db")
        c = conn.cursor()
        c.execute("INSERT INTO event(name,description,price,date,time,location,cityID,username) VALUES(?,?,?,?,?,?,?,?)",
                  (eventName, desc, price, date, time,location, city,user))

        c.execute("SELECT cityname FROM city WHERE cityID=(?)",(city))
        row=c.fetchone()

        conn.commit()
        conn.close()


        return render_template("eventconfirmed.html",eventname=eventName,description=desc,location=location,city=row[0],
                               price=price,date=date,time=time)

    elif request.method == "GET":
        pass

@app.route("/eventinfo")
def eventInfo():
        eventID = request.args.get('id')
        conn = sqlite3.connect("eventwebsite.db")
        c = conn.cursor()


        c.execute("SELECT event.*,c.cityname FROM event JOIN city c on c.cityID = event.cityID WHERE eventid=(?)",(eventID))
        rows = c.fetchone()

        return render_template("eventinfo.html",eventInfo=rows)

@app.route("/ownedevents")
def ownEvents():
    # Getting the info of cities to display as table titles.
    conn = sqlite3.connect("eventwebsite.db")
    c = conn.cursor()
    c.execute("SELECT * FROM city ORDER BY cityID")
    rows = c.fetchall()

    cities = {}
    for nameTuple in rows:
        cities[nameTuple[0]] = {
            "cityName": str(nameTuple[1]),
            "noOfEvents": 0,
            "events": []
        }

    c.execute("SELECT event.*,c.cityname FROM event JOIN city c on c.cityID = event.cityID WHERE username=(?)",(str(session["username"]),))
    rows = c.fetchall()

    for tupleInfo in rows:
        if tupleInfo[8] in cities:
            cities[tupleInfo[8]]["noOfEvents"] += 1
            cities[tupleInfo[8]]["events"].append({
                "eventid":tupleInfo[0],
                "name":tupleInfo[1],
                "description":tupleInfo[2],
                "price":tupleInfo[3],
                "date":tupleInfo[4],
                "time":tupleInfo[5],
                "isActive":1,
                "location":tupleInfo[7],
            })
    #If username is in session that info will be sent during rendering as well.
    if 'username' in session:
        return render_template("ownedevents.html", username=session['username'],cityInfo=cities)
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
