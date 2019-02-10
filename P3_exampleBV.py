#conda create -n deepeeg
#source activate deepeeg
#chomd +x install.sh
#bash install.sh
#!git clone https://github.com/kylemath/eeg-notebooks
#python
from utils import *
data_dir = '/Users/kylemathewson/Desktop/data/'
exp = 'P3'
#subs = ['001','002','004','005','006','007','008','010']
subs = [ '001']

sessions = ['ActiveDry','ActiveWet','PassiveWet']

nsesh = len(sessions)
event_id = {'Target': 1, 'Standard': 2}

epochs = []
for sub in subs:
	print('Loading data for subject ' + sub)
	for session in sessions:
		#Load Data
		raw = LoadBVData(sub,session,data_dir,exp)
		#Pre-Process EEG Data
		epochs.append(PreProcess(raw,event_id,
							emcp=True, rereference=True,
							plot_erp=True, rej_thresh_uV=200))

print(epochs)
epochs = concatenate_epochs(epochs)	
print(epochs)

#Engineer Features for Model
feats = FeatureEngineer(epochs,model_type='NN',electrode_median=False)
#Create Model
model,_ = CreateModel(feats, units=[16,16,16,16,16], dropout=.15)
#Train with validation, then Test
TrainTestVal(model,feats)

