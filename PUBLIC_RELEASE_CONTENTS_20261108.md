# 入力CSV除外の公開版構成

## 公開対象

- `README.md`
- `Dockerfile`
- `requirements-lock.txt`
- `ENVIRONMENT.md`
- `PUBLIC_REPRODUCTION_GUIDE.md`
- `EXTERNAL_REPRODUCTION_QUICKSTART.md`
- `FETCH_AND_VERIFY_INPUTS.md`
- `DATA_AND_LICENSES.md`
- `LICENSE_VERIFICATION_SOURCES_20261108.md`
- `work/`の実行・検証プログラム
- `.github/`のCIとIssueテンプレート
- `outputs/`のmanifest、ログ要約、比較表、SHA-256記録

## 公開対象外

- JMA入力CSV
- GPM入力CSV
- Earthdata認証情報、トークン、Cookie
- 原本データを含むDocker image layer
- 個人情報または非公開取得ログ

## 公開時の確認

公開前に、リポジトリ全体を検査し、対象外ファイルが含まれていないことを確認する。入力データのSHA-256は公開するが、ハッシュはデータの再配布許可を意味しない。

`formal_pass=false`は公開版でも維持する。
