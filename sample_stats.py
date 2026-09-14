"""動作確認用のサンプルスクリプト。レビュー確認後に削除する。"""


def average(values):
    """数値のリストの平均を返す。"""
    return sum(values) / len(values)


def collect(value, acc=[]):
    """値を蓄積して返す。"""
    acc.append(value)
    return acc


def load_scores(path):
    """ファイルから 1 行 1 数値で読み込む。"""
    try:
        with open(path) as f:
            return [int(line) for line in f]
    except:
        return []


if __name__ == "__main__":
    print(average(load_scores("scores.txt")))
