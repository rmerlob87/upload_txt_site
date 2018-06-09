
import os
import secrets
from flask import url_for, current_app
from flask_login import current_user
from flask_mail import Message
from upload_txt_site import mail

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def save_file(form_file):
    random_hex = secrets.token_hex(8)
    f_n, f_ext = os.path.splitext(form_file.filename)
    file_fn = current_user.username + "_" + f_n + "_" + random_hex + f_ext
    file_path = os.path.join(current_app.root_path, 'static/files_posted', file_fn)
    form_file.save(file_path)
    return file_fn

def read_file(filename):
    file_path = os.path.join(current_app.root_path, 'static/files_posted', filename)
    with open(file_path, "r") as f:
        file_contents = f.readlines()
    return file_contents

def create_plot(filename):
    random_hex = secrets.token_hex(8)
    f_n, _ = os.path.splitext(filename)
    file_path = os.path.join(current_app.root_path, 'static/files_posted', filename)
    graph_filename = current_user.username + "_" + f_n + "_" + random_hex + ".pdf"
    graph_file_path = os.path.join(current_app.root_path, 'static/graphs_rendered', graph_filename)
    
    with open(file_path, "r") as f:
        data = list()
        for line in f:
            x, y = line.split(",")
            x = float(x.replace("\n",""))
            y = float(y.replace("\n",""))
            data.append((x, y))

    data = np.array(data)
    plt.plot(data[:,0], data[:,1])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(data[:,0], data[:,1])
    ax.grid()
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    fig.savefig(graph_file_path)

    return graph_filename