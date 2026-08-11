from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import current_user, login_required
from aidenflask import db
from models import Note
from datetime import datetime

notes_bp=Blueprint("notes",__name__,template_folder="templates")

@notes_bp.route("/notes", methods=["GET","POST"])
@login_required
def notes():
    search_query = request.args.get("q", "").strip()

    if request.method=="POST":
        note_text = request.form.get("note", "").strip()
        note = Note(note=note_text, user_id=current_user.id)
        if len(note.note) < 1:
            user_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.date.desc()).all()
            return render_template("notes.html", error="Note is too short", notes=user_notes, q=search_query)
        else: 
            db.session.add(note)
            db.session.commit()
            return redirect(url_for('notes.notes'))

    user_notes = Note.query.filter_by(user_id=current_user.id)
    if search_query:
        user_notes = user_notes.filter(Note.note.ilike(f"%{search_query}%"))
    user_notes = user_notes.order_by(Note.date.desc()).all()
    return render_template("notes.html", notes=user_notes, q=search_query)

@notes_bp.route("/edit-note/<int:note_id>", methods=["POST"])
@login_required
def edit_note(note_id):
    note = Note.query.get(note_id)
    if not note or note.user_id != current_user.id:
        return jsonify({"status": "error", "message": "Not allowed"}), 403

    updated_text = request.form.get("note", "").strip()
    if len(updated_text) < 1:
        return jsonify({"status": "error", "message": "Note is too short"}), 400

    note.note = updated_text
    note.date = datetime.now()
    db.session.commit()
    return jsonify({"status": "success"}), 200

@notes_bp.route("/delete-note/<int:note_id>", methods=["POST"])
@login_required
def delete_note(note_id):
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 403