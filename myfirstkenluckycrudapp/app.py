from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder='Templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        order_content = request.form['content']
        new_order = Orders(content=order_content)
        try:
            db.session.add(new_order)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your order'
    else:
        all_orders = Orders.query.order_by(Orders.date_created).all()
        return render_template('index.html', orders = all_orders)

@app.route('/delete/<int:id>')
def delete(id):
    order_to_delete = Orders.query.get_or_404(id)
    try:
        db.session.delete(order_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    order = Orders.query.get_or_404(id)
    if request.method == 'POST':
        order.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue modifying the order'
    else:
        return render_template('update.html', order=order)


if __name__ == '__main__':
    app.run(debug=True)