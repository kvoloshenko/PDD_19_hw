import sqlite3

def get_cursor(connect_string):
    # conn = sqlite3.connect('sqlite/hh_db.sqlite')
    conn = sqlite3.connect(connect_string)
    cursor = conn.cursor()
    return cursor

def read_last_request_id(connect_string):
    cursor = get_cursor(connect_string)
    cursor.execute('select max(rq.id) from hh_requests rq')
    rows =cursor.fetchall()
    # print(type(rows),f'rows={rows}' )
    last_request_id = rows[0][0]
    # print (type(last_request_id),f'last_request_id={last_request_id}')
    return last_request_id

def read_keywords (connect_string, request_id):
    cursor = get_cursor(connect_string)
    cursor.execute(f'select rq.keywords from hh_requests rq where rq.id = {request_id}')
    rows = cursor.fetchall()
    # print(type(rows), f'rows={rows}')
    keywords = rows[0][0]
    # print (type(keywords), f'keywords={keywords}')
    return keywords

def read_skills(connect_string, request_id):
    cursor = get_cursor(connect_string)
    cursor.execute(f'select rs.skill_name, rs.skill_count, rs.skill_persent from hh_responses rs where rs.requests_id = {request_id} order by rs.skill_count desc')
    rows = cursor.fetchall()
    # print(type(rows), f'rows={rows}')
    requirements = []
    for row in rows:
        i_dic = {}
        # print(type(row),f'fow={row}')
        i_dic['name'] = row[0]
        i_dic['count'] = row[1]
        i_dic['persent'] = row[2]
        # print(f'i_dic={i_dic}')
        requirements.append(i_dic)
    return requirements

def write_requests(connect_string, requests):
    conn = sqlite3.connect(connect_string)
    cursor = conn.cursor()
    cursor.execute("insert into hh_requests (keywords) VALUES (?)", (f'"{requests}"',))
    conn.commit()
    cursor.execute('select max(rq.id) from hh_requests rq')
    rows = cursor.fetchall()
    last_request_id = rows[0][0]
    conn.close()
    return last_request_id

def write_responses(connect_string, last_request_id, responses):
    conn = sqlite3.connect(connect_string)
    cursor = conn.cursor()
    # print(type(responses))

    for item in responses:
        # print (type(item),f'item={item}')
        i_name = item['name']
        i_count = item['count']
        i_persent = item['persent']
        # insert_s = f'insert into hh_responses (requests_id, skill_name, skill_count, skill_persent) VALUES ({last_request_id}, "{i_name}", {i_count}, {i_persent})'
        # print(f'insert_s={insert_s}')
        cursor.execute("insert into hh_responses (requests_id, skill_name, skill_count, skill_persent) VALUES (?, ?, ?, ?)",(last_request_id, f'"{i_name}"', i_count, i_persent,))
    conn.commit()
    conn.close()

# if __name__ == '__main__':
    # connect_string = 'hh_test.sqlite'
    # last_request_id = write_requests(connect_string, 'NAME:(C#)')
    # print(type(last_request_id), f'last_request_id={last_request_id}')
    # requirements = [{'name': 'net', 'count': 16, 'persent': 21}, {'name': 'c', 'count': 12, 'persent': 16}]
    # write_responses(connect_string, last_request_id, requirements)

    # keywords = get_keywords(connect_string, last_request_id)
    # print(type(keywords), f'keywords={keywords}')
    # requirements = read_skills(connect_string, last_request_id)
    # print(type(requirements), f'requirements={requirements}')