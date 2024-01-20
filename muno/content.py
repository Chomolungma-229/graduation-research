from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from muno.auth import login_required
from muno.db import get_db

bp = Blueprint('content', __name__)


@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    if request.method == 'POST':
        # TODO:ここで受け取ったデータをDBへ格納する
        content = ""
        speaker = ""
        content = str(request.form['sentence'])
        speaker = str(request.form['speaker'])
        if request.form['sentence'] != "":
            db = get_db()
            db.execute(
                'INSERT INTO sentence (content, speaker, input_by)'
                ' VALUES (?, ?, ?)',
                (content, speaker, g.user['username']),
            )
            db.commit()
    return render_template('content/index.html', title="index")


@bp.route('/mypage', methods=('GET', 'POST'))
@login_required
def mypage():

    return render_template('content/mypage.html', title="mypage")
