# JMA・GPM入力の出典・ライセンス監査

## 判定

入力CSVのSHA-256、CSV内の出典列、ローカル取得記録は確認できた。しかし、権威あるライセンス記録と再配布許可は確認できない。したがって、入力CSVはGitHub releaseやZenodoへ同梱しない。

## JMA

- 対象：`jma_independent_events_12station_daily_v2.csv`
- SHA-256：`e3cdb24f08f8bd65f5ffafac40d771592869fd1843999f0cbd6510739c7eb7f9`
- 出典：CSVの`source_url`列に気象庁の日別値ページURLが記録されている。
- 版：v2訂正版。Mishima列補正の監査記録がある。
- 取得記録：2026-10-04〜2026-10-05のローカル取得・監査成果物がある。
- ライセンス／再配布：未確認。

## GPM

- 対象：`gpm_independent_events_11station_30min_complete.csv`
- SHA-256：`6d7b1e467c293da2966c200a60d6f9e3639e1ccf7702fd0076c84e1e305a7a86`
- 出典：`3B-HHR.MS.MRG.3IMERG.*.HDF5`のソースファイル名が記録されている。
- 版：ローカル記録上はIMERG V07Bのファイルパターン。完全なコレクション引用は未添付。
- 取得記録：2026-10-04の取得計画・監査成果物がある。
- ライセンス／再配布：未確認。Earthdata認証トークンが必要な取得経路として記録されている。

## 公開方針

コード、Docker設定、検証プログラム、manifest、Issueテンプレートは公開準備済み。入力データは、(a)権威あるライセンスと再配布許可を記録する、または(b)取得・照合手順とSHA-256だけを公開し、許諾済みfixtureへ切り替えるまで公開保留とする。
