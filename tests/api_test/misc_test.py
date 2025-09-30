from os import unlink
from pathlib import Path
import pytest
from helpers import strings, files


@pytest.fixture(name="context")
def fixture_context(admin_user):
    context = {}
    yield context
    if context:
        admin_user.delete(f'/users/{context["id"]}')


class TestAPI:
    def test_create_user(self, context, admin_user):
        """Creates a random user withinthe WNEC application"""
        random = strings.random(6)
        user = {
            "email": f"{random}@example.com",
            "name": random,
            "username": random,
            # Adds extra characters to password to meet minimum requirements
            # https://jira.thomsonreuters.com/browse/WNEC-6211
            "password": random + "QA1!",
        }

        # Create user
        response, status = admin_user.post("/users", user)
        context.update({"id": response["id"]})
        assert status == 200
        assert "id" in response

    @pytest.mark.tag("slow")
    def test_log_download(self, admin_user):
        """
        It should be possible to download a collection of system logs.
        https://jira.thomsonreuters.com/browse/WNEC-3642
        """
        file = "logs.zip"

        status = admin_user.download("/filelog/download", file)

        assert status == 200
        assert Path(file).exists()

        # Delete the downloaded file
        unlink(file)

    def test_channel_list_sorted_by_id(self, admin_user):
        """
        Playout now channel list should be returned with channel IDs in
        ascending order (1, 2, 3, n)
        https://jira.thomsonreuters.com/browse/WNEC-4702
        """
        channels, status = admin_user.get("/playout/now")

        assert status == 200

        # Expecting IDs in order (1, 2, 3, n)
        expected_ids = list(range(1, len(channels) + 1))

        # IDs received in response
        ids = [int(channel["id"]) for channel in channels]

        assert ids == expected_ids, "Channel IDs should be returned in order"

    @pytest.mark.skip(reason="Differs from Squash, unknown reason")
    def test_whitelisted_appsettings(self, admin_user):
        """
        Whitelisted app settings should return the required keys in the response
        https://jira.thomsonreuters.com/browse/WNEC-4799
        """

        # TODO Implement regular user (non-admin) authentication type and unauthenticated type
        response, status = admin_user.get("/whitelisted-appsettings")

        assert status == 200

        required_keys = files.parametrize("api:required_keys_whitelisted_appsettings")

        for key in required_keys["authorized_admin"]:
            assert key in response, f"The key {key} should be in the response"

    def test_sensitive_information_appsettings(self, admin_user):
        """
        Sensitive information should be returned as a boolean false value only
        https://jira.thomsonreuters.com/browse/WNEC-5457
        """

        response, status = admin_user.get("/appsettings")

        assert status == 200

        for key in files.parametrize("api:sensitive_keys_appsettings"):
            if key in response:
                assert not response[key]
