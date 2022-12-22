import pytest
from conftest import scale_to

# ------------TESTS------------
class TestScaleUp:
    # ------------SCALE 0-3------------
    @pytest.mark.benchmark(
        group="scale-up"
    )
    @pytest.mark.dependency()
    def test_scale_0_to_3(self, load_config, benchmark):
        results = []
        def setup():
            scale_to(load_config, 0)
        def result():
            results.append(scale_to(deployment_config=load_config, pod_count=3))
        benchmark.pedantic(result, setup=setup, rounds=3, iterations=1)

        assert all(results) is True

    # ------------SCALE 0-1------------
    @pytest.mark.benchmark(
        group="scale-up"
    )
    @pytest.mark.dependency()
    def test_scale_0_to_1(self, load_config, benchmark):
        results = []
        def setup():
            scale_to(load_config, 0)
        def result():
            results.append(scale_to(deployment_config=load_config, pod_count=1))
        benchmark.pedantic(result, setup=setup, rounds=3, iterations=1)

        assert all(results) is True

    # ------------SCALE 1-3------------
    @pytest.mark.benchmark(
        group="scale-up"
    )
    @pytest.mark.dependency()
    def test_scale_1_to_3(self, load_config, benchmark):
        results = []
        def setup():
            scale_to(load_config, 1)
        def result():
            results.append(scale_to(deployment_config=load_config, pod_count=3))
        benchmark.pedantic(result, setup=setup, rounds=3, iterations=1)

        assert all(results) is True

    
class TestScaleDown:
    # ------------SCALE 3-0------------
    @pytest.mark.benchmark(
        group="scale-down"
    )
    @pytest.mark.dependency()
    def test_scale_3_to_0(self, load_config, benchmark):
        results = []
        def setup():
            scale_to(load_config, 3)
        def result():
            results.append(scale_to(deployment_config=load_config, pod_count=0))
        benchmark.pedantic(result, setup=setup, rounds=3, iterations=1)

        assert all(results) is True


    # ------------SCALE 3-1------------
    @pytest.mark.benchmark(
        group="scale-down"
    )
    @pytest.mark.dependency()
    def test_scale_3_to_1(self, load_config, benchmark):
        results = []
        def setup():
            scale_to(load_config, 3)
        def result():
            results.append(scale_to(deployment_config=load_config, pod_count=1))
        benchmark.pedantic(result, setup=setup, rounds=3, iterations=1)

        assert all(results) is True

    # ------------SCALE 1-0------------
    @pytest.mark.benchmark(
        group="scale-down"
    )
    @pytest.mark.dependency()
    def test_scale_1_to_0(self, load_config, benchmark):
        results = []
        def setup():
            scale_to(load_config, 1)
        def result():
            results.append(scale_to(deployment_config=load_config, pod_count=0))
        benchmark.pedantic(result, setup=setup, rounds=3, iterations=1)

        assert all(results) is True