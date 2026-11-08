# 固定環境の実行手順

## 目的

DockerイメージはPythonランタイムと検証プログラムを固定する。元のJMA・GPMデータと保存済みの3本の処理スクリプトはイメージへコピーせず、実行時に読み取り専用でマウントする。

## Docker実行

作業室でイメージをビルドする。

```bash
docker build --tag nova-dti-jma-gpm:2026-11-08 .
```

保存資産を読み取り専用でマウントし、既存スクリプトを指定して実行する。出力先は元スクリプトの仕様により、保存資産側の比較ディレクトリになる。

```bash
docker run --rm \
  -v /Users/fujikijunichi/Documents/Codex/2026-09-27/new-chat:/opt/nova-code:ro \
  -v /Volumes/1tbinside/NOVA:/Volumes/1tbinside/NOVA:ro \
  -v "$PWD/work:/opt/repro/work" \
  nova-dti-jma-gpm:2026-11-08 \
  --code-dir /opt/nova-code \
  --base-dir /Volumes/1tbinside/NOVA/external_data/real_events \
  --log /opt/repro/work/docker-run-log.json
```

現行の処理スクリプトは出力を書き込むため、上記の完全読み取り専用実行は入力確認で停止する可能性がある。実際の再現実行では、入力アーカイブをコピーした検証用作業領域だけを読み書き可能にし、原本を直接マウントしない。

## CIの位置づけ

`.github/workflows/reproducibility-contract.yml`は、依存なしで実行できる最小CIである。Python構文と「入力・コードが欠けた場合に失敗して停止する」契約を検証する。

実データをCIへ自動公開・アップロードする設定は含めていない。完全再現CIへ進むには、許諾済みの小型fixtureと、そのSHA-256を別途固定する必要がある。
