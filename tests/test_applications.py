import pytest


@pytest.mark.anyio
async def test_create_and_list_applications(client):
    payload = {
        "company": "CodeReview",
        "title": "Junior Backend",
        "url": "https://hh.ru/vacancy/123",
        "status": "applied",
        "notes": "Откликнулся, жду ответ",
        "tags": "python,fastapi,remote",
    }

    r = await client.post("/applications", json=payload)
    assert r.status_code == 201
    created = r.json()
    assert created["company"] == "CodeReview"

    r = await client.get("/applications")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


@pytest.mark.anyio
async def test_patch_application_updates_only_one_field(client):
    payload = {
        "company": "Arelag",
        "title": "Trainee Python Developer",
        "url": "https://hh.ru/vacancy/999",
        "status": "applied",
        "notes": "Отправил анкету",
        "tags": "python,fastapi",
    }

    r = await client.post("/applications", json=payload)
    assert r.status_code == 201
    app_id = r.json()["id"]

    patch = {"status": "interview"}

    r = await client.patch(f"/applications/{app_id}", json=patch)
    assert r.status_code == 200
    updated = r.json()
    assert updated["status"] == "interview"
    assert updated["company"] == "Arelag"


@pytest.mark.anyio
async def test_patch_not_found(client):
    r = await client.patch("/applications/999999", json={"status": "rejected"})
    assert r.status_code == 404


@pytest.mark.anyio
async def test_delete_application(client):
    payload = {
        "company": "TestCompany",
        "title": "TestTitle",
        "url": "https://example.com",
        "status": "applied",
        "notes": None,
        "tags": None,
    }

    r = await client.post("/applications", json=payload)
    assert r.status_code == 201
    app_id = r.json()["id"]

    r = await client.delete(f"/applications/{app_id}")
    assert r.status_code == 204