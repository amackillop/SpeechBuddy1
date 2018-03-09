import json

res = '''{"Transcript": "my problem has been resolved thanks to colleague Brian call at text up the problem is that before the PIP I try to install Google Cloud manually by downloading the source and running setup talk to you why","Confidence": 0.931040287018,"Words": [["my", 0.0, 1.2],["problem", 1.2, 1.7],["has", 1.7, 1.9],["been", 1.9, 2.0],["resolved", 2.0, 2.6],["thanks", 2.6, 3.0],["to", 3.0, 3.2],["colleague", 3.2, 3.7],["Brian", 3.7, 4.1],["call", 4.1, 4.5],["at", 4.5, 4.9],["text", 4.9, 5.4],["up", 5.4, 5.6],["the", 5.6, 6.7],["problem", 6.7, 7.0],["is", 7.0, 7.6],["that", 7.6, 8.2],["before", 8.2, 8.6],["the", 8.6, 9.1],["PIP", 9.1, 9.4],["I", 9.4, 10.1],["try", 10.1, 10.6],["to", 10.6, 10.9],["install", 10.9, 11.1],["Google", 11.1, 11.6],	["Cloud", 11.6, 12.0],["manually", 12.0, 12.7],["by", 12.7, 12.9],["downloading", 12.9, 13.5],["the", 13.5, 13.7],["source", 13.7, 14.1],	["and", 14.1, 14.3],["running", 14.3, 14.8],["setup", 14.8, 15.8],["talk", 15.8, 16.1],	["to", 16.1, 16.2], ["you", 16.2, 16.3],["why", 16.3, 16.5]]}'''


def wpmCall(StrData):
    jsData = json.dumps(StrData)
    print(jsData)

wpmCall(res)