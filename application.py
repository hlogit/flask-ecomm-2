from cs50 import SQL
from flask_session import Session
from flask import Flask, render_template, redirect, request, session, jsonify
import datetime
import collections
import urllib
import hashlib

# # Instantiate Flask object named app
app = Flask(__name__)

# # Configure sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Creates a connection to the database
db = SQL ( "sqlite:///data.db" )

@app.route("/")
def index():
    shirts = db.execute("SELECT * FROM shirts ORDER BY team ASC")
    shirtsLen = len(shirts)    # Initialize variables
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    if 'user' in session:
        shoppingCart = db.execute("SELECT team, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY team")
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        shirts = db.execute("SELECT * FROM shirts ORDER BY team ASC")
        shirtsLen = len(shirts)
        w_id = session['uid']
        users = db.execute(f"SELECT * FROM users  WHERE id='{w_id}' ")
        print(users)
        addr = users[0]["address"]
        print(addr)
        return render_template ("index.html", users=users[0], addr=addr, shoppingCart=shoppingCart, shirts=shirts, shopLen=shopLen, shirtsLen=shirtsLen, total=total, totItems=totItems, display=display, session=session )
    return render_template ( "index.html", shirts=shirts, shoppingCart=shoppingCart, shirtsLen=shirtsLen, shopLen=shopLen, total=total, totItems=totItems, display=display)



@app.route('/prod/', methods=['GET'])
def prod():
    pid = request.args.get('id').lower()
    print(pid)
    print(pid)
    sql = "SELECT * FROM shirts where id=%s" % (pid)
    shirts = db.execute(sql)
    shirtsLen = len(shirts)
    # Initialize variables  
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    if 'user' in session:
        shoppingCart = db.execute("SELECT team, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY team")
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        sql = "SELECT * FROM shirts where id=%s" % (pid)
        shirts = db.execute(sql)
        shirtsLen = len(shirts)
        print(shirts)  
        return render_template ("prod.html", shoppingCart=shoppingCart, shirts=shirts, shopLen=shopLen, shirtsLen=shirtsLen, total=total, totItems=totItems, display=display, session=session )
    return render_template ( "prod.html", shirts=shirts, shoppingCart=shoppingCart, shirtsLen=shirtsLen, shopLen=shopLen, total=total, totItems=totItems, display=display)



@app.route("/buy/")
def buy():
    # Initialize shopping cart variables
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    qty = int(request.args.get('quantity'))
    if session:
        # Store id of the selected shirt
        id = int(request.args.get('id'))
        # Select info of selected shirt from database
        goods = db.execute("SELECT * FROM shirts WHERE id = :id", id=id)
        # Extract values from selected shirt record
        # Check if shirt is on sale to determine price
        if(goods[0]["onSale"] == 1):
            price = goods[0]["onSalePrice"]
        else:
            price = goods[0]["price"]
        team = goods[0]["team"]
        image = goods[0]["image"]
        subTotal = qty * price
        # Insert selected shirt into shopping cart
        
        w_id = session['uid']
        ins_cart  =f"INSERT INTO cart (id, qty, team, image, price, subTotal, w_id) VALUES ('{id}', '{qty}', '{team}', '{image}', '{price}', '{subTotal}', '{w_id}')" 
        print(ins_cart)
        print(ins_cart)
        db.execute(ins_cart)

        # db.execute("INSERT INTO cart (id, qty, team, image, price, subTotal) VALUES (:id, :qty, :team, :image, :price, :subTotal)", id=id, qty=qty, team=team, image=image, price=price, subTotal=subTotal)
        shoppingCart = db.execute("SELECT team, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY team")
        shopLen = len(shoppingCart)
        # Rebuild shopping cart
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        # Select all shirts for home page view
        shirts = db.execute("SELECT * FROM shirts ORDER BY team ASC")
        shirtsLen = len(shirts)
        # Go back to home page
        return render_template ("index.html", shoppingCart=shoppingCart, shirts=shirts, shopLen=shopLen, shirtsLen=shirtsLen, total=total, totItems=totItems, display=display, session=session )


