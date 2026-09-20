import torch
import torch.nn as nn
import torch.nn.functional as F

class SparseAutoencoder(nn.Module):
    def __init__(self, input_dim, latent_dim):
        super().__init__()
        self.encoder = nn.Linear(input_dim, latent_dim)
        self.decoder = nn.Linear(latent_dim, input_dim)

    def encode(self, x):
        return F.relu(self.encoder(x))

    def decode(self, z):
        return self.decoder(z)

    def forward(self, x):
        z = self.encode(x)
        x_hat = self.decode(z)
        return x_hat, z

class TopKSparseAutoencoder(nn.Module):
    def __init__(self, input_dim, latent_dim, k=32):
        super().__init__()
        self.k = k
        self.encoder = nn.Linear(input_dim, latent_dim)
        self.decoder = nn.Linear(latent_dim, input_dim)

    def encode(self, x):
        pre_acts = F.relu(self.encoder(x))
        topk_vals, topk_indices = torch.topk(pre_acts, self.k, dim=-1)
        z = torch.zeros_like(pre_acts)
        z.scatter_(-1, topk_indices, topk_vals)
        return z

    def decode(self, z):
        return self.decoder(z)

    def forward(self, x):
        z = self.encode(x)
        x_hat = self.decode(z)
        return x_hat, z

class GatedSparseAutoencoder(nn.Module):
    def __init__(self, input_dim, latent_dim):
        super().__init__()
        self.encoder_gate = nn.Linear(input_dim, latent_dim)
        self.encoder_mag = nn.Linear(input_dim, latent_dim)
        self.decoder = nn.Linear(latent_dim, input_dim)

    def encode(self, x):
        pi = self.encoder_gate(x)
        gate = (pi > 0).float()
        mag = F.relu(self.encoder_mag(x))
        return gate * mag

    def decode(self, z):
        return self.decoder(z)

    def forward(self, x):
        pi = self.encoder_gate(x)
        f_gate = F.relu(pi)
        gate = (pi > 0).float()
        mag = F.relu(self.encoder_mag(x))
        z = gate * mag
        x_hat = self.decoder(z)
        x_hat_gate = self.decoder(f_gate)
        return x_hat, z, x_hat_gate, f_gate

