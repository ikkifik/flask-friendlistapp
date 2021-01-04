from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'

# Initialize the database
db = SQLAlchemy(app)

# Create db model
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # create a function to return a string when we added
    def __repr__(self):
        return '<name %r>' % self.id


subscribers = []

@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    friend_to_delete = Friends.query.get_or_404(id)

    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect('/friends')
    except:
        return "There was an error deleting your friend.."

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    title = 'Update My Friend List'
    friend_to_update = Friends.query.get_or_404(id)
    
    if request.method == 'POST':
        friend_to_update.name = request.form['name']

        # push to database
        try:
            db.session.commit()
            return redirect('/friends')
        except: 
            return "there was error!"

    else:
        return render_template('update.html', title=title, friend_to_update=friend_to_update )


@app.route('/friends', methods=['POST', 'GET'])
def friends():
    title = 'My Friend List'

    if request.method == 'POST':
        friend_name = request.form['name']
        new_friend = Friends(name=friend_name)

        # push to database
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except: 
            return "there was error!"

    else:        
        friends = Friends.query.order_by(Friends.date_created)
        return render_template('friends.html', title=title, friends=friends )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    names = ['John', 'Mia', 'Wes', 'Sally']
    return render_template('about.html', names=names)

@app.route('/subscribe')
def subscribe():
    title = 'Subscribe to get my newsletter!'
    return render_template('subscribe.html', title=title)

@app.route('/form', methods=['POST'])
def form():
    title = 'Thank You for Subscribing!'
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')

    if not first_name or not last_name or not email:
        error_statement = "Oops.. all form is required"
        return render_template('subscribe.html', 
            error_statement=error_statement,
            first_name=first_name,
            last_name=last_name,
            email=email)

    subscribers.append(f"{first_name} {last_name} || {email}")
    
    return render_template('form.html', title=title, subscribers=subscribers)