from flask import Blueprint, jsonify, request, session
from sqlOperations import get_native_contests,get_native_contest_details,updateProblemStatus,getProblemStatus
from apis import submit_code

nativeContest = Blueprint('nativeContest', __name__)


@nativeContest.route("/getContests")
def getContests():
    return jsonify({"data": get_native_contests()})


@nativeContest.route("/getContestName")
def getContestName():
    return jsonify({"data" : get_native_contest_details()[0][0] })


@nativeContest.route("/submit", methods=["POST"])
def submit():

    data = request.get_json()
    code = data["code"]
    lang = data["lang"]
    prob = data["prob"]
    verdict = submit_code(code,lang,prob)
    if session.get('user',None) is None:
        return jsonify({"data" : 'PLease Log In', "Status" : [0,0,0,0]})
    if verdict == 'AC':
        result = updateProblemStatus(prob, True, session["user"])
    else:
        result = updateProblemStatus(prob, False, session["user"])
    return jsonify({"data": verdict, "Status": result})

@nativeContest.route('/status')
def status():
    if session.get('user',None) is None:
        return jsonify({"data" : 'PLease Log In', "Status" : [0,0,0,0]})
    return jsonify({"data" : getProblemStatus(session["user"])})
