#!/bin/bash
# test bayesian in noniid
# try to avoid poor training (take out mnist)

python main.py --exp_num 1 --C 1.0 --num_clients 20 --class_ratio 0.3 0.3 0.3 --iid_type noniid noniid noniid --task_type cifar10 fashion_mnist emnist --algo_type proposed --seed 15 --notes exp4C1c20d1.0-seed15-o-alpha-le1-lr1.0 --cpumodel --optimal_sampling --local_epochs 1 1 1 --round_num 600 --insist --lr 1.0
python main.py --exp_num 1 --C 1.0 --num_clients 20 --class_ratio 0.3 0.3 0.3 --iid_type noniid noniid noniid --task_type cifar10 fashion_mnist emnist --algo_type proposed --seed 15 --notes exp4C1c20d1.0-seed15-o-alpha-le1-lr0.5 --cpumodel --optimal_sampling --local_epochs 1 1 1 --round_num 600 --insist --lr 0.5
python main.py --exp_num 1 --C 1.0 --num_clients 20 --class_ratio 0.3 0.3 0.3 --iid_type noniid noniid noniid --task_type cifar10 fashion_mnist emnist --algo_type proposed --seed 15 --notes exp4C1c20d1.0-seed15-o-alpha-le1-lr0.3 --cpumodel --optimal_sampling --local_epochs 1 1 1 --round_num 600 --insist --lr 0.3
python main.py --exp_num 1 --C 1.0 --num_clients 20 --class_ratio 0.3 0.3 0.3 --iid_type noniid noniid noniid --task_type cifar10 fashion_mnist emnist --algo_type proposed --seed 15 --notes exp4C1c20d1.0-seed15-o-alpha-le1-lr0.1 --cpumodel --optimal_sampling --local_epochs 1 1 1 --round_num 600 --insist --lr 0.1
python main.py --exp_num 1 --C 1.0 --num_clients 20 --class_ratio 0.3 0.3 0.3 --iid_type noniid noniid noniid --task_type cifar10 fashion_mnist emnist --algo_type proposed --seed 15 --notes exp4C1c20d1.0-seed15-o-alpha-le2-lr0.3 --cpumodel --optimal_sampling --local_epochs 2 2 2 --round_num 300 --insist --lr 0.3
python main.py --exp_num 1 --C 1.0 --num_clients 20 --class_ratio 0.3 0.3 0.3 --iid_type noniid noniid noniid --task_type cifar10 fashion_mnist emnist --algo_type proposed --seed 15 --notes exp4C1c20d1.0-seed15-o-alpha-le2-lr0.1 --cpumodel --optimal_sampling --local_epochs 2 2 2 --round_num 300 --insist --lr 0.1