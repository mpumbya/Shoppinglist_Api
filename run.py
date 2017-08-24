import os

from app import create_app
from flask import request, jsonify, abort
from app import models


config_name = os.getenv('APP_SETTINGS','development')
app = create_app(config_name)

#This is the Resister route
@app.route('/auth/register', methods=['POST'])
def users():
    if request.method == "POST":
        data = request.json
        if 'username' in data and 'email' in data and 'password' in data:
            usr = models.User.query.filter_by(email=data['email'])
            #
            if usr is None:
                usr = models.User(data['username'], data['email'], data['password'])
                usr.save()
                return jsonify({"status":"pass", "username": usr.username, "message": "user created"}), 200
            return jsonify({"status":"fail","message": "user already exists"}), 200
        return jsonify({"status":"fail", "message":"missing paramaters"})
    abort(400)

#This is the Login route
@app.route('/auth/login', methods=['POST'])
def login():
    if request.method == "POST":
        data = request.json
        if 'email' in data and 'password' in data:
            usr = models.User.query.filter_by(email=data['email']).first()
            #
            if usr is not None :
                if usr.password == data['password']:
                    return jsonify({"status":"pass", "username": usr.username, "message": "user logged in successfully"}), 200
            return jsonify({"status":"fail","message": "user does not exist"}), 200
        return jsonify({"status":"fail", "message":"Wrong paramaters"})
    abort(400)

    #This is the reset_password route
@app.route('/auth/reset', methods=['POST'])
def reset():
    if request.method == "POST":
        data = request.json
        if 'email' in data and 'new_password' in data and 'old_password' in data:
            usr = models.User.query.filter_by(email=data['email']).first()
            #
            if usr is not None :
                if usr.password == data['old_password']:
                    usr.password = data['new_password']
                    usr.save()
                    return jsonify({"status":"pass", "username": usr.username, "message": "Password changed successfully"}), 200
            return jsonify({"status":"fail","message": "Password not matching"}), 200
        return jsonify({"status":"fail", "message":"Wrong paramaters"})
    abort(400)

# This is the create List route
@app.route('/lists/create', methods=['POST'])
def createList():
    if request.method == "POST":
        data = request.json
        if 'name' in data and 'description' in data:
            lst = models.List.query.filter_by(name=data['name']).first()
            #
            if lst is None:
                #if lst.name == data['old_name']:
                #    lst.name == data['new_name']
                lst = models.List(data['name'], data['description'])
                lst.save()
                return jsonify({"status":"pass", "name": lst.name, "message": "Shopping List Created"}), 200
            return jsonify({"status":"fail","message": "Shopping List already exists"}), 200
        return jsonify({"status":"fail", "message":"missing paramaters"})
    abort(400)

# This is the edit list route
@app.route('/lists/', methods=['GET'])
def allists():
    if request.method == "GET":
        lst = models.List.query.all()
        results=[]

        for l in lst:
            obj = {
                'id':l.list_Id,
                'name':l.name,
                'description':l.description
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response



@app.route('/lists/modify/<int:id>', methods=['GET','PUT','DELETE'])
def modifyList(id, **kwargs):
    lst = models.List.query.filter_by(list_Id=id).first()
    if not lst:
        abort(404)

    if request.method == 'DELETE':
        lst.delete()
        return jsonify({"status":"pass","message":"list {} deleted successfully".format(lst.list_Id)}), 200

    elif request.method == 'PUT':
        name = str(request.data.get('name',''))
        description = str(request.data.get('description',''))
        lst.name = name
        lst.description = description
        lst.save()
        response = jsonify({
            'id':lst.list_Id,
            'name':lst.name,
            'description':lst.description
        })
        response.status_code = 200
        return response
    
    else:
        response = jsonify({
            'id':lst.list_Id,
            'name':lst.name,
            'description':lst.description
        })
        response.status_code = 200
        return response

# This is the create list route


if __name__ =='__main__':
    app.run(port = 5001)