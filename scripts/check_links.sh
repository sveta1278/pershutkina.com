#!/usr/bin/env bash
# Проверяет все ссылки <a href> во всех HTML-файлах сайта.
# Внешние ссылки: код ответа после редиректов. Внутренние: существует ли файл и якорь.
# Запуск из корня репозитория: bash scripts/check_links.sh
set -u
cd "$(dirname "$0")/.."

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
fail=0
checked=""

for page in $(find . -name '*.html' -not -path './node_modules/*' | sort); do
  dir=$(dirname "$page")
  for href in $(grep -oE '<a [^>]*href="[^"]+"' "$page" | sed -E 's/.*href="([^"]*)"$/\1/' | sed 's/&amp;/\&/g' | sort -u); do
    case "$href" in
      mailto:*)
        echo "OK    mailto        $page -> $href" ;;
      http://*|https://*)
        case " $checked " in *" $href "*) continue ;; esac
        checked="$checked $href"
        code=$(curl -s -o /dev/null -L -m 25 -A "$UA" -w '%{http_code}' "$href")
        case "$code" in
          200) echo "OK    $code           $href" ;;
          999) echo "OK?   $code (LinkedIn blocks bots, check by hand) $href" ;;
          403) echo "OK?   $code (bot protection, check in a browser) $href" ;;
          *)   echo "FAIL  $code           $href"; fail=1 ;;
        esac ;;
      *)
        path="${href%%#*}"; anchor=""
        [[ "$href" == *"#"* ]] && anchor="${href#*#}"
        if [ -z "$path" ]; then target="$page"
        elif [[ "$path" == /* ]]; then target=".$path"
        else target="$dir/$path"; fi
        [ -d "$target" ] && target="${target%/}/index.html"
        if [ ! -f "$target" ]; then
          echo "FAIL  missing file  $page -> $href"; fail=1
        elif [ -n "$anchor" ] && ! grep -q "id=\"$anchor\"" "$target"; then
          echo "FAIL  missing #$anchor  $page -> $href"; fail=1
        else
          echo "OK    local         $page -> $href"
        fi ;;
    esac
  done
done

[ "$fail" -eq 0 ] && echo "All links OK" || { echo "Some links are broken"; exit 1; }
