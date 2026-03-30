from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from aidenflask import db
from models import Note
from datetime import datetime

notes_bp=Blueprint("notes",__name__,template_folder="templates")

@notes_bp.route("/notes", methods=["GET","POST"])
@login_required
def notes():
    if request.method=="POST":
        note=Note(note=request.form.get("note"),user_id=current_user.id,date=datetime.now())
        if len(note.note) < 1:
            return render_template("notes.html", error="Note is too short")
        else: 
            db.session.add(note)
            db.session.commit()

    user_notes=Note.query.filter_by(user_id=current_user.id).all()
    return render_template("notes.html", notes=user_notes)