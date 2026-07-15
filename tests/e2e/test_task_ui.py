"""End-to-end browser tests for the Task Tracker web UI."""

from playwright.sync_api import Page, expect


def test_page_loads_with_heading(page: Page, base_url):
    page.goto(base_url)
    expect(page.get_by_role("heading", name="Task Tracker")).to_be_visible()


def test_empty_state_shown_when_no_tasks(page: Page, base_url):
    page.goto(base_url)
    expect(page.get_by_test_id("empty-state")).to_be_visible()
    expect(page.get_by_test_id("task-item")).to_have_count(0)


def test_create_task_appears_in_list(page: Page, base_url):
    page.goto(base_url)
    page.get_by_test_id("title-input").fill("Buy milk")
    page.get_by_test_id("description-input").fill("2% organic")
    page.get_by_test_id("add-button").click()

    task_list = page.get_by_test_id("task-list")
    expect(task_list).to_contain_text("Buy milk")
    expect(task_list).to_contain_text("2% organic")
    expect(page.get_by_test_id("empty-state")).to_be_hidden()


def test_create_task_requires_title(page: Page, base_url):
    page.goto(base_url)
    page.get_by_test_id("add-button").click()
    # HTML5 required validation blocks submission, so no task is added.
    expect(page.get_by_test_id("task-item")).to_have_count(0)
    expect(page.get_by_test_id("empty-state")).to_be_visible()
