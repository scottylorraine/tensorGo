from flask import Flask, request, jsonify, Markup, redirect, url_for  # Import necessary modules from Flask
from pymongo import MongoClient  # Import MongoClient to interact with MongoDB
from datetime import datetime  # Import datetime to get the current time
import os  # Import os to access environment variables
import json

# Initialize the Flask application
app = Flask(__name__)

# Set up the MongoDB client
client = MongoClient(os.environ.get("MONGODB_URI", "mongodb://localhost:27017/"))

# Connect to the database named 'flask_db'
db = client.flask_db

# Connect to the collection named 'data' within the 'flask_db' database
collection = db.data

# Define the route for the root URL
@app.route('/')
def index():
    current_time = datetime.now().strftime("%B %d, %Y, %I:%M %p")
    html_string = Markup(f"""
    <html>
        <head>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Inria+Sans:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&family=Mukta:wght@200;300;400;500;600;700;800&display=swap" rel="stylesheet">
        </head>
        <body 
            style="
                font-family: 'Inria Sans', sans-serif;
                background-color: rgb(243, 159, 7);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;

            "
        >
            <h1 style="color: white; font-size: 45px">TensorGo Assignment</h1>
            <p style="color: white; text-align: center; font-size: 40px">
                Welcome to the Flask App using MongoDB!!!<br />
                Developed and Deployed by Sanivada Ananth<br />
                The current time is: {current_time}
            </p>
            <div
            style="
                display: flex;
                flex-direction: row;
                justify-content: center;
                gap:40px">
                <button 
                    id="submitButton"
                    style="
                        font-family: 'Inria Sans', sans-serif;
                        border: 1px solid #333;
                        border-radius: 10px;
                        margin-top: 10px;
                        padding: 5px 10px;
                        font-size: 20px;
                        cursor: pointer;
                    "
                    onmouseover="this.style.backgroundColor = '#CCCCCC'"
                    onmouseout="this.style.backgroundColor = '#FFFFFF'"
                    onclick="window.location.href = '/submit';"
                >
                    Post Data
                </button>
                <button 
                    id="dataButton"
                    style="
                        font-family: 'Inria Sans', sans-serif;
                        border: 1px solid #333;
                        border-radius: 10px;
                        margin-top: 10px;
                        padding: 5px 10px;
                        font-size: 20px;
                        cursor: pointer;
                    "
                    onmouseover="this.style.backgroundColor = '#CCCCCC'"
                    onmouseout="this.style.backgroundColor = '#FFFFFF'"
                    onclick="window.location.href = '/data';"
                >
                    Stored Data
                </button>

            </div>
        </body>
    </html>
    """)
    return html_string

# Define the route for the '/submit' endpoint
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # Get the name from the form data
        name = request.form.get('name')
        # Create a dictionary with the name
        data = {"Name": name}
        # Insert the data into the 'data' collection in MongoDB
        collection.insert_one(data)
        # Redirect to the '/data' route
        return redirect(url_for('data'))
    
    # Display the form if the request method is GET
    html_string = Markup("""
    <html>
        <head>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Inria+Sans:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&family=Mukta:wght@200;300;400;500;600;700;800&display=swap" rel="stylesheet">
        </head>
        <body 
            style="
                font-family: 'Inria Sans', sans-serif;
                background-color: rgb(243, 159, 7);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            "
        >
            <h2 style="color: white; text-align: center;font-size: 35px">Enter Name</h2>
            <form action="/submit" method="post" style="display: flex; flex-direction: row; align-items: center; justify-content: center; ">
                <input 
                    type="text" 
                    name="name" 
                    placeholder="Enter your name" 
                    style="padding: 5px; font-size: 16px; border-radius: 5px; border: 1px solid #333;"
                    required
                />
                <button 
                    type="submit"
                    style="
                        font-family: 'Inria Sans', sans-serif;
                        border: 1px solid #333;
                        border-radius: 10px;
                        padding: 5px 10px;
                        font-size: 20px;
                        cursor: pointer;
                        margin-left: 10px;
                    "
                    onmouseover="this.style.backgroundColor = '#CCCCCC'"
                    onmouseout="this.style.backgroundColor = '#FFFFFF'"
                >
                    Submit
                </button>
            </form>
            <button 
                id="homeButton"
                style="
                    font-family: 'Inria Sans', sans-serif;
                    border: 1px solid #333;
                    border-radius: 10px;
                    margin-top: 10px;
                    padding: 5px 10px;
                    font-size: 20px;
                    cursor: pointer;
                "
                onmouseover="this.style.backgroundColor = '#CCCCCC'"
                onmouseout="this.style.backgroundColor = '#FFFFFF'"
                onclick="window.location.href = '/';"
            >
                Home
            </button>
        </body>
    </html>
    """)
    return html_string

# Define the route for the '/data' endpoint
@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        data = request.get_json()
        collection.insert_one(data)
        return jsonify({"status": "Data inserted"}), 201
    elif request.method == 'GET':
        data = list(collection.find({}, {"_id": 0}))
        pretty_data = json.dumps(data, indent=4)
        
        html_string = Markup(f"""
    <html>
        <head>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Inria+Sans:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&family=Mukta:wght@200;300;400;500;600;700;800&display=swap" rel="stylesheet">
        </head>
        <body
        style="
                font-family: 'Inria Sans', sans-serif;
                background-color: rgb(243, 159, 7);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            "
        >
            <h2 style="text-align: center; color:white;font-size: 30px">Stored Data</h2>
            <pre style="background-color: rgb(243, 159, 7); padding: 10px; border-radius: 5px; color: #ffffff; font-size: 15px; font-family: 'Inria Sans', sans-serif;">
{pretty_data}
            </pre>
            <button 
                id="homeButton"
                style="
                    font-family: 'Inria Sans', sans-serif;
                    border: 1px solid #333;
                    border-radius: 10px;
                    margin-top: 10px;
                    padding: 5px 10px;
                    font-size: 20px;
                    cursor: pointer;
                "
                onmouseover="this.style.backgroundColor = '#CCCCCC'"
                onmouseout="this.style.backgroundColor = '#FFFFFF'"
                onclick="window.location.href = '/';"
            >
                Home
            </button>
        </body>
    </html>
    """)
        return html_string

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
