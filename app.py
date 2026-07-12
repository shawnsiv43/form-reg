from flask import Flask,request,jsonify,render_template
import sqlite3
import webbrowser
conn=sqlite3.connect("C:\\Users\\hi_sh\\formregsave.db")
cursor=conn.cursor()

latest_sql_err=None

app=Flask(__name__)
@app.route("/regform")
def dis():
    return render_template("index.html")
@app.route("/api/reg")
def diss():
    global latest_sql_err
    conn=sqlite3.connect("C:\\Users\\hi_sh\\formregsave.db")
    cursor=conn.cursor()
    uName=request.args.get("uName")
    print("uname is",uName)
    eName=request.args.get("eName")
    print("eName is",eName)
    passName=request.args.get("passName")
    print("passName is",passName)
    cpassName=request.args.get("cpassName")
    print("cpassName is",cpassName)
    ageName=request.args.get("ageName")
    print("ageName is",ageName)
    try:
        information=(uName,eName,ageName,passName,cpassName)
        insert_query='''Insert into info(username,email,age,password,confirmpassword)
        Values(?,?,?,?,?)'''

        cursor.execute(insert_query,information)
        print('db saved')

        conn.commit()

        conn.close()
        latest_sql_err=None
        return jsonify({"regMsg":f"Your Registration has been {uName}, {eName}, {passName}, {cpassName}, {ageName}"})
    except sqlite3.IntegrityError as e:
        latest_sql_err=str(e)

        return jsonify({"regMsg":f"Registration failure. Integrity constraint on {uName}","error":latest_sql_err})
    finally:
        conn.close()
@app.route("/success")
def disss():
    global latest_sql_err
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
    
    print("success",isSuccess)
    return render_template(
        "success.html",
        isSuccess=isSuccess
    )
    







if __name__ == "__main__":
    app.run(debug=True)