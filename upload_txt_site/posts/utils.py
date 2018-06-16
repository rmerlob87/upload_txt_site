import os
import secrets
import numpy as np
from flask import current_app
from flask_login import current_user
import boto3
import io

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt # noqa


def save_file(form_file):
    random_hex = secrets.token_hex(8)
    f_n, f_ext = os.path.splitext(form_file.filename)
    file_fn = current_user.username + "_" + f_n + "_" + random_hex + f_ext
    file_path = os.path.join(current_app.root_path,
                             'static/files_posted', file_fn)
    form_file.save(file_path)
    return file_fn


def read_file(filename):
    file_path = os.path.join(current_app.root_path,
                             'static/files_posted', filename)
    with open(file_path, "r") as f:
        file_contents = f.readlines()
    return file_contents


def create_plot(BUCKET_NAME, folder, form_file):
    # with open(form_file, "r") as f:
    data = list()
    form_file.seek(0)
    for line in form_file:
        line = line.decode("utf-8")
        x, y = line.split(",")
        x = float(x.replace("\n", ""))
        y = float(y.replace("\n", ""))
        data.append((x, y))

    data = np.array(data)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(data[:, 0], data[:, 1])
    ax.grid()
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    s3 = boto3.client('s3')
    random_hex = secrets.token_hex(8)
    f_n, f_ext = os.path.splitext(form_file.filename)
    KEY = folder + "/" + f_n + random_hex + ".pdf"
    filelike = io.BytesIO(b"")
    fig.savefig(filelike, format="pdf")
    filelike.seek(0)
    s3.put_object(Bucket=BUCKET_NAME, Body=filelike, Key=KEY,
                  ContentType='application/pdf')
    return KEY
