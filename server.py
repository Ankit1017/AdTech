from init import app
from add_gen import *
from flask import Response,stream_with_context
@app.route('/')
def add_show():
    return Response(stream_with_context(generate_frames_dual("choclate","tv")))
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)