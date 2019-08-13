# REST API v1
# Software
Based on [EVE](https://docs.python-eve.org/en/stable/)

For main storage used [Mongo](https://www.mongodb.com/)

[Postman](https://www.getpostman.com/) for API test
Python 3.6
```sh
$ apt install mongodb
$ snap install postman
```
```sh
$ pip install -r requirements.txt
```
# DB structure
- Users
- Categories
- Items

# Easy to opperate!
##### User
create via POST query

http://127.0.0.1:5000/v1/users

body of request:

-- username = "some_password"

-- password = "new_password"
##### Items
create via POST query
http://127.0.0.1:5000/v1/items

parameters:

-- name = "some_new_name"

-- [price, views, photo, parent_category, owner] - optional

Pay attention - to upload a image you should change type field(from "text" to "file")

Basic Auth:

-- Username = <login>

-- Password = <password>

get all items via GET query

http://127.0.0.1:5000/v1/items

get items via GET query with filters

http://127.0.0.1:5000/v1/items?where={"name":"item_name","price":13.0}

http://127.0.0.1:5000/v1/categories?where={"_id":<parent_id>}

http://127.0.0.1:5000/v1/categories?where={"_id":<user_id>}

Sorting

http://127.0.0.1:5000/v1/items?sort=-price

##### Categories

Only GET query allowed

http://127.0.0.1:5000/v1/categories?max_results=5&page=2

##### Categories + Items

GET query

http://127.0.0.1:5000/v1/over-all
