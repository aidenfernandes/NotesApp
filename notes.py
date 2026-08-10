from flask import Blueprint, render_template, request, jsonify, redirect, url_for
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
            return redirect(url_for('notes.notes'))

    user_notes=Note.query.filter_by(user_id=current_user.id).all()
    return render_template("notes.html", notes=user_notes)

@notes_bp.route("/delete-note/<int:note_id>", methods=["POST"])
@login_required
def delete_note(note_id):
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 403