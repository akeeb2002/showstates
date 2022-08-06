import webbrowser
import os
import pymysql
import requests
from bs4 import BeautifulSoup


TAG_DOCTYPE = '<!DOCTYPE html>'
TAG_HTML = 'html'
TAG_HEAD = 'head'
TAG_BODY = 'body'
TAG_TABLE = 'table'
TAG_TH = 'th'
TAG_TD = 'td'
TAG_TR = 'tr'
TAG_PAR = 'p'
TAG_H1 = 'h1'
TAG_BR = 'br'
TAG_LINK = 'link'
TAG_A = 'a'


def read_password():
    with open("password.txt") as file:
        password = file.read().strip()
    return password


def connect_to_DB():
    password = read_password()
    conn = pymysql.connect(host="mars.cs.qc.cuny.edu", port=3306, user="", passwd=password, database="")
    # cursor = conn.cursor()
    # cursor.execute("SHOW DATABASES")
    # for row in cursor:
    #     print(row)
    return conn

def create_element(tag, content, attributes="", end_tag=True):
    element = "<" + tag + " " + attributes + ">"
    if end_tag:
        element += content + "</" + tag + ">"
    return element + "\n"


def create_elements(tag, list_contents):
    elements = ""
    for content in list_contents:
        elements += create_element(tag, content)
    return elements


def create_table(headers, data):
    rows = create_elements(TAG_TH, headers)
    for datum in data:
        name = datum[0]
        href = 'href="https://en.wikipedia.org/wiki/' + name.replace(" ", "_") + '_(state)' + '"'
        a = create_element(TAG_A, name, href, True)
        tda = create_element(TAG_TD, a)
        tds = create_elements(TAG_TD, datum[1:])
        row = create_element(TAG_TR, tda + tds)
        rows += row
    table = create_element(TAG_TABLE, rows)
    return table


def open_file_in_browser(file_name):
    url = 'file:///' + os.getcwd() + '/' + file_name
    webbrowser.open_new_tab(url)


def get_state_data():
    conn = connect_to_DB()
    cursor = conn.cursor()
    query = "SELECT * FROM state ORDER BY state_name"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return rows


def write_file(file_name, message):
    f = open(file_name, 'w')
    f.write(message)
    f.close()


def main():
    states = get_state_data()
    headers = ["State", "Abbreviation", "Capital"]
    table = create_table(headers, states)
    heading = create_element(TAG_H1, "Akeeb's United States")
    link_attributes = 'rel="stylesheet" href="myStyle.css"'
    link = create_element(TAG_LINK, "", link_attributes, end_tag=False)
    head = create_element(TAG_HEAD, link)
    body = create_element(TAG_BODY, heading + table)
    message = create_element(TAG_HTML, head + body)
    write_file("../assignment3/states.html", message)
    open_file_in_browser("../assignment3/states.html")


if __name__ == "__main__":
    main()
