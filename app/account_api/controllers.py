








@communities.route('<int:community_id>/issue/create', methods=['POST'])
def create_issue():
    title = request.form.get('title', None)
    info = request.form.get('info', None)

    issue = Issue(title, info)
    db.session.add(issue)
    db.session.commit()
    response = {'status':200}
    return jsonify(**response)

@communities.route('<int:community_id>/issue/update/<int:issue_id>', methods=['PUT'])
def update(issue_id):
    json_dict = request.get_json()
    issue_id = Issue.query.get(issue_id)
    issue.plan = json_dict['plan']
    action_plan.pros = json_dict['pros']
    action_plan.cons = json_dict['cons']
    db.session.commit()
    response = {'status':200}
    return jsonify(**response)  

@communities.route('<int:community_id>/issue/delete/<int:issue_id>', methods=['POST'])
def delete(action_plan_id):
    action_plan = ActionPlan.query.get(action_plan_id)
    db.session.delete(action_plan)
    db.session.commit()
    response = {'status':200}
    return jsonify(**response)

@communities.route('<int:community_id>/issue/<int:issue_id>', methods=['GET'])
def get(action_plan_id):
    action_plan = ActionPlan.query.get(action_plan_id)
    return jsonify(**action_plan.serialize())

@communities.route('<int:community_id>/issue/create', methods=['POST'])
def create():
    plan = request.form.get('plan', None)
    pros = request.form.get('pros', None)
    cons = request.form.get('cons', None)
    info = request.form.get('info', None)
    action_plan = ActionPlan(plan, pros, cons, info)
    db.session.add(action_plan)
    db.session.commit()
    response = {'status':200}
    return jsonify(**response)

@communities.route('<int:community_id>/issue/update/<int:issue_id>', methods=['PUT'])
def update(action_plan_id):
    json_dict = request.get_json()
    action_plan = ActionPlan.query.get(action_plan_id)
    action_plan.plan = json_dict['plan']
    action_plan.pros = json_dict['pros']
    action_plan.cons = json_dict['cons']
    db.session.commit()
    response = {'status':200}
    return jsonify(**response)  

@communities.route('<int:community_id>/issue/delete/<int:issue_id>', methods=['POST'])
def delete(action_plan_id):
    action_plan = ActionPlan.query.get(action_plan_id)
    db.session.delete(action_plan)
    db.session.commit()
    response = {'status':200}
    return jsonify(**response)

@communities.route('<int:community_id>/issue/<int:issue_id>', methods=['GET'])
def get(action_plan_id):
    action_plan = ActionPlan.query.get(action_plan_id)
    return jsonify(**action_plan.serialize())

@communities.route('/actionPlans', methods=['GET'])
def list():
    action_plans = ActionPlan.query.all()
    return json.dumps([action_plan.serialize() for action_plan in action_plans])
