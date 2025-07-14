from flask import Blueprint, render_template, request
from ..services import MemoryManagement

memory_bp = Blueprint('memory', __name__, url_prefix='/memory')

@memory_bp.route('/', methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template('memory_upload.html', title="Homepage")
    if request.method == "POST":
        image_file = request.files.get("image")

        MemoryManagement.upload_memory(description=request.form["description"],
                                       date=request.form["date"],
                                       image_file=image_file)

    return render_template('memory_upload.html', title="Homepage")