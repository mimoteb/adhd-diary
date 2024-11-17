# Requirements:
# Flask, SQLAlchemy, PyYAML

import os
import yaml
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Load configuration from YAML file
with open("config.yaml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = cfg['database']['uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)

# Define the Table Model
class CopingEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    trigger = db.Column(db.String(255), nullable=False)
    emotion_reaction = db.Column(db.String(255), nullable=False)
    behavior_response = db.Column(db.String(255), nullable=False)
    consequences = db.Column(db.String(255), nullable=False)
    thoughts = db.Column(db.String(255), nullable=False)
    coping_strategy = db.Column(db.String(255), nullable=False)

# Create Database tables if not present
db.create_all()

# Routes
@app.route('/')
def index():
    entries = CopingEntry.query.all()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    new_entry = CopingEntry(
        date=request.form['date'],
        time=request.form['time'],
        trigger=request.form['trigger'],
        emotion_reaction=request.form['emotion_reaction'],
        behavior_response=request.form['behavior_response'],
        consequences=request.form['consequences'],
        thoughts=request.form['thoughts'],
        coping_strategy=request.form['coping_strategy']
    )
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    entry = CopingEntry.query.get(id)
    if request.method == 'POST':
        entry.date = request.form['date']
        entry.time = request.form['time']
        entry.trigger = request.form['trigger']
        entry.emotion_reaction = request.form['emotion_reaction']
        entry.behavior_response = request.form['behavior_response']
        entry.consequences = request.form['consequences']
        entry.thoughts = request.form['thoughts']
        entry.coping_strategy = request.form['coping_strategy']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', entry=entry)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_entry(id):
    entry = CopingEntry.query.get(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/get_entries', methods=['GET'])
def get_entries():
    date = request.args.get('date')
    entries = CopingEntry.query.filter_by(date=date).all()
    entries_list = []
    for entry in entries:
        entries_list.append({
            "id": entry.id,
            "date": entry.date,
            "time": entry.time,
            "trigger": entry.trigger,
            "emotion_reaction": entry.emotion_reaction,
            "behavior_response": entry.behavior_response,
            "consequences": entry.consequences,
            "thoughts": entry.thoughts,
            "coping_strategy": entry.coping_strategy
        })
    return jsonify(entries_list)

if __name__ == '__main__':
    app.run(debug=True)

# Template files (in the templates directory):
# 1. index.html - display entries and provide add/edit/delete buttons
# 2. edit.html - form to edit existing entry
