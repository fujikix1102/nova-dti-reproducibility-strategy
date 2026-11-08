# GitHub配置・公開可否確認

## 配置可能な構成

以下はGitHubリポジトリ直下へ配置できる。

- `README.md`, `Dockerfile`, `requirements-lock.txt`
- `ENVIRONMENT.md`
- `PUBLIC_REPRODUCTION_GUIDE.md`
- `EXTERNAL_REPRODUCTION_QUICKSTART.md`
- `REPRODUCTION_REPORT_TEMPLATE.md`
- `DATA_AND_LICENSES.md`
- `.github/workflows/reproducibility-contract.yml`
- `.github/ISSUE_TEMPLATE/reproduction-success.yml`
- `.github/ISSUE_TEMPLATE/reproduction-mismatch.yml`
- `work/verify_manifest.py`, `work/compare_external_execution.py`, `work/freeze_execution_record.py`
- `outputs/`の固定manifest、比較表、実行記録

## 確認済み

- Docker設定とIssueテンプレートが存在する。
- manifest、実行ログ、SHA-256、seed、期待構造、許容誤差の記録がある。
- `formal_pass=false`の境界がREADME・manifest・記録に明記されている。
- GitHub Actionsの最小契約テストがある。

## 公開前ブロッカー

1. 現在の作業ディレクトリはまだGitリポジトリではない。GitHubリポジトリの作成・push・releaseは未実施。
2. JMA入力CSVの再配布ライセンスと出典記録が未確認。
3. GPM入力CSVの再配布ライセンスと出典記録が未確認。
4. データをそのまま公開できない場合の、取得手順または小型fixtureが未確定。
5. 公開URL、Zenodo DOI、外部評価は未作成・未確認。

## 公開可否

コード、Docker設定、検証プログラム、説明書、Issueテンプレートは公開準備済み。入力データはライセンス確認が終わるまで公開可とは判定しない。したがって、現時点の公開可否は「コード部分は可、入力データ部分は保留」である。

## 次の安全な順序

1. JMA・GPM入力の原典、版、取得日、ライセンス、再配布可否を台帳へ記録する。
2. 再配布不可なら、取得・照合手順または許諾済みfixtureへ切り替える。
3. Gitリポジトリを作成し、入力を含めないコード版を先にpushする。
4. GitHub Actionsを実行し、Issueを有効化する。
5. 入力公開可否が確定してから、タグ付きreleaseと必要ならZenodoを作成する。
