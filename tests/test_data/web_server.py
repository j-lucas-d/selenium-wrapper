""" Web server which serves web pages for testing the selenium wrapper """

from flask import Flask, request

app = Flask(__name__)

generic = """
<html>
<head>
<script language="JavaScript">
    function execute() {
        document.getElementById("output").innerHTML = "Passed";
    }
</script></head><body>
<div id="output"></div>
"""

button_page = f"""
{generic}
<input type="button" value="Form Button" id="button1" onClick="execute()">
</body></html>
"""

text_entry = f"""
{generic}
<form method="GET" action="/output">
<input type="text" value="default value" id="text1">
<input type="submit">
</form>
</body></html>
"""

alert_page = """<html><body><script>alert("This is an alert")</script></body></html>"""

delayed_element = """
<html><head>
<script>
    setTimeout(execute, 5000);
    function execute() {
        divTag = document.createElement("div");
        divTag.id = "output"
        divTag.innerHTML = 'Div Tag Exists';
        document.body.appendChild(divTag);
    }
</script>
</head><body>
</body></html>
"""

delayed_element_removal = """
<html><head>
<script>
    window.onload = execute;
    setTimeout(removal, 5000);
    
    function removal() {
        var divs = document.getElementsByTagName('div');
        divs[0].parentNode.removeChild(divs[0]);
    }
    function execute() {
        divTag = document.createElement("div");
        divTag.id = "output"
        divTag.innerHTML = 'Div Tag Exists';
        document.body.appendChild(divTag);
        //return divTag;
    }
</script>
</head><body>
</body></html>
"""


@app.route("/")
def main():
    return "Naught, but disappointment thou shalt find within this realm."


@app.route("/delayed_element")
def delayed_elem():
    return delayed_element


@app.route("/remove_element")
def remove_elem():
    return delayed_element_removal


@app.route("/output")
def output():
    return "passed"


@app.route("/text_entry")
def textbox():
    return text_entry


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
