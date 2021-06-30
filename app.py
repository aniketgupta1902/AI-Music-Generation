from flask import Flask, render_template, redirect, request
import gen_music
import os, glob

app = Flask(__name__)
Flag = False
@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/',methods=['POST'])
def marks():
    if request.method == 'POST':
        gen_music.generate_new()
        Flag = True
    
    return render_template('index.html', flag = Flag)

if __name__ == '__main__':
    app.run(debug=True)
    files = glob.glob('static/')
    for f in files:
        os.remove(f)