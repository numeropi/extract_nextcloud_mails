# extract_nextcloud_mails
Script to extract and filter out nextcloud mails by lastLogin time, groupnames and groupby languages. Useful for maintenance, mailing and analytics.

# Developers
Ivan ([Komun.org](https://komun.org)). ![Komun.org](https://komun.org/user/themes/komun/images/komun_logo_p.png "Komun.org")

(Tip: create yourself a safe and private Nextcloud account [here](https://nubo.komun.org))

# Usage
* Download this repository in your Nextcloud server
* Find out the database access details (usually in config/config.php)
* Install python3 mysql support: **sudo apt install python3-mysqldb**
* Create a config.py file with the access parameters or edit them directly in the extract_nextcloud_mails.py
```python
DB_HOST = "localhost"
DB_USERNAME = "nextcloud"
DB_PASSWORD = "db_password"
DB_NAME = "db_name"
```

# Configuring filters
You can leave empty or edit the following filters inside the script
```python
languages_groupby = ['en','es','ca']
last_login_filter_time = timedelta(days=30) #leave as None if you don't want to filter by last_login
groups_filter = ['premium'] #groupnames are case-sensitive, leave as empty list if no filter by groups
```

The script has 3 ways to filter:

# Output
Example of filtering by Spanish, Catalan, English or Others languages

```
Filtering by groups ['premium']
Filtering by last login time 30 days, 0:00:00
Grouping by language ['en', 'es', 'ca']
-------------------- 
Lang ca
ccccc <cccccc@riseup.net>
-------------------- 
Lang en
aaaa <aaaa@telenet.be>
bbbb <bbbb@bbbb.es>
-------------------- 
Lang other
yyyy <yyy@riseup.net>
-------------------- 
Lang es
xxxx <xxxx@xxxx.com>
xxx <delete@delete.com>
```

# Hack it
Send us a pull request, create a Nextcloud plugin based on this, etc.

# Feedback
Add bug/feature request in this bug repository.

# Help us
Buy us a coffee: https://liberapay.com/bitarkivo/ 
