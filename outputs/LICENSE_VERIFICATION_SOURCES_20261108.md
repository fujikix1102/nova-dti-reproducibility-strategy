# ライセンス確認結果

確認日: 2026-11-08 JST

## JMA

JMA公式の利用案内では、JMAサイトのコンテンツは出典表示を条件に複製・公衆送信・翻案等を利用できる旨が示され、政府標準利用規約（第1.0版）を基礎とし、CC BY 4.0と互換と説明されている。一方、JMA自身が著作権者でない第三者権利、個別法令、データページ固有の条件は別途確認が必要である。

対象CSVはJMAの日別ページの数値を抽出・整形した派生CSVなので、公開時には次を付す必要がある。

- 各JMA source URL
- 「JMA公式ページをもとに作成・編集した」旨
- 取得日と対象ページのSHA-256
- JMAが作成したものと誤認されない説明

暫定判定：**出典表示付きの派生データ公開は可能性が高いが、個別ページ・第三者権利の最終確認前に公開確定しない。**

Sources: [JMA利用上の留意事項](https://www.data.jma.go.jp/developer/ryuui.pdf), [JMA公式サイトの利用規約説明](https://www.data.jma.go.jp/mscweb/en/general/note.html), [JMA過去データの注意事項](https://www.data.jma.go.jp/risk/obsdl/top/attention.html)

## GPM IMERG

NASA Earthdataの公式資料は、NASA Earth Science dataの全面的・公開共有方針を示している。GES DISCのIMERG V07データセットページには、公式データ引用情報とDOI `10.5067/GPM/IMERGDF/DAY/07`が記載されている。ローカルCSVの元ファイル名はIMERG V07Bの30分プロダクト形式であるため、公開前に日次V07ページではなく、該当する30分V07Bコレクションの公式landing page・DOI・利用条件へ照合する必要がある。

暫定判定：**NASAの公開方針から再利用可能性は高いが、今回のV07B 30分コレクションに直接対応する公式メタデータと引用情報を確認するまで、CSV再配布を確定しない。**

Sources: [GES DISC IMERG V07 dataset page](https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGDF_07/summary?keywords=imerg), [NASA Earthdata open data guidance](https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance), [Earthdata use-constraints guidance](https://wiki.earthdata.nasa.gov/spaces/CMR/pages/121311158/Use%2BConstraints)

## 公開判断

コードと再現手順は公開準備済み。入力CSVは、JMAは出典・加工表示を付した派生データとして、GPMは該当V07Bコレクションの公式条件・引用を確認した後に公開可否を決定する。確認前は、取得手順とSHA-256のみを公開する。
