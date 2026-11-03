#!/usr/bin/env bash
# 把部署包推到 Windows 虚拟机的 C:\Users\Public\（通过 UTM guest agent）
#
# 为什么是 push 而不是 exec：
#   utmctl file push/pull 可用，utmctl exec 在 UTM 5.0.8 + Windows guest 上静默失败
#   （返回码永远 0、命令没执行）。所以流程是「我推文件，人在 guest 里双击 bat」。
set -euo pipefail
VM="${VM:-Win10-LTSC}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXCEL="$ROOT/mod/data/global/excel"
DEST='C:\Users\Public'

command -v utmctl >/dev/null || { echo "找不到 utmctl"; exit 1; }
[ "$(utmctl status "$VM")" = "started" ] || { echo "VM $VM 没在运行（utmctl start $VM）"; exit 1; }

push() { utmctl file push "$VM" "$DEST\\$2" < "$1"; echo "  ↑ $2"; }

echo "推送脚本："
for f in "$ROOT"/deploy/windows/*; do push "$f" "d2_$(basename "$f")"; done

echo "推送数据表（CubeMain 故意不推）："
for t in Hireling MonStats Runes SetItems Skills TreasureClassEx UniqueItems; do
  push "$EXCEL/$t.txt" "d2_$t.txt"
done

echo
echo "完成。在 Windows 里打开 $DEST 双击 d2_00_set_path.bat"
