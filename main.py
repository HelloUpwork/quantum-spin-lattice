from app import App
import numpy as np
import pickle

app = App()

app.set_lattice_parameters(2, 2)
app.set_action_parameters(1.0, 0.3)
app.run_simulation()
# app.sweep(64)
# results = np.zeros((64, 64))
# for j1_idx in range(0, 64):
#     for j2_idx in range(0, 64):
#         j1 = -1.0 + j1_idx*(2/64)
#         j2 = -1.0 + j2_idx*(2/64)
#         app.set_action_parameters(j1, j2)
#         app.run_simulation()
#         results[j1_idx][j2_idx] = app.get_ground_state_energy()
#         print(f"For J1={j1}, J2={j2}: Ground State Energy = {app.get_ground_state_energy()}")

# filename = 'simulation_results.pkl'
# with open(filename, 'wb') as file:
#     pickle.dump(results, file)