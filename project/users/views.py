import sys
sys.path.append('../../')
from project import db

import datetime
import requests
from project.users.models import Users
from project.users.request_acceptor import InstagramBot
from flask_login import login_required, login_user, logout_user,current_user
from flask import Blueprint, render_template, redirect, url_for, request, session


users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/request_accepted_count', methods=['GET', 'POST'])
def request_accepted_count():
    print(str(session['request_accepted_counter']) + 'in request accepted count')
    return str(session['request_accepted_counter'])
    # return "5"


@login_required
@users_blueprint.route('/accept_pending_requests', methods=['GET', 'POST'])
def accept_pending_requests():
    # import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        try:
            no_of_request_to_accept = request.form['noOfFollowers']
            user = Users.query.filter_by(insta_username=session['insta_username']).first()
            user.accept_request_count = int(no_of_request_to_accept)
            db.session.commit()
        except:
            custom_number = request.form['customUserInputNumber']
            if int(custom_number) > 0:
                user = Users.query.filter_by(insta_username=session['insta_username']).first()
                user.accept_request_count = int(custom_number)
                db.session.commit()
            else:
                pass
        print("inside func")
        is_subscribed = user.is_subscribed
        if is_subscribed:
            user = Users.query.filter_by(insta_username=session['insta_username']).first()
            instagram_accept_request_count = user.accept_request_count
            if instagram_accept_request_count[:-1] == 'K':
                instagram_accept_request_count = instagram_accept_request_count[:-1]
                instagram_accept_request_count = int(instagram_accept_request_count) * 1000
            else:
                instagram_accept_request_count = int(instagram_accept_request_count)

            insta_obj = InstagramBot(session['insta_username'], session['insta_password'])
            insta_obj.login2()
            counts =insta_obj.pending_request_count()

            try:
                if counts <= instagram_accept_request_count:
                    insta_obj.accept_pending_requests(counts)
                else:
                    insta_obj.accept_pending_requests(instagram_accept_request_count)
            except:
                resp = "No request to accept"
            insta_obj.closeBrowser()
            resp = ''
            # return render_template('acceptor_display.html', instagram_username = session['insta_username'], resp=resp)
        else:
            return redirect(url_for('core.pricing'))
    try:
        user = Users.query.filter_by(insta_username=session['insta_username']).first()
        till_date = user.till_date
        last_day = (till_date - datetime.datetime.utcnow()).days
    except:
        last_day = None
    print(current_user.is_authenticated)
    return render_template('AcceptRequests.html', instagram_username = session['insta_username'], last_day=last_day)



@users_blueprint.route('/live_counter', methods=['GET','POST'])
def live_counter():

    if request.method == 'POST':
        try:

            instagram_username = request.form['instagram_username']
            session['live_counter'] = instagram_username
            response = requests.get('https://www.instagram.com/web/search/topsearch/?query={un}'.format(un=instagram_username))
            resp = response.json()
            for i in resp['users']:
                if i['user']['username'] == instagram_username.lower():
                    user_id = i['user']['pk']
                    count = i['user']['follower_count']
            name = '@'+instagram_username[0].capitalize() + instagram_username[1:]
            return render_template('count_display.html', name=name, user_count=count)
        except:
            return render_template('LiveCounter.html')
    return render_template('LiveCounter.html')

@login_required
@users_blueprint.route('/request_acceptor_api', methods=['GET','POST'])
def request_acceptor():
    # import ipdb; ipdb.set_trace()
    user = Users.query.filter_by(insta_username=session['insta_username']).first()
    instagram_accept_request_count = user.accept_request_count
    if instagram_accept_request_count[:-1] == 'K':
        instagram_accept_request_count = instagram_accept_request_count[:-1]
        instagram_accept_request_count = int(instagram_accept_request_count) * 1000

    insta_obj = InstagramBot(session['insta_username'], session['insta_password'])
    insta_obj.login2()
    counts = session['insta_pending_req_count']
    print(counts)
    if counts < instagram_accept_request_count:
        resp = insta_obj.accept_pending_requests(counts)
    else:
        resp = insta_obj.accept_pending_requests(instagram_accept_request_count)
    insta_obj.closeBrowser()

    return render_template('result.html', resp=resp)




@users_blueprint.route('/login', methods=['GET','POST'])
def login():

    # import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        instagram_username = request.form['userEmailID']
        instagram_password = request.form['userLoginPassword']

        session['insta_username'] = instagram_username
        session['insta_password'] = instagram_password
        session['request_accepted_counter'] = 0
        insta_bot = InstagramBot(instagram_username, instagram_password)
        insta_login_response = insta_bot.login()
        insta_bot.closeBrowser()

        if insta_login_response == False:
            msg = 'Invalid Credentails'
            return render_template('index.html', msg=msg)

        if insta_login_response:
            user_obj = Users.query.filter_by(insta_username=instagram_username).first()
            if not user_obj:
                new_user = Users(insta_username=instagram_username)
                db.session.add(new_user)
                db.session.commit()

        user = Users.query.filter_by(insta_username=instagram_username).first()
        if insta_login_response and user is not None:

            if user.is_subscribed:
                if datetime.datetime.utcnow() < user.till_date:
                    ok = login_user(user)
                    print(ok)
                    print("subscribed")
                    print(current_user.is_authenticated())
                    next = request.args.get('next')

                    if next == None or not next[0] == '/':
                        next = url_for('users.accept_pending_requests')
                    return redirect(next)

            if user.is_subscribed == False:
                try:
                    if datetime.datetime.utcnow() > user.till_date:
                        user.till_date = None
                        user.from_date = None
                        user.is_subscribed = False
                        db.session.commit()
                except:
                    ok = login_user(user)
                    print(ok)
                    print("Not subscribed")
                    next = request.args.get('next')
                    if next == None or not next[0] == '/':
                        next = url_for('core.pricing')
                    return redirect(next)

    return render_template('index.html')



@login_required
@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@users_blueprint.route('/test')
def test():
    return render_template('result.html', last_day=2)

@users_blueprint.route('/api_testing')
def api_testing():
    return render_template('acceptor_display.html')