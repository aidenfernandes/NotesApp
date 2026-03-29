from flask import Blueprint, render_template, request
from aidenflask import db
from models import Note

notes_bp=Blueprint("notes",__name__,template_folder="templates")

@notes_bp.route("/notes", methods=["GET","POST"])
def notes():
    if request.method=="POST":
        note=Note(note=request.form.get("note"))
        db.session.add(note)
        db.session.commit()

    return render_template("notes.html")