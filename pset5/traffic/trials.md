TRIALS

# default from lecture

  ## Convolution layer
    32 filters
    relu activation
    3 by 3 kernal

  ## Max-pooling layer
    2 by 2 pool size

  # Flatten units

  # Hidden layer
    128 units
    relu activation
    50% dropout

  # Output layersoutput for all 43 signs
    43 output categories
    softmax activation

  # Compile neural network
    adam optimizer
    categorical crossentropy loss
    accuracy metrics

  # Results
    loss: 0.1323
    accuracy: 0.9664
    speed: 438 ms/epoch


# convolution layer 16 filters
    loss: 0.1630
    accuracy: 0.9643
    speed: 299 ms/epoch

# convolution layer 64 filters
    loss: 0.1463
    accuracy: 0.9631
    speed: 778 ms/epoch

# convolution layer filter size of 2 by 2
    loss: 0.3171
    accuracy: 0.9155
    speed: 409 ms/epoch

# convolution layer filter size of 9 by 9
    loss: 0.1220
    accuracy: 0.9717
    speed: 595 ms/epoch

# 0 convulution layers
    loss: 1.3308
    accuracy: 0.6464
    speed: 215 ms/epoch

# 2 convolution layers
    loss: 0.0643
    accuracy: 0.9864
    speed: 1 s/epoch

# 3 convolution layers
    loss: 0.0437
    accuracy: 0.9899
    speed: 2 s/epoch

# pooling size of 1 by 1
    loss: 0.1922
    accuracy: 0.9562
    speed: 1 s/epoch

# pooling size of 4 by 4
    loss: 0.2060
    accuracy: 0.9496
    speed: 322 ms/epoch

# 0 pooling layers
    loss: 0.1294
    accuracy: 0.9675
    speed: 785 ms/epoch

# 2 pooling layers
    loss: 0.2345
    accuracy: 0.9395
    speed: 348 s/epoch

# 3 pooling layers
    loss: 0.6552
    accuracy: 0.8094
    speed: 319 ms/epoch

# hidden layer with 64 units
    loss: 0.2785
    accuracy: 0.9306
    speed: 363 s/epoch

# hidden layer with 256 units
    loss: 0.1132
    accuracy: 0.9706
    speed: 548 ms/epoch

# hidden layer 25% dropout
    loss: 0.1164
    accuracy: 0.9718
    speed: 416 s/epoch

# hidden layer 75% dropout
    loss: 0.5642
    accuracy: 0.8482
    speed: 430 ms/epoch

# 0 hidden layers
    loss: 0.1368
    accuracy: 0.9752
    speed: 335 ms/epoch

# 2 hidden layers
    loss: 0.2804
    accuracy: 0.9400
    speed: 422 ms/epoch

# 3 hidden layers
    loss: 0.9013
    accuracy: 0.7227
    speed: 429 s/epoch























