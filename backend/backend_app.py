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
    try:
        with open("posts.json", "r") as fileobj:
            blog_posts = json.load(fileobj)
    except FileNotFoundError:
        return "File not found", 404
    # Get the title, content from the json file
    data = request.get_json()
    title = data['title']
    content = data['content']
    # If missing title and content, raise an error
    if title == "" or content == "":
        return jsonify({'error': 'Title and content are required'}), 400
    # Generate a unique identifier for the new post
    new_post_id = len(blog_posts) + 1
    # Create a new blog post dictionary
    new_post = {
        'id': new_post_id,
        'title': title,
        'content': content
    }
    blog_posts.append(new_post)
    # Save data to a newfile
    with open('posts.json', 'w') as newfile:
        json.dump(blog_posts, newfile, indent=4)
    # Redirect back to homepage
    return redirect(url_for('index'))


@app.route('/api/posts/<int:post_id>', methods=['GET', 'POST'])
def delete(post_id):
    """ Find the blog post with the given id and remove it from the list"""
    with open("posts.json", "r") as fileobj:
        posts = json.load(fileobj)
    for post in posts:
        if post['id'] == post_id:
            posts.remove(post)
        if not id:
            return jsonify({'error': 'Post Not Found'}), 404
        with open('posts.json', 'w') as newfile:
            json.dump(posts, newfile, indent=4)
        # Redirect back to the home page
        return redirect(url_for('index'))
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 201


@app.route('/api/posts/<id>', methods=['PUT'])
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
        # Update the post in the JSON file
        post['id'] = request.form['id']
        post['title'] = request.form['title']
        post['content'] = request.form['content']

        with open('job_posts.json', 'w')as fileobj:
            json.dump(blog_posts, fileobj, indent=4)

    # Redirect back to index
    return redirect(url_for('index'))
    # Else, it's a GET request. So display the update.html page
    #return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
