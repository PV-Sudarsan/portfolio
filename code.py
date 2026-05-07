from flask import Flask, request
app = Flask(__name__)
@app.route("/")
def login():
    return """
    <h2>Login Page</h2>
    <form action="/set-hidden" method="post">
        Username: <input type="text" name="userName"><br><br>
        Password: <input type="password" name="password"><br><br>
        <input type="submit" value="Login">
    </form>
    """
@app.route("/set-hidden", methods=["POST"])
def set_hidden():
    userName = request.form.get("userName", "").strip()
    password = request.form.get("password", "").strip()

    if userName == "" or password == "":
        return "Please enter both username and password.<br><br>" + login()

    if userName == "sho" and password == "1234":
        return f"""
        <h3>Logged in successfully.</h3>
        <p>Click the button below to see Username and Password values.</p>

        <form action="/get-hidden" method="post">
            <input type="hidden" name="userName" value="{userName}">
            <input type="hidden" name="password" value="{password}">
            <input type="submit" value="See Values">
        </form>
        """
    return "Wrong username or password.<br><br>" + login()
@app.route("/get-hidden", methods=["POST"])
def get_hidden():
    userName = request.form.get("userName", "")
    password = request.form.get("password", "")
    return f"""
    <h3>Hidden Field Values</h3>
    Username: {userName}<br><br>
    Password: {password}
    """
if __name__ == "__main__":
    allow_host = "*"
    app.run(debug=True, host="0.0.0.0") 

















from flask import Flask, session, render_template_string

app = Flask(__name__)

# Secret key is required for session handling
app.secret_key = "my_secret_key"


@app.route("/SessionTracker")
def session_tracker():
    # Get current visit count from session
    count = session.get("tracker.count", 0)

    # Increment count
    count += 1

    # Save updated count in session
    session["tracker.count"] = count

    html = """
    <html>
    <head>
        <title>SessionTracker</title>
    </head>
    <body>
        <h1>Session Tracking Demo</h1>

        You've visited this page {{ count }}
        {% if count == 1 %}
            time.
        {% else %}
            times.
        {% endif %}

        <p></p>

        <h2>Here is your session data:</h2>

        {% for key, value in session_data.items() %}
            {{ key }}: {{ value }} <br>
        {% endfor %}
    </body>
    </html>
    """

    return render_template_string(
        html,
        count=count,
        session_data=session
    )


if __name__ == "__main__":
    app.run(debug=True)
