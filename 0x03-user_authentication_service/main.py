#!/usr/bin/env python3
"""
End-to-end integration test module
"""
import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """
    the test for registering user
    """
    data = {"email": email, "password": password}
    response = requests.post("{}/users".format(BASE_URL), data=data)
    if response.status_code == 400:
        assert response.json()["message"] == "email already registered"
    else:
        assert response.status_code == 200
        assert response.json().get("email") == email
        assert response.json().get("message") == "user created"
        print("User registered successfully.")


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test for logging in with the wrong password
    """
    data = {"email": email, "password": password}
    response = requests.post("{}/sessions".format(BASE_URL), data=data)
    assert response.status_code == 401
    print("Incorrect login attempt handled.")


def profile_unlogged() -> None:
    """
    Test for checking profile while not logged in
    """
    response = requests.get("{}/profile".format(BASE_URL))
    assert response.status_code == 403
    print("Profile request for unlogged user handled.")


def log_in(email: str, password: str) -> str:
    """
    Test for logging in with the correct credentials
    """
    data = {"email": email, "password": password}
    response = requests.post("{}/sessions".format(BASE_URL), data=data)
    assert response.status_code == 200
    session_id = response.cookies.get("session_id")
    assert response.json().get("email") == email
    assert response.json().get("message") == "logged in"
    print("User logged in successfully.")
    return session_id


def profile_logged(session_id: str) -> None:
    """
    Test for checking profile while logged in
    """
    cookies = {"session_id": session_id}
    response = requests.get("{}/profile".format(BASE_URL), cookies=cookies)
    assert response.status_code == 200
    assert response.json().get("email")  # == "guillaume@holberton.io"
    print("Profile request for logged-in user handled.")


def log_out(session_id: str) -> None:
    """
    Test for logging out
    """
    cookies = {"session_id": session_id}
    response = requests.delete("{}/sessions".format(BASE_URL), cookies=cookies)
    assert response.history
    assert response.history[0].status_code == 302
    assert response.status_code == 200
    print("User logged out successfully.")


def reset_password_token(email: str) -> str:
    """
    Test for checking the reset password token
    """
    data = {"email": email}
    response = requests.post("{}/reset_password".format(BASE_URL), data=data)
    assert response.status_code == 200
    reset_token = response.json().get("reset_token")
    assert response.json().get("email") == email
    print("Reset password token obtained.")
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Test for checking update password
    """
    data = {
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
            }
    response = requests.put("{}/reset_password".format(BASE_URL), data=data)
    assert response.status_code == 200
    assert response.json().get('email') == email
    assert response.json().get('message') == "Password updated"
    print("Password updated successfully.")


if __name__ == "__main__":
    EMAIL = "guillaume@holberton.io"
    PASSWD = "b4l0u"
    NEW_PASSWD = "t4rt1fl3tt3"

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
