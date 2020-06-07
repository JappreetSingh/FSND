# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`

eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBRZFpBbXF2Rl9WYVo5bTJCX0hicyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtamFwcC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVjYzYxOGFiM2MyOTIwYzVjMzI5ZWM2IiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNTkxNTAxMjk0LCJleHAiOjE1OTE1MDg0OTQsImF6cCI6ImNtcjlRdE02TGlQMjk0M01CZlRlVUVSRXZCdTRFUnRDIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6ZHJpbmtzLWRldGFpbCJdfQ.x3Y0sdpWs3sROtV1msTqAmWmfGPjDERGhb2VlJgKfaUdoHAY-Yp-vKWaWp_QD51XJzBNEM_B_vsBOvkERaJlzL1v6WejhOkVa8BqF04etH7zKpp8IUXLaE2-ZDXTv-yuTJUhyFML1pnFULQP73O87KRYhZ7sGNneECvkmSZV1PEaN_zWa5-clCmNQfSpCyXQJAcmIypLhZSiio8NXWdMl8kslGxwyAE4IzWZoVnDzsZIcnKprdqCG3DMaiF_uLH4_I33tyB0tLd1TxSbCzxYHs3PRixlQCsq2WlYnb4IKWK6rq2e7K8l7BtyzHDQD5CvtcHNpJ8pLawCxPR-z6YbBA

eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBRZFpBbXF2Rl9WYVo5bTJCX0hicyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtamFwcC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkYmNjYjQ1NmQwNjIwMDEzMzBjMTViIiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNTkxNTAxMTU1LCJleHAiOjE1OTE1MDgzNTUsImF6cCI6ImNtcjlRdE02TGlQMjk0M01CZlRlVUVSRXZCdTRFUnRDIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.KGCU63qw9g-aVr2jr2WnPMa0H5T9Qz-YXt0ZGIOoR69t9Ocl338LLa4B45Djjxe21Da7UqGgX87ibxWichfch7G2g7-7DxmXn4bkpajF6OH7hSrkMr7Y6WItyIIXQLjIiJjf9rjBBe_OjbLH9ov7FAPWAKI1-nxlT7eNOPltSPwuV7ZP9QCzwMugGpAa7TilQSru0zLa5uv5leLTUxkug02QRJPsp07krepoIgmoRmlJB3Rqawy6gTvv5acQcGhxHXMuGchnwdWiWiGVkvBqpcEwUnBhv83v01mv6hUbGgJ_ho2TYDCqkTFrhnGwShw7dai2ZxOHIPyQJxdDMjO_0Q