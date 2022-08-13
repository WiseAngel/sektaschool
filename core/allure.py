import allure
from allure_commons import types


def step(title):
    return allure.step(title)


def suite(suite_name):
    return allure.suite(suite_name)


def sub_suite(sub_suite_name):
    return allure.sub_suite(sub_suite_name)


def title(test_title):
    return allure.title(test_title)


def description(test_description):
    return allure.description(test_description)


def description_html(test_description_html):
    return allure.description_html(test_description_html)


def label(label_type, *labels):
    return allure.label(label_type, *labels)


def severity(severity_level):
    return allure.severity(severity_level)


def epic(*epics):
    return allure.epic(*epics)


def story(*stories):
    return allure.story(*stories)


def feature(*features):
    return allure.feature(*features)


def parent_suite(parent_suite_name):
    return allure.parent_suite(parent_suite_name)


def tag(*tags):
    return allure.tag(*tags)


def id(ident):
    return allure.id(ident)


def link(url, link_type=types.LinkType.LINK, name=None):
    return allure.link(url, link_type, name)


def issue(url, name=None):
    return allure.issue(url, name)


def owner(owner):
    return allure.label("owner", owner)


def testcase(url, name):
    return allure.testcase(url, name)


class Attach(object):

    def __call__(self, body, name=None, attachment_type=None, extension=None):
        allure.attach(body=body, name=name, attachment_type=attachment_type, extension=extension)

    def file(self, source, name=None, attachment_type=None, extension=None):
        allure.attach.file(source=source, name=name, attachment_type=attachment_type,
                           extension=extension)


attach = Attach()


class Dynamic(object):

    @staticmethod
    def title(test_title):
        allure.dynamic.title(test_title)

    @staticmethod
    def description(test_description):
        allure.dynamic.description(test_description)

    @staticmethod
    def description_html(test_description_html):
        allure.dynamic.description_html(test_description_html)

    @staticmethod
    def label(label_type, *labels):
        allure.dynamic.label(label_type, *labels)

    @staticmethod
    def severity(severity_level):
        allure.dynamic.severity(severity_level)

    @staticmethod
    def feature(*features):
        allure.dynamic.feature(*features)

    @staticmethod
    def story(*stories):
        allure.dynamic.story(*stories)

    @staticmethod
    def tag(*tags):
        allure.dynamic.tag(*tags)

    @staticmethod
    def link(url, link_type=types.LinkType.LINK, name=None):
        allure.dynamic.link(url, link_type, name)

    @staticmethod
    def issue(url, name=None):
        allure.dynamic.issue(url, name)

    @staticmethod
    def testcase(url, name=None):
        allure.dynamic.testcase(url, name)

    @staticmethod
    def suite(suite_name):
        allure.dynamic.suite(suite_name)

    @staticmethod
    def parent_suite(parent_suite_name):
        allure.dynamic.parent_suite(parent_suite_name)

    @staticmethod
    def sub_suite(sub_suite_name):
        allure.dynamic.sub_suite(sub_suite_name)
