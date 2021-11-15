\ Model Production
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  X[0] + 2 X[1]
Subject To
 vincolo_materiali_P1: 2 X[0] + 5 X[1] >= 20
 vincolo_materiali_P2: X[0] + X[1] <= 7
 vincolo_tecnologico_1: X[0] - 4 X[1] <= 0
 vincolo_tecnologico_2: 2 X[0] - X[1] >= 0
Bounds
Generals
 X[0] X[1]
End
