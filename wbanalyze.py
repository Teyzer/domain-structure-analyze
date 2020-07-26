import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import loginfo
import sys
import re

data = {
    "web_page": {
        "origin_domain": {
            "visited": [],
            "awaiting": [],
            "forbidden": [],
            "list": []
        },
        "other_domain": {
            "visited": [],
            "awaiting": [],
            "forbidden": [],
            "no_response": [],
            "list": []
        },
    },
    "tel": [],
    "mail": []
}

regex_mail = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
forbidden_end_file = [".jpg", ".png", ".pdf", ".gif", ".svg", ".zip", ".rar", ".torrent"]

tree_chars = ["└", "├", "─", "│"]


def represent_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def tree(array, characters_space=3):
    print("")
    loginfo.success("Rendering tree of the website")
    adder = "───"
    array.sort()
    for _element in array:
        usable = format_for_tree(_element)
        length = len(usable.split("/"))
        if _element == array[0]:
            print(usable)
            continue
        if _element != array[-1]:
            start_string = "├"
        else:
            start_string = "└"
        for part in usable.split("/"):
            if part == "":
                continue
            start_string += adder + " " + part + "/ "
        print(start_string)


def verify_url(url):
    obj = urlparse(url)
    if obj.scheme == "":
        return False

    net_loc = obj.netloc
    if net_loc == "" or len(net_loc.split('.')) < 2:
        return False
    if len(net_loc.split('.')[-1]) < 2 or len(net_loc.split('.')[-1]) > 5:
        return False

    return True


def verify_mail_format(mail):
    if re.search(regex_mail, mail):
        return True
    else:
        return False


def format_for_tree(url):
    if not url.endswith("/"):
        url += "/"
    parse = urlparse(url)
    if parse.path == "/":
        return parse.netloc + parse.path
    else:
        return parse.path[1:]


def formatted_count(count, characters_left=5):
    length = len(str(count))
    to_add = characters_left - length
    return "(" + str(count) + ")" + " " * to_add


def find_all(string, search):
    found_index = []
    for x in range(len(string)):
        index = string.find(search)
        if index == -1:
            return found_index
        found_index.append((index + len(found_index)))
        string = string[:index] + string[(index + 1):]
    return found_index


def find_domain_type(url):
    web_page = data["web_page"]
    if url in web_page["origin_domain"]["awaiting"]:
        return "origin_domain"
    elif url in web_page["other_domain"]["awaiting"]:
        return "other_domain"
    return None


def set_url_visited(url, domain_type=None):
    if domain_type not in ["origin_domain", "other_domain"]:
        domain_type = find_domain_type(url)
    try:
        domain = data["web_page"][domain_type]
        domain["awaiting"].remove(url)
        domain["visited"].append(url)
        return True
    finally:
        return False


def is_in_data(element):
    for element_type_key in data:
        element_type = data[element_type_key]
        if element in element_type:
            return True
        for domain_key in element_type:
            if "domain" not in domain_key:
                continue
            domain = element_type[domain_key]
            for website_key in domain:
                websites = domain[website_key]
                if element in websites:
                    return True
    return False


def fetch_url_content(url):
    try:
        r = requests.get(url)
        return r.content
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        loginfo.error("Cannot connect to url {0} ERR:{1}".format(url, e))
    return False


def find_elements(content, url, pre_link):
    elements_found = {"web": [], "tel": [], "mail": []}
    if "href=" in content:
        link_pos = content.find("href=") + 6
        splitter = content[link_pos - 1]
        if content[link_pos] != "#" and content[link_pos] != splitter:
            after_link = content[link_pos:].split(splitter)[0]
            if content[link_pos:link_pos + 4] == "tel:":
                num_string = content[(link_pos + 4):]
                num = num_string.split(splitter)[0]
                elements_found["tel"].append(num)
            elif content[link_pos:link_pos + 7] == "mailto:":
                mail_string = content[(link_pos + 7):]
                mail = mail_string.split(splitter)[0]
                elements_found["mail"].append(mail)
            elif after_link.startswith("http://") or after_link.startswith("https://"):
                if urlparse(pre_link).netloc != urlparse(after_link).netloc:
                    elements_found["web"].append("{0}://{1}".format(urlparse(after_link).scheme, urlparse(after_link).netloc))
                else:
                    elements_found["web"].append(after_link)
            elif urlparse(url).netloc == urlparse(pre_link).netloc:
                if not urlparse(after_link).path.startswith("/"):
                    after_link = "/" + after_link
                elements_found["web"].append("{0}://{1}{2}".format(urlparse(pre_link).scheme, urlparse(pre_link).netloc, urlparse(after_link).path))
    if "@" in content:
        positions = find_all(content, "@")
        for position in positions:
            index, past_break = 0, 0
            while True:
                index += 1
                character = content[position - index]
                if character == " " or character == ">" or character == "\"" or character == "'" or character == ":":
                    past_break = position - index
                    break
            index, after_break = 0, 0
            while True:
                index += 1
                character = content[position + index]
                if character == " " or character == "<" or character == "\"" or character == "'" or character == ":":
                    after_break = position + index
                    break
            mail_str = content[past_break + 1:after_break]
            if verify_mail_format(mail_str):
                elements_found["mail"].append(mail_str)
    return elements_found


