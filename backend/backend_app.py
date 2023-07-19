from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Returns a list of posts to a template for display.All posts sorted by their title"""
    with open("backend/posts.json", "r") as file:
        posts = json.load(file)
    sort_field = request.args.get('sort')
    sort_direction = request.args.get('direction')

    if sort_field and sort_field in ['title', 'content']:
        sorted_posts = sorted(posts, key=lambda post: post[sort_field], reverse=(sort_direction == 'desc'))
        return {"posts": sorted_posts}
    else:
        return jsonify(posts)


@app.route('/api/posts', methods=['POST'])
def add():
    """ Add new blog_post to the list if a Post request is sent."""
    try:
        with open("backend/posts.json", "r") as fileobj:
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
    with open('backend/posts.json', 'w') as newfile:
        json.dump(blog_posts, newfile, indent=4)

    return jsonify({"message": f"Post with title {title} has been added successfully."})


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete(post_id):
    """ Find the blog post with the given id and remove it from the list"""
    with open("backend/posts.json", "r") as fileobj:
        blog_posts = json.load(fileobj)
    # Delete post by its id
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
        # If no post with given id, return an error response
        if not post_id:
            return jsonify({'error': 'Post Not Found'}), 404
    # Save data to a newfile
    with open('backend/posts.json', 'w') as newfile:
        json.dump(blog_posts, newfile, indent=4)
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 201


@app.route('/api/posts/<int:post_id>', methods=['POST'])
def update(post_id):
    """
        Fetch the blog posts from the JSON file.
        Update an existing blog post.
    """
    try:
        with open("backend/job_posts.json", "r") as fileobj:
            posts = json.load(fileobj)
    except FileNotFoundError:
        return "File not found", 404

    data = request.get_json()
    for post in posts:
        if post['id'] == post_id:
            # Update the title if provided
            if "title" in data:
                post["title"] = data["title"]
            # Update the content if provided
            if "content" in data:
                post["content"] = data["content"]

        with open('backend/job_posts.json', 'w')as fileobj:
            json.dump(posts, fileobj, indent=4)

        return jsonify({
            "id": post["id"],
            "title": post["title"],
            "content": post["content"]
        })
    # If post with given id is not found, return error message
    return jsonify({"error": "Post not found."}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """ Returns posts where the title or content contain is given in the search terms."""
    with open("backend/posts.json", "r") as fileobj:
        posts = json.load(fileobj)

    search_results = []
    title = request.args.get('title')
    content = request.args.get('content')

    if not title and not content:
        return {'message': 'Please provide at least one search term'}

    for post in posts:
        if title and title.lower() not in post['title'].lower():
            search_results.append(post)
        if content and content.lower() not in post['content'].lower():
            search_results.append(post)
    return jsonify(search_results)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
