import sys
import time
import requests
import datetime
from project import db
from datetime import timedelta
from project.users.models import Users, Counter
from project.users.request_acceptor import InstagramBot
from flask_login import login_required, login_user, logout_user, current_user
from flask import Blueprint, render_template, redirect, url_for, request, session, make_response, jsonify
import pdb
import math
# from project import LOGGER_DEBUG

sys.path.append('../../')

from project.users.memcache_ctrl import client

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/request_accepted_counter', methods=['GET', 'POST'])
def request_accepted_counter():
    ctr, counterval=None, None
    total_request = 0
    failed_request = 0
    is_complete = False
    try:
        instagram_username = session['insta_username']
        total_request = client.get("total_request_to_accept" + instagram_username)
        failed_request = client.get("total_failed_requests" + instagram_username)

        failed_request = 0 if failed_request is None else failed_request
        total_request = 0 if total_request is None else total_request

        ctr=client.get(session["insta_username"])
        print("ctr",session["insta_username"], ctr)
        if ctr is not None:
            if total_request == ctr + failed_request:
                is_complete=True
            print("ctr -> ", ctr)
        elif Counter:
            counterval = Counter.query.filter_by(insta_username=session['insta_username']).first()
    except Exception as error:
        print("Not able to get count ", error)
        time.sleep(1)

    if ctr == None and counterval is not None:
        ctr = counterval.counts

    if ctr == None:
        ctr = 0
    return make_response(jsonify({'successful': ctr, "failed":failed_request, "isComplete": is_complete, "total":total_request}), 200)


@login_required
@users_blueprint.route('/accept_pending_requests', methods=['GET', 'POST'])
def accept_pending_requests(context=None):
    instagram_username = session.get("insta_username", None)
    print("instagram_username",  session)
    #if instagram_username is None:
    #    return redirect(url_for("users.login"))
    #is_subscription_check, url_redirect=check_subscription(instagram_username)
    #if not is_subscription_check:
    #    return redirect(url_redirect)

    if request.method == 'POST':
        resp = 'Success'
        MAX_RESULT_SIZE = 1000
        custom_number = request.form['customUserInputNumber']

        client.set("total_request_to_accept"+instagram_username, custom_number)

        # skip = int(request.form.get("skip", 990))
        # print("skip", skip, custom_number)
        skip = 0
        try:
            custom_number = int(custom_number)
        except:
            custom_number = int(custom_number[:-1])

        insta_obj = InstagramBot(session['insta_username'], session['insta_password'])

        insta_obj.login(False)

        remaining_records_to_process = custom_number
        record_processed = 0

        for x in range(0, custom_number, MAX_RESULT_SIZE):
            new_list_of_records=insta_obj.get_pending_request_details()
            print("Got total Items ", len(new_list_of_records))

            if x == 0 and len(new_list_of_records)==0:
                resp = "No request to accept"

            if remaining_records_to_process >= MAX_RESULT_SIZE:
                insta_obj.start_accepting_request(new_list_of_records[skip:MAX_RESULT_SIZE])
                remaining_records_to_process -= MAX_RESULT_SIZE
                record_processed += MAX_RESULT_SIZE
            else:
                sub_list = new_list_of_records[:remaining_records_to_process]
                insta_obj.start_accepting_request(sub_list)
                record_processed += len(sub_list)
                print("total Hits done ", record_processed)
                record_processed_local = client.get(session['insta_username'])
                resp = "Request accepted Count {}".format(record_processed_local)
                print(resp)
                # return resp, 200

        # pdb.set_trace()
        insta_obj.closeBrowser()
        return resp, 200
        # counts = insta_obj.pending_request_count()
        # instagram_accept_request_count = custom_number
        # try:
        #     if counts <= instagram_accept_request_count:
        #         insta_obj.accept_pending_requests(counts)
        #     else:
        #         insta_obj.accept_pending_requests(instagram_accept_request_count)
        # except:
        #     resp = "No request to accept"
        # return resp, 200

    try:
        user = Users.query.filter_by( insta_username=session['insta_username']).first()
        till_date = user.till_date
        last_day = (till_date - datetime.datetime.utcnow()).days

    except BaseException:
        last_day = None

    countval = Counter.query.filter_by(insta_username=instagram_username).first()

    if countval is None:
        newcounts = Counter(insta_username=instagram_username)
        db.session.add(newcounts)
        db.session.commit()
        countval = Counter.query.filter_by(insta_username=session['insta_username']).first()

    countval.counts = 0
    db.session.commit()

    return render_template('AcceptRequests.html', instagram_username=instagram_username, last_day=last_day)