def process_elements(array, start_url, stay_on_domain, explore_all_domain):
    added = {"origin_domain": 0, "other_domain": 0, "tel": 0, "mail": 0}
    for key in array:
        for element in array[key]:
            if is_in_data(element):
                continue
            if key == "web":
                if urlparse(element).netloc != urlparse(start_url).netloc:
                    added["other_domain"] += 1
                    for forbidden in forbidden_end_file:
                        if element.endswith(forbidden):
                            data["web_page"]["other_domain"]["forbidden"].append(element)
                            element = None
                            break
                    if element is None:
                        continue
                    if not stay_on_domain:
                        data["web_page"]["other_domain"]["awaiting"].append(element)
                    data["web_page"]["other_domain"]["list"].append(element)
                    continue
                else:
                    added["origin_domain"] += 1
                    for forbidden in forbidden_end_file:
                        if element.endswith(forbidden):
                            data["web_page"]["origin_domain"]["forbidden"].append(element)
                            element = None
                            break
                    if element is None:
                        continue
                    if explore_all_domain:
                        data["web_page"]["origin_domain"]["awaiting"].append(element)
                    data["web_page"]["origin_domain"]["list"].append(element)
                    continue
            elif key == "tel":
                added["tel"] += 1
                data["tel"].append(element)
                continue
            elif key == "mail":
                added["mail"] += 1
                data["mail"].append(element)
                continue
    return added


def get_contents(content, start_url, stay_on_domain, original_url, explore_all_domain):
    keys = ["origin_domain", "other_domain", "tel", "mail"]
    add_round = {"origin_domain": 0, "other_domain": 0, "tel": 0, "mail": 0}
    texts = "a p h1 h2 h3 h4 h5 h6 i b"
    elements = BeautifulSoup(content, features="html.parser")
    for tag in texts.split(" "):
        for element in elements.find_all(tag):
            returned = find_elements(str(element), start_url, pre_link=original_url)
            if returned is None:
                continue
            added = process_elements(returned, start_url, stay_on_domain, explore_all_domain)
            for key in keys:
                add_round[key] += added[key]
    return add_round


def analyze_web_page(url, stay_on_domain=False, explore_sub_domains=False, max_results=None):

    data["web_page"]["origin_domain"]["list"].append(url)
    data["web_page"]["origin_domain"]["awaiting"].append(url)
    loginfo.info(loginfo.all_start.format(url))
    content = fetch_url_content(url)
    get_contents(content, url, stay_on_domain, url, explore_sub_domains)
    set_url_visited(url)

    count = 0
    got_out = 1

    while True:

        count += 1

        web_page = data["web_page"]
        if len(web_page["origin_domain"]["awaiting"]) + len(web_page["other_domain"]["awaiting"]) == 0:
            loginfo.error("Ran out of website to analyze")
            break

        if len(web_page["origin_domain"]["awaiting"]) != 0:
            new_url = web_page["origin_domain"]["awaiting"][0]
        elif len(web_page["other_domain"]["awaiting"]) != 0:
            if got_out == 1:
                loginfo.info_sum(loginfo.finished_domain_start.format(url, str(count - 1)))
                got_out = 0
            new_url = web_page["other_domain"]["awaiting"][0]

        set_url_visited(new_url)
        content = fetch_url_content(new_url)
        if not content:
            continue
        stat = get_contents(content, new_url, stay_on_domain, url, True)
        loginfo.info(loginfo.starter_string.format(formatted_count(count), stat["origin_domain"],
                                                   stat["other_domain"], stat["tel"],
                                                   stat["mail"], new_url))

        if count % 20 == 0:
            loginfo.success_sum(loginfo.summarize.format(len(data["web_page"]["origin_domain"]["list"]),
                                                         len(data["web_page"]["other_domain"]["list"]),
                                                         len(data["tel"]), len(data["mail"]),
                                                         count))

        if max_results is not None:
            if count == max_results:
                break

    if len(data["tel"]) > 0:
        print("")
        loginfo.success("Found following numbers : ")
        for tel in data["tel"]:
            loginfo.info(tel)
    if len(data["mail"]) > 0:
        print("")
        loginfo.success("Found following mails : ")
        for mail in data["mail"]:
            loginfo.info(mail)
    tree(data["web_page"]["origin_domain"]["list"])
