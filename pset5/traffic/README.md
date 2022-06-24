CS50AI, PROBLEM SET 5 (TRAFFIC)
NEURAL NETWORK PARAMETER EXPLORATION

To test the parameters used in the convolutional neural network, a base run was 
performed using the defaults used in class (handwriting.py), and then the 
parameters were individually modified during subsequent runs to determine the 
effect on loss, accuracy and speed.

The default values used are as follows:
  convolutional layer: 32 filters, relu activation, 3*3 kernal, 1 layer
  pooling layer: 2*2 pool size, 1 layer
  hidden layer: 128 units, 50% dropout


The following table shows the effect of modifier the convolutional neural 
network parameters. Positive signs (+) and negative signs (-) were used to show 
increases or decreases, respectively, from the default values.

LAYER
  PARAMETER       LOSS      ACCURACY    SPEED

CONVOLUTIONAL
  LAYERS:
    0             1.3308+   0.6464-     215 MS/EPOCH-
    1 (DEFAULT)   0.1323    0.9664      438 MS/EPOCH
    2             0.0643-   0.9864+     1 S/EPOCH+
    3             0.0437-   0.9899+     2 S/EPOCH+
  FILTERS:
    16            0.1630+   0.9643-     299 MS/EPOCH-
    32 (DEFAULT)  0.1323    0.9664      438 MS/EPOCH
    64            0.1463+   0.9631-     778 MS/EPOCH+
  FILTER SIZE:
    2*2           0.3171+   0.9155-     409 MS/EPOCH-
    3*3 (DEFAULT) 0.1323    0.9664      438 MS/EPOCH
    9*9           0.1220-   0.9717+     595 MS/EPOCH+

POOLING
  LAYERS:
    0             0.1294-   0.9675+     785 MS/EPOCH+
    1 (DEFAULT)   0.1323    0.9664      438 MS/EPOCH
    2             0.2345+   0.9395-     348 MS/EPOCH-
    3             0.6552+   0.8094-     319 MS/EPOCH-
  POOL SIZE:
    1*1           0.1922+   0.9562-     1 S/EPOCH+
    2*2 (DEFAULT) 0.1323    0.9664      438 MS/EPOCH
    4*4           0.2060+   0.9496-     322 MS/EPOCH-

HIDDEN
  LAYERS:
    0             0.1368+   0.9752+     335 MS/EPOCH-
    1 (DEFAULT)   0.1323    0.9664      438 MS/EPOCH
    2             0.2804+   0.9400-     422 MS/EPOCH-
    3             0.9013+   0.7227-     429 MS/EPOCH-
  UNITS:
    64            0.2785+   0.9306-     363 MS/EPOCH-
    128 (DEFAULT) 0.1323    0.9664      438 MS/EPOCH
    256           0.1132-   0.9706+     548 MS/EPOCH+
  DROPOUT:
    25%           0.1164-   0.9718+     416 MS/EPOCH-
    50% (DEFAULT) 0.1323    0.9664      438 MS/EPOCH
    75%           0.5642+   0.8482-     430 MS/EPOCH

    
Parameters are listed below in order of highest to lowest accuracy. The default
values are indicated by the === layer (0.9664).
 
  ACCURACY    PARAMETER
    0.9899    3 convolutional layers
    0.9864    2 convolutional layers
    0.9752    0 hidden layers
    0.9718    25% hidden layer dropout
    0.9717    9*9 convolutional layer filter size
    0.9706    256 hidden layer units
    0.9675    0 pooling layers
  ================================================
    0.9643    16 convolutional layer filters
    0.9631    64 convolutional layer filters
    0.9562    1*1 pooling layer pool size
    0.9496    4*4 pooling layer pool size
    0.9400    2 hidden layers
    0.9395    2 pooling layers
    0.9306    64 hidden layer units
    0.9155    2*2 convolutional layer filter size
    0.8482    75% hidden layer dropout
    0.8094    3 pooling layers
    0.7277    3 hidden layers
    0.6464    0 convolutional layers

  
Parameters are listed below in order of lowest to highest speed (ms/epoch). The
default values are indicated by the === layer (438 ms/epoch).

  SPEED       PARAMETER
    215       0 convolutional layers
    299       16 convolutional layer filters
    319       3 pooling layers
    322       4*4 pooling layer pool size
    335       0 hidden layers
    348       2 pooling layers
    363       64 hidden layer units
    409       2*2 convolutional layer filter size
    416       25% hidden layer dropout
    422       2 hidden layers
    429       3 hidden layers
    430       75% hidden layer dropout
  ================================================
    548       256 hidden layer units
    595       9*9 convolutional layer filter size
    778       64 convolutional layer filters
    785       0 pooling layers
   1000       2 convolutional layers
   1000       1*1 pooling layer pool size
   2000       3 convolutional layers
  
 
In summary, depending if accuracy or speed is the preferred parameter,
different parameter values would be justified. It's interesting that removing
the hidden layer resulted in both increased accuracy and faster execution
compared to the default settings. It's also interesting to note that removing
both pooling layers and hidden layers resulted in similar accuracy (0.9617
layers removed, 0.9664 default) and speed (409 ms/epoch layers removed, 438
ms/epoch default). This is obviously a very rudimentary analysis and there are
likely valid explanations for why this is the case.