@app.route("/update_addr/", methods=['POST'])
def update_addr():
    # Initialize shopping cart variables  苗栗縣7
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    addr = (request.form.get('addr'))
    # addr = (request.args.get('addr'))
    print(addr)
    print(addr)
    print(request.form)
    if session:
        # Store id of the selected shirt
        w_id = session['uid']
        db.execute(f"update  users SET address='{addr}' WHERE id = '{w_id}'")
        '''
        id = int(request.args.get('id'))
        # Select info of selected shirt from database
        goods = db.execute("SELECT * FROM shirts WHERE id = :id", id=id)
        # Extract values from selected shirt record
        # Check if shirt is on sale to determine price
        if(goods[0]["onSale"] == 1):
            price = goods[0]["onSalePrice"]
        else:
            price = goods[0]["price"]
        team = goods[0]["team"]
        image = goods[0]["image"]
        subTotal = qty * price
        # Insert selected shirt into shopping cart
        db.execute("INSERT INTO cart (id, qty, team, image, price, subTotal) VALUES (:id, :qty, :team, :image, :price, :subTotal)", id=id, qty=qty, team=team, image=image, price=price, subTotal=subTotal)
        
        '''
        shoppingCart = db.execute("SELECT team, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY team")
        shopLen = len(shoppingCart)
        # Rebuild shopping cart
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        # Go back to cart page
        return render_template ("cart.html", addr=addr, shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session )


