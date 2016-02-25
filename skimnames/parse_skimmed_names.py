#
#  extracts relevant information from skimmed html files
#
#####################################################################

import socket, os

if socket.gethostname() == 'bigArch':
    SKIMM_FOLDER = "/home/dave/workspace/pycharm/fetch/skimmedWorklist/"
else:
    SKIMM_FOLDER = "/media/skimmedWorklist"




def find_html_files(inFolder: str) -> [str]:
    file_list = []
    filename = inFolder + 'worklist.jsp'
    if os.path.isfile(filename):
        file_list.append(filename)
    for x in range(1, 10001):
        filename = inFolder + 'worklist.jsp?page_id=' + str(x)
        if os.path.isfile(filename):
            file_list.append(filename)
    return file_list


htmlfiles = find_html_files(SKIMM_FOLDER)
x=1
