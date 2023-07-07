from flask import Flask, jsonify, url_for, request, redirect, render_template, url_for
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Returns a list of posts to a template for display."""
    with open("posts.json", "r") as file:
        posts = json.load(file)
    return jsonify(posts)


@app.route('/api/posts', methods=['POST'])
def add():
    """ Add new blog_post to the list if a Post request is sent."""
    blog_posts = []
    if request.method == 'POST':
        # Get the title, content from the form
        title = request.form['title']
        content = request.form['content']
        # Make sure that both title and content are provided
        if not title or not content:
            return jsonify({'error': 'Title and content are required'}), 400
        # Create a new blog post dictionary
        new_post = {
            'title': title,
            'content': content
        }
        blog_posts.append(new_post)
        # Save data to a newfile
        with open('posts.json', 'w') as newfile:
            json.dump(blog_posts, newfile, indent=4)
        # Redirect back to homepage
        return redirect(url_for('get_posts'))
    return render_template('index.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """ Find the blog post with the given id and remove it from the list"""
    with open("job_posts.json", "r") as fileobj:
        blog_posts = json.load(fileobj)
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
    # Redirect back to the home page
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
        Fetch the blog posts from the JSON file.
        Update the form to send a post request.
    """
    try:
        with open("job_posts.json", "r") as fileobj:
            blog_posts = json.load(fileobj)
    except FileNotFoundError:
        return "File not found", 404

    for post in blog_posts:
        if post['id'] == post_id:
            if request.method == 'POST':
                # Update the post in the JSON file
                post['author'] = request.form['author']
                post['title'] = request.form['title']
                post['content'] = request.form['content']

                with open('job_posts.json', 'w')as fileobj:
                    json.dump(blog_posts, fileobj, indent=4)

            # Redirect back to index
            return redirect(url_for('index'))
        # Else, it's a GET request. So display the update.html page
        return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
