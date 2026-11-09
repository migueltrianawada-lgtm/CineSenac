import os
import urllib.request

import pytest
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs


@pytest.mark.skipif(
    os.environ.get("RUN_CONTAINER_TESTS") != "1",
    reason="Defina RUN_CONTAINER_TESTS=1 para executar com Docker/Testcontainers.",
)
def test_flask_image_serves_home_page():
    with (
        DockerContainer("cinesenac:ci")
        .with_exposed_ports(5000)
        .with_env("CINESENAC_SECRET_KEY", "container-test-only-secret")
        .with_env("CINESENAC_DATABASE", "/tmp/cine-senac-test.sqlite")
    ) as container:
        wait_for_logs(container, "Running on", timeout=60)
        address = container.get_container_host_ip()
        port = container.get_exposed_port(5000)

        with urllib.request.urlopen(f"http://{address}:{port}/", timeout=10) as response:
            page = response.read()

        assert response.status == 200
        assert "CineSenac".encode() in page
        assert b"Filmes" in page
