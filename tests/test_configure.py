import datetime
import sys
from unittest import mock

import pytest

import freezegun
import freezegun.config


def setup_function():
    freezegun.config.reset_config()


def teardown_function():
    freezegun.config.reset_config()


def test_default_ignore_list_is_overridden():
    freezegun.configure(default_ignore_list=['threading', 'tensorflow'])

    with mock.patch("freezegun.api._freeze_time.__init__", return_value=None) as _freeze_time_init_mock:

        freezegun.freeze_time("2020-10-06")

        expected_ignore_list = [
            'threading',
            'tensorflow',
        ]

        _freeze_time_init_mock.assert_called_once_with(
            time_to_freeze_str="2020-10-06",
            tz_offset=0,
            ignore=expected_ignore_list,
            tick=False,
            as_arg=False,
            as_kwarg='',
            auto_tick_seconds=0,
            real_asyncio=False,
        )

def test_extend_default_ignore_list():
    freezegun.configure(extend_ignore_list=['tensorflow'])

    with mock.patch("freezegun.api._freeze_time.__init__", return_value=None) as _freeze_time_init_mock:

        freezegun.freeze_time("2020-10-06")

        expected_ignore_list = [
            'nose.plugins',
            'six.moves',
            'django.utils.six.moves',
            'google.gax',
            'threading',
            'multiprocessing',
            'queue',
            'selenium',
            '_pytest.terminal.',
            '_pytest.runner.',
            'gi',
            'prompt_toolkit',
            'tensorflow',
        ]

        _freeze_time_init_mock.assert_called_once_with(
            time_to_freeze_str="2020-10-06",
            tz_offset=0,
            ignore=expected_ignore_list,
            tick=False,
            as_arg=False,
            as_kwarg='',
            auto_tick_seconds=0,
            real_asyncio=False,
        )

def test_extend_default_ignore_list_duplicate_items():
    freezegun.configure(extend_ignore_list=['tensorflow', 'pymongo', 'tensorflow','rabbitmq'])
    freezegun.configure(extend_ignore_list=['tensorflow'])

    with mock.patch("freezegun.api._freeze_time.__init__", return_value=None) as _freeze_time_init_mock:

        freezegun.freeze_time("2020-10-06")

        expected_ignore_list = [
            'nose.plugins',
            'six.moves',
            'django.utils.six.moves',
            'google.gax',
            'threading',
            'multiprocessing',
            'queue',
            'selenium',
            '_pytest.terminal.',
            '_pytest.runner.',
            'gi',
            'prompt_toolkit',
            'tensorflow',
            'pymongo',
            'rabbitmq',
        ]

        _freeze_time_init_mock.assert_called_once_with(
            time_to_freeze_str="2020-10-06",
            tz_offset=0,
            ignore=expected_ignore_list,
            tick=False,
            as_arg=False,
            as_kwarg='',
            auto_tick_seconds=0,
            real_asyncio=False,
        )

FROZEN_DATETIME = datetime.datetime(2020, 2, 29, 0, 0, 0, tzinfo=datetime.timezone.utc)
current = datetime.datetime.now(datetime.timezone.utc)

@pytest.fixture
def fixture_fake_module_ignored():
    """Fixture yielding time by ignoring the module"""
    from . import another_module
    with freezegun.freeze_time(FROZEN_DATETIME, ignore=["tests.another_module"]) as freezer:
        assert another_module.get_fake_gmtime()().tm_year == current.year
        assert another_module.get_fake_datetime().now().year == current.year
        yield freezer
        assert another_module.get_fake_gmtime()().tm_year == current.year
        assert another_module.get_fake_datetime().now().year == current.year
    if "tests.another_module" in sys.modules:
        del sys.modules["tests.another_module"]


def test_fixture_fake_module_ignored(fixture_fake_module_ignored):
    from . import another_module
    assert another_module.get_fake_gmtime()().tm_year == current.year
    assert another_module.get_fake_datetime().year == current.year
    if "tests.another_module" in sys.modules:
        del sys.modules["tests.another_module"]


@pytest.fixture
def fixture_fake_module_not_ignored():
    """Fixture yielding time without ignoring the module"""
    from . import another_module
    with freezegun.freeze_time(FROZEN_DATETIME) as freezer:
        assert another_module.get_fake_gmtime()().tm_year == FROZEN_DATETIME.year
        assert another_module.get_fake_datetime().now().year == FROZEN_DATETIME.year
        yield freezer
        assert another_module.get_fake_gmtime()().tm_year == FROZEN_DATETIME.year
        assert another_module.get_fake_datetime().now().year == FROZEN_DATETIME.year
    if "tests.another_module" in sys.modules:
        del sys.modules["tests.another_module"]


def test_fakedatetime_is_not_ignored(fixture_fake_module_not_ignored):
    from . import another_module
    assert another_module.gmtime().tm_year == FROZEN_DATETIME.year
    assert another_module.datetime.now().year == FROZEN_DATETIME.year
    if "tests.another_module" in sys.modules:
        del sys.modules["tests.another_module"]




