from flask import Flask, render_template, request, redirect, url_for,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
# from datetime import timedelta
from bson import ObjectId

#Created flask instance
app = Flask(__name__)

#Creats the Database and initialized.
client = MongoClient('localhost', 27017)
db = client['estimationdb1'] 
users_collection = db['data']
estim_collection=db['estiminfo']

#created welcome route
@app.route('/index',methods=['GET'])
#@jwt_required()
def show():
    return render_template('index.html')

#created user registration route
@app.route('/userregister', methods=['GET', 'POST'])
def user_register():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        if users_collection.find_one({'username':username}):
            return "user already existed.Try register  with new user "
        else:
            hash_pwd=generate_password_hash(password)
            users_collection.insert_one({'username':username,'password':hash_pwd})
            #return "user succssfully created"
            return redirect(url_for('login'))
    return render_template('register.html')   

#created login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username})
        if not user:
            return jsonify('user not found')
        if  user and check_password_hash(user['password'],password):
            return redirect(url_for('estimation'))
        else:
            return jsonify('Invalid user')
    return render_template('login.html')

#Creats the estimation fieds
@app.route('/estimation',methods=['GET','POST'])
def estimation():
    if request.method=='POST':
        task_title=request.form['taskName']
        complexity=request.form['complexity']
        size=request.form['size']
        type_of_task=request.form['taskType']
        #stored to database 
        estimation_task={'task_title':task_title,'complexity':complexity,'size':size,'type_of_task':type_of_task}
        estim_collection.insert_one(estimation_task)
        #Estimation calculation
        def estim_Calculation(type_of_task):
            estim_data_task= list(estim_collection.find({"type_of_task":type_of_task  },{"_id":0}))
            estim_data_len = len(estim_data_task)
            data=0
            size_val={'small':3,'medium':6,'large':10}
            for item in estim_data_task:
                for key,value in item.items():
                    if key=='size':
                        data=data+size_val[value]
            estimated_value = int(data/estim_data_len)
            return estimated_value
        estimated_value = estim_Calculation(type_of_task)
        estimated_range=f"{estimated_value-2}  - {estimated_value+2}"
        #Confidence level
        def confidence_level(hours):
            if hours < 4:
                return "Low"
            elif hours <= 7:
                return "Medium"
            else:
                return "High"
        confidence_level = confidence_level(estimated_value)
        estim_data = {"Estimated_effort" : estimated_value,"Confidence_level" : confidence_level,
            "Estemated_range" : estimated_range}
        # print(estim_data)
        return render_template('estimationresult.html', estim_data=estim_data)       
    return render_template('estimationform.html')

#Show list of estimations
@app.route('/estimation_data', methods=['GET'])
def show_estimations():
    estimationdata = estim_collection.find()
    return render_template('estimationlist.html', estimationdata=estimationdata)

#update the estimation from
@app.route('/update_form/<string:id>', methods=['GET', 'POST'])
def update_form(id):
    task= estim_collection.find_one({'_id':ObjectId(id)})
    #print(task)
    if request.method == 'POST':
        title = request.form.get('task_title')
        complexity = request.form.get('complexity')
        size = request.form.get('size')
        task_type = request.form.get('type_of_task')
        data_dict= {}
        data={'task_title': title,'complexity': complexity,'size': size,'type_of_task': task_type}
        for key, value in data.items():
            if value is not None:
                data_dict[key] = value
        query = {"_id": ObjectId(id)}
        content = {"$set": data_dict}
        update_data = estim_collection.find_one_and_update(query, content, upsert=False)
        if update_data:
            return redirect('/estimation_data')
        else:
            return jsonify("data not found")
    return render_template('estimationupdate.html',task=task)


# #delete the estimation field
@app.route('/delete/<id>', methods=['GET'])
def delete_estimation(id):
    estim_collection.delete_one({'_id': ObjectId(id)})
    return redirect('/estimation_data')

#logout route
@app.route('/logout')
def logout():
    return redirect(url_for('login'))
#run the application
if __name__ == '__main__':
    app.run(debug=True,port=5011)

