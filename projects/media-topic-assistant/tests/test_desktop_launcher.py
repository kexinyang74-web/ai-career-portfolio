from unittest.mock import Mock

import pytest

import launch_desktop as launcher


def test_running_service_opens_browser_without_spawning(tmp_path, monkeypatch):
    monkeypatch.setattr(launcher, 'ready', lambda: True)
    spawn = Mock()
    browser = Mock()
    monkeypatch.setattr(launcher, 'spawn_service', spawn)
    monkeypatch.setattr(launcher.webbrowser, 'open', browser)
    launcher.launch(tmp_path)
    spawn.assert_not_called()
    browser.assert_called_once_with(launcher.URL)


def test_cold_start_waits_for_ready_before_browser(tmp_path, monkeypatch):
    readiness = iter([False, False, True])
    monkeypatch.setattr(launcher, 'ready', lambda: next(readiness))
    monkeypatch.setattr(launcher, 'port_busy', lambda: False)
    process = Mock()
    process.poll.return_value = None
    spawn, browser = Mock(return_value=process), Mock()
    monkeypatch.setattr(launcher, 'spawn_service', spawn)
    monkeypatch.setattr(launcher.webbrowser, 'open', browser)
    monkeypatch.setattr(launcher.time, 'sleep', lambda seconds: None)
    launcher.launch(tmp_path)
    spawn.assert_called_once_with(tmp_path)
    browser.assert_called_once_with(launcher.URL)


def test_occupied_port_does_not_stop_or_start_anything(tmp_path, monkeypatch):
    monkeypatch.setattr(launcher, 'ready', lambda: False)
    monkeypatch.setattr(launcher, 'port_busy', lambda: True)
    spawn = Mock()
    monkeypatch.setattr(launcher, 'spawn_service', spawn)
    with pytest.raises(RuntimeError, match='8765'):
        launcher.launch(tmp_path)
    spawn.assert_not_called()


def test_failed_start_does_not_open_browser(tmp_path, monkeypatch):
    monkeypatch.setattr(launcher, 'ready', lambda: False)
    monkeypatch.setattr(launcher, 'port_busy', lambda: False)
    process = Mock()
    process.poll.return_value = 1
    monkeypatch.setattr(launcher, 'spawn_service', Mock(return_value=process))
    browser = Mock()
    monkeypatch.setattr(launcher.webbrowser, 'open', browser)
    with pytest.raises(RuntimeError, match='日志'):
        launcher.launch(tmp_path)
    browser.assert_not_called()
