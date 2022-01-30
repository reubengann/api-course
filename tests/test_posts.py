def test_get_all_posts(authorized_client, example_posts):
    response = authorized_client.get("/posts/")
    assert response.status_code == 200
    assert len(example_posts) == len(response.json())


def test_get_one_post(authorized_client, example_posts):
    post_id = example_posts[0].id
    response = authorized_client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["content"] == example_posts[0].content


def test_get_nonexistant_post(authorized_client, example_posts):
    post_id = max(e.id for e in example_posts) + 1
    response = authorized_client.get(f"/posts/{post_id}")
    assert response.status_code == 404


def test_create_post(authorized_client, test_user, example_posts):
    res = authorized_client.post(
        "/posts/", json={"title": "Cool ass title", "content": "ooby dooby"}
    )
    assert res.status_code == 201
    response = res.json()
    assert response["title"] == "Cool ass title"
    assert response["published"]


def test_unauthorized_user_create(client):
    res = client.post(
        "/posts/", json={"title": "Cool ass title", "content": "ooby dooby"}
    )
    assert res.status_code == 401


def test_unauthorized_user_cannot_delete(client, example_posts):
    res = client.delete(f"/posts/{example_posts[0].id}")
    assert res.status_code == 401


def test_authorized_user_can_delete(authorized_client, example_posts):
    res = authorized_client.delete(f"/posts/{example_posts[0].id}")
    assert res.status_code == 204


def test_delete_nonexistant_post(authorized_client, example_posts):
    post_id = max(e.id for e in example_posts) + 1
    response = authorized_client.get(f"/posts/{post_id}")
    assert response.status_code == 404


def test_delete_someone_elses_post(authorized_client, test_user, example_posts):
    for p in example_posts:
        if p.owner_id != test_user["id"]:
            post_id = p.id
            break
    else:
        raise Exception
    response = authorized_client.delete(f"/posts/{post_id}")
    assert response.status_code == 401
