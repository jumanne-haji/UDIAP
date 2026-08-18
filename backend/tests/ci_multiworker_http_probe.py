import asyncio
import sys
import time
import httpx
import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.core.config import settings

BASE_URL = "http://127.0.0.1:8000"

async def check_redis_direct():
    print("\n--- REDIS CONNECTIVITY ---")
    assert settings.REDIS_URL
    r = aioredis.from_url(settings.REDIS_URL)
    pong = await r.ping()
    assert pong is True
    await r.aclose()
    print("[PASS] Redis PING/PONG")

async def check_postgres_dialect():
    print("\n--- POSTGRESQL DIALECT ---")
    assert settings.DATABASE_URL
    engine = create_async_engine(settings.DATABASE_URL)
    dialect = engine.dialect.name
    print(f"[CI VERIFICATION] Active Database Dialect: {dialect}")
    assert dialect == "postgresql"
    await engine.dispose()
    print("[PASS] PostgreSQL dialect confirmed")

async def await_server_ready(timeout_seconds=30):
    print("\n--- SERVER READINESS ---")
    start = time.time()
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=5) as client:
        while time.time() - start < timeout_seconds:
            try:
                r = await client.get("/health")
                if r.status_code == 200:
                    print("[PASS] /health HTTP 200")
                    return
            except httpx.RequestError:
                pass
            await asyncio.sleep(0.5)
    raise RuntimeError("Gunicorn failed readiness check")

async def verify_rate_limiting():
    print("\n--- RATE LIMITING ---")
    statuses = []
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=5) as client:
        payload = {
            "username": "ratelimit_test@example.com",
            "password": "WrongPassword123!"
        }
        for _ in range(40):
            r = await client.post("/api/v1/auth/login", data=payload)
            statuses.append(r.status_code)
            if r.status_code == 429:
                break

    print(f"[CI RATE LIMIT] {statuses}")
    assert 429 in statuses
    print("[PASS] HTTP 429 enforced")

async def verify_multiworker_pipeline_concurrency():
    print("\n--- MULTI-WORKER PIPELINE ---")

    email = f"ci_worker_{int(time.time())}@example.com"
    password = "SecureCIPassword123!"

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=20) as client:

        reg = await client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "password": password,
                "full_name": "CI Concurrency Test User"
            }
        )

        assert reg.status_code in (200, 201), reg.text

        login = await client.post(
            "/api/v1/auth/login",
            data={
                "username": email,
                "password": password
            }
        )

        assert login.status_code == 200, login.text

        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        assessment = await client.post(
            "/api/v1/assessments/",
            json={
                "title": "CI Concurrency Test Assessment",
                "responses": {
                    "logic_score": 85,
                    "adaptability": 90
                }
            },
            headers=headers
        )

        assert assessment.status_code in (200, 201), assessment.text
        assessment_id = assessment.json()["id"]

        url = f"/api/v1/assessments/{assessment_id}/evaluate"

        async def evaluate():
            return await client.post(url, headers=headers)

        responses = await asyncio.gather(
            *[evaluate() for _ in range(5)],
            return_exceptions=True
        )

        for r in responses:
            if isinstance(r, Exception):
                raise r
            assert r.status_code in (200, 201), r.text

        payloads = [r.json() for r in responses]
        genome_ids = {p["genome_id"] for p in payloads}
        report_ids = {p["report_id"] for p in payloads}

        assert len(genome_ids) == 1
        assert len(report_ids) == 1

        engine = create_async_engine(settings.DATABASE_URL)

        async with engine.connect() as conn:
            genome_count = (
                await conn.execute(
                    text(
                        "SELECT COUNT(*) FROM genomes "
                        "WHERE assessment_id = :aid"
                    ),
                    {"aid": assessment_id}
                )
            ).scalar()

            report_count = (
                await conn.execute(
                    text(
                        "SELECT COUNT(*) FROM ai_reports "
                        "WHERE assessment_id = :aid"
                    ),
                    {"aid": assessment_id}
                )
            ).scalar()

        await engine.dispose()

        print(
            f"[CI DATABASE] genomes={genome_count}, "
            f"ai_reports={report_count}"
        )

        assert genome_count == 1
        assert report_count == 1

        print("[PASS] Multi-worker idempotency verified")

async def main():
    await check_redis_direct()
    await check_postgres_dialect()
    await await_server_ready()
    await verify_rate_limiting()
    await verify_multiworker_pipeline_concurrency()
    print("\n=== ALL CI INFRASTRUCTURE CHECKS PASSED ===")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as exc:
        print(f"\n[CI PROBE FAILURE] {exc}", file=sys.stderr)
        sys.exit(1)
