#!/usr/bin/env python3
import time

import rq_dashboard
from flask import Flask
from flask import render_template
from flask import stream_with_context, request, Response
from redis import Redis
from rq import Queue
from rq.job import Job

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")

redis_connection = Redis.from_url(app.config["REDIS_URL"])
q = Queue(connection=redis_connection)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/execute', methods=['GET', 'POST'])
def execute():
    field = request.args['field']
    job = q.enqueue("tasks.selenium_task", args=(field,))
    if request.method == 'POST':
        return job.id

    def generate():
        yield f'<br>Job ID: {job.id}</br>'
        yield f'<br>Executing...</br>'
        while not Job.fetch(job.id, redis_connection).is_finished:
            time.sleep(1)
        yield f'<br>Results:</br>'
        yield f'<ul>'
        for result in job.return_value:
            yield f'<li>{result}</li>'
        yield f'</ul>'
        yield f'<br>Job finished</br>'

    return Response(stream_with_context(generate()))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969)
