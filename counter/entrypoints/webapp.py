from io import BytesIO
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from counter import config

app = Flask(__name__)

count_action = config.get_count_action()
load_dotenv()

@app.route('/', methods=['GET','POST'])
def base():
    if request.method == 'POST':
        pass
    template = 'base.html'
    return render_template(template)

@app.route('/object-count', methods=['POST'])
def object_count():
    uploaded_file = request.files['file']
    threshold = float(request.form.get('threshold', 0.5))
    image = BytesIO()
    uploaded_file.save(image)
    count_response = count_action.execute(image, threshold)
    return jsonify(count_response)

@app.route('/predict-objects-by-img', methods=['POST'])
def predict_objects_by_img():
    uploaded_file = request.files['file']
    threshold = float(request.form.get('threshold', 0.5))
    image = BytesIO()
    uploaded_file.save(image)
    count_response = count_action.execute(image, threshold)
    return jsonify(count_response)



if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
