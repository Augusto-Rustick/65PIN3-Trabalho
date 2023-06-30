set smac=65-PIN3/src/solver/smac/runner_smac.py
set irce=65-PIN3/src/solver/irace/starter.py
set bsln=65-PIN3/src/solver/rs/baseline.py

@REM python <solver> <net> <maxExperiments> <ExportToCsv> <Instances>

python %smac% nd 100 True
python %smac% nd 200 True
python %smac% nd 300 True
python %smac% nd 400 True
python %smac% nd 500 True

python %bsln% nd 100 True
python %bsln% nd 200 True
python %bsln% nd 300 True
python %bsln% nd 400 True
python %bsln% nd 500 True

python %irce% nd 180 True
python %irce% nd 200 True
python %irce% nd 300 True
python %irce% nd 400 True
python %irce% nd 500 True