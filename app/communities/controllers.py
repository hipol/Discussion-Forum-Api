from flask import Blueprint, abort, request, render_template, \
                  flash, g, session, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from app import db
from app.user_auth.models import User
from werkzeug import check_password_hash
from app.communities.models import Community, Issue, ActionPlan, ActionPlanVoteUserJoin, Comment
from flask import Flask, jsonify
from flask.ext.httpauth import HTTPBasicAuth

######

communities = Blueprint('communbp', __name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(email_or_token)
    if not user:
        # try to authenticate with email/password
        user = User.query.filter_by(email = email_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

# Set the route and accepted methods
@communities.route('/', methods=['GET'])
def home():
    #communitieslist = Community.query.all()
    #return jsonify({"communities" : [community.serialize() for community in communitieslist]})
    return "hello"

@communities.route('/community', methods=['GET'])
def get_communities():
    communitieslist = Community.query.all()
    return jsonify({"community" : [community.serialize() for community in communitieslist]})

#
@communities.route('/<int:community_id>/issue', methods=['GET'])
def get_issue_for_community(community_id):
    issuelist = Issue.query.filter_by(community_id=community_id)
    return jsonify({"issue" : [issue.serialize() for issue in issuelist]})

@communities.route('/issue', methods=['GET'])
@auth.login_required
def get_all_issues():
    issuelist = Issue.query.all()
    return jsonify({"issue" : [issue.serialize() for issue in issuelist]})

@communities.route('/<int:community_id>/issue/create', methods=['POST'])
def create_issue(community_id):
    if not request.json or 'title' not in request.json:
        abort(400)
    title = request.json['title']
    info = request.json.get('info', "")
    author_id = g.user.id

    issue = Issue(title, info, community_id, author_id)
    db.session.add(issue)
    db.session.commit()
    response = {'status':200}
    return jsonify(**response)

#@communities.route('<int:community_id>/issue/update/<int:issue_id>', methods=['PUT, GET'])
#def update(community_id, issue_id):
#    json_dict = request.get_json()
#    issue_id = Issue.query.filter_by(community_id=community_id).filter_by(id=issue_id)
#    issue.plan = json_dict['plan']
#    action_plan.pros = json_dict['pros']
#    action_plan.cons = json_dict['cons']
#    db.session.commit()
#    response = {'status':200}
#    return jsonify(**response)  


@communities.route('/<int:community_id>/issue/delete/<int:issue_id>', methods=['POST'])
def delete_issue(issue_id):
    issue = Issue.query.filter_by(id=issue_id)
    db.session.delete(issue)
    db.session.commit()
    response = {'status':200}
    return jsonify(**response)

@communities.route('/issue/<int:issue_id>', methods=['GET'])
def get_specific_issues(issue_id):
    issuelist = Issue.query.filter_by(id=issue_id)
    return jsonify({"issue" : [issue.serialize() for issue in issuelist]})

@communities.route('/issue/<int:issue_id>/plan/create', methods=['POST'])
@cross_origin()
#@auth.login_required
def create_action_plan(issue_id):
    plan = request.json.get('plan')
    article = request.json.get('article')
 #   author_id = g.user.id
    author_id = 1

    if plan is None or article is None:
        abort(400) # missing arguments

    action_plan = ActionPlan(plan, article, author_id, issue_id)
    db.session.add(action_plan)
    db.session.commit()
    response = {'status':200}
    return jsonify(**response)

# @communities.route('<int:community_id>/issue/update/<int:issue_id>', methods=['PUT'])
 #def update(action_plan_id):
#    json_dict = request.get_json()
 #   action_plan = ActionPlan.query.get(action_plan_id)
 #   action_plan.plan = json_dict['plan']
  #  action_plan.pros = json_dict['pros']
   #db.session.commit()
  #  response = {'status':200}
  #  return jsonify(**response)  

@communities.route('/actionplan/delete/<int:action_plan_id>', methods=['POST'])
def delete_action_plan(action_plan_id):
    action_plan = ActionPlan.query.filter_by(id=action_plan_id)
    db.session.delete(action_plan)
    db.session.commit()
    response = {'status':200}
    return jsonify(**response)

@communities.route('/actionplan/<int:action_plan_id>', methods=['GET'])
def get_specific_action_plan(action_plan_id):
    action_plan = ActionPlan.query.filter_by(id=action_plan_id)
    return jsonify({"action_plans" : [plan.serialize() for plan in action_plan]})

@communities.route('/actionplan', methods=['GET'])
def get_all_action_plans():
    action_plans = ActionPlan.query.all()
    return jsonify({"action_plans" : [action_plan.serialize() for action_plan in action_plans]})

@communities.route('/<int:action_plan_id>/vote', methods=['POST'])
def vote_action_plan(action_plan_id):
    voter_id = request.json.get('userid')

    vote = ActionPlanVoteUserJoin(action_plan_id, voter_id)
    db.session.add(vote)
    db.session.commit()
    response = {'status':200}
    return jsonify(**response)

@communities.route('/<int:action_plan_id>/delete_vote', methods=['POST'])
def delete_vote(action_plan_id):
    voter_id = request.json.get('userid')

    vote = ActionPlanVoteUserJoin.query.filter_by(action_plan_id = action_plan_id, voter_id = voter_id)
    db.session.delete(vote)
    db.session.commit()
    response = {'status':200}
    return jsonify(**response)

@communities.route('/vote', methods=['GET'])
def get_all_votes():
    votes = ActionPlanVoteUserJoin.query.all()
    return jsonify({"votes" : [vote.serialize() for vote in votes]})


@communities.route('/<int:action_plan_id>/comment/create', methods=['POST'])
#@auth.login_required
def create_comment(action_plan_id):
    text = request.json.get('comment')
    author_id = request.json.get('userid')

    commenttt = Comment(text, action_plan_id, author_id)
    db.session.add(commenttt)
    db.session.commit()
    response = {'status':200}
    return jsonify(**response)

@communities.route('/actionplan/<int:action_plan_id>/comments', methods=['GET'])
def get_comments(action_plan_id):
    comment = Comment.query.filter_by(action_plan_id=action_plan_id)
    return jsonify({"comments" : [comment_ind.serialize() for comment_ind in comment]})
