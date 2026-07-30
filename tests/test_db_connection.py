from b3_database.connection import DatabaseConnectionManager


def test_database_connection_uses_environment_variables(monkeypatch):
    monkeypatch.setenv("POSTGRES_USER", "test_user")
    monkeypatch.setenv("POSTGRES_PASSWORD", "test_password")
    monkeypatch.setenv("POSTGRES_DB", "test_db")
    monkeypatch.setenv("POSTGRES_HOST", "test_host")
    monkeypatch.setenv("POSTGRES_PORT", "5433")

    class DummyPool:
        def __init__(self, *args, **kwargs):
            self.kwargs = kwargs

    monkeypatch.setattr("b3_database.connection.pool.SimpleConnectionPool", DummyPool)

    DatabaseConnectionManager._pool = None

    pool = DatabaseConnectionManager.get_pool()
    assert isinstance(pool, DummyPool)
    assert pool.kwargs["user"] == "test_user"
    assert pool.kwargs["password"] == "test_password"
    assert pool.kwargs["database"] == "test_db"
    assert pool.kwargs["host"] == "test_host"
    assert pool.kwargs["port"] == 5433
