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

drag_and_drop = """
<html><head>
<script src="jquery-1.7.2.min.js"></script>
<script src="jquery-ui.min.js"></script>
<script src="jquery.ui.touch-punch.min.js"></script> // Drag and drop

<script language="Javascript">
    // Used for timing button presses
    var time = 0;
    // Mark anything with the class "blocks" as a draggable object
    $(function() {$( ".blocks" ).draggable();});
    // Function shortcut
    function $E(id) { return document.getElementById(id); }
    // Bind to mouse up event for changing element attributes
    document.onmouseup = MouseUp;
    document.onmousedown = MouseDown;

    function MouseDown(e) {
        if (e == null) e = window.event; // MSIE
        var id = (e.target || e.srcElement).id; // Get the ID of the element that was clicked on
        if (id.indexOf("block") >= 0) {
            rect = $E(id).getBoundingClientRect();
            $E("position").innerHTML = rect.top;
            time = new Date().getTime() / 1000;
        }
    }
    function MouseUp(e) {
        if (e == null) e = window.event; // MSIE
        var id = (e.target || e.srcElement).id;
        if (id.indexOf("block") >= 0) {
        rect = $E(id).getBoundingClientRect();
            $E("position").innerHTML = rect.top;
            $E("separator").innerHTML = (new Date().getTime() / 1000) - time;
        }
    }
   
</script>
<style>
    .blocks {
        width: 25%;
        height: 25%;
        border-style: solid;
        border-width: 1px;
    }
</style></head><body>
<div id="block1" class="blocks">Block 1</div>
<div id="separator" class="blocks">0</div>
<div id="block2" class="blocks">Block 2</div>
<div id="position" class="blocks">0</div>
</body></html>
"""

hyperlink = """<html><body><a href="/">Go To Root</a></body></html>"""

keypress = """<html><head><script src="jquery-1.7.2.min.js"></script><script language="Javascript">
$(document).keypress(
    function(e) {
        var keycode = (e.keyCode ? e.keyCode : e.which);
        document.getElementById("char").innerHTML = String.fromCharCode(keycode); // Show character
        document.getElementById("code").innerHTML = keycode; // Show ASCII key code
    }
);
function mouse(id) {
    document.getElementById(id).innerHTML='executed';
    return false; // Prevent default behaviour
}

</script></head><body>
<div id="char">Press a Key</div><div id="code"></div>
<span id="right_click" onContextMenu="mouse(this.id)">Right click here</span></br>
<span id="double_click" onDblClick="mouse(this.id)">Double-click here</span></br> 
<span id="hover" onMouseOver="mouse(this.id)">Mouse over here</span></br>
</body></html>"""

long_page = """
<html><head><script language="Javascript">
window.onload = function() {
    // Create long list horizontally
    for (i=0; i < 500; i++) {
        var divTag = document.createElement("span");
        document.body.appendChild(divTag);
        divTag.id = "hor" + i;
        divTag.innerHTML = i;
        //divTag.style.float = "left";
        
    }

    // Create long list vertically
    for (i=0; i < 500; i++) {
        var divTag = document.createElement("div");
        document.body.appendChild(divTag);
        divTag.id = "ver" + i;
        divTag.innerHTML = i;
    }
    
    // Scroll automatically once if user specifies "right" or "down" as a URL parameter
    option = window.location.search.substr(1);
    if (option == "right") {
        window.scrollTo(window.screen.availWidth / 2, 0);
    }
    else if (option == "down") {
        window.scrollTo(0, window.screen.availHeight / 2);
    }
    
    window.onscroll = function() {myFunction()};
    function myFunction() {
        var y = document.body.scrollTop|| document.documentElement.scrollTop;
        var x = document.body.scrollLeft || document.documentElement.scrollLeft;
        var output = x || y;
        document.getElementById("scroll").innerHTML = output;
        
        /*if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
            document.getElementById("output").innerHTML = "vertical";
        }
        if (document.body.scrollLeft > 50 || document.documentElement.scrollLeft > 50) {
            document.getElementById("output").innerHTML = "horizontal";
        }*/
    }
}
</script></head><body><div id="scroll">0</div></body></html>
"""


@app.route("/jquery-1.7.2.min.js")
def jquery():
    with open("tests/test_data/jquery-1.7.2.min.js") as hdl:
        data = hdl.read()
    return data


@app.route("/jquery-ui.min.js")
def jquery2():
    with open("tests/test_data/jquery-ui.min.js") as hdl:
        data = hdl.read()
    return data


@app.route("/jquery.ui.touch-punch.min.js")
def jquery3():
    with open("tests/test_data/jquery.ui.touch-punch.min.js") as hdl:
        data = hdl.read()
    return data


@app.route("/")
def main():
    return """<html><body>
    <div id="default">Naught, but disappointment thou shalt find within this realm.</div>
    </body></html>"""


@app.route("/long")
def long():
    return long_page


@app.route("/keypress")
def key_press():
    return keypress


@app.route("/link")
def link():
    return hyperlink


@app.route("/drag")
def drag():
    return drag_and_drop


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
