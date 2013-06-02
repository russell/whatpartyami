#!/usr/bin/python
import os
import sys
from lxml import etree
from datetime import date
from collections import defaultdict
import json

start_date = date(2010, 1, 1)

PARTIES = {"AG": "Australian Greens",
           "ALP": "Australian Labor Party",
           "AUS": "Austraila Party",
           "CLP": "National Party",
           "Ind.": "Independent",
           "LP": "Liberal Party",
           "Nats": "National Party"}

VOTE_PARTY = {
    "CWM": "Liberal Party",
    "Country Liberal Party": "Liberal Party",
}


KEYWORDS = [
    ("I believe the government should improve the public heath system.", ["health"]),
    ("I am concerned about my Superannuation.", ["superannuation"]),
    ("I am concerned about climate change.", ["clean energy", "carbon", "climate change", "ozone", "renewable energy"]),
    ("I think the government should increased taxes on non-renewable resource based companies.", ["minerals", "petroleum"]),
    ("I believe in same sex marriage.", ["marriage"]),
    ("I am concerned about the number of asylum seekers.", ["asylum", "migration"])
]

COUNT = defaultdict(dict)


def load_members(file):
    members = json.load(open(file))
    d = {}
    for member in members:
        name = member["lastname"] + ", " + member["firstname"][0]
        party = member["party"]

        if member["party"] == "SPK":
            continue

        from_date = date(*map(int, member["fromdate"].split("-")))
        if from_date < start_date and member["towhy"] not in ["still_in_office"]:
            continue

        if member["towhy"] in ["retired", "defeated", "elected_elsewhere"]:
            continue

        if d.get(name) == member["party"]:
            continue  # skip people with the same name and party

        if member["party"] in VOTE_PARTY:
            party = VOTE_PARTY[member["party"]]
        assert name not in d
        d[name] = party
    d["Burke, A"] = "Liberal Party"
    d['Katter, B'] = 'Australia Party'
    return d


def find_question(text):
    text = " ".join(text)
    for question, keys in KEYWORDS:
        for key in keys:
            if key in text.lower():
                return question


def find_debate(tag):
    while True:
        if tag.tag == "debate":
                return tag
        tag = tag.getparent()


def clean_up_titles(titles):
    return [title.strip() for title in titles.split(",")]


def get_members(names):
    ret = defaultdict(int)
    for member in names:
        name = member.text.strip()
        first_initial = name.find(",") + 3
        name = name[:first_initial]
        try:
            name = MEMBERS[name]
        except KeyError:
            # if there is an error in the data set, then guess
            # print "Name error found %s" % name
            name = [MEMBERS[m] for m in MEMBERS if m.startswith(m[:-2])][0]
        ret[name] += 1
    return ret


def get_bill_titles(debate):
    return [clean_up_titles(e.text)
            for e in debate.xpath(".//subdebateinfo/title")][0]


def get_bill_description(debate):
    desc = debate.xpath(".//subdebateinfo")[0].getparent()
    desc = desc.getparent().xpath(".//speech")[0]
    talk = desc.xpath("./talk.text/body")[0]
    speaker = desc.xpath("./talk.start/talker/name")[0].text.strip()
    party = desc.xpath("./talk.start/talker/party")[0].text.strip()
    return speaker, party, etree.tostring(talk, pretty_print=True)


def get_speach(debate):
    debate.xpath("./subdebate.1[1]/speech")


def parse_debates(file):
    root = etree.parse(file)
    divisions = root.xpath("//division.data")

    debates = zip(map(find_debate, divisions), divisions)
    result = []
    for debate, division in debates:
        titles = get_bill_titles(debate)
        speaker, party, description = get_bill_description(debate)
        ayes = get_members(division.xpath("./ayes//name"))
        noes = get_members(division.xpath("./noes//name"))
        pairs = get_members(division.xpath("./pairs//name"))
        question = find_question(titles)
        result.append({"titles": titles,
                       "speaker": speaker,
                       "party": PARTIES[party],
                       "ayes": ayes,
                       "question": question,
                       "noes": noes, "pairs": pairs,
                       "description": description})
    return result

counted = 0


def count_votes(discussion):
    if not discussion["question"]:
        return
    global COUNT
    global counted
    counted += 1
    Q = COUNT[discussion["question"]]
    Q["votes"] = Q.get("votes", {})
    votes = Q["votes"]
    votes["aye"] = votes.get("aye", {})
    votes["nay"] = votes.get("nay", {})
    for party, count in discussion["ayes"].items():
        votes["aye"][party] = count + votes["aye"].get(party, 0)
    for party, count in discussion["noes"].items():
        votes["nay"][party] = count + votes["nay"].get(party, 0)
    votes["aye"]


if __name__ == "__main__":
    filenames = os.listdir("data")
    global MEMBERS
    MEMBERS = load_members("representatives.json")

    for filename in filenames:
        filename = "data/" + filename.split("/")[-1]
        # filename = sys.argv[1]
        out_filename = filename.split(".")[0] + ".json"
        out_filename = "json/" + out_filename.split("/")[-1]
        print filename
        try:
            parsed_data = parse_debates(filename)
        except:
            with open("errors.txt", "a") as myfile:
                myfile.write("%s\n" % filename)

        json.dump(parsed_data, open(out_filename, "w"), indent=5)
        for discussion in parsed_data:
            count_votes(discussion)

        result = []
        for q, votes in COUNT.items():
            parties = defaultdict(lambda: (0, 0))
            for party, count in votes["votes"]["aye"].items():
                y, n = parties[party]
                parties[party] = count + y, n
            for party, count in votes["votes"]["nay"].items():
                y, n = parties[party]
                parties[party] = y, count + n
            result.append({"q": q, "votes": parties})
    json.dump(result, open("output.json", "w"))
    print counted
    # Write file
