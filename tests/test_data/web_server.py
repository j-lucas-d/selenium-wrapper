""" Web server which serves web pages for testing the selenium wrapper """

from flask import Flask, request

app = Flask(__name__)

button_page = """
<html>
<head>
<script language="JavaScript">
    function form_button() {
        document.getElementById("form_button_output").innerHTML = "Done";
    }
</script></head><body>
<input type="button" value="Form Button" id="button1" onClick="form_button()">
<span id="button1_output"></span>
</body></html>
"""

alert_page = """<html><body><script>alert("This is an alert")</script></body></html>"""

@app.route("/")
def main():
    return "Naught, but disappointment thou shalt find within this realm."


@app.route("/button")
def button():
    return button_page

@app.route("/alert")
def alert():
    return alert_page

@app.route("/params")
def params():
    text = request.args.get('value')
    return f'<html><body><div id="text">{text}</div></body></html>'

if __name__ == "__main__":
    """ For manually testing the webpages """
    app.run()
