import sys
import argvs_analyse as arg_ana
import wbanalyze as wb
import loginfo


if __name__ == "__main__":
    print('\r')

    # Default values
    explore_sub_domain = True  # --only-domain -> False
    stay_on_domain = True  # --explore-all -> False
    max_in = None  # -m -> max

    # Be sure options are well filled
    opts = arg_ana.get_opts(sys.argv)
    if not opts:
        sys.exit()

    # use options
    start_url = opts.get("-t")
    if "-m" in opts:
        if wb.represent_int(opts.get("-m")):
            max_in = int(opts.get("-m"))
        else:
            loginfo.error("Please enter a number for -m")
            sys.exit()
    if "--only-domain" in opts:
        explore_sub_domain = False
    if "--explore-all" in opts:
        stay_on_domain = False

    # verify url format
    if not wb.verify_url(start_url):
        loginfo.error("The URL is not in the good format")
        sys.exit()

    # start analyzing
    wb.analyze_web_page(start_url, stay_on_domain=stay_on_domain,
                        explore_sub_domains=explore_sub_domain,
                        max_results=max_in)