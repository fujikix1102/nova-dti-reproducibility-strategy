# NOVA–DTI JMA–GPM v2 再現パッケージ

このパッケージは、JMA–GPM v2の訂正済み探索的比較を、固定Docker環境と固定乱数seedで再実行・検証する最小経路を提供する。

これは校正、正式検証、因果推論、観測的発見を行うパッケージではない。manifestの`formal_pass`は意図的に`false`であり、実行しても正式PASSへ変更してはならない。

## 期待結果

- matched daily records: 81
- event–station groups: 27
- events: 3
- stations: 9
- bootstrap replicates: 2,000
- random seed: `20261108`
- `formal_pass`: `false`

## 1. Dockerイメージを作る

```bash
docker build --tag nova-dti-jma-gpm:2026-11-08 .
```

## 2. 検証用入力を用意する

原本を直接変更しない。JMA・GPM入力と3本の既存処理スクリプトを、読み書き可能な検証用ディレクトリへ複製する。実行スクリプトは出力を同じ比較ディレクトリへ書くため、原本の読み取り専用マウントでは実行しない。

想定する配置は次の通り。

```text
repro-root/
  code/
    recompute_jma_gpm_v2.py
    bootstrap_v2.py       # bootstrap_v2_seeded.pyをこの名前で配置
    downstream_v2.py
  nova/external_data/real_events/
    independent_events_jma_expanded/
    independent_events_gpm_station_extract_expanded/
```

## 3. Dockerで再実行する

```bash
docker run --rm \
  -v "$PWD/repro-root/code:/opt/nova-code:ro" \
  -v "$PWD/repro-root/nova:/Volumes/1tbinside/NOVA" \
  -v "$PWD/repro-root:/mnt/repro" \
  nova-dti-jma-gpm:2026-11-08 \
  --code-dir /opt/nova-code \
  --base-dir /Volumes/1tbinside/NOVA/external_data/real_events \
  --log /mnt/repro/docker-run-log.json
```

## 4. manifestで一括検証する

```bash
python3 work/verify_manifest.py \
  outputs/docker-seeded-reproduction-manifest-20261108.json \
  --code-dir repro-root/code \
  --base-dir repro-root/nova/external_data/real_events \
  --output-dir repro-root/nova/external_data/real_events/independent_events_comparison_expanded \
  --log repro-root/docker-run-log.json
```

終了コード`0`かつ出力`"status": "PASS"`なら、manifestに対する入力・コード・出力・構造・ログの検証が通っている。欠損、SHA-256不一致、構造不一致、`formal_pass`の変更は失敗として扱う。

## 5. 証跡

- 固定条件：[docker-seeded-reproduction-manifest-20261108.json](outputs/docker-seeded-reproduction-manifest-20261108.json)
- 実行結果：[docker-seeded-reproduction-report-20261108.md](outputs/docker-seeded-reproduction-report-20261108.md)
- Docker設定：[Dockerfile](Dockerfile)
