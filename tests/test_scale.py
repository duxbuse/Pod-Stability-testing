import pytest
from conftest import scale_to

# ------------FIXTURES------------

@pytest.fixture
def set_to_10(load_config):
    return scale_to(load_config, 10)

@pytest.fixture
def set_to_5(load_config):
    return scale_to(load_config, 5)

@pytest.fixture
def set_to_0(load_config):
    return scale_to(load_config, 0)



# ------------TESTS------------

class TestScaleUp:
    # ------------SCALE 0-10------------
    @pytest.mark.benchmark(
        group="scale-up",
        min_time=0.1,
        max_time=0.5,
        min_rounds=5,
    )
    @pytest.mark.dependency()
    def test_scale_0_to_10(self, load_config, benchmark, set_to_0):
        @benchmark
        def result():
            return scale_to(deployment_config=load_config, pod_count=10)

        assert result is None

    # ------------SCALE 0-5------------
    @pytest.mark.benchmark(
        group="scale-up",
        min_time=0.1,
        max_time=0.5,
        min_rounds=5,
    )
    @pytest.mark.dependency()
    def test_scale_0_to_5(self, load_config, benchmark, set_to_0):
        @benchmark
        def result():
            return scale_to(deployment_config=load_config, pod_count=5)

        assert result is None

    # ------------SCALE 5-10------------
    @pytest.mark.benchmark(
        group="scale-up",
        min_time=0.1,
        max_time=0.5,
        min_rounds=5,
    )
    @pytest.mark.dependency()
    def test_scale_5_to_10(self, load_config, benchmark, set_to_5):
        @benchmark
        def result():
            return scale_to(deployment_config=load_config, pod_count=10)

        assert result is None

    

class TestScaleDown:
    # ------------SCALE 10-0------------
    @pytest.mark.benchmark(
        group="scale-down",
        min_time=0.1,
        max_time=0.5,
        min_rounds=5,
    )
    @pytest.mark.dependency()#depends=["TestScaleUp::test_scale_10"]
    def test_scale_10_to_0(self, load_config, benchmark, set_to_10):
        @benchmark
        def result():
            return scale_to(deployment_config=load_config, pod_count=0)

        assert result is None


    # ------------SCALE 10-5------------
    @pytest.mark.benchmark(
        group="scale-down",
        min_time=0.1,
        max_time=0.5,
        min_rounds=5,
    )
    @pytest.mark.dependency()
    def test_scale_10_to_5(self, load_config, benchmark, set_to_10):
        @benchmark
        def result():
            return scale_to(deployment_config=load_config, pod_count=5)

        assert result is None