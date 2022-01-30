def test_get_all_posts(authorized_client, example_posts):
    response = authorized_client.get("/posts/")
    assert response.status_code == 200
    assert len(example_posts) == len(response.json())


def test_get_one_posts(authorized_client, example_posts):
    post_id = example_posts[0].id
    response = authorized_client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["content"] == example_posts[0].content
