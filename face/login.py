from flask import *
import sqlite3 as sql
from flask import render_template
from flask import request
import os.path
import cv2

app = Flask(__name__)
app.secret_key = "aishwarya"


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/add',methods=['POST'])
def add():
    if request.method == 'POST':
      name = request.form.get('name')
      password = request.form.get('password')

      con = sql.connect("database.db")
      cur = con.cursor()
      cur.execute('''INSERT INTO details(name,password) VALUES (?,?)''',(name,password))
      con.commit()
      con.close()
      return render_template('login.html')

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/password')
def password():
    return render_template('password.html')

@app.route('/face')
def face():
    return render_template('face.html')

@app.route('/capture')
def capture():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("face capture")
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("face capture", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            count = 1
            name = session['name']
            img_name = "{}.jpg".format(name)
            save_path = '/home/neosoft/Desktop/Aishwarya_codes/face/static/users_images'
            completeName = os.path.join(save_path, img_name)
            cv2.imwrite(completeName, frame)
            status = "{} written!".format(img_name)
            break

    cam.release()
    cv2.destroyAllWindows()
    return render_template('success.html',status = status)


@app.route('/check',methods=['POST','GET'])
def check():
    name = request.form.get('name')
    password = request.form.get('password')

    with sql.connect('database.db') as con:
      cur = con.cursor()
      c = cur.execute(f"SELECT * from details WHERE name='{name}' AND password='{password}'")
      if not c.fetchone():
          return render_template('home.html')
      else:
          con.row_factory = sql.Row
          cur = con.cursor()
          cur.execute(f"SELECT * from details WHERE name='{name}' AND password='{password}'")
          if request.method == "POST":
            session['name'] = request.form['name']
          return render_template("success.html")

      con.close()


if __name__ == '__main__':
    app.run(debug=True)