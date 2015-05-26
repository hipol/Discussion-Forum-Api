from flask import Blueprint, abort, request, render_template, \
                  flash, g, session, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from app import db
from app.user_auth.models import User
from werkzeug import check_password_hash
from app.communities.models import Community, Issue, ActionPlan, ActionPlanVoteUserJoin, Comment, Event, CommentVoteUserJoin
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
def get_all_issues():
    issuelist = Issue.query.all()
    return jsonify({"issue" : [issue.serialize() for issue in issuelist]})

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


@communities.route('/issue/delete/<int:issue_id>', methods=['POST'])
@auth.login_required
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
@auth.login_required
def create_action_plans(issue_id):
    plan = request.json.get('plan')
    article = request.json.get('article')
    author_id = request.json.get('userid')

    if plan is None or article is None:
        abort(400) # missing arguments

    action_plan = ActionPlan(plan, article, author_id, issue_id)
    db.session.add(action_plan)

    event = Event(2, author_id)
    event.action_plan_id = action_plan.id
    db.session.add(event)

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
@auth.login_required
def delete_action_plan(action_plan_id):
    action_plan = ActionPlan.query.filter_by(id=action_plan_id).first()
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
@auth.login_required
def vote_action_plan(action_plan_id):
    voter_id = request.json.get('userid')
    vote = ActionPlanVoteUserJoin(action_plan_id, voter_id)
    db.session.add(vote)
    ap = ActionPlan.query.filter_by(id = action_plan_id).first()
    ap.votes += 1

    event = Event(4, author_id)
    event.actionplanvoteuserjoins_id  = vote.id 
    db.session.add(event)

    db.session.commit()
    response = {'status':200}
    return jsonify(**response)

@communities.route('/<int:action_plan_id>/check_vote/<int:voter_id>', methods=['GET'])
@auth.login_required
def check_vote(action_plan_id, voter_id):
    vote = ActionPlanVoteUserJoin.query.filter_by(action_plan_id = action_plan_id, voter_id = voter_id).first()
    if not vote:
        return 'False'
    return 'True'

@communities.route('/<int:action_plan_id>/delete_vote_by/<int:voter_id>', methods=['POST'])
@auth.login_required
def delete_vote(action_plan_id, voter_id):
    vote = ActionPlanVoteUserJoin.query.filter_by(action_plan_id = action_plan_id, voter_id = voter_id).first()
    db.session.delete(vote)
    ap = ActionPlan.query.filter_by(id = action_plan_id).first()
    ap.votes -= 1
    db.session.commit()
    response = {'status':200}
    return jsonify(**response)

@communities.route('/vote', methods=['GET'])
def get_all_votes():
    votes = ActionPlanVoteUserJoin.query.all()
    return jsonify({"votes" : [vote.serialize() for vote in votes]})

@communities.route('/commentvote', methods=['GET'])
def get_all_commentvotes():
    votes = CommentVoteUserJoin.query.all()
    return jsonify({"votes" : [vote.serialize() for vote in votes]})

@communities.route('/<int:action_plan_id>/comment/create', methods=['POST'])
@auth.login_required
def create_comment(action_plan_id):
    text = request.json.get('comment')
    author_id = request.json.get('userid')

    comment = Comment(text, action_plan_id, author_id)
    db.session.add(comment)

    event = Event(3, author_id)
    event.comment_id = comment.id 
    db.session.add(event)

    db.session.commit()
    response = {'status':200}
    return jsonify(**response)

@communities.route('/comment/delete/<int:comment_id>', methods=['POST'])
@auth.login_required
def delete_comment(comment_id):
    com = Comment.query.filter_by(id=comment_id).first()
    db.session.delete(com)
    db.session.commit()
    response = {'status':200}
    return jsonify(**response)

@communities.route('/<int:action_plan_id>/<int:comment_id>/upvote', methods=['POST'])
@auth.login_required
def upvote_comment(action_plan_id, comment_id):
    voter_id = request.json.get('userid')
    vote = CommentVoteUserJoin(comment_id, voter_id, 1)
    db.session.add(vote)
    comment = Comment.query.filter_by(id = comment_id).first()
    comment.upvotes += 1

    event = Event(5, author_id)
    event.commentvoteuserjoins_id = vote.id 
    db.session.add(event)

    db.session.commit()
    response = {'status':200}
    return jsonify(**response)

@communities.route('/<int:action_plan_id>/<int:comment_id>/check_vote/<int:voter_id>', methods=['GET'])
@auth.login_required
def check_vote_comment(action_plan_id, comment_id, voter_id):
    vote = CommentVoteUserJoin.query.filter_by(comment_id = comment_id, voter_id = voter_id).first()
    if not vote:
        return '0'
    if vote.main_value == 1:
        return '1'
    if vote.main_value == -1:
        return '-1'
    return 'false'

@communities.route('/<int:action_plan_id>/<int:comment_id>/delete_upvote_by/<int:voter_id>', methods=['POST'])
@auth.login_required
def delete_upvote_comment(action_plan_id, comment_id, voter_id):
    vote = CommentVoteUserJoin.query.filter_by(comment_id = comment_id, voter_id = voter_id).first()
    db.session.delete(vote)
    comment = Comment.query.filter_by(id = comment_id).first()
    comment.upvotes -= 1
    db.session.commit()
    response = {'status':200}
    return jsonify(**response)

@communities.route('/<int:action_plan_id>/<int:comment_id>/downvote', methods=['POST'])
@auth.login_required
def downvote_comment(action_plan_id, comment_id):
    voter_id = request.json.get('userid')
    vote = CommentVoteUserJoin(comment_id, voter_id, -1)

    db.session.add(vote)
    comment = Comment.query.filter_by(id = comment_id).first()
    comment.downvotes += 1

    event = Event(5, author_id)
    event.commentvoteuserjoins_id = vote.id 
    db.session.add(event)

    db.session.commit()
    response = {'status':200}
    return jsonify(**response)

@communities.route('/<int:action_plan_id>/<int:comment_id>/delete_downvote_by/<int:voter_id>', methods=['POST'])
@auth.login_required
def delete_downvote_comment(action_plan_id, comment_id, voter_id):
    vote = CommentVoteUserJoin.query.filter_by(comment_id = comment_id, voter_id = voter_id).first()
    db.session.delete(vote)
    comment = Comment.query.filter_by(id = comment_id).first()
    comment.downvotes -= 1
    db.session.commit()
    response = {'status':200}
    return jsonify(**response)

@communities.route('/actionplan/<int:action_plan_id>/comments', methods=['GET'])
def get_comments(action_plan_id):
    comment = Comment.query.filter_by(action_plan_id=action_plan_id)
    return jsonify({"comments" : [comment_ind.serialize() for comment_ind in comment]})

@communities.route('/events', methods=['GET'])
def get_events():
    eventlist = Event.query.all()
    return jsonify({"issue" : [event.serialize() for event in reversed(eventlist)]})

@communities.route('/<int:community_id>/create/issue', methods=['POST'])
def create_issue():
    title = request.json.get('title')
    info = request.json.get('article')
    author_id = request.json.get('userid')
    picture = request.json.get('picture')

    if title is None or info is None or picture is None:
        abort(400) # missing arguments

    issue = Issue(title, info, author_id, picture)
    issue.community_id = community_id
    db.session.add(issue)

    event = Event(1, author_id)
    event.issue_id = issue.id
    db.session.add(event)

    db.session.commit()
    response = {'status':200}
    return jsonify(**response)
