from flask import Flask,render_template,request,redirect,url_for,session
import pymysql
import os
app=Flask(__name__)
app.secret_key = os.urandom(24)

connection=pymysql.connect(host='localhost',user='root',password='',db='flaskmartdb')
@app.route('/')
def home():
    return render_template("login.html")
@app.route('/check', methods=['GET','POST'])
def check():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['pass']
        cursor = connection.cursor()
        cursor.execute("select *from login where username ='"+username+"' and  password='" +password+"'")
        user = cursor.fetchone()
        if user is None:
            return "Username or Password is wrong"
        else:
            return render_template("studentdata.html")
@app.route('/admin_check',methods=["GET","POST"])
def admin():
    if request.method == 'POST':
        username = request.form['auser']
        password = request.form['apass']
        cursor = connection.cursor()
        cursor.execute("select *from admin where username ='"+username+"' and  password='" +password+"'")
        user = cursor.fetchone()
        if user is None:
            return "Username or Password is wrong"
        else:
            return render_template("indexdb.html")
    return render_template("admin.html")

@app.route('/studentdata',methods=["GET","POST"])
def user():
        sql1 = "SELECT *FROM studentflask"
        connection = pymysql.connect(host='localhost', user='root', password='', db='flaskmartdb')
        with connection.cursor() as cursor:
            cursor.execute(sql1)
            res1 = cursor.fetchall()
            return render_template("studentdata.html", rs1=res1)
@app.route('/addstd',methods=['GET','POST'])
def addstudent():
    msg1="-"

    sid=getmax();

    if request.method=='POST':
        sname=request.form.get('stdnm')
        sadd=request.form.get('sadd')
        scity=request.form.get('scity')
        sfee=request.form.get('sfee')

        UPLOAD_FOLDER=os.path.basename('static')
        app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

        file=request.files['photo']

        ufname="img_"+str(sid)+".jpg"

        f=os.path.join(app.config['UPLOAD_FOLDER'],ufname)
        file.save(f)



        connection=pymysql.connect(host='localhost',user='root',password='',db='flaskmartdb')

        with connection.cursor() as cursor:
            sql1="INSERT INTO studentflask (roll_no,std_name,std_add,std_city,std_fees,img_file) VALUES (%s,%s,%s,%s,%s,%s)"

            cursor.execute(sql1,(sid,sname,sadd,scity,sfee,ufname))

            connection.commit()

        msg1="Record Added Successfully"

        sid=getmax();

    return render_template('addstudent.html',msg=msg1,maxid=sid)

@app.route('/managestd')

def managestudent():
    sql1="SELECT *FROM studentflask"
    connection=pymysql.connect(host='localhost',user='root',password='',db='flaskmartdb')

    with connection.cursor() as cursor:
        cursor.execute(sql1)
        res1=cursor.fetchall()
        return render_template("managestd.html",rs1=res1)

@app.route('/delstd',methods=['GET','POST'])
def delstd():
    dil=request.args.get('id')
    connection = pymysql.connect(host='localhost', user='root', password='', db='flaskmartdb')

    sql1="DELETE FROM studentflask where roll_no = "+dil

    with connection.cursor() as cursor1:
        cursor1.execute(sql1)
        connection.commit()

    sql1="SELECT *FROM studentflask"
    connection = pymysql.connect(host='localhost', user='root', password='', db='flaskmartdb')
    with connection.cursor() as cursor:
        cursor.execute(sql1)
        res1 = cursor.fetchall()
        return render_template("managestd.html", rs1=res1)

@app.route('/updatestd',methods=['GET','POST'])
def updatestd():
    sid=request.args.get('id')
    connection = pymysql.connect(host='localhost', user='root', password='', db='flaskmartdb')
    sql1 = "select *FROM studentflask where roll_no = "+sid
    with connection.cursor() as cursor1:
        cursor1.execute(sql1)
        res1 = cursor1.fetchall()
        return render_template("updatestd.html", rs1=res1)


@app.route('/updateprocestd',methods=['GET','POST'])
def updateprocestd():

    if request.method=='POST':
        sid=request.form.get('rno')
        sname=request.form.get('stdnm')
        sadd=request.form.get('sadd')
        scity=request.form.get('scity')
        sfee = request.form.get('sfee')

        UPLOAD_FOLDER=os.path.basename('static')
        app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
        file=request.files['photo']
        ufname="img_"+str(sid)+".jpg"
        f=os.path.join(app.config['UPLOAD_FOLDER'],ufname)
        file.save(f)

        connection=pymysql.connect(host='localhost',user='root',password='',db='flaskmartdb')

        with connection.cursor() as cursor:
            sql1 = "UPDATE studentflask SET std_name = %s,std_add = %s,std_city = %s,std_fees = %s,img_file = %s where roll_no = %s"

            cursor.execute(sql1,(sname,sadd,scity,sfee,ufname,sid))
            connection.commit()

        sql1="SELECT * FROM studentflask"
        connection = pymysql.connect(host='localhost', user='root', password='', db='flaskmartdb')
        with connection.cursor() as cursor:
            cursor.execute(sql1)
            res1 = cursor.fetchall()
            return render_template("managestd.html", rs1=res1)

def getmax():
    connection = pymysql.connect(host='localhost', user='root', password='', db='flaskmartdb')
    with connection.cursor() as cursor:
        cursor.execute("select max(roll_no) from studentflask")
        res1 = cursor.fetchall()
        id=1
        try:
            id=res1[0][0]+1
        except:
            id=1
        return id
#if __name__ == '__main':
app.run(debug=True)













