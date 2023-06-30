set smac=65-PIN3/src/solver/smac/runner_smac.py
set irace=65-PIN3/src/solver/irace/starter.py
set baseline=65-PIN3/src/solver/rs/baseline.py

@REM python <solver> <net> <maxExperiments> <ExportToCsv> <Instances>

python %smac% nd 100 True
python %smac% nd 200 True
python %smac% nd 300 True
python %smac% nd 400 True
python %smac% nd 500 True
python %baseline% nd 100 True
python %baseline% nd 200 True
python %baseline% nd 300 True
python %baseline% nd 400 True
python %baseline% nd 500 True
python %irace% nd 180 True
python %irace% nd 200 True
python %irace% nd 300 True
python %irace% nd 400 True
python %irace% nd 500 True