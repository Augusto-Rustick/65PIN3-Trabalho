set smac=65-PIN3/src/solver/smac/runner_smac.py
set irace=65-PIN3/src/solver/irace/starter.py
set baseline=65-PIN3/src/solver/irace/starter.py


@REM python <solver> <net> <maxExperiments> <ExportToCsv> <Instances>

python %smac% nd 50 True
python %baseline% nd 50 True
python %irace% nd 180 True