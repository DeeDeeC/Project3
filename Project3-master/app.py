from flask import Flask, render_template, request, url_for
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, DateField
import main_functions

credentials = main_functions.read_from_file("credentials.json")
password = credentials["password"]

connection_string = "mongodb+srv://Jordy:{0}@project3.rqprq.mongodb.net/Project3?retryWrites=true&w=majority".format(password)

app = Flask(__name__)
app.config["SECRET_KEY"] = "COP4813"
app.config["MONGO_URI"] = connection_string
mongo = PyMongo(app)


class Expenses(FlaskForm):
    description = StringField('Description')
    category = SelectField('Category', choices=[('日本語', '日本語'),
                                                ('ストロングゼロ', 'ストロングゼロ'),
                                                ('ライトノベル', 'ライトノベル'),
                                                ('𠮷野家', '𠮷野家'),
                                                ('大学', '大学'),
                                                ('コンピューター', 'コンピューター'),
                                                ('フライト', 'フライト'),
                                                ('電話', '電話'),
                                                ('動機', '動機'),
                                                ('生活', '生活')])

    cost = DecimalField('Cost')
    date = DateField('Date')
    # TO BE COMPLETED (please delete the word pass above)


def get_total_expenses(category):
    expense_category = 0
    query = {"category": category}
    records = mongo.db.expenses.find(query)

    for x in records:
        expense_category += float(x["cost"])
    return expense_category
    # TO BE COMPLETED (please delete the word pass above)


@app.route('/')
def index():
    my_expenses = mongo.db.expenses.find()
    categories = mongo.db.expenses.find({}, {"category": 1})
    total_cost = 0

    for i in my_expenses:
        total_cost += float(i["cost"])

    expensesByCategory = {}  # [("example" , get_total_expenses("example"))]
    for j in categories:
        expensesByCategory[j["category"]] = get_total_expenses(j["category"])
    # expensesByCategory is a list of tuples
    # each tuple has two elements:
    ## a string containing the category label, for example, insurance
    ## the total cost of this category
    return render_template("index.html", expenses=total_cost, expensesByCategory=expensesByCategory)


@app.route('/addExpenses', methods=["GET", "POST"])
def addExpenses():
    # INCLUDE THE FORM
    expensesForm = Expenses(request.form)

    if request.method == "POST":
        description = request.form['description']
        category = request.form['category']
        cost = request.form['cost']
        date = request.form['date']
        record = {'description': description, 'category': category, 'cost': float(cost), 'date': date}
        mongo.db.expenses.insert_one(record)
        # INSERT ONE DOCUMENT TO THE DATABASE
        # CONTAINING THE DATA LOGGED BY THE USER
        # REMEMBER THAT IT SHOULD BE A PYTHON DICTIONARY
        return render_template("expenseAdded.html")
    return render_template("addExpenses.html", form=expensesForm)


app.run()
