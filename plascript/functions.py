import numpy as np
import random
from openjij import SQASampler


# 観測点の座標。要素数はNparaと合わせる
s = [0, 0, 0]  # 観測点の座標
mu, sigma = 0, 1
Npara = 3  # 特徴量空間のパラメータ数（特徴量の数）
Nmater = 10  # 教材の数


# ランダム教材作成
def make_sample() -> dict:
    """ランダムな教材を作成する

    Args:

    Returns:
        x(dict):教材リスト
    """
    x = {}
    for i in range(Nmater):
        x[i] = [random.gauss(mu, sigma) for i in range(Npara)]

    return x


def courseware2matrix(coursewares: dict) -> np.ndarray:
    """教材の辞書からパラメータをだけのarrayを作る

    Args:
        coursewares(dict):教材リスト

    Returns:
        mat(np.array):パラメータ配列
    """
    mat = np.zeros([Nmater, Npara])
    for i in range(Nmater):
        mat[i, :] = coursewares[i]
    # print(mat)
    return mat


def make_dist_mat(mat, s):
    """教材パラメータから対角行列をつくる

    Args:
        mat(np.ndarray):教材パラメータ配列

    Returns:
        dist_mat(np.array):パラメータの対角行列
        dist(dict):観測点からの距離のリスト

    """
    dist = {}
    # for i in range(Nmater):
    #     dist[i] = euclidean_distance(s, mat[i, :])
    #     print(dist[i])

    for i, li in enumerate(mat):
        dist[i] = np.linalg.norm(li - s)

    # distを対角行列化
    new_dist = np.array([])  # 新しい配列を初期化

    for i in range(Nmater):
        new_dist = np.append(new_dist, dist[i])
    dist = new_dist
    dist_mat = np.diag(dist)
    print(dist_mat)

    return dist_mat, dist


def create_penalty(N, K):
    P = np.zeros([N, N])
    for i in range(N):
        for j in range(N):
            P[i, j] = 1
    for i in range(N):
        P[i, i] = P[i, i] - 2 * K
    return P


def sample(QUBO, num_reads):
    sampler = SQASampler()
    sampleset = sampler.sample_qubo(QUBO, num_reads=num_reads)
    sample = sampleset.first.sample
    return sample
