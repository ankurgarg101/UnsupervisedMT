import os
import subprocess
from collections import OrderedDict
from logging import getLogger
import numpy as np
import torch
from torch import nn

TOOLS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AST_SCRIPT_PATH = os.path.join(TOOLS_PATH, 'ast/metrics.py')
print (AST_SCRIPT_PATH)
assert os.path.isfile(AST_SCRIPT_PATH), "AST tool and post processing script not found in  %s" % TOOLS_PATH

def eval_other_metrics(ref,hyp):
    """
    Given a file of hypothesis and reference files,
    evaluates other metrics like ast and bracket checking. (only uses ref file if necessary)
    """
    assert os.path.isfile(ref) and os.path.isfile(hyp)
    command = 'python3 '+ AST_SCRIPT_PATH + ' -ref %s -hyp %s'
    p = subprocess.Popen(command % (ref, hyp), stdout=subprocess.PIPE, shell=True)
    result = p.communicate()[0].decode("utf-8").split('\n')
    ast = -1
    bracket = -1
    for line in result:
        line = line.strip().split()
        if len(line)>1:
            if line[0].startswith('AST'):
                ast = float(line[1])
            elif line[0].startswith('Brackets'):
                bracket = float(line[1])
            else:
                print('Impossible to parse AST score! "%s"' % result)
                return -1, -1
    return ast, bracket

eval_other_metrics('../../../../config_train_75_0_0_0/results/hyp28.x-y.valid.txt','../../../../config_train_75_0_0_0/results/hyp28.x-y.valid.txt')