from sympy import symbols, diff, pi, Abs, N, sqrt

# Declarar las variables simbólicas
f39P, f220K, fcolp, C39P, C220K, fmed = symbols('f39P f220K fcolp C39P C220K fmed')
error_f39P, error_f220K, error_fmed, error_C39P, error_C220K = symbols('error_f39P error_f220K error_fmed error_C39P error_C220K')

# Fórmula de C_colp
C_colp = (f39P**2 * C39P - f220K**2 * C220K) / (f220K**2 - f39P**2)

# Derivadas de C_colp
dC_df39P = diff(C_colp, f39P)
dC_df220K = diff(C_colp, f220K)
dC_dC39P = diff(C_colp, C39P)
dC_dC220K = diff(C_colp, C220K)

# Fórmula de error (ponderación de incertidumbres) para C_colp
error_C_colp = sqrt(
    (Abs(dC_df39P * error_f39P))**2 +
    (Abs(dC_df220K * error_f220K))**2 +
    (Abs(dC_dC39P * error_C39P))**2 +
    (Abs(dC_dC220K * error_C220K))**2
)

# Mostrar incertidumbres parciales de C_colp
print("\nIncertidumbres parciales de C_colp:")
uncertainty_dC_df39P = Abs(dC_df39P * error_f39P)
print("Abs(dC_df39P * error_f39P) =", uncertainty_dC_df39P)

uncertainty_dC_df220K = Abs(dC_df220K * error_f220K)
print("Abs(dC_df220K * error_f220K) =", uncertainty_dC_df220K)

uncertainty_dC_dC39P = Abs(dC_dC39P * error_C39P)
print("Abs(dC_dC39P * error_C39P) =", uncertainty_dC_dC39P)

uncertainty_dC_dC220K = Abs(dC_dC220K * error_C220K)
print("Abs(dC_dC220K * error_C220K) =", uncertainty_dC_dC220K)

print("\nError total de C_colp (simbólico):", error_C_colp)

# Sustitución de valores numéricos para C_colp
valores = {
    f39P: 1566089.2,
    f220K: 1578237.2,
    C39P: 39.7641675333333e-12,
    C220K: 23.6312625e-12,
    error_f39P: 38,
    error_f220K: 56,
    error_C39P: 0.000472949999999084e-12,
    error_C220K: 0.00174344999999948e-12,
    fmed: 1566115.6,
    error_fmed: 29
}

C_colp_num = N(C_colp.subs(valores))
print("\nC_colp numérico:", C_colp_num)

uncertainty_dC_df39P_num = N(uncertainty_dC_df39P.subs(valores))
print("Abs(dC_df39P * error_f39P) numérico:", uncertainty_dC_df39P_num)

uncertainty_dC_df220K_num = N(uncertainty_dC_df220K.subs(valores))
print("Abs(dC_df220K * error_f220K) numérico:", uncertainty_dC_df220K_num)

uncertainty_dC_dC39P_num = N(uncertainty_dC_dC39P.subs(valores))
print("Abs(dC_dC39P * error_C39P) numérico:", uncertainty_dC_dC39P_num)

uncertainty_dC_dC220K_num = N(uncertainty_dC_dC220K.subs(valores))
print("Abs(dC_dC220K * error_C220K) numérico:", uncertainty_dC_dC220K_num)

error_C_colp_num = N(error_C_colp.subs(valores))
print("\nError total de C_colp numérico:", error_C_colp_num)

# Fórmula de L
C_colp_val = symbols('C_colp_val')
error_C_colp_val = symbols('error_C_colp_val')
L = 1 / ((2 * pi * f220K)**2 * (C_colp_val + C220K))

# Derivadas de L
dL_df220k = diff(L, f220K)
dL_dCcolp = diff(L, C_colp_val)
dL_dC220k = diff(L, C220K)

# Fórmula de error en L
error_L = sqrt(
    (Abs(dL_df220k * error_f220K))**2 +
    (Abs(dL_dCcolp * error_C_colp_val))**2 +
    (Abs(dL_dC220k * error_C220K))**2
)

