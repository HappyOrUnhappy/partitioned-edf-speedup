import math
import itertools
from math import gcd


def lcm(a: int, b: int) -> int:
    """计算两个正整数的最小公倍数"""
    return a * b // gcd(a, b)


def vec_lcm(vec: list[int]) -> int:
    """计算整数向量所有元素的LCM"""
    current_lcm = 1
    for num in vec:
        current_lcm = lcm(current_lcm, num)
    return current_lcm


def f_func(x: float) -> int:
    """论文定义的需求计数函数 f(x)"""
    if x >= 0:
        return math.floor(x) + 1
    else:
        return 0


def is_feasible(p: list[int], n: int) -> tuple[bool, int]:
    """
    校验向量 p 是否满足论文条件(5)：∀t∈Z+, Σf((t-i)/p_i) ≤ t
    仅校验 1 ≤ t ≤ LCM(p)+n 区间（DBF极值充分区间）
    返回 (是否可行, 最大校验t值)
    """
    # 前置剪枝：总利用率>1时必然不可行，直接跳过
    sum_inv = sum(1.0 / pi for pi in p)
    if sum_inv > 1 :
        return False, 0

    l = vec_lcm(p)
    max_t = l + n

    for t in range(1, max_t + 1):
        total = 0
        for i in range(n):
            paper_i = i + 1
            val = (t - paper_i) / p[i]
            total += f_func(val)
            # 提前终止：累加超过t直接跳出
            if total > t:
                return False, max_t
        if total > t:
            return False, max_t
    return True, max_t


def compute_eta(p: list[int], n: int) -> float:
    """计算辅助函数 η(p)"""
    res = 0.0
    for idx in range(n):
        paper_i = idx + 1
        ni = n - paper_i + 0.5
        res += ni / (n * p[idx])
    return res


def compute_xi_rho(p: list[int], n: int) -> tuple[float, float]:
    """直接计算 ξ(p) 与 ρ = 1+ξ(p)"""
    xi = 0.0
    for idx in range(n):
        paper_i = idx + 1
        ni = n - paper_i
        xi += ni / (n * p[idx])
    rho = 1.0 + xi
    return xi, rho

def extend_p_vector(original_p: list[int], k: int) -> list[int]:
    """
    按照论文Lemma 5的k倍扩展规则，将原始n维p向量扩展为 n*k 维
    对应论文公式(9)：q_j = k * p_{ceil(j/k)} （j为1-based位置）

    扩展性质：
    1. 若 original_p 满足条件(5)，则扩展后的向量也满足条件(5)
    2. 扩展前后 η(p) 值完全相等

    参数:
        original_p: 原始p向量（长度n）
        k: 扩展倍数，正整数
    返回:
        extended_p: 扩展后的p向量，长度为 len(original_p)*k
    """
    n_original = len(original_p)
    extended_length = n_original * k
    extended_p = []

    # j为1-based的位置索引，从1到extended_length
    for j in range(1, extended_length + 1):
        # 计算对应原始向量的索引：ceil(j/k) 对应1-based，转0-based减1
        original_idx = (j - 1) // k
        extended_p.append(k * original_p[original_idx])

    return extended_p

def check_p_vector(p_list: list[int]) -> None:
    """
    输入p向量列表，自动完成可行性校验、η/ξ/ρ计算并格式化打印全部结果
    :param p_list: 待检测的p整数向量
    """
    n = len(p_list)
    feasible, max_t = is_feasible(p_list, n)
    eta_val = compute_eta(p_list, n)
    xi_val, rho_val = compute_xi_rho(p_list, n)

    # 格式化打印输出
    print("=" * 60)
    print("待检测p向量：", p_list)
    print(f"向量维度 n = {n}")
    print("-" * 60)
    print(f"是否满足可行性条件(7): {feasible}")
    print(f"校验区间最大t值: {max_t}")
    print("-" * 60)
    print(f"η(p) = {eta_val:.8f}")
    print(f"ξ(p) = {xi_val:.8f}")
    print(f"ρ    = {rho_val:.8f}")
    print("=" * 60)

if __name__ == "__main__":
    # 直接传入向量即可检测
    p_list = [12, 8, 6, 8, 6, 8, 9, 12]
    check_p_vector(p_list)

    # k=4倍扩展到32维
    k = 4
    p_32_base = extend_p_vector(p_list, k)
    check_p_vector(p_32_base)

    # k=4倍扩展到32维，并修改最后四个元素
    k = 4
    p_32_final = extend_p_vector(p_list, k)
    p_32_final[28] = 44
    p_32_final[29] = 46
    p_32_final[30] = 45
    p_32_final[31] = 185
    check_p_vector(p_32_final)




