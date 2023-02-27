#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
import numpy as np
from tqdm.notebook import tqdm


# In[10]:


# 용량 줄이기
# 데이터 범위 체크 후, 최적화된 타입 적용
def reduce_mem_usage(df):

    # 현재 메모리 사용량
    start_mem = df.memory_usage().sum() / 1024**2
    print('데이터 프레임의 메모리 사용량 : {:.2f} MB'.format(start_mem))

    # 컬럼 하나씩 확인 후 적용
    for col in tqdm(df.columns[1:]):
        col_type = df[col].dtype

        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        else:
            df[col] = df[col].astype('category')

    # 타입변경 후 메모리 사용량
    end_mem = df.memory_usage().sum() / 1024**2
    print('최적화 후 메모리 사용량 : {:.2f} MB'.format(end_mem))
    print('감소율 : {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))

    return df
