from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("inventory.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():

    conn = get_db()

    stock = conn.execute(
        "SELECT * FROM inventory"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        stock=stock
    )

@app.route("/issue", methods=["GET","POST"])
def issue():

    conn = get_db()

    if request.method == "POST":

        employee = request.form["employee"]
        item = request.form["item"]
        qty = int(request.form["qty"])

        stock = conn.execute(
            "SELECT quantity FROM inventory WHERE item=?",
            (item,)
        ).fetchone()

        if stock["quantity"] >= qty:

            new_stock = stock["quantity"] - qty

            conn.execute(
                "UPDATE inventory SET quantity=? WHERE item=?",
                (new_stock,item)
            )

            conn.execute(
                """
                INSERT INTO issues
                (employee,item,qty)
                VALUES
                (?,?,?)
                """,
                (employee,item,qty)
            )

            conn.commit()

        conn.close()

        return redirect("/")

    items = conn.execute(
        "SELECT item FROM inventory"
    ).fetchall()

    conn.close()

    return render_template(
        "issue.html",
        items=items
    )

if __name__ == "__main__":
    app.run(debug=True)
