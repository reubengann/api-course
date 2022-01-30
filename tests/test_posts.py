def test_get_all_posts(authorized_client, example_posts):
    response = authorized_client.get("/posts/")
    assert response.status_code == 200
    assert len(example_posts) == len(response.json())
