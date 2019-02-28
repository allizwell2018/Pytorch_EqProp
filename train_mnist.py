"""
Train MNIST
"""
import torch
from ep_mlp import EPMLP
from fp_solver import FixedStepSolver

model = EPMLP(784, 10, [200], torch.sigmoid)
solver = FixedStepSolver(step_size=0.01, max_steps=100)
opt = torch.optim.Adam(model.parameters(), lr=0.001)

# A batch of data
bsz = 10
imgs = torch.rand(bsz, 784)
labels = torch.FloatTensor(bsz, 10).zero_().scatter_(1, torch.randint(10, [bsz, 1]), 1)

if __name__ == '__main__':
    for _ in range(200000):
        free_states = model.free_phase(imgs, solver)
        cost = model.get_cost(free_states, labels)
        print(torch.sum(cost).item())
        clamp_states = model.clamp_phase(imgs, labels, solver, 10,
                                         out=free_states[-1],
                                         hidden_units=free_states[:-1])

        # update
        opt.zero_grad()
        model.set_gradients(imgs, free_states, clamp_states)
        opt.step()



