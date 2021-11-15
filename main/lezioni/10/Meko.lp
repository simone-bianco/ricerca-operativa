\ Model Meko
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  540 X[0] + 590 X[1]
Subject To
 ore_per_tonnellata[0]: 0.72 X[0] + 0.85 X[1] <= 18
 ore_per_tonnellata[1]: 1.68 X[0] + 1.42 X[1] <= 18
 ore_per_tonnellata[2]: 1.92 X[0] + 2.12 X[1] <= 16
Bounds
End
