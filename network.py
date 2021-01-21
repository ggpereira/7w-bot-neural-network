import torch 
import torch.nn as nn 
import torch.nn.functional as F
from sklearn import preprocessing
from pickle import load 


class Network(nn.Module):
    def __init__(self, inputs, h_neurons, outputs, activation):
        super(Network, self).__init__()
        self.dense0 = nn.Linear(inputs, h_neurons)
        self.activation0 = activation 
        self.dense1 = nn.Linear(h_neurons, h_neurons)
        self.activation1 = activation 
        self.dense4 = nn.Linear(h_neurons, outputs)


    def forward(self, x):
        x = self.dense0(x)
        x = self.activation0(x)
        x = self.dense1(x)
        x = self.activation1(x)
        x = self.dense4(x) 

        return x

# CARD IDS AGE 1 
CARDS_AGE1 = [1, 2, 3, 4, 7, 8, 15, 16, 17, 18, 19, 21, 32, 33, 34, 43, 44, 45, 54, 55, 56]

# CARD IDS AGE 2 
CARDS_AGE2 = [11, 12, 13, 14, 15, 16, 17, 22, 23, 24, 25, 35, 36, 37, 46, 48, 49, 57, 58, 59, 60]

# CARD IDS AGE 3
CARDS_AGE3 = [26, 27, 28, 29, 30, 39, 40, 42, 50, 52, 53, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75]

# AGE 1 NETWORK LABELS
AGE1_LABELS = [101, 102, 103, 104, 107, 108, 115, 116, 117, 118, 119, 121, 132, 133, 134, 143, 144, 145, 154, 155, 156, 
               201, 202, 203, 204, 207, 208, 215, 216, 217, 218, 219, 221, 232, 233, 234, 243, 244, 245, 254, 255, 256, 
               301, 302, 303, 304, 307, 308, 315, 316, 317, 318, 319, 321, 332, 333, 334, 343, 344, 345, 354, 355, 356]

# AGE 2 NETWORK LABELS
AGE2_LABELS = [111, 112, 113, 114, 115, 116, 117, 122, 123, 124, 125, 135, 136, 137, 146, 148, 149, 157, 158, 159, 160, 
               211, 212, 213, 214, 215, 216, 217, 222, 223, 224, 225, 235, 236, 237, 246, 248, 249, 257, 258, 259, 260,
               311, 312, 313, 314, 315, 316, 317, 322, 323, 324, 325, 335, 336, 337, 346, 348, 349, 357, 358, 359, 360]

# AGE 3 NETWORK LABELS
AGE3_LABELS = [126, 127, 128, 129, 130, 139, 140, 142, 150, 152, 153, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175,
               226, 227, 228, 229, 230, 239, 240, 242, 250, 252, 253, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 
               326, 327, 328, 329, 330, 339, 340, 342, 350, 352, 353, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375]


ModelAge1 = Network(32, 80, len(AGE1_LABELS), F.relu)
ModelAge1.load_state_dict(torch.load("./model/model_age1_net1_lr0001_relu.pth"))
ModelAge1.eval()

ModelAge2 = Network(32, 80, len(AGE2_LABELS), F.relu)
ModelAge2.load_state_dict(torch.load("./model/model_age2_net2_lr0001_relu.pth"))
ModelAge2.eval()

ModelAge3 = Network(37, 90, len(AGE3_LABELS), F.relu) 
ModelAge3.load_state_dict(torch.load("./model/model_age3_net3_lr0001_relu.pth")) 
ModelAge3.eval()


def transform_input(data, age):
    inputs = []
    if age == 1:
        inputs = transform_input_age1(data)
    elif age == 2:
        inputs = transform_input_age2(data) 
    elif age == 3:
        inputs = transform_input_age3(data)

    inputs = torch.tensor(inputs, dtype=torch.float)

    return inputs 


def transform_input_age1(data):
    encoder = preprocessing.LabelEncoder()
    encoder = encoder.fit(CARDS_AGE1)
    t_row = []
    resource_neurons = []

    # initialize card neurons with zeros
    cards_neurons = [0 for i in range(len(CARDS_AGE1))]
    
    for id in data["cards_hand_id"]: 
        index = encoder.transform([id])[0]
        cards_neurons[index] = 1

    resource_neurons.append(data["amount"]["civilian"])
    resource_neurons.append(data["amount"]["military"])
    resource_neurons.append(data["amount"]["commercial"])
    resource_neurons.append(data["amount"]["raw_material"])
    resource_neurons.append(data["amount"]["manufactured_goods"])
    resource_neurons.append(data["amount"]["scientific"])
    resource_neurons.append(data["amount"]["guild"])
    resource_neurons.append(data["wonder_id"])
    resource_neurons.append(data["wonder_stage"])
    resource_neurons.append(data["resources"]["shields"])

    coins = 0 
    if data["resources"]["coins"] <= 2:
        coins = 1
    elif data["resources"]["coins"] <= 4:
        coins = 2 
    else:
        coins = 3

    resource_neurons.append(coins)

    scaler = load(open("./scaler/scaler_age1.pkl", "rb"))
    resource_neurons = scaler.transform([resource_neurons])
    
    t_row.extend(cards_neurons)
    t_row.extend(resource_neurons[0])

    return t_row    


