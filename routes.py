from flask import Blueprint, render_template, request, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "Welcome to the Drug Interaction API!"


