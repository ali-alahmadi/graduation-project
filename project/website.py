import os
from flask import Flask, redirect, render_template, request, url_for
from server import DocumentAnalysis as DA
from server import GenerateDiagram as GEN

app = Flask(__name__)
diagramfolder = os.path.join('static','diagram')
app.config['UPLOAD_FOLDER'] = diagramfolder


@app.route('/')
def home():
    return render_template('home.html')    

@app.route('/input', methods=['GET', 'POST'])
def upload_file():
    message = ''
    if request.method == 'POST':
        diagram_type = request.form.get('diagrams')
        file = request.files['file']
        filename = file.filename
        file_extension = os.path.splitext(filename)[1]
        
        if file_extension in ['.txt', '.pdf']:
            DA.DocumentAnalysis.dataInitialization(file,file_extension,diagram_type)
            return redirect(url_for('diagram', diagram_type = diagram_type))
        else:
            message = 'Invalid file type. Please upload a .txt or .pdf file.'

        diagram_type = request.form.get('diagrams')
    return render_template('input.html', message=message)


@app.route('/diagram')
def diagram():
    diagram_type = request.args.get('diagram_type', default=None, type=str)
    image_path = GEN.GenerateDiagram.generate_image(diagram_type)
    umldiagram = os.path.join(app.config['UPLOAD_FOLDER'], image_path)
    return render_template('diagram.html',image_path= umldiagram)


if __name__ == '__main__':
    app.run(debug=True)