# Author: Yuriy Ilchenko (ilchenko@physics.utexas.edu)
# Apply TMVA BDT to an event to get a score 

import os
import sys

if os.environ['TERM'] == 'xterm':
    os.environ['TERM'] = 'vt100'
# Now it's OK to import readline :)
# Import ROOT libraries

import ROOT
from ROOT import TH1F
import array

from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import classification_report, roc_auc_score, roc_curve

from sklearn import tree
import cPickle


reader = ROOT.TMVA.Reader()

m_el_pt = array.array('f',[0])
reader.AddVariable("m_el_pt", m_el_pt)
m_el_eta = array.array('f',[0])
reader.AddVariable("m_el_eta", m_el_eta)
m_el_sigd0PV = array.array('f',[0])
reader.AddVariable("m_el_sigd0PV", m_el_sigd0PV)
m_el_z0SinTheta = array.array('f', [0])
reader.AddVariable("m_el_z0SinTheta", m_el_z0SinTheta)
m_el_etcone20Dpt = array.array('f',[0])
reader.AddVariable("m_el_etcone20Dpt", m_el_etcone20Dpt)
m_el_ptcone20Dpt = array.array('f',[0])
reader.AddVariable("m_el_ptcone20Dpt", m_el_ptcone20Dpt)

# Download BDT weights
#reader.BookMVA("BDT","MVAnalysis_BDT.weights.xml")
reader.BookMVA("BDT",
    #"/Users/musthero/Documents/Yura/Applications/koza4ok/test/ttH_Run1_LeptonID/weights/SKLearn_BDT_electons.weights.xml")
    "/Users/musthero/Documents/Yura/Applications/TMVA-v4.2.0/test/weights/MVAnalysis_BDT_GradBoost.weights.xml")

# Read ROOT file with the events to classify
input_filename = "/Users/musthero/Documents/Yura/Applications/TMVA-v4.2.0/test/output_electrons_fullsim_v5_20per.root"
file = ROOT.TFile.Open(input_filename)
if file.IsZombie():
    print "Root file is corrupt"


# Get a handle to the tree
t = file.JINRTree_3

c = 0
for event in t:
    c = c + 1
    if (c % 10000 == 0):
        print "Event number %i" % c
        sys.stdout.flush()

    if c == 2: break

    if not event.m_el_VeryTightLH == 1 : continue

    m_el_pt[0] = event.m_el_pt 
    m_el_eta[0] = event.m_el_eta
    m_el_etcone20Dpt[0] = event.m_el_etcone20Dpt
    m_el_ptcone20Dpt[0] = event.m_el_ptcone20Dpt
    m_el_sigd0PV[0] = event.m_el_sigd0PV
    m_el_z0SinTheta[0] = event.m_el_z0SinTheta
    m_el_isprompt = event.m_el_isprompt


    # sklearn score
    #score = bdt.predict([m_el_pt[0], m_el_eta[0], m_el_sigd0PV[0], m_el_z0SinTheta[0], 
    #    m_el_etcone20Dpt[0], m_el_ptcone20Dpt[0]]).item(0)

    #score = bdt.decision_function([m_el_pt[0], m_el_eta[0], m_el_sigd0PV[0], m_el_z0SinTheta[0], 
    #    m_el_etcone20Dpt[0], m_el_ptcone20Dpt[0]]).item(0)

    # calculate the value of the classifier with TMVA/TskMVA
    bdtOutput = reader.EvaluateMVA("BDT")

    print "bdtOutput =", bdtOutput


file.Close()




