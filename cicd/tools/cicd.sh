#!/bin/bash

RESULT=""
          for n in ${{ steps.files.outputs.added_modified }}; do
            if [[ "$n" =~ \.py$ ]]; then
              RESULT="$RESULT $n";
            fi
          done
          echo "::set-output name=python_files::$RESULT"