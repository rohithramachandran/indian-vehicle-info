from flask import Flask 

app = Flask(__name__) 

@app.route("/") 
def home_view(): 
		return """<html>
		<body>
		<form action = "/result" method = "POST">
         <p>Vehicle Reg. No. Part1 <input type = "text" name = "first" placeholder="MH47K"/></p>
         <p>Vehicle Reg. No. Part2 <input type = "text" name = "second" placeholder="4272"/></p>
         <p>Captcha <input type = "text" name = "captcha" /></p>
         <p><input type = "submit" value = "submit" /></p>
      </form>
   </body>
</html>"""
