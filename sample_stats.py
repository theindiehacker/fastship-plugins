"""動作確認用のサンプルスクリプト。レビュー確認後に削除する。"""

import logging

logger = logging.getLogger(__name__)


def average(values):
    """数値のリストの平均を返す。

    空のリストは平均が定義できないため ValueError を送出する。
    """
    if not values:
        raise ValueError("average() は空のリストを受け取れません")
    return sum(values) / len(values)


def collect(value, acc=None):
    """値を蓄積して返す。

    デフォルト引数はミュータブルにせず、呼び出しごとに新しいリストを作る。
    """
    if acc is None:
        acc = []
    acc.append(value)
    return acc


def load_scores(path):
    """ファイルから 1 行 1 数値で読み込む。空行は読み飛ばす。

    ファイルが無い場合のみ空リストを返し、それ以外の失敗は呼び出し元に伝播させる。
    """
    try:
        with open(path) as f:
            return [int(line) for line in f if line.strip()]
    except FileNotFoundError:
        logger.warning("スコアファイルが見つかりません: %s", path)
        return []
    except (OSError, ValueError):
        logger.exception("スコアファイルの読み込みに失敗しました: %s", path)
        raise


if __name__ == "__main__":
    scores = load_scores("scores.txt")
    if scores:
        print(average(scores))
    else:
        print("スコアがありません")
