import pulp as pl

# Dados
item_sizes = [4, 8, 1, 4, 2, 1]
num_items = len(item_sizes)
bin_capacity = 10
max_bins = num_items  # no pior caso, 1 item por bin

# Modelo
model = pl.LpProblem("BinPacking-Mathematical", pl.LpMinimize)

# Variáveis
x = pl.LpVariable.dicts("x", ((i, j) for i in range(num_items) for j in range(max_bins)), cat="Binary")
y = pl.LpVariable.dicts("y", (j for j in range(max_bins)), cat="Binary")

# Função objetivo
model += pl.lpSum(y[j] for j in range(max_bins))

# Restrição 1: cada item deve ser alocado a um bin
for i in range(num_items):
    model += pl.lpSum(x[i, j] for j in range(max_bins)) == 1

# Restrição 2: capacidade dos bins
for j in range(max_bins):
    model += pl.lpSum(item_sizes[i] * x[i, j] for i in range(num_items)) <= bin_capacity * y[j]

# ✅ Exportar modelo para arquivo LP (texto legível)
model.writeLP("bin_packing_model.lp")

print("Modelo exportado como 'bin_packing_model.lp'.")

# Resolver
model.solve()

# Resultado
print(f"Status: {pl.LpStatus[model.status]}")
for j in range(max_bins):
    if pl.value(y[j]) > 0.5:
        items_in_bin = [i for i in range(num_items) if pl.value(x[i, j]) > 0.5]
        print(f"Bin {j}: Items {items_in_bin}")