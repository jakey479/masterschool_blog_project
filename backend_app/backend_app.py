from flask import Flask, jsonify, request
from flask_cors import CORS
from uuid import uuid4
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import helpers

app = Flask(__name__)
limiter = Limiter(
    app=app,
    key_func=get_remote_address
)
CORS(app)  # This will enable CORS for all routes
POSTS = [
    {"id": "1", "title": "First post", "content": "This is the first post."},
    {"id": "2", "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
@limiter.limit("5 per minute")
def get_posts():
    sort_key = request.args.get('sort')
    sort_order = request.args.get('direction')
    if sort_key in ['title', 'content']:
        sorted_dictionary = helpers.sort_list_of_dicts_by_value(
            list_of_dicts=POSTS,
            sort_direction=sort_order,
            sort_key=sort_key
        )
        return jsonify(sorted_dictionary)
    elif sort_order == 'desc':
        return jsonify(sorted(POSTS, key=lambda blog_post: blog_post['content'], reverse=False))
    return jsonify(sorted(POSTS, key=lambda blog_post: blog_post['content'], reverse=True))


@app.route('/api/posts', methods=['POST'])
def add_posts():
    data = request.get_json()
    if not (data["title"] or data["content"]):
        return jsonify({"error message": "Sent with missing parameters"}), 400
    post_id = str(uuid4())
    data["id"] = post_id
    POSTS.append(data)
    return jsonify(data), 201


@app.route('/api/posts/<post_id>', methods=['DELETE'])
# @cross_origin(methods=['DELETE'])
def delete_posts(post_id):
    for index, blog_post in enumerate(POSTS):
        if blog_post["id"] == post_id:
            del POSTS[index]
            return jsonify({"message": f"Post with id {post_id} has been deleted successfully."})
    return jsonify({"message": f"post with id {post_id} was not found"}, 404)


@app.route('/api/posts/<post_id>', methods=['PUT'])
def update_posts(post_id):
    data = request.get_json()
    blog_post_to_update = None
    for blog_post in POSTS:
        if blog_post["id"] == post_id:
            blog_post_to_update = blog_post
            break
    if not blog_post_to_update:
        return jsonify({"message": f"post with id {post_id} was not found"}, 404)
    if data["title"]:
        blog_post_to_update["title"] = data["title"]
    if data["content"]:
        blog_post_to_update["content"] = data["content"]
    return jsonify({
        "id": f"{post_id}",
        "title": f"{blog_post_to_update['title']}",
        "content": f"{blog_post_to_update['content']}"
    })


@app.route('/api/posts/search', methods=['GET'])
def return_search_results():
    blog_title = request.args.get('title')
    blog_content = request.args.get('content')
    if blog_title and not blog_content:
        matching_titles = [blog for blog in POSTS if blog_title in blog['title']]
        return jsonify(matching_titles)
    elif blog_content and not blog_title:
        matching_content = [blog for blog in POSTS if blog_content in blog['content']]
        return jsonify(matching_content)
    elif blog_content and blog_title:
        matching_titles_and_content = [
            blog for blog in POSTS if blog_title in blog['title'] and blog_content in blog['content']
        ]
        return jsonify(matching_titles_and_content)
    return jsonify([])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)
