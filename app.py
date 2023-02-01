from flask import Flask ,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db=SQLAlchemy(app)


class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(600),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self) ->str :  # This Method In Class Tells The Interpreter To What to Print When A User Try To Print The current Class Object
        return f"{self.sno}  {self.title}"

@app.route('/',methods=['POST','GET'])


def home_page():

    # if request.method=='POST':
    #     print(request.form["desc"])
    #     todo=Todo(title=request.form["title"],desc=request.form["desc"])
    #     # print(request.form["x"])
    #     # todo=Todo(title='request.form["TITLE"]',desc='request.form["DESC"]')
    #     db.session.add(todo)
    #     db.session.commit()
    # all_todo=Todo.query.all()
    # return render_template('index.html',Todo_Data=all_todo)
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        if title =="" or desc=="":
            pass
        else:
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
            
    allTodo = Todo.query.all() 
    return render_template('index.html', Todo_Data=allTodo)
  

@app.route('/Delete/<int:sno>')
def delete_record(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
  
@app.route('/Edit/<int:sno>',methods=['POST','GET'])
def update_record(sno):
    todo = Todo.query.get_or_404(sno)
    if request.method=='POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect("/")
    else:    
        return render_template('update.html', Todo=todo)

  
@app.route('/about/')
def SHOW_ABOUT_PAGE():
    return render_template("/about.html");
  
  
if __name__=='__main__':
    app.run(debug=True)