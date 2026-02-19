# Rust & Go Error Handling Patterns

## Rust: Result and Option
Rust utiliza tipos algebraicos para el manejo de errores, obligando a tratarlos explícitamente.

```rust
// Propagación con el operador ?
fn read_file(path: &str) -> Result<String, io::Error> {
    let mut file = File::open(path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

// Enums para errores personalizados
#[derive(Debug)]
enum AppError {
    Io(io::Error),
    Parse(std::num::ParseIntError),
    NotFound(String),
}
```

## Go: Explicit Error Returns
Go prefiere retornos explícitos y comprobación inmediata del error.

```go
func getUser(id string) (*User, error) {
    user, err := db.QueryUser(id)
    if err != nil {
        return nil, fmt.Errorf("failed to query user: %w", err)
    }
    return user, nil
}

// Sentinel errors para comparaciones simples
var ErrNotFound = errors.New("not found")

if errors.Is(err, ErrNotFound) {
    // Manejar caso no encontrado
}
```
