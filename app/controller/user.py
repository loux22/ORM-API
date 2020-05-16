from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, User, Post, Comment, Message, Follow
import requests


main = Blueprint('main', __name__, url_prefix='/')

@main.route('/zeaafae')
def index():
    return render_template('pages/index.html')


@main.route('/test')
def test():
    # test insertion ligne
    user = User("louis", 4, "aaa@ynov.com", "aaaa")
    db.session.add(user)

    receive = User(username="louisss", age=7,
                   mail="aa@ynov.com", password="aa")
    db.session.add(receive)
    db.session.commit()

    u = user.query.filter_by(id=1).first()
    r = user.query.filter_by(id=2).first()

    post = Post("louis", "aaa@ynov.com", "aaaa",
                '2019-01-16 00:00:00', '2019-01-16 00:00:00', u)
    db.session.add(post)

    user.like.append(post)

    comment = Comment(content="blabla", publication_date='2019-01-16 00:00:00')
    comment.post = post
    user.comment.append(comment)

    message = Message('aaa', '2019-01-16 00:00:00', u, r)
    db.session.add(message)

    follow = Follow(user, receive)
    db.session.add(follow)

    db.session.commit()
    return "test"


@main.route('/user')
def user():
    return "controller user"


@main.route('/createdb')
def createdb():
    db.drop_all()
    db.create_all()
    return "la db a été créer"

@main.route('/login')
def login():
    return render_template('pages/login.html')

@main.route('/signup')
def signup():    
    return render_template('pages/signup.html')

@main.route('/signup', methods = ['POST'])
def signup_post():
    username = request.form.get('username')
    age = request.form.get('age')
    email = request.form.get('email')
    password = request.form.get('password')
    passwordRepeat = request.form.get('repassword')

    user = User.query.filter_by(email=email).first

    if user:
        flash('L\'adresse email utilisée est déjà utilisée')
        return redirect(url_for('user.signup'))
    
    newUser = User(username=username, age=age, mail=email, password=password)

    db.session.add(newUser)
    db.session.commit()

    return redirect(url_for('user.login'))


@main.route('/profil/<int:id>', methods=['GET', 'POST'], strict_slashes=False)
@main.route('/profil/',  methods=['GET', 'POST'], strict_slashes=False)
def profil(id=None):
    URL_ROOT = request.url_root
    error = None

    if(id == None):
        # user connecter
        url = URL_ROOT + 'api/post/user/' + str(1)
        user = User.query.filter_by(id=1).first()
        if request.method == 'POST':
            username = request.form['username']
            age = request.form['age']
            if username == "":
                error = "vous n'avez pas mis votre username"
            elif age == "":
                error = "vous n'avez pas mis votre age"   
            else:
                user.username = username
                user.age = age
                db.session.commit()
    # 1 est la personne connecter
    elif id == 1:            
        return redirect(url_for('main.profil', id=None))
    else:
        url = URL_ROOT + 'api/post/user/' + str(id)
        user = User.query.filter_by(id=id).first()
        # follower_id=1 etant la personne connecter
           
    followers = Follow.query.filter_by(follower_id=user.id).count()
    following = Follow.query.filter_by(followby_id=user.id).count()
    numberPosts = Post.query.filter_by(user_id=user.id).count()
    stats = {"followers": followers, "following": following, "posts": numberPosts}

    follow = Follow.query.filter_by(follower_id=1, followby_id=id).first()
    if not(follow):
        follow = 1

    if request.method == 'POST':
        if follow == 1:
            # 1 personne connecter
            userLog = User.query.filter_by(id=1).first()
            following = Follow(userLog, user)
            db.session.add(following)
        else:
            db.session.delete(follow)

        db.session.commit()
        return redirect(url_for('main.profil', id=id))

    response = requests.get(url)
    user = response.json()

    return render_template('pages/user/profil.html', stats=stats, error=error, id=id, user=user, follow=follow)