def transform_input_age2(data):
    encoder = preprocessing.LabelEncoder()
    encoder = encoder.fit(CARDS_AGE2)
    t_row = []
    resource_neurons = []

    # initialize card neurons with zeros
    cards_neurons = [0 for i in range(len(CARDS_AGE2))]
    
    for id in data["cards_hand_id"]: 
        index = encoder.transform([id])[0]
        cards_neurons[index] = 1

    resource_neurons.append(data["amount"]["civilian"])
    resource_neurons.append(data["amount"]["military"])
    resource_neurons.append(data["amount"]["commercial"])
    resource_neurons.append(data["amount"]["raw_material"])
    resource_neurons.append(data["amount"]["manufactured_goods"])
    resource_neurons.append(data["amount"]["scientific"])
    resource_neurons.append(data["amount"]["guild"])
    resource_neurons.append(data["wonder_id"])
    resource_neurons.append(data["wonder_stage"])
    resource_neurons.append(data["resources"]["shields"])

    coins = 0 
    if data["resources"]["coins"] <= 2:
        coins = 1
    elif data["resources"]["coins"] <= 4:
        coins = 2 
    else:
        coins = 3

    resource_neurons.append(coins)

    scaler = load(open("./scaler/scaler_age2.pkl", "rb"))
    resource_neurons = scaler.transform([resource_neurons])
    
    t_row.extend(cards_neurons)
    t_row.extend(resource_neurons[0])

    return t_row    


def transform_input_age3(data):
    encoder = preprocessing.LabelEncoder()
    encoder = encoder.fit(CARDS_AGE3)
    t_row = []
    resource_neurons = []

    # initialize card neurons with zeros
    cards_neurons = [0 for i in range(len(CARDS_AGE3))]
    
    for id in data["cards_hand_id"]: 
        index = encoder.transform([id])[0]
        cards_neurons[index] = 1

    resource_neurons.append(data["amount"]["civilian"])
    resource_neurons.append(data["amount"]["military"])
    resource_neurons.append(data["amount"]["commercial"])
    resource_neurons.append(data["amount"]["raw_material"])
    resource_neurons.append(data["amount"]["manufactured_goods"])
    resource_neurons.append(data["amount"]["scientific"])
    resource_neurons.append(data["amount"]["guild"])
    resource_neurons.append(data["wonder_id"])
    resource_neurons.append(data["wonder_stage"])
    resource_neurons.append(data["resources"]["shields"])

    coins = 0 
    if data["resources"]["coins"] <= 2:
        coins = 1
    elif data["resources"]["coins"] <= 4:
        coins = 2 
    else:
        coins = 3

    resource_neurons.append(coins)

    scaler = load(open("./scaler/scaler_age3.pkl", "rb"))
    resource_neurons = scaler.transform([resource_neurons])
    
    t_row.extend(cards_neurons)
    t_row.extend(resource_neurons[0])

    return t_row


def run(inputs, age):
    print('AGE: {}'.format(age))
    label = -1
    if age == 1:
        label = run_age1(inputs)
    elif age == 2:
        label = run_age2(inputs)
    elif age == 3:
        label = run_age3(inputs )
    return label


def run_age1(inputs):
    output = ModelAge1(inputs)
    probs = F.softmax(output)
    _, top_class = probs.topk(k = len(AGE1_LABELS))

    print('OUTPUT: {}'.format(top_class))

    labelencoder = preprocessing.LabelEncoder()
    labelencoder.fit(AGE1_LABELS)
    sorted_labels = labelencoder.inverse_transform(top_class)

    print('OUTPUT TRANSFORMED: {}'.format(sorted_labels))

    return sorted_labels


def run_age2(inputs):
    output = ModelAge2(inputs)
    probs = F.softmax(output)
    _, top_class = probs.topk(k = len(AGE2_LABELS))

    print('OUTPUT: {}'.format(top_class))

    labelencoder = preprocessing.LabelEncoder()
    labelencoder.fit(AGE2_LABELS)
    sorted_labels = labelencoder.inverse_transform(top_class)

    print('OUTPUT TRANSFORMED: {}'.format(sorted_labels))

    return sorted_labels 


def run_age3(inputs):
    output = ModelAge3(inputs)
    probs = F.softmax(output)
    _, top_class = probs.topk(k = len(AGE3_LABELS))

    labelencoder = preprocessing.LabelEncoder()

    print('OUTPUT: {}'.format(top_class))

    labelencoder.fit(AGE3_LABELS)
    sorted_labels = labelencoder.inverse_transform(top_class)

    print('OUTPUT TRANSFORMED: {}'.format(sorted_labels))

    return sorted_labels 