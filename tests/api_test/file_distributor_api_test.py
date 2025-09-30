import pytest
import testdata.FileDistribution.distribution_process
from component_util.file_distributor import FileDistributor

fd = FileDistributor()


@pytest.fixture(name="context", autouse=True)
def fixture_context(admin_user):
    module_context = {
        "ids": [],
    }
    yield module_context
    if module_context["ids"]:
        all(admin_user.delete(f"/distributionprocesses/{id}") for id in module_context["ids"])


@pytest.fixture(autouse=True)
def before_test_setup(context):
    for server_type in fd.DISTRIBUTION_PROTOCOL:
        response, status = fd.create_distribution_process(
            server_type, name=testdata.FileDistribution.distribution_process.existing_name[server_type]
        )
        assert status == 200
        context["ids"].append(response[-1]["id"])


@pytest.mark.parametrize(
    "protocol,payload_kwarg,status_code, exp_response", testdata.FileDistribution.distribution_process.create_distribution_test_data
)
def test_create_distribution(context, protocol, payload_kwarg, status_code, exp_response):
    resp, status = fd.create_distribution_process(protocol, **payload_kwarg)
    assert status == status_code
    if exp_response:
        assert resp == exp_response
    else:
        context["ids"].append(resp[-1]["id"])
        assert all(resp[-1][k] == v for k, v in payload_kwarg.items())
