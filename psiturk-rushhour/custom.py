# this file imports custom routes into the experiment server

from flask import Blueprint, render_template, request, jsonify, Response, abort, current_app
from time import time
from jinja2 import TemplateNotFound
from functools import wraps
from sqlalchemy import or_
from random import sample
from collections import namedtuple
import re

from psiturk.psiturk_config import PsiturkConfig
from psiturk.experiment_errors import ExperimentError
from psiturk.user_utils import PsiTurkAuthorization, nocache

# # Database setup
from psiturk.db import db_session, init_db
from psiturk.models import Participant
from json import dumps, loads

# load the configuration options
config = PsiturkConfig()
config.load_config()
myauth = PsiTurkAuthorization(config)  # if you want to add a password protect route use this

# explore the Blueprint
custom_code = Blueprint('custom_code', __name__, template_folder='templates', static_folder='static')

###########################################################
#  Stuff needed for the bonus calculation
###########################################################

"""
For now just paste the line from task.js
"""
puzzle_files = ['static/json/1509723682_71_prb78717_9_.json', 'static/json/1509488743_04_prb21044_9_.json', 'static/json/1509682160_18_prb72425_9_.json', 'static/json/1509728576_32_prb81064_9_.json', 'static/json/1509470807_13_prb13482_9_.json', 'static/json/1509556552_63_prb34405_9_.json', 'static/json/1509721337_05_prb77447_9_.json', 'static/json/1509477339_66_prb17203_9_.json', 'static/json/1509429110_14_prb5142_9_.json', 'static/json/1509566838_88_prb38511_9_.json', 'static/json/1509573002_21_prb41543_9_.json', 'static/json/1509503827_46_prb25973_9_.json', 'static/json/1509463627_74_prb9799_9_.json', 'static/json/1509649678_15_prb63683_9_.json', 'static/json/1509503135_71_prb25705_9_.json', 'static/json/1509420940_67_prb1228_9_.json', 'static/json/1509555412_17_prb33699_9_.json', 'static/json/1509643218_25_prb61959_9_.json', 'static/json/1509574359_43_prb42331_9_.json', 'static/json/1509477123_34_prb17035_9_.json', 'static/json/1509411897_18_prb717_11_.json', 'static/json/1509459257_76_prb7549_11_.json', 'static/json/1509720742_48_prb77111_11_.json', 'static/json/1509576724_28_prb43652_11_.json', 'static/json/1509555428_47_prb33717_11_.json', 'static/json/1509599054_93_prb52317_11_.json', 'static/json/1509491386_49_prb22491_11_.json', 'static/json/1509652414_89_prb65072_11_.json', 'static/json/1509473974_89_prb15412_11_.json', 'static/json/1509557042_37_prb34602_11_.json', 'static/json/1509490191_26_prb21669_11_.json', 'static/json/1509556026_72_prb34092_11_.json', 'static/json/1509429305_0_prb5252_11_.json', 'static/json/1509559246_47_prb35826_11_.json', 'static/json/1509571615_2_prb40909_11_.json', 'static/json/1509423295_78_prb2510_11_.json', 'static/json/1509556433_37_prb34290_11_.json', 'static/json/1509724613_21_prb79216_11_.json', 'static/json/1509422263_59_prb1969_11_.json', 'static/json/1509587855_12_prb48202_11_.json', 'static/json/1509673998_59_prb68514_14_.json', 'static/json/1509488403_92_prb20888_14_.json', 'static/json/1509455375_45_prb6294_14_.json', 'static/json/1509567550_91_prb38725_14_.json', 'static/json/1509419191_31_prb129_14_.json', 'static/json/1509653121_81_prb65535_14_.json', 'static/json/1509463186_98_prb9596_14_.json', 'static/json/1509656597_95_prb66793_14_.json', 'static/json/1509481208_68_prb19356_14_.json', 'static/json/1509502366_25_prb25255_14_.json', 'static/json/1509554623_5_prb33117_14_.json', 'static/json/1509546655_55_prb28956_14_.json', 'static/json/1509479376_37_prb18275_14_.json', 'static/json/1509457858_6_prb6671_14_.json', 'static/json/1509720366_41_prb76929_14_.json', 'static/json/1509468630_51_prb12360_14_.json', 'static/json/1509464540_58_prb10195_14_.json', 'static/json/1509545962_33_prb28697_14_.json', 'static/json/1509472355_7_prb14485_14_.json', 'static/json/1509503629_34_prb25871_14_.json', 'static/json/1509629349_75_prb57223_16_.json', 'static/json/1509565548_04_prb37893_16_.json', 'static/json/1509577648_29_prb44171_16_.json', 'static/json/1509420356_65_prb813_16_.json', 'static/json/1509474295_6_prb15595_16_.json', 'static/json/1509546793_06_prb29027_16_.json', 'static/json/1509508781_01_prb28189_16_.json', 'static/json/1509623373_2_prb55905_16_.json', 'static/json/1509722874_99_prb78361_16_.json', 'static/json/1509556503_33_prb34360_16_.json']; 

