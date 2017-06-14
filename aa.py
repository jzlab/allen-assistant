import argparse
from allensdk.core.brain_observatory_cache import BrainObservatoryCache
import allensdk.brain_observatory.stimulus_info as stim_info
from pprint import pprint as pp
import pandas as pd
from tqdm import tqdm

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", '--cache_dir', help='Default: ./boc/', type=str, default='boc/')
    ec = parser.add_argument_group('ec_args','Experiment Container Params')
    ec.add_argument("-t","--targeted_structures", help="Target Structure", type=str, action='append')
    ec.add_argument("-c","--cre_lines", help="(e.g. Cux2-CreERT2)", type=str, action='append')
    ec.add_argument("-d","--imaging_depths", help="imaging depth", type=int, action='append')

    ophys = parser.add_argument_group('exp_args','Experiment Params')
    ophys.add_argument("-s","--stimuli", help="stimuli type (e.g. natural_scenes)", type=str, action='append')

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

def extract_ec_params(FLAGS):
    return extract(['cre_lines', 'targeted_structures','imaging_depths'],FLAGS)

def extract_ophys_params(FLAGS):
    params = extract(['stimuli'],FLAGS)
    params['stimuli'] = [ getattr(stim_info,s.upper()) for s in params['stimuli']]
    return params

def fetch_ecs(boc,FLAGS):
    dl_warn('experiment_containers')
    params = extract_ec_params(FLAGS)
    ecs = boc.get_experiment_containers(**params)
    return ecs

def fetch_exps(boc,FLAGS):
    dl_warn('experiment manifests')
    ecs = fetch_ecs(boc,FLAGS)
    ec_ids = [ec['id'] for ec in ecs]
    ophys_params = extract_ophys_params(FLAGS)
    ophys_params['experiment_container_ids'] = ec_ids
    exps = boc.get_ophys_experiments(experiment_container_ids=ec_ids)
    return exps

def fetch_datasets(boc,FLAGS):
    dl_warn('experiment data files')
    exps = fetch_exps(boc,FLAGS)
    ecs_ids = [ exp['experiment_container_id'] for exp in exps]
    exp_ids = [ exp['id'] for exp in exps]
    for id in tqdm(exp_ids,desc='fetch experiments',unit_scale='exp'):
        import pdb; pdb.set_trace()
        data_set = boc.get_ophys_experiment_data(id)

    cells = boc.get_cell_specimens()
    cells = pd.DataFrame.from_records(cells)
    query_cells = cells[cells['experiment_container_id'].isin(ecs_ids)]

    #for cell in query_cells:


if __name__ == "__main__":
    FLAGS = parse_args()
    manifest_path = FLAGS.cache_dir + 'manifest.json'
    boc = BrainObservatoryCache(manifest_file=manifest_path)
    print('Query parameters:\n')
    pp(vars(FLAGS))

    fetch_datasets(boc,FLAGS)
    ecs = fetch_ecs(boc,FLAGS)

    print('Num experiment containers: %d\n' % len(ecs))
    #exps = fetch_exps(boc,FLAGS)
    print('')
    print('Experiments for experiment_container_id %d: %d\n' % (1,1))
