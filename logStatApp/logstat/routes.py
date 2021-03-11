import os

from flask import render_template, request, url_for, flash
from werkzeug.utils import redirect

from logstat import app
from logstat.statsParsers.read_log import read_log
from logstat.statsParsers.stats import get_stats
from logstat.utils import allowed_file


@app.route("/")
@app.route("/index")
def index():
    """
    Route for the landing/default page when the application is accessed.
    Checks if a logfile is uploaded and sets flags in the template to control visibility of stats button
    :return: result of render template for home page
    """
    stats_available = False
    try:
        with(open("logstat/uploads/access.log")):
            stats_available = True
    except IOError:
        app.logger.warn("No log file available yet")
    return render_template("index.html", stats_available=stats_available)


@app.route("/upload", methods=["GET"])
def upload():
    """
    Route handler for the upload file form for uploading files to application
    """
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    """
    route for the function that handles processing of uploaded file
    checks the filename and extension details and reports any errors
    if no errors are found, it will then save the file in the specified directory with the correct name
    :return: redirect to index page
    """
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('upload'))
        f = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if f.filename == '':
            flash('No selected file')
            return redirect(url_for('upload'))
        if f and not allowed_file(f.filename):
            flash("Incorrect extension!")
            return redirect(url_for('upload'))
        if f and allowed_file(f.filename):
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], "access.log"))
            return redirect(url_for("index"))


@app.route("/stats", methods=["GET"])
def stats():
    """
    Route for the stats page. when called, calculates the stats in the log file in real time and generates and returns
    the HTML page with the details populated. It also takes hostname or time range params from the request and uses it
    to filter the stats before processing
    :return: stats page
    """
    host = request.args.get("host")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    log_path = os.path.join(app.config['UPLOAD_FOLDER'], "access.log")
    try:
        log_data = read_log(file_path=log_path, time_start=start_time, time_end=end_time, host=host)
    except TypeError:
        return "The time values in the logfile could not be parsed. Please check the file or your query and try again"
    except ValueError:
        return "Date Range formatting does not seem to match. Please validate your date format and try again"
    if not log_data:
        return "No results found matching specified query. Please ensure you enter a valid hostname or date range."
    stats_data = get_stats(log_data)
    return render_template('stats.html', stats=stats_data)
