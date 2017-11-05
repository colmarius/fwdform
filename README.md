Quickstart contact form processing
----------------------------------

This will be useful if...

* You want to forward a simple contact form to your email
* You have a (S3) static site and don't want to run a server

Usage
-----

Register your email:

```bash
    $ curl --data "email=<your_email>" https://happy-forwarder.herokuapp.com/register
    Token: 780a8c9b-dc2d-4258-83af-4deefe446dee

```

Test (optional):

```bash
    $ curl --data "email=hello@test.com&subject=test&message=hello" \
           https://happy-forwarder.herokuapp.com/user/780a8c9b-dc2d-4258-83af-4deefe446dee
```

Put into action:

```html
<form action="https://happy-forwarder.herokuapp.com/user/<token>">
  Email: <input type="text" name="email"><br>
  Subject: <input type="text" name="subject"><br>
  Message: <textarea name="message" cols="40" rows="5"></textarea>
  <input type="submit" value="Send Message">
</form>
```

NB: Required parameters are: `email`, `subject` and `message`. Other parameters will be ignored.

Privacy concerns?
-----------------

Spin up your own free [Heroku](http://www.heroku.com) instance. A [Sendgrid](https://sendgrid.com/) account required for email delivery.

```bash
    $ git clone https://github.com/colmarius/fwdform.git
    $ heroku create
    $ heroku config:set SENDGRID_API_KEY=<KEY>
    $ heroku addons:add heroku-postgresql:hobby-dev
    $ heroku pg:promote HEROKU_POSTGRESQL_COLOR
    $ heroku ps:scale web=1
```

Deploy the application to your Heroku instance.

```bash
    $ git push heroku master
```

Create the database.

```bash
    $ heroku run python
    >>> from app import db
    >>> db.create_all()
    >>> exit()
```
