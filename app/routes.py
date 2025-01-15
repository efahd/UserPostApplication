from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Post, Comment
from app.forms import RegistrationForm, LoginForm, PostForm, CommentForm

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    # Dsiplay all posts
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('base.html', posts = posts)

@main.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You can now log in!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form = form)

@main.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form = form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/dashboard')
@login_required
def dashboard():
    # Get posts of the current user
    user_posts = Post.query.filter_by(user_id = current_user.id).all()
    return render_template('dashboard.html', posts = user_posts)

@main.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content = form.content.data, user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Post created!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('post.html', form = form, title='New Post')

@main.route('/post/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id = post.id).all()
    form = CommentForm()
    return render_template('post.html', post = post, comments = comments, form = form)

@main.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def comment_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content = form.content.data, post_id = post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added!', 'success')
    return redirect(url_for('main.show_post', post_id = post_id))

@main.route('/post/<int:post_id>/edit', methods=['GET','POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('You do not have permission to edit this post', 'danger')
        return redirect(url_for('main.home'))
    form = PostForm()
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('post.html', form = form, title = 'Edit Post')

@main.route('/post/<int:post_id>/delete', methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404
    if post.author != current_user:
        flash('You do not have permission to delete this post.', 'danger')
        return redirect(url_for('main.home'))
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!', 'success')
    return redirect(url_for('main.dashboard'))