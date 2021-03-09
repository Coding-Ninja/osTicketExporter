import MySQLdb as sql
import sys
import json

def get_comments(con, ticket_Id):
    cur = con.cursor()
    cur.execute("""
select * from 
(
	select
		 concat(title,' : ', note) 							                as body
		,st.email											                          as author
		,DATE_FORMAT(n.created, '%%Y-%%m-%%dT%%T.000+0000')     as  created
	from
		ost_ticket_note n left outer join
		ost_staff st on st.staff_id = n.staff_id
	where
		n.ticket_id = %s
	union all
	select
		 r.response											                        as body
		,st.email											                          as author
		,DATE_FORMAT(r.created, '%%Y-%%m-%%dT%%T.000+0000')     as created
	from
		ost_ticket_response r left outer join
		ost_staff st on st.staff_id = r.staff_id
	where
		r.ticket_id = %s
) as sub
order by
	sub.created asc
""", (ticket_Id, ticket_Id))    

    rows = cur.fetchall()
    results = ''

    for row in rows:
        results += '{ "body" : ' + json.dumps(row[0].decode('latin1')) + ','
        results += '"author" : "' + str(row[1]) + '",'
        results += '"created" : "' + str(row[2]) + '"},'

    return results[:-1]

def get_issues(con):
    cur = con.cursor()
    cur.execute("""
select 
	  t.status 												                  as status
	 ,p.priority											                  as priority
	 ,t.subject												                  as summary
	 ,m.message						        				              as description
	 ,t.email												                    as reporter
	 ,t.ticketID											                  as externalId
	 ,st.email												                  as assignee
	 ,DATE_FORMAT(t.created, '%Y-%m-%dT%T.000+0000')		as created
from 
	 ost_ticket t left outer join
	 ost_ticket_priority p on p.priority_id = t.priority_id left outer join
	 ost_ticket_message m on m.ticket_id = t.ticket_id left outer join
	 ost_staff st on st.staff_id = t.staff_id
order by
	 t.created asc;""")

    rows = cur.fetchall()
    result = ""

    for row in rows:
       result += '{"status" : "' + row[0] + '",'  
       result += '"priority" : "' + row[1] + '",'
       result += '"summary" : ' + json.dumps(row[2].decode('latin1')) + ','
       result += '"description" : ' + json.dumps(row[3].decode('latin1')) + ','
       result += '"reporter" : "' + row[4] + '",'
       result += '"externalId" : "' + str(row[5]) + '",'
       result += '"labels" : ["osTicket"],'
       result += '"assignee" : "' + str(row[6]) + '",'
       result += '"created" : "' + row[7] + '",'
       result += '"comments" : [' + get_comments(con, row[5]) + ']},'

    return result[:-1]

def start_json():
    return """{ "projects": [{
					"name": "Sample data",
					"key": "SAM",
					"issues": ["""
	
def export():
    try:
        con = sql.connect("YOUR_DB_SERVER_IP", "DB_USER", "DB_PASSWORD", "DB_NAME")

        with open('os_export.json','a') as f:
            f.write(start_json() + get_issues(con) + """]}]}""")
        print "fin!"
    except sql.Error, e:
        print "Oops I did it again.." + e.args[1]
    finally:
       if con:
           con.close()

export()
