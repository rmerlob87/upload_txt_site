from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, current_app)
from flask_login import current_user, login_required
from upload_txt_site import db, Config
from upload_txt_site.models import Post
from upload_txt_site.posts.forms import PostForm
from upload_txt_site.posts.utils import create_plot
from upload_txt_site.main.s3Utils import save_to_s3
import os

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        uploaded_file = save_to_s3(Config.S3_BUCKET_NAME,
                                   "userUploads",
                                   form.uploaded_file.data)
        rendered_graph = create_plot(Config.S3_BUCKET_NAME,
                                     "userUploads",
                                     form.uploaded_file.data)
        post = Post(title=form.title.data,
                    content=form.content.data,
                    author=current_user,
                    uploaded_file=uploaded_file,
                    rendered_graph=rendered_graph)

        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if form.uploaded_file.data:
            uploaded_file = save_to_s3(Config.S3_BUCKET_NAME,
                                   "userUploads",
                                   form.uploaded_file.data)
            rendered_graph = create_plot(Config.S3_BUCKET_NAME,
                                     "userUploads",
                                     form.uploaded_file.data)
            post.uploaded_file = uploaded_file
            post.rendered_graph = rendered_graph
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    try:
        file_path = os.path.join(current_app.root_path,
                                 'static/files_posted', post.uploaded_file)
        os.remove(file_path)
    except:
        pass
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