@users_blueprint.route('/request_accepted_count/<int:num>', methods=['GET', 'POST'])
def request_accepted_count(num):
    counter = Counter.query.filter_by(insta_username=session['insta_username']).first()
    ctr = None
    if counter is not None:
       ctr = counter.counts

    return render_template('request_accepted_count.html', num=ctr)


@users_blueprint.route('/live_counter', methods=['GET', 'POST'])
def live_counter():

    if request.method == 'POST':
        try:

            instagram_username = request.form['instagram_username']
            session['live_counter'] = instagram_username
            response = requests.get(
                'https://www.instagram.com/web/search/topsearch/?query={un}'.format(un=instagram_username))
            resp = response.json()
            count = 0
            for i in resp['users']:
                if i['user']['username'] == instagram_username.lower():
                    count = i['user']['follower_count']
            name = '@' + instagram_username[0].capitalize() + instagram_username[1:]
            return render_template('count_display.html',
                                   name=name, user_count=count)
        except BaseException:
            return render_template('LiveCounter.html')
    return render_template('LiveCounter.html')


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        instagram_username = request.form['userEmailID']
        instagram_password = request.form['userLoginPassword']

        session['insta_username'] = instagram_username
        session['insta_password'] = instagram_password
        session['request_accepted_counter_demo'] = 0
        insta_bot = InstagramBot(instagram_username, instagram_password)
        insta_login_response = insta_bot.login()
        insta_bot.closeBrowser()

        if insta_login_response == False:
            msg = 'Invalid Credentials'
            return render_template('index.html', msg=msg)

        if insta_login_response:
            user_obj = Users.query.filter_by(
                insta_username=instagram_username).first()
            if not user_obj:
                new_user = Users(insta_username=instagram_username)
                db.session.add(new_user)
                db.session.commit()

        user = Users.query.filter_by(insta_username=instagram_username).first()
        if insta_login_response and user is not None:
            is_subscription_check, url_redirect = check_subscription(instagram_username)
            if is_subscription_check is True:
                return redirect(url_redirect)
            # print()
            # user.till_date = datetime.datetime.utcnow() + timedelta(days=1)
            # if user.is_subscribed:
            #     if datetime.datetime.utcnow() < user.till_date:
            #
            #         next = request.args.get('next')
            #         print("subscribed", "is_authenticated",current_user.is_authenticated(), "next", next)
            #
            #         if next is None or not next[0] == '/':
            #             next = url_for('users.accept_pending_requests')
            #         return redirect(next)
            #
            # elif user.is_subscribed == False:
            #     try:
            #         if datetime.datetime.utcnow() > user.till_date:
            #             user.till_date = None
            #             user.from_date = None
            #             user.is_subscribed = False
            #             db.session.commit()
            #     except BaseException as err:
            #         print("ERROR-> ", err)
            #         pass
            #     finally:
            #         next = request.args.get('next')
            #         if next is None or not next[0] == '/':
            #             next = url_for('core.pricing')
            #         return redirect(next)

        print("Counter init", client.set(instagram_username, 0))
        print("Fail Counter init", client.set("total_failed_requests"+instagram_username, 0))
    return render_template('index.html')


# @login_required
@users_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    # print(session)
    logout_user()
    return redirect(url_for('core.index'))


def check_subscription(user_name):
    user=Users.query.filter_by(insta_username=user_name).first()
    ok=login_user(user)
    if user is not None:
        user.till_date=datetime.datetime.utcnow() + timedelta(days=1)
        if user.is_subscribed:
            print(url_for('users.accept_pending_requests'))
            return user.is_subscribed, url_for('users.accept_pending_requests')
            # if datetime.datetime.utcnow() < user.till_date:
            #     next=request.args.get('next')
            #     print("subscribed", "is_authenticated", current_user.is_authenticated(), "next", next)
            #     if next is None or not next[0] == '/':
            #         next=url_for('users.accept_pending_requests')
            #     return redirect(next)

        elif user.is_subscribed == False:
            try:
                if datetime.datetime.utcnow() > user.till_date:
                    user.till_date=None
                    user.from_date=None
                    user.is_subscribed=False
                    db.session.commit()
            except BaseException as err:
                print("ERROR-> ", err)
                pass
            finally:
                # next=request.args.get('next')
                # if next is None or not next[0] == '/':
                #     next=url_for
                return user.is_subscribed, url_for('core.pricing')
    else:
        return False, url_for('core.index')
