from flask import Flask, request, render_template, Response, make_response
from dotenv import load_dotenv
import os

load_dotenv()
admin_cookie = os.environ.get("ADMIN_COOKIE", "FAKE_COOKIE")
FLAG = os.environ.get("FLAG", "ehctf{yes_sir_chac_chan_la_fakeflag_roi}")

app = Flask(__name__)


@app.route("/")
def homepage() -> Response:
    """The homepage for the app"""
    cookie = request.cookies.get("cookie", "Guest Pleb")

    # If admin, give flag
    if cookie == admin_cookie:
        return render_template("flag.html", flag=FLAG, user="admin")

    # Otherwise, render normal page
    response = make_response(render_template("index.html", user=cookie))
    response.set_cookie("cookie", cookie)
    return response


if __name__ == "__main__":
    app.run(debug=True)
