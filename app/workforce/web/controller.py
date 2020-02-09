import os

from flask import request, redirect, url_for, render_template, Blueprint
from itsdangerous import SignatureExpired, BadTimeSignature
from http import HTTPStatus
from flask_login import login_required,current_user

from .forms import AddTaskForm
from models import Task, Attachments, User
from app.database import db
import datetime
from flask import current_app
from werkzeug.utils import secure_filename
from sqlalchemy import desc

html_blueprint = Blueprint('html_blueprint', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='web/static'
    )

@html_blueprint.route('/', methods=['GET'])
def index():
    return render_template('login.html')
    
@html_blueprint.route('/dashboard', methods=['GET'])
@login_required
def home():
    user = current_user
    if user:
        return render_template('home.html',user=user)
    else:
        return '', HTTPStatus.BAD_REQUEST

@html_blueprint.route('/debug-sentry')
def trigger_error():
    try:
        division_by_zero = 1 / 0
    except:
        print("Error")


@html_blueprint.route('/addtask', methods = ['GET', 'POST'])
@login_required
def add_task():
    # old picture
    UPLOAD_FOLDER = 'uploads'
    addtask = Task()
    # form data - old picture
    # form = AddTaskForm(obj=addtask)
    form = AddTaskForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            #  update picture data
            addtask.title = form.title.data
            addtask.description = form.description.data
            addtask.expected_end_date = form.expected_end_date.data
            addtask.priority = form.priority.data
            addtask.assignee = form.assignee.data
            addtask.team = form.team.data
            addtask.start_date =  datetime.datetime.now()
            addtask.reporter_id = current_user.id
            print("44444444")
            if 'file' in request.files:
                # breakpoint()
                file = request.files['file']
                if file:
                    file_filenames = []
                    for eachfile in list(request.files.listvalues())[0]:
                        files_filenames = secure_filename(eachfile.filename)
                        file.save(os.path.join(UPLOAD_FOLDER, files_filenames))
                        print('File successfully uploaded')
                        attachmentsObj = Attachments()
                        attachmentsObj.name = files_filenames
                        attachmentsObj.path = os.path.join(UPLOAD_FOLDER, files_filenames)
                        addtask.attachments.append(attachmentsObj)
                else:
                    print('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
                # return redirect(request.url)
            else:
                print("No attachments uploaded by user")
            db.session.add(addtask)
            db.session.commit()

            return '', HTTPStatus.OK

        return render_template('addtask.html', form=form, edit=True)
    else:
        return render_template('addtask.html', form=form, edit=True)


@html_blueprint.route('/statusUpdate/<int:taskId>', methods=['PUT','PATCH'])
def update_status(taskId):
    statusInfo = request.args['status']
    updatetask = Task.query.get(taskId)
    updatetask.task_status = statusInfo
    db.session.commit()
    return '', HTTPStatus.OK

@html_blueprint.route('/myPerformance/<int:userID>', methods=['GET'])
def get_performance(userID):
    tasks = Task.query.filter(Task.task_status=="DONE",Task.assignee_id==userID).all()
    print(type(tasks))
    total_cnt = len(tasks)
    print("--------------------------- "+str(total_cnt))
    cnt=0
    percentage = 0
    if total_cnt > 0:
        for eachtask in tasks:
            print(eachtask.actual_end_date)
            print(eachtask.title)
            if eachtask.actual_end_date != None:
                print("-----inside-----")
                if eachtask.expected_end_date <= eachtask.actual_end_date:
                    cnt = cnt+1
        percentage = (cnt*100)/total_cnt
    print(percentage,total_cnt,cnt)
    return ({'percentage':percentage,"total_cnt":total_cnt,"cnt":cnt},)




