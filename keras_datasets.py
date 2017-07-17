import numpy as np
import pandas as pd
from keras.utils.data_utils import Sequence

class AllenBOSequence(Sequence):
    def __init__(self,data_set,
                 batch_size=32,
                 num_cells=100,
                 choose='random',
                 stimulus='natural_scenes',
                 pred_win=100):

        self.experiment_data = data_set
        self.batch_size = batch_size
        self.num_cells = 100
        self.pred_win=pred_win

        cids = self.experiment_data.get_cell_specimen_ids()
        if choose == 'random':
            self.cell_specimen_ids = np.sort(np.random.choice(
                np.arange(len(cids)),
                num_cells,replace=False))
        if stimulus is not 'spontaneous_activity':
            self.stim_table = self.experiment_data.get_stimulus_table(stimulus)
            self.stim_template = self.experiment_data.get_stimulus_template(stimulus)
        else:
            self.stim_table=self.experiment_data.get_spontaneous_activity_stimulus_table()
        _,self.dff = self.experiment_data.get_dff_traces(cids[self.cell_specimen_ids])

    def __len__(self):
        return len(self.stim_table) // self.batch_size

    def __getitem__(self,idx):
        win = self.pred_win
        start,end = self.stim_table.start[idx].item(),self.stim_table.end[idx].item()
        frame = self.stim_table.frame[idx].item()
        Xtemplate = self.stim_template[idx]
        Xtrace = self.dff[:,start:end]
        batch_Y = self.dff[:,end:end+win][:,0]
        return (np.array([Xtrace]),np.array(batch_Y))
