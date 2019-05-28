import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize, scale
from typing import List


class ComponentRoller:
    def __init__(self, comps: List[pd.DataFrame], roll_size):
        self.comps = comps
        self.roll_size = roll_size

    def count(self):
        return len(self.comps)

    def roll(self):
        picked_id = np.random.choice(self.count(), self.roll_size, replace=False)
        picked_comps = []
        for i in picked_id:
            c = self.comps[i]
            r = np.random.randint(c.shape[1])
            picked_comps.append(c.iloc[:, r])

        mask = np.zeros(self.count())
        for i in picked_id:
            mask[i] = 1
        # translate hot bit to num.
        # i.e. [1, 1, 0, 0] will be coded as 12
        from functools import reduce
        label = reduce(lambda x, y: x * 2 + y, mask)
        label = label.astype('int')

        df = pd.concat(picked_comps, axis=1)
        return df.values, label


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
            the_sample = pd.Series(name=label, data=np.sum(picked_comps * concen_vector, axis=0))
            samples.append(the_sample)
            if i % 100 == 0:
                print('组合数%d: 第%d个样本 --- 标签%d，浓度比%s' % (n_class, i, label, concen_vector))
    df = pd.concat(samples, axis=1)
    return df.values.T, df.columns.tolist()


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