puzzle_files=[ j.split('_')[-3] for j in puzzle_files]
num_of_bonus_puzzles=3
total_bonus=9.0
###########################################################
#  serving warm, fresh, & sweet custom, user-provided routes
#  add them here
###########################################################

#----------------------------------------------
# example custom route
#----------------------------------------------
@custom_code.route('/my_custom_view')
def my_custom_view():
	current_app.logger.info("Reached /my_custom_view")  # Print message to server.log for debugging 
	try:
		return render_template('custom.html')
	except TemplateNotFound:
		abort(404)

#----------------------------------------------
# example using HTTP authentication
#----------------------------------------------
@custom_code.route('/my_password_protected_route')
@myauth.requires_auth
def my_password_protected_route():
	try:
		return render_template('custom.html')
	except TemplateNotFound:
		abort(404)

#----------------------------------------------
# example accessing data
#----------------------------------------------
@custom_code.route('/view_data')
@myauth.requires_auth
def list_my_data():
        users = Participant.query.all()
	try:
		return render_template('list.html', participants=users)
	except TemplateNotFound:
		abort(404)

def add_bonus_data(uniqueId,user,won_puzzles,bonus_puzzles):
    user_data = loads(user.datastring)
    max_trial= int(user_data['data'][-1]['current_trial'])
    for puzzle in bonus_puzzles:
        max_trial+=1
        rec = {"uniqueid":uniqueId,"current_trial":max_trial,"dateTime":time(),"trialdata":'t:['+str(time())+'] event:['+('BONUS_FAIL','BONUS_SUCCESS')[puzzle in won_puzzles]+'] piece:[NA] move#:[NA] move:[NA] instance:['+puzzle+']'}
        user_data['data'].append(rec)
        user.datastring = dumps(user_data)



@custom_code.route('/compute_bonus', methods=['GET'])
def compute_bonus():
    played_puzzles=0;
    if not request.args.has_key('uniqueId'):
        raise ExperimentError('improper_inputs')
    uniqueId = request.args['uniqueId']
    try:
        user = Participant.query.\
               filter(Participant.uniqueid == uniqueId).\
               one()
        user_data = loads(user.datastring) # load datastring from JSON
        won_puzzles=set()
        won_puzzles_numbers=[]
        for record in user_data['data']: # for line in data file
            trial = record['trialdata']
            if isinstance(trial, basestring):
                if 'win' in trial:
                    won_puzzles.add([s.replace('[','').replace(']','') for s in re.findall('\[.*?\]',trial)][5])
        bonus_puzzles=sample(puzzle_files,num_of_bonus_puzzles)
        user.bonus = bonus_by_completion(won_puzzles,bonus_puzzles)
        add_bonus_data(uniqueId,user,won_puzzles,bonus_puzzles)
        db_session.add(user)
        db_session.commit()
        resp = {"bonusComputed": "success"}
        return jsonify(**resp)
    except TemplateNotFound:
        abort(404)
    except Exception as e:
        print 'compute_bonus ERROR:'
        current_app.logger.error(e)  # Print message to server.log for debugging 
        print e



@custom_code.route('/show_bonus', methods=['GET'])
def show_bonus():
    if not request.args.has_key('uniqueId'):
        raise ExperimentError('improper_inputs')
    uniqueId = request.args['uniqueId']
    try:
        user = Participant.query.\
               filter(Participant.uniqueid == uniqueId).\
               one()
        user_data = loads(user.datastring) # load datastring from JSON
        won_puzzles=set()
        succs=[]
        for record in user_data['data']: # for line in data file
            trial = record['trialdata']
            if isinstance(trial, basestring):
                if 'BONUS' in trial:
                    puzzle=[s.replace('[','').replace(']','') for s in re.findall('\[.*?\]',trial)][5]
                    if 'BONUS_SUCCESS' in trial:
                        is_bonus=True
                        amount=total_bonus/num_of_bonus_puzzles
                    elif 'BONUS_FAIL' in trial:
                        is_bonus=False
                        amount=0
                    succs.append((puzzle,is_bonus,amount))
        return render_template('show_bonus.html', success=succs, bonus=user.bonus,time=time())
    except TemplateNotFound:
        abort(404)
    except Exception as e:
        current_app.logger.error(e)  # Print message to server.log for debugging 
        print e


def bonus_by_completion(won_puzzles,bonus_puzzles):
    per_puzzle=total_bonus/num_of_bonus_puzzles
    return len(set(won_puzzles) & set(bonus_puzzles))*per_puzzle

