
from flask import Flask, render_template, redirect, url_for, request, session, flash,jsonify
import mysql.connector

app=Flask(__name__)
app.secret_key='any random string'
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='hemavarshini@2006',
        database='flight_ticket'
    )
@app.route('/home')
def home():
    return render_template('index.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_flight')
def search_flight():
    return render_template('login.html')

@app.route('/search', methods=['GET'])
def search():
    from_city=request.args.get('from_city')
    to_city=request.args.get('to_city')
    a=get_connection()
    cursor=a.cursor(dictionary=True)
    query="""
        SELECT * FROM flights 
        WHERE LOWER(from_city) = LOWER(%s) 
        AND LOWER(to_city) = LOWER(%s)
    """
    cursor.execute(query,(from_city,to_city))
    flights=cursor.fetchall()
    cursor.close()
    a.close()
    return render_template('result.html',flights=flights,from_city=from_city , to_city=to_city)




@app.route('/api/text_result', methods=['GET'])
def text_result():
    from_city = request.args.get('from_city')
    to_city = request.args.get('to_city')
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM flights WHERE LOWER(from_city) = LOWER(%s) AND LOWER(to_city) = LOWER(%s)"
    cursor.execute(query, (from_city, to_city))
    flights = cursor.fetchall()
    cursor.close()
    conn.close()

    result = ""
    for f in flights:
        result += f"✈️ {f['airline']}\n"
        result += f"From: {f['from_city']} → To: {f['to_city']}\n"
        result += f"Time: {f['time']}\n"
        result += f"Price: ₹{f['price']}\n\n"

    return result, 200, {'Content-Type': 'text/plain'}


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing_user = cur.fetchone()

        if existing_user:
            cur.close()
            conn.close()
            return "Username already exists. Please choose a different one."

     
        cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        conn.commit()
        cur.close()
        conn.close()

        session['username'] = username  
        return render_template('search.html') 


    return render_template('signup.html')  




@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session['username'] = username
            return render_template('search.html') 

        else:
            return "Invalid username or password"

    if 'username' in session:
        return "Logged in as " + session['username']

    return render_template('signin.html')  


        
   
if __name__=='__main__':
    app.run(debug=True)