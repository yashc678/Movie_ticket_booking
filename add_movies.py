from flask import Flask, request, url_for
from flask_pymongo import PyMongo
import urllib

app = Flask(__name__)
app.config['MONGO_URI'] ="mongodb://localhost:27017/movie"
mongo = PyMongo(app)

@app.route('/')
def index():
    return '''
        <form method="post" action="/create" enctype="multipart/form-data">
            <input type="text" name="username">
            <input type="file" name="profile_image">
            <input type="submit">
        </form>
    '''

@app.route('/create', methods=['POST'])
def create():
    if 'profile_image' in request.files:
        profile_image = request.files['profile_image']
        mongo.save_file(profile_image.filename, profile_image)
        mongo.db.imageusers.insert_one({'username' : request.form.get('username'), 'profile_image_filename' : profile_image.filename})
        return 'Done!'

@app.route('/file/<path:filename>')
def file(filename):
    return mongo.send_file(filename)

if __name__=='__main__':
    app.run(debug=True)