# Mostrar incertidumbres parciales de L
print("\nIncertidumbres parciales de L:")
uncertainty_dL_df220k = Abs(dL_df220k * error_f220K)
print("Abs(dL/df220K * error_f220K) =", uncertainty_dL_df220k)

uncertainty_dL_dCcolp = Abs(dL_dCcolp * error_C_colp_val)
print("Abs(dL/dC_colp * error_C_colp_val) =", uncertainty_dL_dCcolp)

uncertainty_dL_dC220k = Abs(dL_dC220k * error_C220K)
print("Abs(dL/dC220K * error_C220K) =", uncertainty_dL_dC220k)

print("\nError total de L (simbólico):", error_L)

# Añadir valores numéricos de C_colp y su error al diccionario
valores.update({C_colp_val: C_colp_num, error_C_colp_val: error_C_colp_num})

# Sustitución de valores numéricos para L
L_num = N(L.subs(valores))
print("\nL numérico:", L_num)

uncertainty_dL_df220k_num = N(uncertainty_dL_df220k.subs(valores))
print("Abs(dL/df220K * error_f220K) numérico:", uncertainty_dL_df220k_num)

uncertainty_dL_dCcolp_num = N(uncertainty_dL_dCcolp.subs(valores))
print("Abs(dL/dC_colp * error_C_colp_val) numérico:", uncertainty_dL_dCcolp_num)

uncertainty_dL_dC220k_num = N(uncertainty_dL_dC220k.subs(valores))
print("Abs(dL/dC220K * error_C220K) numérico:", uncertainty_dL_dC220k_num)

error_L_num = N(error_L.subs(valores))
print("\nError total de L numérico:", error_L_num)

# Calcular Cmed y su error
L_sym = symbols('L')
# L_num = 10e-6
valores.update({L_sym: L_num})

# Fórmula de C_med
C_med = 1 / ((2 * pi * fmed)**2 * L_sym)

# Derivadas de C_colp
dCmed_dfmed = diff(C_med, fmed)
dCmed_dL = diff(C_med, L_sym)

#error_L = 300e-12

# Fórmula de error (ponderación de incertidumbres) para C_med
error_C_med = sqrt(
    (Abs(dCmed_dfmed * error_fmed))**2 +
    (Abs(dCmed_dL * error_L))**2
)

# Mostrar incertidumbres parciales de C_med
print("\nIncertidumbres parciales de C_med:")
uncertainty_dCmed_dfmed = Abs(dCmed_dfmed * error_fmed)
print("\nAbs(dCmed_dfmed * error_fmed) =", uncertainty_dCmed_dfmed)

print("\nDerivada respecto a L")
print("\nAbs(dCmed_dL) =", dCmed_dL)
uncertainty_dCmed_dL = Abs(dCmed_dL * error_L)
print("\nAbs(dCmed_dL * error_L) =", uncertainty_dCmed_dL)

print("\nError total de C_med (simbólico):", error_C_med)

# Sustitución de valores numéricos para C_med
C_med_num = N(C_med.subs(valores))
print("\nC_med numérico:", C_med_num)

print("\nC_med - C_colp numérico:", C_med_num - C_colp_num)

uncertainty_dCmed_dfmed_num = N(uncertainty_dCmed_dfmed.subs(valores))
print("\nAbs(dCmed_dfmed * error_fmed) numérico:", uncertainty_dCmed_dfmed_num)

uncertainty_dCmed_dL_num = N(uncertainty_dCmed_dL.subs(valores))
print("\nAbs(dCmed_dL * error_L) numérico:", uncertainty_dCmed_dL_num)

error_C_med_num = N(error_C_med.subs(valores))
print("\nError total de C_med numérico:", error_C_med_num)
print("Error total de C_colp numérico:", error_C_colp_num)

print("\nError total de C_med + Error C_colp numérico:", sqrt(error_C_med_num**2 + error_C_colp_num**2))