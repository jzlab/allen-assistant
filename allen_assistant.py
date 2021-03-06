import argparse
from allensdk.core.brain_observatory_cache import BrainObservatoryCache
import allensdk.brain_observatory.stimulus_info as stim_info
from pprint import pprint as pp
import pandas as pd
from tqdm import tqdm
import scipy.io as sio
import os

def add_base_parser(parser):
    tboc = boc = BrainObservatoryCache(manifest_file='boc/manifest.json')
    vis_structs = tboc.get_all_targeted_structures()
    cre_lines = tboc.get_all_cre_lines()
    stimuli = tboc.get_all_stimuli()
    depths = tboc.get_all_imaging_depths()

    ec = parser.add_argument_group('Experiment Container Params','')

    ec.add_argument("-t","--targeted_structures",
        help="Target Visual Cortex Structure.  Allowed values are: "+"\n ".join(vis_structs),
        metavar='',type=str, action='append',choices=vis_structs)

    ec.add_argument("-c","--cre_lines",
        help="Transgenic mouse line. Allowed values are "+", ".join(cre_lines),
        type=str,action='append',choices=cre_lines,metavar='')

    ec.add_argument("-d","--imaging_depths",
            help="Imaging depths. Allowed values are "+", ".join(str(x) for x in depths),
            type=int, action='append', choices=depths ,metavar='')

    ophys = parser.add_argument_group('Other Params','')

    ophys.add_argument("-s","--stimuli",
            help="Visual stimuli type.  Allowed values are "+", ".join(stimuli),
            type=str, action='append',choices=stimuli,metavar='')

    return parser

def parse_args():

    trace_types=['raw','demixed','neuropil','corrected','dff']

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", '--cache_dir',
            help='Default: ./boc/', type=str, default='boc/', metavar='')

    subparsers = parser.add_subparsers()
    dl_parser = subparsers.add_parser('download',help='Used for downloading files')
    dl_parser.add_argument('--output_dir',
        help='path/to/directory to save files (currently only supports mat files)', type=str,metavar='',
        default='boc/experiment_output_files')
    dl_parser.add_argument('--trace_format',
        help='Fluoresence trace type (default dff). Valid options are '+', '.join(trace_types),
        type=str, metavar='',
        choices=trace_types, default='dff')

    dl_parser = add_base_parser(dl_parser)

    search_parser = subparsers.add_parser('search',help='Used for testing search queries')
    search_parser.add_argument('-o', '--outfile',
        help='Filepath to save text report',type=str,metavar='',default=None)
    search_parser.add_argument('--detailed',
        help='Show a far more detailed report', action='store_true',default=False)

    search_parser = add_base_parser(search_parser)

    return parser.parse_args()


def dl_warn(msg='data'):
    print('Downloading '+msg+' from the Brain Observatory')
    print('This may take a while...')
    print('')


def extract(param_list,all_params):
    extracted_params = {}
    for p in param_list:
        if getattr(all_params,p) is not None:
            extracted_params[p] = getattr(all_params,p)
    return extracted_params

def container_params(FLAGS,boc=None):
    return extract(['cre_lines', 'targeted_structures','imaging_depths'],FLAGS)

def ophys_params(FLAGS,boc):
    ecs = fetch_ecs(FLAGS,boc)
    ec_ids = [ec['id'] for ec in ecs]
    params = extract(['stimuli'],FLAGS)
    # ophys_params['stimuli'] = FLAGS.stimuli
    if FLAGS.stimuli is not None:
        params['stimuli'] = [ getattr(stim_info,s.upper()) for s in params['stimuli']]
    params['experiment_container_ids'] = ec_ids
    return params

def fetch_ecs(FLAGS,boc):
    # dl_warn('experiment container information')
    params = container_params(FLAGS)
    ecs = boc.get_experiment_containers(**params)
    return ecs

def fetch_exps(FLAGS,boc,filters={}):
    # dl_warn('experiment manifest information')
    query_params = ophys_params(FLAGS,boc)
    for key,val in filters.iteritems():
        query_params[key] = val
    exps = boc.get_ophys_experiments(**query_params)
    return exps

def fetch_cells(FLAGS,boc,ecs_ids):
    cells = boc.get_cell_specimens()
    cells = pd.DataFrame.from_records(cells)
    exp_cells = cells.loc[( cells['area'].isin(FLAGS.targeted_structures) ) & 
            (cells['experiment_container_id'].isin(ecs_ids)) &
            (cells['imaging_depth'].isin(FLAGS.imaging_depths)) &
            (cells['all_stim'].isin([True]))]
    return exp_cells

def fetch_datasets(FLAGS,boc,exps):
    ecs_ids = [ exp['experiment_container_id'] for exp in exps]
    exp_ids = [ exp['id'] for exp in exps]

    datasets = []
    ts = []
    traces = []
    for exp_id in tqdm(exp_ids,desc='fetch experiments',leave=False):
        dl_warn('Experiment %d' % exp_id)
        data_set = boc.get_ophys_experiment_data(exp_id)
        cids = data_set.get_cell_specimen_ids()
        if FLAGS.trace_format == 'dff':
            time,n_traces = data_set.get_dff_traces(cell_specimen_ids=cids)
        elif FLAGS.trace_format == 'raw':
            time,n_traces = data_set.get_fluorescence_traces(cell_specimen_ids=cids)
        elif FLAGS.trace_format == 'demixed':
            time,n_traces = data_set.get_demixed_traces(cell_specimen_ids=cids)
        elif FLAGS.trace_format == 'neuropil':
            time,n_traces = data_set.get_neuropil_traces(cell_specimen_ids=cids)
        elif FLAGS.trace_format == 'corrected':
            time,n_traces = data_set.get_corrected_traces(cell_specimen_ids=cids)
        datasets.extend([data_set])
        ts.extend([time])
        traces.extend([n_traces])
    return time, traces,datasets

def write_mat_files(FLAGS,savepath,ts,traces,datasets):

    for t,trace,dataset in zip(ts,traces,datasets):
        exp_id = dataset.get_metadata()['ophys_experiment_id']
        exp_fp = savepath + str(exp_id) + '.mat'
        print('writing '+FLAGS.trace_format+' trace to '+exp_fp)
        sio.savemat(exp_fp, {'time':t, 'dff':trace})


if __name__ == "__main__":
    FLAGS = parse_args()
    manifest_path = FLAGS.cache_dir + 'manifest.json'
    boc = BrainObservatoryCache(manifest_file=manifest_path)

    exps = fetch_exps(FLAGS,boc)

    if 'outfile' in vars(FLAGS).keys():
        ecs = fetch_ecs(FLAGS,boc)
        print('')
        print('RESULTS\n')
        print('Query parameters:')
        print('===============================\n')
        pp(vars(FLAGS))
        print('===============================\n')
        print('')
        print('Number of Experiment Containers: %d\n' % len(ecs))

        print('Number of Experiments returned: %d\n' % len(exps))

        if FLAGS.detailed:
            print('')
            for ec in ecs:
                print('====================================\n')
                print('Experiment Container (ID:'+str(ec['id'])+') metadata:\n')
                pp(ec)
                # print('====================================\n')
                print('')
                print('Experiments:\n')
                pp(fetch_exps(FLAGS,boc,filters={'experiment_container_ids':[ec['id']]}))

    else:
        t,df,datasets = fetch_datasets(FLAGS,boc,exps)
        if 'output_dir' in vars(FLAGS).keys():
            savepath = FLAGS.output_dir+'/'
            if not os.path.exists(savepath):
                os.makedirs(savepath)
            write_mat_files(FLAGS,savepath,t,df,datasets)
