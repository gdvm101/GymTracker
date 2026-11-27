def test_readiness_reads_the_migrated_database(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["X-Request-ID"]


def test_h_only_registers_implemented_routes(client):
    document = client.get("/api/v1/openapi.json").json()
    assert "/api/v1/health" in document["paths"]
    for route in ("/api/v1/ai", "/api/v1/groups", "/api/v1/notifications"):
        assert route not in document["paths"]
        assert client.get(route).status_code == 404
