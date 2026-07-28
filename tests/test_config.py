import importlib
import os


def load_config_with_env(env):
    os.environ["APP_ENV"] = env
    import config
    importlib.reload(config)
    return config


def test_dev_config():
    cfg = load_config_with_env("dev")
    assert cfg.DB_PATH == "stocks_dev.db"
    assert cfg.FETCH_INTERVAL_MINUTES == 5


def test_prod_config():
    cfg = load_config_with_env("prod")
    assert cfg.DB_PATH == "stocks.db"
    assert len(cfg.WATCHLIST) == 15


def test_invalid_env_raises():
    os.environ["APP_ENV"] = "nonsense"
    import config
    try:
        importlib.reload(config)
        assert False, "should have raised"
    except ValueError:
        pass
    finally:
        os.environ["APP_ENV"] = "dev"  # reset for other tests
