\ Model esempio lezione 6: profilatti metallici
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  XA + XB
Subject To
 Vincolo_squadre: 3 XA + 6 XB <= 36
 Vincolo_produzione_giornaliera: XA + XB >= 4
 Vincolo_prima_tecnologia_1_2: XA - 2 XB <= 0
 Vincolo_seconda_tecnologia_2_1: - 2 XA + XB <= 0
 Vincolo_xA_positiva: XA >= 0
 Vincolo_xB_positiva: XB >= 0
Bounds
End
