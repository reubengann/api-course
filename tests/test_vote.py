import pytest

from app import orm


@pytest.fixture
def voted_on_post(example_posts, session, test_user):
    post = example_posts[0]
    vote = orm.Vote(user_id=test_user["id"], post_id=post.id)
    session.add(vote)
    session.commit()
    return post


def test_vote_on_post(authorized_client, example_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": example_posts[0].id, "vote_direction": 1}
    )
    assert res.status_code == 201


def test_cannot_vote_on_post_twice(authorized_client, voted_on_post):
    res = authorized_client.post(
        "/vote/", json={"post_id": voted_on_post.id, "vote_direction": 1}
    )
    assert res.status_code == 409


def test_can_remove_vote(authorized_client, voted_on_post):
    res = authorized_client.post(
        "/vote/", json={"post_id": voted_on_post.id, "vote_direction": 0}
    )
    assert res.status_code == 201


def test_cannot_unvote_unvoted_on_post(authorized_client, example_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": example_posts[0].id, "vote_direction": 0}
    )
    assert res.status_code == 409
