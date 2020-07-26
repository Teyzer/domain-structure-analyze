all_start = "Analyze started at {0}"
starter_string = "{0} Found {1} pages on same domain, {2} pages on other domain, {3} phone number, {4} mails on {5}"
formatter_string = "Found {0} new same domain pages, {1} new other domains, {2} new nums, {3} new mails on given url"
summarize = "Current stats : {0} same domain pages, {1} other domain, {2} phone numbers, {3} emails"
finished_domain_start = " Finished reading pages of {0} with a total of {1} pages!"


def error(string):
    print("[!] {0}".format(string))


def success(string):
    print("[+] {}".format(string))


def info(string):
    print("[-] {}".format(string))


def success_sum(string):
    print("[+] ------------------------------------------------------------- ")
    print("[+] {}".format(string))
    print("[+] ------------------------------------------------------------- ")


def info_sum(string):
    print("[-] ------------------------------------------------------------- ")
    print("[-]")
    print("[-] {}".format(string))
    print("[-]")
    print("[-] ------------------------------------------------------------- ")