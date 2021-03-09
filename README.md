osTicketExporter
===

Export tickets from osTicket to JSON format ready to import into Atlassian JIRA Service Desk.

# Usuage

First clone down this repo e.g:

```shell
$ git clone https://github.com/coding-ninja/osticketexporter
$ cd osTicketExporter
```

You should then modify the connection details to point to your MySql database instance, this can be found
on line 89:

```python
con = sql.connect("YOUR_DB_SERVER_IP", "DB_USER", "DB_PASSWORD", "DB_NAME")
```

Finally you can now just execute the `python` export script _(this is Python 2.7 IIRC)_ :

```shell
$ python exporter.py
```