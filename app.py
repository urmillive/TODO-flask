from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno}{self.title}"


@app.route("/",methods=["GET", "POST"])
def index():
    if request.method =='POST':
        title_ = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title_,desc=desc)
        db.session.add(todo)
        db.session.commit()        
    allTODO = Todo.query.all()
    return render_template("index.html",allTODO=allTODO)

@app.route('/update/<int:sno>',methods=["GET", "POST"])
def update(sno):
    if request.method =='POST':
        title_upd = request.form['title']
        desc_upd = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title_upd
        todo.desc = desc_upd
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
    


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
    

if __name__ == "__main__":
    app.run(debug=False, port=8000)
