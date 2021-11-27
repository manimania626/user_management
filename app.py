from flask import Flask, render_template,url_for,request,flash
from flask_mysqldb import MySQL
from werkzeug.utils import redirect

app = Flask(__name__)

#DATABASE CONNECTION
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="P$wd"
app.config["MYSQL_DB"]="crud"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql = MySQL(app)


#HOME PAGE LOADING
@app.route("/")
def home():
    con=mysql.connection.cursor()
    sql="SELECT * FROM USERS"
    con.execute(sql)
    res=con.fetchall()
    return render_template('home.html',datas=res)

#ADD USERS
@app.route("/addUsers", methods=["GET","POST"])
def addUsers(): 
    if request.method == "POST":
        name=request.form['name']
        age=request.form['age']
        city=request.form['city']
        con=mysql.connection.cursor()
        sql="insert into users(NAME,AGE,CITY) values(%s,%s,%s)"
        con.execute(sql,[name,age,city])
        mysql.connection.commit()
        con.close()
        flash('User added successfully!')
        return redirect(url_for("home"))
    return render_template("addUsers.html")

#UPDATE USERS
@app.route("/editUser/<string:id>",methods=['GET','POST'])
def editUser(id):
    con=mysql.connection.cursor()
    if request.method == "POST":
        name=request.form['name']
        age=request.form['age']
        city=request.form['city']
        con=mysql.connection.cursor()
        sql="update users set NAME=%s,AGE=%s, CITY=%s where id=%s"
        con.execute(sql,[name,age,city,id])
        mysql.connection.commit()
        con.close()
        flash('User updated successfully!')
        return redirect(url_for("home"))

    sql="select * from users where id=%s"
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template('editUser.html',datas=res)

#DELETE USERS
@app.route('/deleteUser/<string:ID>',methods=['POST','GET'])
def deleteUser(ID):
    con=mysql.connection.cursor()
    #sql="delete from users where ID=%s"
    con.execute("DELETE FROM users WHERE ID=%s", (ID,))
    #con.execute(sql,ID)
    mysql.connection.commit()
    con.close()
    flash('User deleted successfully!')
    return redirect(url_for("home"))

if(__name__=='__main__'):
    app.secret_key="abc123"
    app.run(debug=True)