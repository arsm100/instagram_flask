from instagram import app
from flask import render_template
from tests import user_can_follow_each_other # for testing

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
