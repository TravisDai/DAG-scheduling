from env import CholeskyTaskGraph
from a2c import A2C
from a2c import *
from model import Net, SimpleNet, SimpleNet2, ResNetG, SimpleNetMax, SimpleNetW, SimpleNetWSage
from config import config_enhanced
from torch.utils.tensorboard import SummaryWriter
from log_utils import set_writer_dir, name_dir
import os

writer = SummaryWriter(os.path.join('runs', name_dir(config_enhanced)))

# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
# os.environ["CUDA_VISIBLE_DEVICES"] = config_enhanced["GPU_id"]

print("Current config_enhanced is:")
pprint(config_enhanced)
writer.add_text("config", str(config_enhanced))

env = CholeskyTaskGraph(**config_enhanced['env_settings'])
# env.reset()

# model = Net
model = SimpleNet
# model = SimpleNetW
# model = ResNetG
# model = SimpleNetWSage

# model = SimpleNetMax

res = []
means = []
mean_bests = []
for _ in range(10):
    config_enhanced["seed"] += 1
    agent = A2C(config_enhanced, env, model=model, writer=writer)

    # rewards = Parallel(n_jobs=config_enhanced['num_cores'])(
    #     delayed(wrap_non_picklable_objects(agent.training_batch))(config_enhanced['epochs'],
    #                          config_enhanced['nbatch']) for i in range(config_enhanced['num_cores']))

    s, m, cur_best = agent.training_batch()
    res.append(s)
    means.append(m)
    mean_bests.append(cur_best)
print(res)
print(means)
print(mean_bests)
# TODO : evaluate test_mode and save if best than previous
# TODO: Transfer ?
# ToDo : load training batch during GPU training