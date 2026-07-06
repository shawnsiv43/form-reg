from flask import Flask,request,jsonify,render_template


app=Flask(__name__)
@app.route("/regform")
def dis():
    return render_template("index.html")

@app.route("/api/happy")
def diss():
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
    return jsonify({"regMsg":f"Your Registration has been {uName}, {eName}, {passName}, {cpassName}, {ageName}"})


if __name__ == "__main__":
    app.run(debug=True)