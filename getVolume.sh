#!/bin/bash
vol=$(awk '/%/ {gsub(/[\[\]]/,""); print $4}' <(amixer sget $1))
echo $vol