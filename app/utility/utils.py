import torch
import random
import numpy as np
import re

from typing import List


def clean(text: str):
    jamo_patterns = "([ㄱ-ㅎㅏ-ㅣ]+)"  # 한글 단일 자음&모음제거
    english_patterns = "[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]"
    special_patterns = "[-=+,#/\:$. @*\"※&%ㆍ』\\‘|\(\)\[\]\<\>`'…》.!?]"  # 공백 특수문자 제거
    text = re.sub(pattern=jamo_patterns, repl="", string=text)
    text = re.sub(pattern=special_patterns, repl="", string=text)
    text = re.sub(pattern=english_patterns, repl="", string=text)
    text = re.sub(r"[0-9]+", "", string=text)
    text = text.replace("~", "")
    text = text.strip()
    return text


def mean_pooling(model_output, attention_mask):
    model_output = torch.from_numpy(model_output[0])
    # First element of model_output contains all token embeddings
    token_embeddings = model_output
    attention_mask = torch.from_numpy(attention_mask)
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size())
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask, input_mask_expanded, sum_mask


def softmax(x):
    f_x = np.exp(x) / np.sum(np.exp(x))
    return f_x


def top_k_sampling(score_list: List[int], weight: int = 1):
    score_list = [i * weight for i in score_list]
    softmax_list = softmax(score_list)

    pick = random.choices(range(len(score_list)), weights=softmax_list)

    return pick[0]
