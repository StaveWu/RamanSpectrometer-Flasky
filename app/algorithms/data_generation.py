import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize, scale
from typing import List
from functools import reduce


class ComponentRoller:
    def __init__(self, comps: List[pd.DataFrame], roll_size):
        self.comps = comps
        self.roll_size = roll_size

    def count(self):
        return len(self.comps)

    def roll(self):
        picked_ids = np.random.choice(self.count(), self.roll_size, replace=False)
        picked_comps = []
        picked_comp_ids = []  # to hold component ids instead of list id where component be.
        for i in picked_ids:
            # random select a sample from existing samples
            c = self.comps[i]
            r = np.random.randint(c.shape[1])
            picked_comps.append(c.iloc[:, r])
            # gather component id
            picked_comp_ids.append(c.columns[0])

        df = pd.concat(picked_comps, axis=1)
        return df.values, self._to_str_label(picked_comp_ids)

    @staticmethod
    def _to_str_label(comp_ids: list):
        """
        change comp_ids to str label. e.g.
        (1, 2, 5) ==> '11001'
        :param comp_ids: a tuple containing picked component id
        :return: str label
        """
        str_len = max(comp_ids)
        mask = [0] * str_len
        for i in comp_ids:
            mask[i-1] = 1
        return reduce(lambda x, y: x + y, map(str, mask))


class ConcentrationRoller:
    def __init__(self, lower_bound, upper_bound, roll_size):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.roll_size = roll_size
        self.roll_history = {}

    def roll_unique(self, label):
        vector = np.random.choice(np.arange(self.lower_bound, self.upper_bound, 1), self.roll_size)
        vector_normed = normalize(vector.reshape(1, -1)).flatten()
        return vector_normed if self.roll_size == 1 or self._add_to_history(label, vector_normed) \
            else self.roll_unique(label)

    def _add_to_history(self, label, vector):
        if label not in self.roll_history:
            self.roll_history[label] = set()
        prev_count = len(self.roll_history[label])
        self.roll_history[label].add(tuple(vector))
        cur_count = len(self.roll_history[label])
        return cur_count != prev_count


def generate_train_data(comps: List[pd.DataFrame], concen_upper_bound=1000, num_per_combination=1000):
    """
    use for generating train data
    :param comps: component list. each component in the list corresponds tp a component, represented by
    a dataframe, where each column of dataframe is a sample of the component, the column name indicates the
    component id, the index indicates Raman shift, and the values indicate intensity.
    :param concen_upper_bound:
    :param num_per_combination:
    :return: (data, labels)
    """
    cps = [to_int_index(c) for c in comps]
    cps = alignment(cps)
    cps = [scale_dataframe(c) for c in cps]

    samples = []
    for n_class in range(1, len(cps) + 1):
        comps_roller = ComponentRoller(cps, n_class)
        concen_roller = ConcentrationRoller(1, concen_upper_bound, n_class)
        for i in range(num_per_combination):
            picked_comps, label = comps_roller.roll()
            concen_vector = concen_roller.roll_unique(label)
            the_sample = pd.Series(name=label, data=np.sum(picked_comps * concen_vector, axis=1))
            samples.append(the_sample)
            if i % 100 == 0:
                print('组合数{}: 第{}个样本 --- 标签{}，浓度比{}'.format(n_class, i, label, concen_vector))
    df = pd.concat(samples, axis=1)
    return df.values.T, np.array(_to_vectors(df.columns.tolist()))


def _to_vectors(labels):
    """
    e.g. ['11', '11001'] ==> [[1, 1, 0, 0, 0], [1, 1, 0, 0, 1]]
    :param labels:
    :return:
    """
    res = [[int(s) for s in label] for label in labels]
    max_len = 0
    for ele in res:
        if len(ele) > max_len:
            max_len = len(ele)
    return [ele + [0] * (max_len - len(ele)) for ele in res]


def to_int_index(df: pd.DataFrame):
    index = np.array(df.index).round()
    data = df.values
    data_average = np.array([np.mean(d, axis=0) for d in split_by_duplicate_index(index, data)])
    return pd.DataFrame(index=set(index), data=data_average, columns=df.columns.tolist())


def split_by_duplicate_index(index, data):
    if len(index) != len(data):
        raise ValueError('expect the same length')
    res = []
    group = [data[0]]
    for i in range(1, len(index)):
        if index[i] != index[i - 1]:
            res.append(np.array(group))
            group = [data[i]]
        else:
            group.append(data[i])
    res.append(np.array(group))
    return res


def alignment(dfs: List[pd.DataFrame]):
    grid = [df.shape[1] for df in dfs]
    df = pd.concat(dfs, axis=1)
    df = df.fillna(method='ffill')
    df = df.fillna(method='bfill')
    res = []
    pt = 0
    for g in grid:
        res.append(df.iloc[:, pt:pt+g])
        pt += g
    return res


def scale_dataframe(df: pd.DataFrame):
    return pd.DataFrame(index=df.index, data=scale(df.values), columns=df.columns.tolist())