@app.route("/update/")
def update():
    # Initialize shopping cart variables
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    qty = int(request.args.get('quantity'))
    if session:
        # Store id of the selected shirt
        id = int(request.args.get('id'))
        db.execute("DELETE FROM cart WHERE id = :id", id=id)
        # Select info of selected shirt from database
        goods = db.execute("SELECT * FROM shirts WHERE id = :id", id=id)
        # Extract values from selected shirt record
        # Check if shirt is on sale to determine price
        if(goods[0]["onSale"] == 1):
            price = goods[0]["onSalePrice"]
        else:
            price = goods[0]["price"]
        team = goods[0]["team"]
        image = goods[0]["image"]
        subTotal = qty * price
        # Insert selected shirt into shopping cart
        db.execute("INSERT INTO cart (id, qty, team, image, price, subTotal) VALUES (:id, :qty, :team, :image, :price, :subTotal)", id=id, qty=qty, team=team, image=image, price=price, subTotal=subTotal)
        shoppingCart = db.execute("SELECT team, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY team")
        shopLen = len(shoppingCart)
        # Rebuild shopping cart
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        # Go back to cart page
        return render_template ("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session )


@app.route("/filter/")
def filter():
    if request.args.get('continent'):
        query = request.args.get('continent')
        shirts = db.execute("SELECT * FROM shirts WHERE continent = :query ORDER BY team ASC", query=query )
    if request.args.get('sale'):
        query = request.args.get('sale')
        shirts = db.execute("SELECT * FROM shirts WHERE onSale = :query ORDER BY team ASC", query=query)
    if request.args.get('id'):
        query = int(request.args.get('id'))
        shirts = db.execute("SELECT * FROM shirts WHERE id = :query ORDER BY team ASC", query=query)
    if request.args.get('kind'):
        query = request.args.get('kind')
        shirts = db.execute("SELECT * FROM shirts WHERE kind = :query ORDER BY team ASC", query=query)
    if request.args.get('price'):
        query = request.args.get('price')
        shirts = db.execute("SELECT * FROM shirts ORDER BY onSalePrice ASC")
    shirtsLen = len(shirts)
    # Initialize shopping cart variables
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    if 'user' in session:
        # Rebuild shopping cart
        shoppingCart = db.execute("SELECT team, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY team")
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        # Render filtered view
        return render_template ("index.html", shoppingCart=shoppingCart, shirts=shirts, shopLen=shopLen, shirtsLen=shirtsLen, total=total, totItems=totItems, display=display, session=session )
    # Render filtered view
    return render_template ( "index.html", shirts=shirts, shoppingCart=shoppingCart, shirtsLen=shirtsLen, shopLen=shopLen, total=total, totItems=totItems, display=display)


@app.route("/checkout_ori/")
def checkout_ori():
    order = db.execute("SELECT * from cart")
    # Update purchase history of current customer
    for item in order:
        ins_purchase =f"INSERT INTO purchases (uid, w_id, id, team, image, quantity) VALUES('{session['uid']}', '{session['uid']}', '{item['id']}', '{item['team']}', '{item['image']}', '{item['qty']}') " 
        # db.execute("INSERT INTO purchases (uid, id, team, image, quantity) VALUES(:uid, :id, :team, :image, :quantity)", uid=session["uid"], id=item["id"], team=item["team"], image=item["image"], quantity=item["qty"] )
        print(ins_purchase)
        print(ins_purchase)
        db.execute(ins_purchase)
    # Clear shopping cart
    w_id = session['uid']
    db.execute(f"DELETE from cart where w_id='{w_id}'")
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    # Redirect to home page
    return redirect('/')


@app.route("/remove/", methods=["GET"])
def remove():
    # Get the id of shirt selected to be removed
    out = int(request.args.get("id"))
    # Remove shirt from shopping cart
    w_id = session['uid']
    db.execute(f"DELETE from cart WHERE id=:id AND  w_id='{w_id}'", id=out)
    # Initialize shopping cart variables
    totItems, total, display = 0, 0, 0
    # Rebuild shopping cart
    shoppingCart = db.execute("SELECT team, image, SUM(qty), SUM(subTotal), price, id FROM cart GROUP BY team")
    shopLen = len(shoppingCart)
    for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
    # Turn on "remove success" flag
    display = 1
    # Render shopping cart
    return render_template ("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session )


@app.route("/login/", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/new/", methods=["GET"])
def new():
    # Render log in page
    return render_template("new.html")


@app.route("/logged/", methods=["POST"] )
def logged():
    # Get log in info from log in form
    user = request.form["username"].lower()
    pwd = request.form["password"]
    #pwd = str(sha1(request.form["password"].encode('utf-8')).hexdigest())
    # Make sure form input is not blank and re-render log in page if blank
    if user == "" or pwd == "":
        return render_template ( "login.html" )
    # Find out if info in form matches a record in user database
    query = "SELECT * FROM users WHERE username = :user AND password = :pwd"
    # print(query)
    rows = db.execute ( query, user=user, pwd=pwd )

    # If username and password match a record in database, set session variables
    if len(rows) == 1:
        session['user'] = user
        session['time'] = datetime.datetime.now( )
        session['uid'] = rows[0]["id"]
    # Redirect to Home Page
    if 'user' in session:
        return redirect ( "/" )
    # If username is not in the database return the log in page
    return render_template ( "login.html", msg="Wrong username or password." )


@app.route("/history/")
def history():
    # Initialize shopping cart variables
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    # Retrieve all shirts ever bought by current user
    myShirts = db.execute("SELECT * FROM purchases WHERE w_id=:uid", uid=session["uid"])
    myShirtsLen = len(myShirts)
    # Render table with shopping history of current user
    return render_template("history.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session, myShirts=myShirts, myShirtsLen=myShirtsLen)


@app.route("/logout/")
def logout():
    # clear shopping cart
    db.execute("DELETE from cart")
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/register/", methods=["POST"] )
def registration():
    # Get info from form
    username = request.form["username"]
    password = request.form["password"]
    confirm = request.form["confirm"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    # See if username already in the database
    rows = db.execute( "SELECT * FROM users WHERE username = :username ", username = username )
    # If username already exists, alert user
    if len( rows ) > 0:
        return render_template ( "new.html", msg="Username already exists!" )
    # If new user, upload his/her info into the users database
    new = db.execute ( "INSERT INTO users (username, password, fname, lname, email) VALUES (:username, :password, :fname, :lname, :email)",
                    username=username, password=password, fname=fname, lname=lname, email=email )
    # Render login template
    return render_template ( "login.html" )


@app.route("/cart/")
def cart():
    if 'user' in session:
        # Clear shopping cart variables
        totItems, total, display = 0, 0, 0
        # Grab info currently in database
        w_id = session['uid']
        shoppingCart = db.execute(f"SELECT team, image, SUM(qty), SUM(subTotal), price, id FROM cart  WHERE w_id='{w_id}' GROUP BY team")
        # Get variable values
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
            

    w_id = session['uid']          
    users = db.execute(f"SELECT * FROM users  WHERE id='{w_id}' ")
    print(users)
    addr = users[0]["address"]
    # Render shopping cart
    return render_template("cart.html", addr=addr, shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session)


#@app.route("/to_pay/", methods=['GET'] )
def to_pay(total=998):
    #total = request.args.get('total')
    TotalAmount = total
    print("---------------------------------------0")
    print(total)
    print(total)
    print("---------------------------------------0")
    #正式環境：https://payment.ecpay.com.tw/Cashier/QueryTradeInfo/V5
    #測試環境：https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5
    url_real = "https://payment.ecpay.com.tw/Cashier/QueryTradeInfo/V5"   # v5
    url = "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5"   # v5
    form_html0 =""
    form_html0="<form   target=\"_blank\" action=\"%s\" method=\"POST\">\n"%(url)
    this_server_ip= "220.229.9.32"
    this_server_port= "5000"
    PaymentInfoURL= "http://%s:%s/getData1"%(this_server_ip,this_server_port)
    ReturnURL= "http://%s:%s/getData1"%(this_server_ip,this_server_port)
    
    print( "==into_pay==")
    currentDT = datetime.datetime.now()
    dt=currentDT.strftime("%Y%m%d%H%M%S")
    MerchantTradeNo ="ecPay"+dt
    print(MerchantTradeNo)
    #sys.exhttps://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5  <base href="https://payment-stage.ecpay.com.tw/">
    #stt ='HashIV=5294y06JbISpM5x9&ChoosePayment=Credit&EncryptType=1&ItemName= nnntesst7&MerchantID=2000132&MerchantTradeDate=2021/10/20 01:03:18&MerchantTradeNo=ecPay1234&PaymentType=aio&ReturnURL=http://your.web.site/receive.php&TotalAmount=97&TradeDesc=nnnpay&HashIV=v77hoKGq4kWxNNIS'
    #stt = stt.encode('utf-8')
    #CheckMacValue = hashlib.sha256(stt).hexdigest()
    header = {"content-type": "application/x-www-form-urlencoded;charset=utf-8"}
    #'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
    FormData2 = {"ChoosePayment": 'Credit',
    "EncryptType": 1,
    "MerchantTradeDate": '2021/10/20 04:35:18',
    "PaymentType": 'aio',
    "ItemName": 'nnntesst6a#nnntesst2#nnntesst3',
    "MerchantTradeNo": MerchantTradeNo,
    "PaymentInfoURL":PaymentInfoURL,
    "ReturnURL": ReturnURL, 
    "TotalAmount": total,
    "TradeDesc": 'nnnpay', 
    "MerchantID": '2000132',
    "ecurl": url,
    }

    FormData = {"ChoosePayment": 'Credit',
    "EncryptType": 1,
    "MerchantTradeDate": '2021/10/20 04:35:18',
    "PaymentType": 'aio',
    "ItemName": 'nnntesst6a#nnntesst2#nnntesst3',
    "MerchantTradeNo": MerchantTradeNo,
    "PaymentInfoURL":PaymentInfoURL,
    "ReturnURL": ReturnURL, 
    "TotalAmount": total,
    "TradeDesc": 'nnnpay', 
    "MerchantID": '2000132',
    }
    #"CheckMacValue": CheckMacValue,
    # 字典转换k1=v1 & k2=v2 模式   content
    print( "====")
    od = collections.OrderedDict(sorted(FormData.items()))
    data = urllib.parse.urlencode(FormData)
    #print( "==od==")
    o_sorted_vars = ""
    for key in sorted(FormData):
        # #print( "==sorted od==")
        vars = "%s=%s&" %(key,FormData[key])
        # print ("%s=%s" %(key,FormData[key]))
        o_sorted_vars += vars
    #pprint.pprint( od)
    # print(FormData)

    new_vars = "HashKey=%s%sHashIV=%s" % ("5294y06JbISpM5x9&",o_sorted_vars, "v77hoKGq4kWxNNIS")
    vars_str_urlencode = urllib.parse.quote_plus(new_vars)
    vars_str_urlencode_lower = vars_str_urlencode.lower()
    CheckMacValue = (hashlib.sha256(vars_str_urlencode_lower.encode('utf-8')).hexdigest())

    FormData.update({'CheckMacValue': CheckMacValue.upper()})
    FormData2.update({'CheckMacValue': CheckMacValue.upper()})
    print("---------------------------------------1")
    for key in sorted(FormData):
        v = FormData[key]
        form_html0+="   <input type=\"hidden\" name=\"%s\" value=\"%s\">\n" %(key,v)
    form_html0+="   <input type=\"text\"  value=\"%s\"  readonly>\n" %(TotalAmount)
    form_html0+="   <input type=\"submit\" value=\"Submit\">\n</form>"
    #print(form_html0)
    print(FormData)
    print("---------------------------------------1")
        
    return (FormData2)

  

@app.route("/checkout/")
def checkout():

    if 'user' in session:
        # Clear shopping cart variables
        
        totItems, total, display = 0, 0, 0
        # Grab info currently in database
        w_id = session['uid']
        shoppingCart = db.execute(f"SELECT team, image, SUM(qty), SUM(subTotal), price, id FROM cart  WHERE w_id='{w_id}' GROUP BY team")
        # Get variable values
        shopLen = len(shoppingCart)
        users = db.execute(f"SELECT * FROM users  WHERE id='{w_id}' ")
        addr = users[0]["address"]
        for i in range(shopLen):
            total += round(shoppingCart[i]["SUM(subTotal)"])
            totItems += shoppingCart[i]["SUM(qty)"]
    # Render shopping cart
        ecp_FormData2 = to_pay(total)

        
        # ecp_hidden = unicode(ecp_hidden, "utf-8")
        print("a-------------------2")
        print(ecp_FormData2)
        print("a-------------------2")
        print(type(ecp_FormData2))
        print("a-------------------")
    return render_template("checkout.html", addr=addr, shoppingCart=shoppingCart, ecp_FormData=ecp_FormData2, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session)
  
@app.route("/getData1", methods=['POST', 'GET'])
def getInfo():
	print( "==getInfo==")
	print(request.__dict__)
	text_input = request.__dict__
	with open('data.txt', 'a') as data_file:
		data_file.write(text_input)
	#textInput = request.form["data"]
	#print(textInput)
	#return render_template("text.html",text=textInput)
	print( "==getInfo==")
	return jsonify({'message': 'Data saved sucessfully!'}), 200
	


# @app.errorhandler(404)
# def pageNotFound( e ):
#     if 'user' in session:
#         return render_template ( "404.html", session=session )
#     return render_template ( "404.html" ), 404


# Only needed if Flask run is not used to execute the server
#if __name__ == "__main__":
#    app.run( host='0.0.0.0', port=8080 )
