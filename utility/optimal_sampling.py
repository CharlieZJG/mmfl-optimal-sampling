import torch
import numpy as np
import random

def get_gradient_norm(weights_this_round, weights_next_round):
    # get gradient by subtracting weights_next_round from weights_this_round
    weight_diff = {name: (weights_this_round[name] - weights_next_round[name]).cpu() for name in weights_this_round}
    # Calculate the L2 norm of the weight differences
    norm = sum(torch.norm(diff, p=2) ** 2 for diff in weight_diff.values()) ** 0.5
    norm.item()
    return norm.item(), weight_diff
def get_optimal_sampling(chosen_clients, clients_task, all_data_num, gradient_record):
    # gradient_record: the shape is [task_index][client_index]
    # chosen_clients provide the index of the chosen clients in a random order
    # clients_task has the same order as chosen_clients
    # multiple tasks sampling will degenerate to single task sampling when task=1
    # therefore we can use the same function.
    if type(clients_task) == list:
        clients_task = np.array(clients_task)
    sample_num = len(chosen_clients)  # m in the paper
    tasks_num = len(gradient_record)
    # random.shuffle(task_indices) # make task order random
    all_clients_num = len(gradient_record[0])

    all_gradients = gradient_record.copy()

    for task_index in range(tasks_num):
        for client_index in range(all_clients_num):
        # from U to U~ in the paper
            all_gradients[task_index][client_index] *= all_data_num[task_index][client_index] / np.sum(
            all_data_num[task_index])

    client_gradients_sumTasks = np.zeros(all_clients_num) # this is M_i in the proof
    for client_index in range(all_clients_num):
        for task_index in range(tasks_num):
            client_gradients_sumTasks[client_index] += all_gradients[task_index][client_index]

    # sort the gradients of the clients for this task, get a list of indices
    sorted_indices = np.argsort(client_gradients_sumTasks)

    n = all_clients_num
    m = sample_num

    l = n - m + 1
    best_l = l
    if m == 0: # if m=0, we get best_l = n+1 above, which is wrong. how to solve?
        best_l = n

    while True:
        l += 1
        if l > n:
            break
        # sum the first l smallest gradients
        sum_upto_l = sum(client_gradients_sumTasks[sorted_indices[i]] for i in range(l))
        upper = sum_upto_l / client_gradients_sumTasks[sorted_indices[l-1]]
        # if 0<m+l-n<=upper, then this l is good. find the largest l satisfying this condition
        if 0 < m + l - n <= upper:
            best_l = l
    # compute p
    p_s_i = np.zeros((tasks_num, all_clients_num))
    sum_upto_l = sum(client_gradients_sumTasks[sorted_indices[i]] for i in range(best_l))
    # print('sum_upto_l', sum_upto_l)
    for i in range(len(sorted_indices)):
        if i >= best_l:
            for task_index in range(tasks_num):
                p_s_i[task_index][sorted_indices[i]] = all_gradients[task_index][sorted_indices[i]] / client_gradients_sumTasks[sorted_indices[i]]
        else:
            for task_index in range(tasks_num):
                p_s_i[task_index][sorted_indices[i]] = (m + best_l - n) * all_gradients[task_index][sorted_indices[i]] / sum_upto_l


    # below is unfinished
    allocation_result = np.zeros(all_clients_num, dtype=int)
    for client_idx in range(all_clients_num):
        if abs(1-np.sum(p_s_i[:, client_idx])) < 1e-6:
            p_not_choose = 0
        else:
            p_not_choose = 1 - np.sum(p_s_i[:, client_idx])
        # append p_not_choose to the head of p_s_i
        p_client = np.zeros(tasks_num+1)
        p_client[0] = p_not_choose
        p_client[1:] = p_s_i[:, client_idx]
        allocation_result[client_idx] = np.random.choice(np.arange(-1, tasks_num), p=p_client)
    allocation_result = allocation_result.tolist()
    clients_task = [s for s in allocation_result if s != -1]
    chosen_clients = [i for i in range(len(allocation_result)) if allocation_result[i] != -1]
    # get p_dict
    p_dict = []
    for task_index in range(tasks_num):
        p_dict.append([p_s_i[task_index][i] for i in range(all_clients_num) if allocation_result[i] == task_index])

    return clients_task, p_dict, chosen_clients

def get_clients_num_per_task(clients_task, tasks_num):
    clients_num_per_task = [0] * tasks_num # list with length of tasks_num
    for task_index in range(tasks_num):
        # count the number of clients for each task
        clients_num_per_task[task_index] = clients_task.tolist().count(task_index)
    return clients_num_per_task

