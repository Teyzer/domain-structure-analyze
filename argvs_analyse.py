import getopt
import sys

errors = [("opt-crash", "GetOpt crashed while reading options, you may have forgot to fill an option"),
          ("miss -w", "Error with the -w argument"),
          ("miss args", "You're missing the following arguments : {}"),
          ("", "Unable to get from where the error come from")]

needed_arguments = ["-t"]


def reply_usage(why="", to_format=None):
    print("[!] Correct usage: python explorer.py -t <target_url> [-m <max_entries] [--explore-all] [--only-domain]")
    for error_id, error in errors:
        if error_id == why:
            if to_format is None:
                print("↳ {0}".format(error))
            else:
                print("↳ {0}".format(error.format(str(to_format))))
    return False


def get_opts(argv):
    toRet = {}
    try:
        opts, args = getopt.getopt(argv[1:], "t:m:h", ["explore-all", "only-domain"])
    except getopt.GetoptError:
        return reply_usage("opt-crash")
    for opt, arg in opts:
        if opt == "-h":
            return_help()
            sys.exit()
    for opt, arg in opts:
        if opt in needed_arguments:
            needed_arguments.remove(opt)
        toRet.update({opt: arg})
    if len(needed_arguments) > 0:
        reply_usage("miss args", to_format=needed_arguments)
    return toRet


def return_help():
    print("  Help / Usage")
    print(" -t <target_url> : Specify the starting url ( required )")
    print(" -m <max> : Specify the max number of page to visit ( optional )")
    print(" --explore-all : If you want to explore not same-origin domain as well ( optional )")
    print("                 If used, please specify a maximum too, if not the thread will be infinite")
    print(" --only-domain : If you want to visit only the homepage of each domain ( optional )")
