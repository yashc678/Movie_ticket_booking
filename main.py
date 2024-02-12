from flask import Flask,request,render_template,redirect
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/movie"
mg = PyMongo(app)

@app.route('/')
def login_page():
    return render_template('user_log.html')

@app.route('/verify',methods=['POST','GET'])
def verify():
    username=request.form.get('username')
    password=request.form.get('password')
    data=list(mg.db.user.find({}))
    m='invalid'
    print(data)
    for i in data:
        if i['username']==username and i['password']==password:
            m='valid'
            break
    if m=='valid':
        return render_template('home.html')
    else:
        return render_template('invalid.html')
@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup_logic',methods=["POST","GET"])
def logic():
    username = request.form.get('username')
    password = request.form.get('password')
    firstname=request.form.get('firstname')
    lastname=request.form.get('lastname')
    mg.db.user.insert_one({"username": username, 'password': password,'firstname':firstname,'lastname':lastname})
    return render_template('user_log.html')



@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/movie_form')
def movie_form():
    return render_template('booking.html')
@app.route('/booking_info',methods=["POST","GET"])
def booking_info():
    name=request.form.get('name')
    name=name.lower()
    time=request.form.get('time')
    qty=int(request.form.get('qty'))

    message='not_book'
    data = list(mg.db.movie_a.find({'name': name,'time':time}))
    n_data=len(data)
    if n_data>0:
        for i in data:
            if i['qty']<qty:
                break
            if i['time']==time and i['name']==name:
                mg.db.movie_a.update_one({'name':name},{'$set':{'qty':i['qty']-qty}})
                message='result'

    return redirect(message)

@app.route('/result')
def show():
    return render_template('pass.html')

@app.route('/not_book')
def not_book():
    return render_template('fail.html')


@app.route('/search',methods=["POST","GET"])
def search():
    display_data=[]
    movieName=request.form.get('movieName')
    movieName=movieName.lower()
    if movieName!='':
        data = list(mg.db.movie_a.find({'name': movieName}))
    else:
        data = list(mg.db.movie_a.find())

    for i in data:
        display_data.append({'name': i['name'], 'time': i['time'], 'qty': i['qty']})

    return render_template('display.html', data=display_data)



@app.route('/display')
def display():
    display_data=[]
    data=list(mg.db.movie_a.find())
    for i in data:
        if i['qty']<=0:
            mg.db.movie_a.delete_one({'qty':i['qty']})
    data = list(mg.db.movie_a.find())
    for i in data:
        display_data.append({'name':i['name'],'time':i['time'],'qty':i['qty']})

    return render_template('display.html',data=display_data)

if __name__=='__main__':
    app.run(debug=True,port=5000)