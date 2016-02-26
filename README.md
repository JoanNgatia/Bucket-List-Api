[![Code Issues](https://www.quantifiedcode.com/api/v1/project/e0557b55469e43bbada740de6704a1fc/badge.svg)](https://www.quantifiedcode.com/app/project/e0557b55469e43bbada740de6704a1fc)
[Code Climate]:https://codeclimate.com/github/andela-jngatia/Bucket-List-Api
[![Code Climate](https://codeclimate.com/github/andela-jngatia/Bucket-List-Api/badges/gpa.svg)](https://codeclimate.com/github/andela-jngatia/Bucket-List-Api)
[![Build Status](https://travis-ci.org/andela-jngatia/Bucket-List-Api.svg?branch=develop)](https://travis-ci.org/andela-jngatia/Bucket-List-Api)
[![Coverage Status](https://coveralls.io/repos/github/andela-jngatia/Bucket-List-Api/badge.svg?branch=develop)](https://coveralls.io/github/andela-jngatia/Bucket-List-Api?branch=develop)


# BUCKETLIST API
This is a bucket list API built on [Flask](http://flask.pocoo.org/).

This feature rich API has token based authentication, pagination and search capabilities.


The features attached to the service include: 
* authenticating a user
* creating new bucketlist items
* updating and deleting the items 
* retrieving a list of all created bucket lists by a registered user.

## Accessing resources 
httpie, the 'fresher' CLI client, can be used to access the different resources on the different routes.Good old Postman, can also be used to test out the routes.

A sample request to log in user 'jo' with password 'w' is:

```http POST http://localhost:5000/auth/login/ username='jo' password='w'```

A token is generated after this request.Hold on to it.You'll need it for access to bucketlists that you will create.

Simply attach the token to the request body for all routes that require login.
An example of this is :

```http http://localhost:5000/bucketlists/ 'token:<token_body>' ```

This route returns all bucketlists created by the logged in user.

### Extra features
A user is also able to specify the number of bucketlists they would like to view per page.The default is however set at 20 with a 100-bucketlist max limit.

``` http http://localhost:5000/bucketlists/?limit=2 'token:<token_body>' ```


A user can also search for a bucektlist by name, by appending the name to the request body.

``` http://localhost:5000/bucketlists/?q=ride  'token:<token_body>' ```

This request returns all bucketlists whose names contain the word ride.

### API endpoints
Possible API endpoints for use with this application can be found on this [Apiary Doc](http://docs.bucketlist6.apiary.io/#)

### How it works on your local machine
1. Simply clone the repo by running ```git clone https://github.com/andela-jngatia/Bucket-List-Api.git```.
2. Install dependencies as per the requirements.txt file within your virtual environment. ```pip install -r requirements.txt```.
3. Initialize the databse skeleton by running ```python app/models.py```
4. Create the database by running ```python main/manage.py db init ``` and make the migrations required by running
```python main/manage.py db migrate```
5. Access the API by running ```python manage.py runserver```
6. Create bucketlists and update them as you wish using either the httpie option as discussed or using [Postman](https://www.getpostman.com/).


### Running tests
1. Navigate to project directory.
2. Run `nosetests` to test the system.
3. Run `nosetests --with-coverage` to check coverage.
