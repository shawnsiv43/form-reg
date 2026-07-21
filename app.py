from flask import Flask,request,jsonify,render_template,redirect,url_for
import sqlite3
#import webbrowser

def get_db():
    conn=sqlite3.connect("C:\\databases\\formregsave.db")
    conn.row_factory=sqlite3.Row
    return conn

latest_sql_err=None

app=Flask(__name__)
@app.route("/regform")
def dis():
    return render_template("form.html")
@app.route("/api/reg")
def diss():
    global latest_sql_err
    conn=sqlite3.connect("C:\\databases\\formregsave.db")
    cursor=conn.cursor()
    uName=request.args.get("uName")
    print("uname is",uName)
    eName=request.args.get("eName")
    print("eName is",eName)
    passName=request.args.get("passName")
    print("passName is",passName)
    ageName=request.args.get("ageName")
    print("ageName is",ageName)
    try:
        information=(uName,eName,ageName,passName)
        insert_query='''Insert into info(username,email,age,password)
        Values(?,?,?,?)'''

        cursor.execute(insert_query,information)
        print('db saved')

        conn.commit()
        latest_sql_err=None
        return jsonify({"regMsg":f"Your Registration has been {uName}, {eName}, {passName}, {ageName}"})
    except sqlite3.IntegrityError as e:
        latest_sql_err=str(e)

        return jsonify({"regMsg":f"Registration failure. Integrity constraint on {uName}","error":latest_sql_err})
    finally:
        conn.close()
# @app.route("/success")
# def disss():
#     global latest_sql_err
    isSuccess=request.args.get("isSuccess")
    # html_content=f"""<h1>{isSuccess}</h1>
    # <a href="http://127.0.0.1:5000/regform">Register a change in the fields</a>"""
    # with open("index2.html","w") as file:
    #     file.write(html_content)
    #webbrowser.open("index2.html")
    # if latest_sql_err:
    #     error_to_return=latest_sql_err
    #     latest_sql_err=None
    #     return jsonify({"status":"error","error":error_to_return})
    # return jsonify({"status":"success","error":None})
    #webbrowser.open("C:\\Users\\hi_sh\\python-coding-git\\form-reg\\templates\\success.html")
    #return "<H1>success</H1>"

    # print("success",isSuccess)
    # return render_template(
    #     "success.html",
    #     isSuccess=isSuccess
    # )
# @app.route("/search")
# def dissss():
#     return render_template(
#         "search.html"
#     )
# @app.route("/search_submit")
# def disssss():
#     print("happy")
#     conn=sqlite3.connect("C:\\Users\\hi_sh\\formregsave.db")
#     cursor=conn.cursor()
#     input=request.args.get("input")
#     query="SELECT * from info where username=?"
#     rows=cursor.execute(query,(input,)).fetchall()
#     conn.commit()
#     string=''
#     for row in rows:
#         string=f"""Username: {row[0]}
#         Email: {row[1]}
#         Age: {str(row[2])}
#         Password: {str(row[3])}
#         Confirm Passord: {row[4]}"""
#     conn.close()
#     return jsonify({'lll':string})

@app.route("/delete/<string:input2>",methods=['GET','POST'])
def delete(input2):
    conn=sqlite3.connect("C:\\databases\\formregsave.db")
    cursor=conn.cursor()
    #input2=request.args.get("input2")
    print(input2)
    query2="""Delete From info
    where username=?"""
    cursor.execute(query2,(input2,))
    conn.commit()
    conn.close()
    return redirect(url_for("list_all_users"))

@app.route("/update/<string:username>", methods=['GET','POST'])
def update(username):
    conn=get_db()
    print("Shawn")
    print(request.method)
    print(username)



    print("Mmarcus")
    if request.method=="POST":

        data=request.get_json()
        print(data)
        print(data["email"])
        print(data["age"])
        print(data["password"])
        print(username)
        try:
            sql_query="""Update info
            Set email=?,
            age=?,
            password=?,
            Where username=?"""
            conn.execute(sql_query,(data["email"],data["age"],data["password"],username))
            conn.commit()
            return jsonify({"happy":"success"})
        finally:
            conn.close()
    print("Get stuff called")
    print(username)
    user=conn.execute("Select * from info where username=?",(username,)).fetchone()
    print(user)
    conn.close()
    return render_template(
        'form.html',
        user=user,
        error=None
    )


@app.route("/allusers")
def list_all_users():
    conn=get_db()
    users=conn.execute("Select * from info").fetchall()
    conn.close()
    return render_template(
        "listusers.html",
        users=users
    )








if __name__ == "__main__":
    app.run(debug=True)