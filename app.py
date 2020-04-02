from myproject import app,db,mail
from flask_mail import Message
from  flask import render_template, redirect, url_for, flash, abort,request
from flask_login import login_user, login_required, logout_user,UserMixin,current_user
from myproject.models import User 
from myproject.forms import LoginForm, RegistrationForm,RequestResetForm,ResetPasswordForm
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/',methods= ['GET','POST'])
def index():
    return render_template('index.html')


@app.route('/register',methods=['POST','GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username = form.username.data,
                    email =form.email.data,
                    password = form.password.data)

        db.session.add(user)
        db.session.commit()
        flash("Thank you for registration !!")
        return redirect(url_for('login'))
    return render_template("signup.html",form= form)



@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
        next = request.args.get('next')

        if next == None or not next[0]== '/':
            next = url_for('blog')
    return render_template('login.html',  form=form )


    
@app.route('/blog',methods=['GET','POST'])

def blog():
    return render_template('blog.html')

@app.route('/logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("Thank you for visiting my website",'info')
    return redirect(url_for('logged_out'))


@app.route('/logged_out', methods=['GET','POST'])
def logged_out():
    return render_template('<h1> You logged out successfully!!!</h1>')

    
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',sender='lewismutembei001@gmail.com',recipients=['teshlewie668@gmail.com'])
    msg.body =f''' To reset your password,visit the following link:
{url_for('reset_token', token =token,_external =True)}

If you did not make this request then simply ignore this email and no changes will be made 
'''
    mail.send(msg)


@app.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if  form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset  your password ','info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title ="Reset Password", form = form)

@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That token is invalid or expires','warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        user.password_hash= password_hash
        db.session.commit()
        flash("Your password has been updated! You can now login")
        return redirect(url_for('login'))
 


    return render_template('reset_token.html', title = "Reset Password",form=form)


if __name__ == "__main__":
    app.run(debug =True)

