import os
from flask import Flask, request, redirect, url_for, render_template, session
from werkzeug.utils import secure_filename
from detect_experimentation import main
from utils.map_results import classes

UPLOAD_FOLDER = "./static/input_images/"
OUTPUT_FOLDER = "./static/results/"
ALLOWED_EXTENSIONS = set(["txt", "pdf", "png", "jpg", "jpeg", "gif"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)
# models = {}
# main(source, name)
DETECTION_URL = "/detection"
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "This is your secret key to utilize session in Flask"


@app.route("/", methods=["GET", "POST"])
def healthy():
    return {"status": "I am healthy"}


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        print("we are here")
        file = request.files["uploaded-file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            session["filename"] = filename
            results = main(
                source=os.path.join(UPLOAD_FOLDER, filename), name=filename
            ).tolist()
            result_list = []
            for i, values in enumerate(results):
                mapped_dictionary = dict()
                mapped_dictionary["class"] = classes(values[5])
                mapped_dictionary["conf"] = round(values[4], 2)
                result_list.append(mapped_dictionary)
            print(result_list)
            session["results"] = result_list
            return redirect(url_for("displayImage"))
        return render_template("upload.html")
    print("or here")
    return render_template("upload.html")


@app.route("/show_image", methods=["GET", "POST"])
def displayImage():
    # Retrieving uploaded file path from session
    img_file_path = os.path.join(
        "/static/results", session.get("filename", None)
    )
    print(img_file_path)
    # Display image in Flask application web page
    return render_template(
        "show.html",
        user_image=img_file_path,
        detection_results=session.get("results"),
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0", port=1000, debug=True
    )  # debug=True causes Restarting with stat
