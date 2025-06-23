# Sample Code for Refactoring

This file contains some basic code examples that need refactoring.

## User Authentication Function

```python
def authenticate_user(username, password):
    # This function has several issues that need refactoring
    users = [
        {"username": "admin", "password": "admin123", "role": "admin"},
        {"username": "user1", "password": "pass123", "role": "user"},
        {"username": "user2", "password": "mypass", "role": "user"}
    ]
    
    for user in users:
        if user["username"] == username and user["password"] == password:
            print("Login successful!")
            return True
    
    print("Login failed!")
    return False
```

## Data Processing Function

```javascript
function processUserData(users) {
    // This function could be improved
    let result = [];
    for (let i = 0; i < users.length; i++) {
        if (users[i].age >= 18) {
            if (users[i].status == "active") {
                if (users[i].email != null && users[i].email != "") {
                    result.push({
                        name: users[i].firstName + " " + users[i].lastName,
                        email: users[i].email,
                        age: users[i].age,
                        isAdult: true
                    });
                }
            }
        }
    }
    return result;
}
```

## Database Connection

```go
func connectToDatabase() {
    // Poor error handling and resource management
    db, err := sql.Open("mysql", "user:password@/dbname")
    if err != nil {
        fmt.Println("Error connecting to database:", err)
        return
    }
    
    // No defer db.Close()
    
    rows, err := db.Query("SELECT * FROM users")
    if err != nil {
        fmt.Println("Query error:", err)
        return
    }
    
    // No defer rows.Close()
    
    for rows.Next() {
        var id int
        var name string
        rows.Scan(&id, &name)
        fmt.Printf("ID: %d, Name: %s\n", id, name)
    }
}
```

## API Handler

```python
def handle_api_request(request):
    # This API handler has security and error handling issues
    if request.method == "POST":
        data = request.get_json()
        user_id = data["user_id"]  # No validation
        action = data["action"]    # No validation
        
        if action == "delete":
            # Direct SQL execution - SQL injection risk
            query = f"DELETE FROM users WHERE id = {user_id}"
            db.execute(query)
            return {"status": "success"}
        elif action == "update":
            name = data["name"]
            email = data["email"]
            query = f"UPDATE users SET name = '{name}', email = '{email}' WHERE id = {user_id}"
            db.execute(query)
            return {"status": "success"}
    
    return {"status": "error"}
```

## Issues to Address

The code above has several problems:

1. **Security Issues**: Hardcoded passwords, SQL injection vulnerabilities
2. **Poor Error Handling**: No proper exception handling
3. **Resource Management**: Missing cleanup (defer statements, context managers)
4. **Code Duplication**: Repeated patterns that could be abstracted
5. **Poor Validation**: No input validation or sanitization
6. **Inefficient Logic**: Nested conditions that could be simplified
7. **Magic Numbers/Strings**: Hardcoded values that should be constants
8. **Poor Separation of Concerns**: Mixed responsibilities in single functions

These examples are perfect for demonstrating refactoring techniques and best practices.
