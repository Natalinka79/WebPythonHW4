import requests
from testpage import OperationHelper
import pytest
import logging
import yaml
import time

with open("testdata.yaml", encoding='utf-8') as f:
    testdata = yaml.safe_load(f)
name = testdata.get("login")
pswd = testdata.get("password")
title = testdata.get("title")
description = testdata.get("description")
content = testdata.get("content")
user = testdata.get("username")
email = testdata.get("user_email")
contact = testdata.get("content_contact")
addr_post = testdata.get("address_post")
url_post = testdata.get("url_post")
not_me_title = testdata.get("not_me_title")

S = requests.Session()


def test_step1(browsser):
    logging.info("Test1 Starting")
    testpage = OperationHelper(browsser)
    testpage.go_to_site()
    testpage.enter_login("test")
    testpage.enter_pass("test")
    testpage.click_login_button()
    assert testpage.get_error_text() == "401", "Test FAILED!"


def test_step2(browsser):
    logging.info("Test2 Starting")
    testpage = OperationHelper(browsser)
    testpage.go_to_site()
    testpage.enter_login(name)
    testpage.enter_pass(pswd)
    testpage.click_login_button()
    assert testpage.get_user_text() == f"Hello, {name}", "Test FAILED!"


def test_step3(browsser):
    logging.info("Test3 Stsrting")
    testpage = OperationHelper(browsser)
    testpage.click_new_post_btn()
    testpage.enter_title(title)
    testpage.enter_description(description)
    testpage.enter_content(content)
    testpage.click_save_btn()
    time.sleep(3)
    assert testpage.get_res_text() == title, "Test FAILED!"


def test_step4(browsser):
    # test contact us
    logging.info("Test Contact_us Starting")
    testpage = OperationHelper(browsser)
    testpage.click_contact_link()
    testpage.enter_contact_name(user)
    testpage.enter_contact_email(email)
    testpage.enter_contact_content(contact)
    testpage.click_contact_send_btn()
    assert testpage.get_allert_message() == "Form successfully submitted", "Test FAILED!"


def test_step5(login):
    logging.info("Test check not me post started")
    res = S.get(url=url_post, headers={'X-Auth-Token': login}, params={'owner': 'notMe'}).json()['data']
    logging.debug(f"get request return: {res}")
    result_title = [i['title'] for i in res]
    assert not_me_title in result_title, 'Пост с заданным заголовком не найден'
    """assert str(not_me_title) in result_title, 'Пост с заданным заголовком не найден'"""

def test_step6(login):
    logging.info("Test create post started")
    url=addr_post
    headers={'X-Auth-Token': login}
    d={'title': title,
       'description': description,
       'content': content
       }
    res = S.post(url, headers=headers, data=d)
    logging.debug(f"Response is {str(res)}")
    assert str(res) == '<Response [200]>', "Новый пост не создан"


def test_step7(login, get_description):
    logging.info("Test check description started")
    url = url_post
    headers = {'X-Auth-Token': login}
    data_json = S.get(url=url, headers=headers).json()['data']
    logging.debug(f"get request return: {data_json}")
    res = [i['description'] for i in data_json]
    assert get_description in res, 'test_step7 FAIL'


def test_send_email(email_sender):
    assert email_sender['To'] == 'Natalinka.79@mail.ru'


if __name__ == "__main__":
    pytest.main(["-vv"])