import logging
import unittest
import env
from helpers.api import API


#
# def intercept_request(route, request):
#     if request.url == "http://10.99.13.117":
#         route.continue_()
#     else:
#         # route.fulfill(body="Intercepted!")
#         route.continue_()
#
#
# def test_api(story_page):
#     story_page.navigate()
#     story_page.timeout()
#     base_url = f"http://{.env.ip}"
#     response, status = API().get(f'{base_url}/api/v1/search?advisories=false')
#     assert status == 200, "Unable to fetch the Playout information"
#     playout_info = response
#     logging.info(playout_info)


def test_FTPS_distribution_UI(story_page):
    story_page.navigate()
    story_page.hamburger.click()
    story_page.file_distributor_icon.click()
    story_page.add_new_FD.first.click()
    story_page.FD_name.fill("CS")
    story_page.SD.first.click()  # SD
    story_page.HD.first.click()
    story_page.script.first.click()
    story_page.protocol_method.last.click()
    story_page.timeout()
    story_page.ftps_distribution()
    story_page.navigate()
    for i in range(1, 4):
        story_page.add_to_distributor.nth(i).click()
        story_page.page.wait_for_timeout(3000)
    story_page.page.locator('//ul[@class = "tab vertical"]//li[5]').click()
    story_page.page.locator('//ul[@class = "tab horizontal inpage no-print"]//li[2]').click()
    story_page.timeout()
    story_page.navigate()
    story_page.hamburger.click()
    story_page.file_distributor_icon.click()
    story_page.add_new_FD.first.click()
    story_page.FD_name.fill("CS")
    story_page.SD.first.click()  # SD
    story_page.HD.first.click()
    story_page.script.first.click()
    story_page.protocol_method.last.click()
    story_page.timeout()
    story_page.ftps_distribution()
    story_page.timeout()


def test_FTPS_existing_name(story_page):
    story_page.navigate()
    story_page.hamburger.click()
    story_page.file_distributor_icon.click()
    story_page.add_new_FD.first.click()
    story_page.FD_name.fill("CS")
    story_page.SD.first.click()  # SD
    story_page.HD.first.click()
    story_page.script.first.click()
    story_page.protocol_method.last.click()
    story_page.timeout()
    story_page.ftps_distribution()
    story_page.page.wait_for_timeout(6000)
    story_page.navigate()
    for i in range(1, 4):
        story_page.add_to_distributor.nth(i).click()
        story_page.page.wait_for_timeout(3000)
    story_page.page.locator('//ul[@class = "tab vertical"]//li[5]').click()
    story_page.page.locator('//ul[@class = "tab horizontal inpage no-print"]//li[2]').click()
    story_page.timeout()
    story_page.navigate()


def test_FTPS_existing(story_page):
    story_page.navigate()
    story_page.hamburger.click()
    story_page.file_distributor_icon.click()
    story_page.page.wait_for_timeout(6000)
    story_page.add_new_FD.first.click()
    story_page.FD_name.fill("CS")
    story_page.SD.first.click()  # SD
    story_page.HD.first.click()
    story_page.script.first.click()
    story_page.protocol_method.last.click()
    story_page.timeout()
    story_page.ftps_distribution()
    story_page.page.wait_for_timeout(6000)
    story_page.navigate()
    for i in range(1, 4):
        story_page.add_to_distributor.nth(i).click()
        story_page.page.wait_for_timeout(3000)
    story_page.page.locator('//ul[@class = "tab vertical"]//li[5]').click()
    story_page.page.locator('//ul[@class = "tab horizontal inpage no-print"]//li[2]').click()
    story_page.timeout()
    story_page.navigate()


#

# @then(parsers.parse("Check if we can play a {source} file on sdi 2"))
# def test_play_live(source, live_page):
#     live_page.navigate()
#     live_page.event_rows.first.click()
#     live_page.page.wait_for_timeout(3000)
#     live_page.event_rows.first.click()
#     live_page.page.wait_for_timeout(3000)
#     text = live_page.event_rows.first.text_content()
#     live_page.playout_now_button.click()
#     live_page.page.wait_for_timeout(3000)
#     live_page.petal_two.click()
#     live_page.page.wait_for_timeout(20000)
#     base_url = f"http://{.env.ip}"
#     response, status = API().get(f'{base_url}/api/v1/playout/now')
#     assert status == 200, "Unable to fetch the Playout information"
#     playout_info = response
#     logging.info(playout_info)
