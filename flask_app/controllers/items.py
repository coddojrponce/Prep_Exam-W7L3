from flask_app import app     
from flask import render_template,redirect,request,session
from flask_app.models.item import Item

@app.route("/items")
def dash():
    if 'user_id' not in session:
        return redirect("/")
    items=Item.get_all()
    return render_template("dash.html",items=Item.get_all())

@app.route("/items/new")
def create_item():
    if 'user_id' not in session:
        return redirect("/")
    return render_template("create.html")

@app.route("/items/<int:id>/edit")
def edit_item(id):
    if 'user_id' not in session:
        return redirect("/")
    item=Item.get_one(id)
    return render_template("edit.html",item=item)

@app.route("/items/<int:id>/view")
def view_one_item(id):
    if 'user_id' not in session:
        return redirect("/")
    item=Item.get_one(id)
    return render_template("view_one.html",item=item)

# Create

@app.route("/items/create",methods=['POST'])
def create():
    if 'user_id' not in session:
        return redirect("/")
    print(request.form)
    if not Item.validate_item(request.form):
        print(request.form)
        return redirect("/items/new")
    data ={
        "user_id":session['user_id'],
        "name":request.form["name"],
        "description":request.form["description"],
        "price":request.form["price"],
        "img_url":request.form["img_url"]
    }
    Item.save(data)
    return redirect("/items")

@app.route("/items/<int:id>/like")
def like(id):
    if 'user_id' not in session:
        return redirect("/")
    Item.like(id,session['user_id'])
    return redirect("/items")

# Read 

# Update
@app.route("/items/update",methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect("/")
    data ={
        "user_id":session['user_id'],
        "name":request.form["name"],
        "description":request.form["description"],
        "price":request.form["price"],
        "img_url":request.form["img_url"],
        'id':request.form["id"]
    }
    Item.update(data)
    return redirect("/items")

# Delete

@app.route('/items/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect("/")
    Item.delete(id,session['user_id'])
    return redirect('/items')